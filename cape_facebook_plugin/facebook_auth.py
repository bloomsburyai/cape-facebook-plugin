from cape_facebook_plugin.facebook_settings import URL_BASE
from cape_facebook_plugin.facebook_settings import facebook_auth_endpoints
from userdb.facebook_bot import FacebookBot
from webservices.app.app_middleware import requires_auth
from logging import debug
from api_helpers.input import required_parameter
from sanic.response import redirect
from uuid import uuid4

_endpoint_route = lambda x: facebook_auth_endpoints.route(URL_BASE + x, methods=['GET', 'POST'])


@_endpoint_route('/link-account')
@requires_auth
def _link_account(request):
    redirect_uri = required_parameter(request, 'redirect_uri')
    bot = FacebookBot()
    bot.user_id = request['user'].user_id
    bot.authorization_code = str(uuid4())
    bot.save()
    redirect_uri += '&authorization_code=' + bot.authorization_code
    debug("Redirecting facebook auth to " + redirect_uri)
    return redirect(redirect_uri)
