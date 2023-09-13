from itertools import product
import threading
from time import time, sleep
from threading import Thread
import requests
from os import system
from sys import argv

########

url = "" # https://url.com/
ext = ".png"
fileNameLength = 5 # https://url.com/xxxxx.png/
verboose = True
webhook = "" # discord
name = ""
errorLimit = 1000

######## 

chars = "abcdefghijklmnopqrstuvwxyz1234567890"
combis = product(chars, repeat=fileNameLength)
possibilities = len(chars) ** fileNameLength

valid = 0
weird = 0
errors = 0
errorOffset = 0

threadCount = 250
threads = []
threadIndexes = []
stop = False

currentIndex = 0
lastIndex = 0

urls = []

start = None

indexLock = threading.Lock()
errorLock = threading.Lock()
validLock = threading.Lock()
weirdLock = threading.Lock()

system(f"title Urltester v6 (Made by Timxxx) : [{str(currentIndex).zfill(len(str(possibilities)))}] : found {valid} : errors {errors} : weird {weird}")

if len(argv) > 5 and argv[1].isdigit() and argv[2].isdigit() and argv[3].isdigit() and argv[4].isdigit() and argv[5].isdigit():
    threadCount = int(argv[1])
    valid = int(argv[2])
    weird = int(argv[3])
    errorOffset = int(argv[4])
    start = int(argv[5])
    print(f"{threadCount} threads")
else:
    threadCount = input("Thread count: ")
    if threadCount.isdigit():
        threadCount = int(threadCount)
    else:
        threadCount=1

print("Getting last index")
try:
    with open(".indexv6", "r") as file:
        content = file.read()
        if  content.isdigit():
            lastIndex = int(content)
            print(f"Starting at {lastIndex}")
        else:
            file.close()
            print("Index was invalid")
            man = input("Enter last index manually ('enter' for 0): ")
            lastIndex = 0 if man == "" else int(man)
            with open(".indexv6", "w") as file:
                file.write(str(lastIndex))
except:
    print("No last index was found.")
    man = input("Enter last index manually ('enter' for 0): ")
    lastIndex = 0 if man == "" else int(man)
    with open(".indexv6", "w") as file:
        file.write(str(lastIndex))

def generateUrls():
    global currentIndex, possibilities
    while currentIndex < possibilities:
        yield url + "".join(combis.__next__()) + ext 

def increaseErrors(): 
    with errorLock: 
        global errors
        errors += 1

def downloadImage(_url):
    request = requests.get(_url)
    with open("imgs/" + _url.split("/")[-1], "wb") as file:
        file.write(request.content)

def sendToWebhook(_url, index, modified, status=None):
    if webhook == "": return
    index = str(index).zfill(len(str(possibilities)))
    try:
        if status == None:
            data = {"content": f"Created at: {modified} {name}\nIndex: {index}/{possibilities}\n{_url}"}
            requests.post(webhook, json=data)
        else:
            data = {"content": f"Weird Link : Code {status} {name}\nCreated at: {modified}\nIndex: {index}/{possibilities}\n{_url}"}
            requests.post(webhook, json=data)
    except Exception as e:
        print(f"Webhook ({errors}) : {_url}, {e}")

def testUrl(_url, threadIndex, index, tries=0):
    if stop: return
    try:
        if tries > 3: return
        request = requests.head(_url)
        if request.status_code == 200:
            sendToWebhook(_url, index, request.headers.get("last-modified"))
            print(f"Thread #{str(threadIndex).zfill(len(str(threadCount)))} : [{str(index).zfill(len(str(possibilities)))}] {_url} ({request.status_code}) valid")
            with validLock: global valid; valid += 1
            downloadImage(_url)
        elif request.status_code != 404:
            sendToWebhook(_url, index, request.headers.get("last-modified"), request.status_code)
            print(f"Thread #{str(threadIndex).zfill(len(str(threadCount)))} : [{str(index).zfill(len(str(possibilities)))}] {_url} ({request.status_code}) weird")
            with weirdLock: global weird; weird += 1
        else:
            if verboose: print(f"Thread #{str(threadIndex).zfill(len(str(threadCount)))} : [{str(index).zfill(len(str(possibilities)))}] {_url} ({request.status_code})")
    except Exception as e:
        increaseErrors()
        if not stop: 
            print(f"Thread #{threadIndex} ({errors}) : {e}")
            sleep(5)
        testUrl(_url, threadIndex, index, tries+1)

def testUrls(threadIndex):
    sleep(2)
    global threadIndexes, urls, currentIndex, errors
    try:
        for i in generateUrls():
            if stop: return
            indexLock.acquire()
            currentIndex += 1
            index = currentIndex
            indexLock.release()
            testUrl(i, threadIndex, index)
    except Exception as e:
        increaseErrors()
        if str(e) != "generator raised StopIteration":
            if not stop: print(f"Thread #{threadIndex} ({errors}) : {e}")

# skip generator to current index
for i in range(0, lastIndex):
    combis.__next__()
currentIndex = lastIndex

# start the threads
for i in range(threadCount):
    threads.append(Thread(target=testUrls, args=(i+1,)))
    threads[i].start()
    print(f"Thread #{i+1} started")

if start == None: start = (time() * 1000).__round__()

whileError = False
try:
    while currentIndex < possibilities:
        alive = 0
        for i in threads: 
            if i.is_alive(): alive += 1
        system(f"title Urltester v6 (Made by Timxxx) : [{str(currentIndex).zfill(len(str(possibilities)))}] : found {valid} : errors {errors+errorOffset} : weird {weird} : threads {alive}")
        if errors > errorLimit:
            stop = True
            break
        if alive < threadCount-20:
            stop = True
            break
        sleep(5)
        with open(".indexv6", "w") as file:
            file.write(str(currentIndex))
    whileError=True
except:
    stop=True
    whileError = True
    

end = time() * 1000

if whileError:
    sleep(5)
    with open(".indexv6", "w") as file:
        file.write(str(currentIndex))
    alive = 0
    for i in threads:
        if i.is_alive(): alive += 1
    system(f"title Urltester v6 (Made by Timxxx) : [{str(currentIndex).zfill(len(str(possibilities)))}] : found {valid} : errors {errors+errorOffset} : weird {weird} : threads {alive}")

    print(f"finished! running for {end-start:0.1f}s")
    print(f"threads still running {alive} : errors {errors+errorOffset}")
    print(f"current {currentIndex} - possible {possibilities} : equal {currentIndex==possibilities}")
    print(f"(session: {currentIndex-lastIndex})")
    input("Press enter to exit..")
else:
    sleep(5)
    alive = 0
    for i in threads:
        if i.is_alive(): alive += 1
    system(f"title Urltester v6 (Made by Timxxx) : [{str(currentIndex).zfill(len(str(possibilities)))}] : found {valid} : errors {errors+errorOffset} : weird {weird} : threads {alive}")
    print("Error limit reached!")
    sleep(5)
    system(f"start python {argv[0]} {threadCount} {valid} {weird} {errors+errorOffset} {start.__round__()}")

