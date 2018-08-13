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

from sanic import Blueprint
import os

URL_BASE = '/facebook'
facebook_event_endpoints = Blueprint('facebook_event_endpoints')
facebook_auth_endpoints = Blueprint('facebook_auth_endpoints')
facebook_verification = os.getenv('CAPE_FACEBOOK_VERIFICATION', 'REPLACEME')

THIS_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__)))
