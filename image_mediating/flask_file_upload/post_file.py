import requests

url = "http://localhost:5000/picture/"

files = {
    "file": open("sample_img.jpg", "rb")
}
response = requests.post(url, files=files)
text = response.content
with open("response.html", "w+") as f:
    f.write(text)
