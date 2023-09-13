import re, os, hashlib
from pathlib import Path
from urllib.parse import urlparse 
from requests import get
from bs4 import BeautifulSoup

def write_bytes(path: Path, content: bytes):
    print(f"writing to {path}")
    os.makedirs(path.parent, exist_ok=True)
    with open(path, "wb") as file:
        file.write(content)

def dump_elements(page: BeautifulSoup, file: Path,  element: tuple[str, str]):
    for el in page.find_all(element[0], recursive=True, **{element[1]: True}):
        link = str(el[element[1]])
        if link.startswith(("http", "https")): continue
        
        content: bytes
        if link.startswith("/"): content = get(f"{base_url}{link}").content
        else: content = get(f"{url}{link}").content
        
        path = cwd / link.removeprefix("/")
        write_bytes(path, content)

# https://stackoverflow.com/a/7160778/19335246
url_regex = re.compile(
    r'^(?:http)s?://'
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
    r'localhost|'
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
    r'(?::\d+)?'
    r'(?:/?|[/?]\S+)$', re.IGNORECASE )

url = input("url to dump: ").strip()
while not url_regex.match(url): url = input("please enter a valid url: ").strip()

parsed_url = urlparse(url)
base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
path = str(Path(parsed_url.path).parent).replace("\\", "/")
url = f"{parsed_url.scheme}://{parsed_url.netloc}{path}"

cwd = Path(os.getcwd()) / "dumps" / hashlib.md5(base_url.encode()).hexdigest()
print(f"dumping into '{cwd}'")

# url index
content = get(f"{base_url}{parsed_url.path}{'?'+parsed_url.query if parsed_url.query else ''}").content
index = BeautifulSoup(content, "html.parser")

path = cwd / Path(parsed_url.path.removeprefix("/"))
write_bytes(path, content)

# dump elements containing links
dump_elements(index, path, ("link", "href"))
dump_elements(index, path, ("script", "src"))
dump_elements(index, path, ("img", "src"))

