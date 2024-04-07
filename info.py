import os
import json

USER_UUID = os.environ.get('USER_UUID', '')
ADMIN_UUID = os.environ.get('ADMIN_UUID', '')
APP_SECRET = os.environ.get('APP_SECRET', '')

with open(os.environ.get("herokuJson", ''), 'r', encoding="UTF8") as f:
    JSONCONFIG = json.load(f)