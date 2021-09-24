import random
import requests
import threading
import time
from os import system

# Made by Timxxx#0248
###############################

url = "" # https://url.com/
ext = ".png"
fileNameLength = 5 # https://url.com/xxxxx.png/
webhook = ""
verboose = False

###############################

chars = "abcdefghijklmnopqrstuvwxyz1234567890"
urls = []
valid = []
threads = {}
errorIndexes = []

threadCount = input("Thread count: ")
if threadCount.isdigit:
    threadCount = int(threadCount)
    threadcount = 250 if threadCount > 250 else threadCount
else:
    threadCount=1

# validate url
if url[len(url)-1] != "/": url += "/" 
index = 0

def sendToWebhook(_url, modified, threadIndex):
    if webhook != "":
        data = {"content": f"{modified} (timxxx)\n{_url}"}
        response = requests.post(webhook, json=data)
        print(f"[{len(urls)}] Url got sent to to webhook ({response.status_code}) | {_url} : Thread #{threadIndex}")

def generateRandUrl(length=5):
    fileName = "".join(random.choice(chars) for i in range(length))
    _url = url + fileName + ext
    if _url in urls:
        _url = generateRandUrl(length)
    return _url

def isValid(_url):
    request = requests.head(_url)
    return (request.status_code == 200, request)

def testUrl(_url, threadIndex):
    urls.append(_url)
    _valid, request = isValid(_url)

    if _valid:
        sendToWebhook(_url, request.headers.get("last-modified"), threadIndex)
        valid.append(_url)
    else:
        if verboose: print(f"[{len(urls)}] Nothing found on {_url} ({request.status_code}): Thread #{threadIndex}")
        elif request.status_code != 404: print(f"[{len(urls)}] Weird {_url} ({request.status_code}): Thread #{threadIndex}")

def searchForUrls(threadIndex):
    print(f"Thread #{threadIndex} is starting")
    time.sleep(5)
    try:
        while True:
            testUrl(generateRandUrl(fileNameLength), threadIndex)
    except:
        print(f"An error occured in thread #{threadIndex}")
        del(threads[threadIndex])
        errorIndexes.append(threadIndex)

print("Starting to search...")

for i in range(threadCount):
    threads[i+1] = threading.Thread(target=searchForUrls, args=(i+1,))
    threads[i+1].start()

while True:
    system(f"title Url #{len(urls)}")
    if len(errorIndexes) > 0:
        time.sleep(2)
        for i in errorIndexes:
            print(f"Restarting thread #{i}")
            threads[i] = threading.Thread(target=searchForUrls, args=(i,))
            threads[i].start()
    time.sleep(10)