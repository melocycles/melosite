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
    'benevole':         {"type": "text",    "is_required": True},
    'referent':         {"type": "text",    "is_required": False},
    'title':            {"type": "text",    "is_required": True},
    'dateEntre':        {"type": "date",    "is_required": True},
    'dateSortie':       {"type": "date",    "is_required": False},
    'statutVelo':       {"type": "select",  "is_required": True,  "select_values" : ["en stock", "réservé", "vendu", "donné", "démonté", "recyclé", "perdu"]},
    'origine':          {"type": "select",  "is_required": True,  "select_values" : ["don", "trouvé", "achat", "récup", "déchetterie"]},
    'etatVelo':         {"type": "select",  "is_required": False, "select_values" : ["très bon", "moyen", "mauvais", "pour pièces"]},
    'marque':           {"type": "text",    "is_required": False},
    'typeVelo':         {"type": "select",  "is_required": False, "select_values" : ["VTT", "vélo de route", "VTC", "BMX", "cargo", "pliant"]},
    'tailleRoue':       {"type": "select",  "is_required": False, "select_values" : ["12 pouces", "14 pouces", "16 pouces", "20 pouces", "24 pouces", "26 pouces", "27.5 pouces", "29 pouces", "600", "650","700"]},
    'tailleCadre':      {"type": "select",  "is_required": False, "select_values" : ["enfant", "XS", "S", "M", "L", "XL", "XXL"]},
    'bicycode':         {"type": "text",    "is_required": False},
    'electrique':       {"type": "select",  "is_required": False, "select_values" : ["non", "oui"]},
    'prochaineAction':  {"type": "select",  "is_required": False, "select_values" : ["à vendre", "à donner", "à démonter", "à recycler", "à réparer"]},
    'valeur':           {"type": "float",   "is_required": False},
    'destinataireVelo': {"type": "text",    "is_required": False},
    'descriptionPublic':{"type": "textarea","is_required": False},
    'descriptionPrive': {"type": "textarea","is_required": False}
}