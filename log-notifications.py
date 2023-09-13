# phone notifications from log file

from os import getenv
import io, time, requests, dotenv

dotenv.load_dotenv()
def env(name: str): return getenv(name) or "" 

file_path = env("ln-file-path") # path to logfile
look_for = env("ln-look-for") # string to search for in log lines (case insensitive)
ntfy_topic = env("ln-ntfy-topic") # https://ntfy.sh
ntfy_title = env("ln-ntfy-title") # push notification 
ntfy_message = env("ln-ntfy-message") # push notification 
ntfy_priority = env("ln-ntfy-priority") # push notification 


# https://stackoverflow.com/a/53121178/19335246
def follow(file: io.TextIOWrapper):
    while True:
        line = file.readline()
        if not line or not line.endswith('\n'):
            time.sleep(2)
            continue
        yield line

def check(line: str): 
    return line.find(look_for.lower()) != -1


with open(file_path, encoding="utf-8") as file:
    for line in follow(file):
        result = check(line.lower())
        if not result: continue
        print("found matching line:", line.strip())
        print("sending notifications.. (press ctrl+c to stop)")
        while True:
            try:
                requests.post("http://ntfy.sh/" + ntfy_topic, ntfy_message, headers={"Title": ntfy_title, "Priority": ntfy_priority})
                time.sleep(5)
            except KeyboardInterrupt: break
        print("stopped sending notifications")