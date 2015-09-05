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
    with open(filename, "rb") as f:
        settings = json.loads(f.read())
    return settings

APP_SETTINGS = get_app_settings()
CLIENT_SETTINGS = get_client_settings()
COMPANY_SETTINGS = get_latest_company_settings()
