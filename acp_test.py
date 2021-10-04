import requests
from bs4 import BeautifulSoup
import string

player = "steam:110000139d00cbe"
print(f"Fetching {player}")

path = "C:/Users/Timothy/Documents/Dateien/"

url = f"http://fivecore.cc/dataplayer.php?usr={player}"
data = requests.get(url, allow_redirects=False)

soup = BeautifulSoup(data.content, "html.parser")
bank = int(soup.find("h2").text[0:-1].replace(",", ""))
cash = int(soup.findAll("h2")[1].text[0:-1].replace(",", ""))
sname = soup.find(id="data_name").text.split("(")[0].strip()
icname = soup.find(id="data_name").parent.find("p").text.split(":")[1].strip()
job = (soup.findAll("h2")[2].text.split("[")[0].strip(), soup.findAll("h2")[2].text.split("[")[1].replace("]", "").strip())
phoneNumber = soup.findAll("p")[5].text.split(":")[1].strip()
level = soup.findAll("p")[6].text.split(":")[1].strip()


print("")
print(f"Steamname: {sname}")
print(f"Name: {icname}")
print(f"Phonenumber: {phoneNumber}")
print(f"Job: {job[0]}, Grade: {job[1]}")
print(f"Cash: {cash}$")
print(f"Bank: {bank}$")
print(f"Level: {level}")
