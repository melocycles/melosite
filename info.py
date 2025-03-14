import os
import json

USER_UUID = os.environ.get('USER_UUID', '')
ADMIN_UUID = os.environ.get('ADMIN_UUID', '')
APP_SECRET = os.environ.get('APP_SECRET', '')

try:
    with open(os.environ.get("herokuJson", ''), 'r', encoding="UTF8") as f:
        JSONCONFIG = json.load(f)
except:
    JSONCONFIG = json.loads(os.environ.get("herokuJson", ''))

dict_form = {
    'benevole':     {"type": "text",    "is_required": True},
    'ref':          {"type": "text",    "is_required": False},
    'name':         {"type": "text",    "is_required": True},
    'entry_date':   {"type": "date",    "is_required": True},
    'exit_date':    {"type": "date",    "is_required": False},
    'bike_status':  {"type": "select",  "is_required": True,  "select_values" : ["en stock", "réservé", "vendu", "donné", "démonté", "recyclé", "perdu"]},
    'origin':       {"type": "select",  "is_required": True,  "select_values" : ["don", "trouvé", "achat", "récup", "déchetterie"]},
    'exit_type':    {"type": "select",  "is_required": False, "select_values" : ["très bon", "moyen", "mauvais", "pour pièces"]},
    'brand':        {"type": "text",    "is_required": False},
    'bike_type':    {"type": "select",  "is_required": False, "select_values" : ["VTT", "vélo de route", "VTC", "BMX", "cargo", "pliant"]},
    'wheel_size':   {"type": "select",  "is_required": False, "select_values" : ["12 pouces", "14 pouces", "16 pouces", "20 pouces", "24 pouces", "26 pouces", "27.5 pouces", "29 pouces", "600", "650","700"]},
    'frame_size':   {"type": "select",  "is_required": False, "select_values" : ["enfant", "XS", "S", "M", "L", "XL", "XXL"]},
    'bicycode':     {"type": "text",    "is_required": False},
    'is_electric':  {"type": "select",  "is_required": False, "select_values" : [False, True]},
    'next_action':  {"type": "select",  "is_required": False, "select_values" : ["à vendre", "à donner", "à démonter", "à recycler", "à réparer"]},
    'value':        {"type": "int",   "is_required": False},
    'bike_dest':    {"type": "text",    "is_required": False},
    'public_desc':  {"type": "textarea","is_required": False},
    'private_desc': {"type": "textarea","is_required": False}
}