import requests
from blimp_client.global_settings import COMPANY_SETTINGS

API_KEY = COMPANY_SETTINGS["mailgun_secret_key"]
DOMAIN_NAME = COMPANY_SETTINGS["domain_name"]
COMPANY_NAME = COMPANY_SETTINGS["company_name"]


class ImageEmailer(object):

    def __init__(self):
        pass

    def email_image(self, to_email, image_url):
        message = "Hello!  The picture your requested can be downloaded from %s" % image_url
        send_email_with_data(to_email, "Digital Picture Delivery!", message)


def send_email_with_data(customer_email, subject, text):
    return requests.post(
        "https://api.mailgun.net/v2/%s/messages" % DOMAIN_NAME,
        auth=("api", API_KEY),
        data={"from": "%s<no-reply@%s>" % (COMPANY_NAME, DOMAIN_NAME),
              "to": customer_email,
              "subject": subject,
              "text": text})


def send_complex_message(to_address):
    return
    html_template = "/Users/slobdell/projects/workout-generator/workout_generator/scripts/email_template.html"
    with open(html_template, "rb") as f:
        html_content = f.read()
    return requests.post(
        "https://api.mailgun.net/v2/%s/messages" % DOMAIN_NAME,
        auth=("api", API_KEY),
        data={"from": "Scott Lobdell <scott@workoutgenerator.net>",
              "to": to_address,
              "subject": "WorkoutGenerator v2.0 Released and Free to You!",
              "html": html_content})
