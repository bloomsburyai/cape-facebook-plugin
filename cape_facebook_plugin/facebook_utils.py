import requests
from logging import debug


FACEBOOK_URL = "https://graph.facebook.com/v2.6/me/messages?access_token=EAAIhnidxBjwBAD1ZA9QaZCphNKRUriQz6Rg6YHqGMjpYOtqjVsbwtvzDTzzwQZC8iJhN9GnqZBC7VWGN9h3t46g6S2W8r6lJl83aJ3ptqSiEsyFp5v9B1p5T1SG2VzbADZApU9nSonvuYbSMHDCj6GY8BruZCPrpXajiua9HOCbgZDZD"


def send_facebook_message(recipient, message):
    facebook_request = requests.Session()
    response = facebook_request.post(FACEBOOK_URL, json={
        'messaging_type': 'RESPONSE',
        'recipient': {
            'id': recipient
        },
        'message': {
            'text': message
        }
    })
    debug(response.text)
    facebook_request.close()


def send_facebook_login_message(recipient):
    facebook_request = requests.Session()
    response = facebook_request.post(FACEBOOK_URL, json=
    {
        "recipient": {
            "id": recipient
        },
        "message": {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "generic",
                    "elements": [
                        {
                            "title": "Welcome!",
                            "image_url": "https://thecape.ai/logo.png",
                            "subtitle": "Hi! Please log in to your Cape account and I'll start answering your questions!",
                            "buttons": [
                                {
                                    "type": "account_link",
                                    "url": f'https://ui-thermocline.thecape.ai/authentication.html?configuration=%7B"authentication":%7B"login":%7B"redirectURL":"https://facebook.thecape.ai/facebook/link-account"%7D%7D%7D'
                                }
                            ]
                        }
                    ]
                }
            }
        }
    })
