from dotenv import load_dotenv
import os
from database.database_service import DatabaseService
from house_scraper import HouseScraper
from database.house_image import HouseImage
from database.house_post import HousePost
from messenger_service import MessengerService
from api_service import ApiView
import threading
import signal
import time
from timeloop import Timeloop
from datetime import timedelta
import sys

load_dotenv()

tl = Timeloop()


def add_house_posts():
    posts = HouseScraper().get_all_posts(session)
    original_urls = []

    print('Getting house posts...')

    for post in posts:
        object_to_save = post
        object_to_save['is_new'] = 1
        object_to_save['is_liked'] = 0
        object_to_save['image_urls'] = [
            HouseImage(**img) for img in post['image_urls']]

        original_urls.append(object_to_save['original_url'])

        session.add(HousePost(**object_to_save))

    print('{} Posts retrieved'.format(len(posts)))

    if len(posts) > 0:
        urls_joined = '\n\n'.join(original_urls)
        print('Added {0} new house listings!'.format(len(posts)))

        messenger_service = MessengerService(
            os.getenv('FB_EMAIL'), os.getenv('FB_PASSWORD'))
        messenger_service.send_message(
            'Atsirado {1} nauji skelbimai:\n {0}'.format(urls_joined, len(posts)))


def init_session():
    global database
    global session
    global api
    global api_thread
    database = DatabaseService('root', 'localhost', 'house_scrapper')
    session = database.get_session()
    api = ApiView().init()
    ApiView.register(api)
    api_thread = threading.Thread(target=api.run).start()


def commit_close_session():
    session.commit()
    session.close()
    print('Done')


@tl.job(interval=timedelta(hours=1))
def check_for_new_posts():
    add_house_posts()
    commit_close_session()


def shutdown_handler(sig, frame):
    print('Service is shutting down...')
    sys.exit()


if __name__ == '__main__':
    signal.signal(signal.SIGINT, shutdown_handler)
    tl.start(block=False)
    init_session()
    check_for_new_posts()
