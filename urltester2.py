import random
import validators
import requests

# Made by Timxxx#0248
###############################

url = "" # https://url.com/
ext = ".png"
fileNameLength = 5 # https://url.com/xxxxx.png/
webhook = ""

###############################

chars = "abcdefghijklmnopqrstuvwxyz1234567890"
urls = []
valid = []

# validate url
if url[len(url)-1] != "/": url += "/" 
index = 0

def sendToWebhook(_url):
    if webhook != "":
        data = {"content": _url}
        response = requests.post(webhook, json=data)
        print(f"[{len(urls)}] Url got sent to to webhook ({response.status_code}) | {_url}")

def generateRandUrl(length=5):
    fileName = "".join(random.choice(chars) for i in range(length))
    _url = url + fileName + ext
    if _url in urls:
        _url = generateRandUrl(length)
    return _url

def isValid(_url):
    request = requests.head(_url)
    return request.status_code == 200

def testUrl(_url):
    urls.append(_url)
    if isValid(_url):
        sendToWebhook(_url)
        valid.append(_url)
    else:
        print(f"[{len(urls)}] Nothing on {_url}")

print("Started to search...")
while True:
    testUrl(generateRandUrl(fileNameLength))