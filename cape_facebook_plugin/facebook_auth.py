# Copyright 2018 BLEMUNDSBURY AI LIMITED
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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
