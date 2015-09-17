import requests
import base64

url = "http://localhost:6969/picture/"
with open("sample_img.jpg", "rb") as f:
    contents = f.read()
    b64_jpeg_string = base64.urlsafe_b64encode(contents)

post_data = {
    "b64jpeg": b64_jpeg_string,
    "phone_number": "+14156606378"
}
response = requests.post(url, data=post_data)
text = response.content
with open("response.html", "w+") as f:
    f.write(text)
