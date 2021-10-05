from bs4 import BeautifulSoup
import validators
import requests
import os
from sys import argv

counter = 0

if len(argv) == 2: url = argv[1]
else: url = input("Enter the url to dump: ")

while not validators.url(url):
    url = input("Please enter an valid url: ")

print(f"Dumping : '{url}'")

path = os.getcwd().replace("\\", "/")
path += f"/dumps/{url.split('//')[1].replace('/', '-').replace('.', '-')}/"
if path[-1] == "-": path = path[:-2] + "/"
print("")

def createDir(p):
    try: 
        os.makedirs(p)
        print(f"Created dir {p}")
    except: pass

# create the dump dir
createDir(path)

r = requests.get(url, allow_redirects=False)
site = BeautifulSoup(r.text, "html.parser")


# dump html
with open(f"{path}index.html", "wb") as fp:
    fp.write(r.content)
    counter += 1

print(f"[{counter:04}] Dumped index")

# dump css
for link in site.findAll("link"):
    link = str(link["href"])
    if link.find(".css") != -1:
        if link.find("http") != -1 or link.find("https") != -1: continue
        if link.startswith("/"): link = link[1:]

        createDir(path + "".join([i + "/" for i in link.split("/")[0:-1]]))
        req = requests.get(f"{url}/{link}", allow_redirects=False)
        with open(path + link, "wb") as fp:
            fp.write(req.content)
        counter += 1
        print(f"[{counter:04}] Dumped {link}")

# dump js
for link in site.findAll("script", src=True):
    link = str(link["src"])
    if link.find(".js") != -1:
        if link.find("http") != -1 or link.find("https") != -1: continue
        if link.startswith("/"): link = link[1:]

        createDir(path + "".join([i + "/" for i in link.split("/")[0:-1]]))
        req = requests.get(f"{url}/{link}", allow_redirects=False)
        with open(path + link, "wb") as fp:
            fp.write(req.content)
        counter += 1
        print(f"[{counter:04}] Dumped {link}")

# dump graphics
for link in site.findAll("img", src=True):
    link = str(link["src"])
    if link == "": continue
    if link.find("http") != -1 or link.find("https") != -1: continue
    if link.startswith("/"): link = link[1:]

    createDir(path + "".join([i + "/" for i in link.split("/")[0:-1]]))
    req = requests.get(f"{url}/{link}", allow_redirects=False)
    with open(path + link, "wb") as fp:
        fp.write(req.content)
    counter += 1
    print(f"[{counter:04}] Dumped {link}")

print(f"\nDumping finished!\nDumped {counter} files")