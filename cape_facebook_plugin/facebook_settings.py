from sanic import Blueprint
import os

URL_BASE = '/facebook'
facebook_event_endpoints = Blueprint('facebook_event_endpoints')
facebook_auth_endpoints = Blueprint('facebook_auth_endpoints')
facebook_verification = os.getenv('CAPE_FACEBOOK_VERIFICATION', 'REPLACEME')

THIS_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__)))
