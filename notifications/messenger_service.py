import re
import fbchat
from fbchat import Client
from fbchat.models import Message

from notifications.notification_service import NotificationService

fbchat._util.USER_AGENTS = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36"]
fbchat._state.FB_DTSG_REGEX = re.compile(r'"name":"fb_dtsg","value":"(.*?)"')


class MessengerService(NotificationService):

    def __init__(self, settings):
        super().__init__(settings)

        self.client = Client(email=self.settings.username,
                             password=self.settings.password, max_tries=1)

    def send_message(self, message):
        self.client.send(Message(text=message),
                         thread_id='user_account_uid', thread_type=ThreadType.USER)


class MessengerSettings:
    def __init__(self, username, password):
        self.username = username
        self.password = password