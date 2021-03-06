import random
import validators
import pandas as pd
from requests_futures.sessions import FuturesSession
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

count = input("Count of urls to test: ")
if(not count.isdigit()):
    count = 10
count = int(count)

# validate url
if url[len(url)-1] != "/": url += "/" 

index = 0

def sendToWebhook(_url):
    if webhook != "":
        data = {"content": _url}
        response = requests.post(webhook, json=data)
        print(f"Url got sent to to webhook ({response.status_code}) | {_url}")

def generateRandUrl(length=5):
    fileName = "".join(random.choice(chars) for i in range(length))
    return url + fileName + ext

def getRequest(_url):
    session = FuturesSession()
    head = session.head(_url)
    if(head.result().status_code==200): 
        sendToWebhook(_url)
    else:
        print(f"Nothing on: {_url}")
    return head

def getStatusCode(request):
    try:
        return request.result().status_code
    except:
        return 408

print("Generating urls...")

# generate list urls
for i in range(count):
    _url = generateRandUrl(fileNameLength)
    if _url not in urls and validators.url(_url):
        urls.append(_url)
        print(f"generated ({i+1}): {_url}")

print("Started to search...")

# make a request for every url
df = pd.DataFrame({"url": urls})
df["statusCode"] = df["url"].apply(getRequest).apply(getStatusCode)

# get the valid urls
df.set_index(["statusCode"])
for _url in df.loc[df["statusCode"]==200].values:
    valid.append(_url[0])

print(valid)

stats = df.groupby('statusCode')["url"].count().reset_index()
print(stats)

_ = "is" if len(valid)==1 else "are"
print(f"\nTested {len(urls)} urls, {len(valid)} {_} valid")