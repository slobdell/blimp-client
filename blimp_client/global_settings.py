import json


def get_app_settings():
    with open("app_settings.json", "rb") as f:
        settings = json.loads(f.read())
    return settings


def get_client_settings():
    with open("client_settings.json", "rb") as f:
        settings = json.loads(f.read())
    return settings


def get_latest_company_settings():
    filename = APP_SETTINGS["COMPANY_SETTINGS_FILE"]
    try:
        with open(filename, "rb") as f:
            settings = json.loads(f.read())
    except IOError:
        settings = {}
    return settings

APP_SETTINGS = get_app_settings()
CLIENT_SETTINGS = get_client_settings()
COMPANY_SETTINGS = get_latest_company_settings()
CHANNEL_PREFIX = "%s:%s:" % (COMPANY_SETTINGS.get("client_company_id", ""), COMPANY_SETTINGS.get("raspberry_client_id", ""))
