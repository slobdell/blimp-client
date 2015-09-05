import os

from celery import Celery

from blimp_client.global_settings import APP_SETTINGS, COMPANY_SETTINGS

app = Celery('this_can_be_anything', broker='redis://localhost:6379/0')


@app.task(name="some_unique_name")
def arbitrary_task(serializable_input):
    print "GOT HERE"
    # do anything here
    pass


@app.task(name="send_photo")
def send_photo(filename, phone_num_or_email):
    full_path = "%s%s" % (APP_SETTINGS["UPLOAD_FOLDER"], filename)
    with open(full_path, "rb") as f:
        jpeg_string = f.read()

    if COMPANY_SETTINGS["sms_photos"]:
        pass

    elif COMPANY_SETTINGS["email_photos"]:
        pass
    os.remove(full_path)


if __name__ == "__main__":
    arbitrary_task.delay("hello world")
