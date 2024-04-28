import os
import json

USER_UUID = os.environ.get('USER_UUID', '')
ADMIN_UUID = os.environ.get('ADMIN_UUID', '')
APP_SECRET = os.environ.get('APP_SECRET', '')

JSONCONFIG = json.loads(os.environ.get("herokuJson", ''))