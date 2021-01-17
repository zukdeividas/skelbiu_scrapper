import fbchat
from fbchat import Client, User
import os
import re
from dotenv import load_dotenv

fbchat._util.USER_AGENTS = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36"]
fbchat._state.FB_DTSG_REGEX = re.compile(r'"name":"fb_dtsg","value":"(.*?)"')

load_dotenv()

client = Client(email=os.getenv('FB_EMAIL'),
                password=os.getenv('FB_PASSWORD'), max_tries=1)
print(list(map(lambda user: (user.name, user.uid), client.fetchAllUsers())))