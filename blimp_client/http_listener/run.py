#!.virtualenv/bin/python
from app import app

from blimp_client.global_settings import APP_SETTINGS

port = int(APP_SETTINGS["HTTP_LISTEN_URL"].split(":")[-1])

app.run(debug=True, host="0.0.0.0", port=port)
