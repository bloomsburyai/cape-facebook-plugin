import json
from collections import deque
from webservices.bots_common.utils import process_action, markdown_to_text, get_file_contents
from external_integration_facebook.facebook_settings import URL_BASE, facebook_verification
from external_integration_facebook.facebook_settings import facebook_event_endpoints
from external_integration_facebook.facebook_utils import send_facebook_message, send_facebook_login_message
from userdb.facebook_bot import FacebookBot
from userdb.user import User
from webservices.app.app_middleware import respond_with_text
from webservices.app.app_document_endpoints import _upload_document as responder_upload_document
from logging import debug, warning
from api_helpers.input import required_parameter, optional_parameter
from api_helpers.text_responses import BOT_FILE_UPLOADED
from api_helpers.exceptions import UserException
from urllib.parse import urlparse
import os.path

_endpoint_route = lambda x: facebook_event_endpoints.route(URL_BASE + x, methods=['GET', 'POST'])

_processed_events = deque(maxlen=1000)


def process_file(user, comm_id, request, attachment):
    try:
        text = get_file_contents(attachment['payload']['url'])
        request['user'] = user
        request['args']['text'] = text
        request['args']['title'] = os.path.basename(urlparse(attachment['payload']['url']).path)
        request['args']['origin'] = attachment['payload']['url']
        request['args']['replace'] = 'true'
        responder_upload_document(request)
        send_facebook_message(comm_id, BOT_FILE_UPLOADED)
    except UserException as e:
        send_facebook_message(comm_id, e.message)


def process_message(sender, request, message):
    if message['mid'] in _processed_events:
        # We've already processed this event
        return
    _processed_events.append(message['mid'])
    bot = FacebookBot.get('facebook_psid', sender)
    if bot is None:
        send_facebook_login_message(sender)
    else:
        user = User.get('user_id', bot.user_id)
        if 'text' in message:
            response = process_action(user, bot.facebook_psid, request, message['text'])
            if response is not None:
                send_facebook_message(sender, markdown_to_text(response['text']))
            else:
                send_facebook_message(sender, "Sorry, I had a problem doing that.")
        elif 'attachments' in message:
            for attachment in message['attachments']:
                if attachment['type'] == 'file':
                    process_file(user, bot.facebook_psid, request, attachment)


@_endpoint_route('/receive-event')
@respond_with_text
def receive_event(request):
    debug("facebook args: " + str(request['args']))
    mode = optional_parameter(request, 'hub.mode', None)
    if mode is not None:
        if mode == 'subscribe':
            token = required_parameter(request, 'hub.verify_token')
            challenge = required_parameter(request, 'hub.challenge')
            if token == facebook_verification:
                return challenge
            else:
                warning("Invalid token")
        else:
            warning("Unsupported facebook mode")
    else:
        entries = optional_parameter(request, 'entry', None)
        if entries is not None:
            entries = json.loads(entries)
            for entry in entries:
                if 'messaging' in entry:
                    for message_entry in entry['messaging']:
                        sender = message_entry['sender']['id']
                        if 'account_linking' in message_entry:
                            if message_entry['account_linking']['status'] == 'linked':
                                authorization_code = message_entry['account_linking']['authorization_code']
                                bot = FacebookBot.get('authorization_code', authorization_code)
                                bot.facebook_psid = sender
                                bot.save()
                            elif message_entry['account_linking']['status'] == 'unlinked':
                                bot = FacebookBot.get('facebook_psid', sender)
                                bot.delete_instance()
                        else:
                            process_message(sender, request, message_entry['message'])

        else:
            warning("Unsupported facebook event")

    return "OK"
