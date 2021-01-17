from dotenv import load_dotenv
import os
from database.database_service import DatabaseService
from house_scraper import HouseScraper
from notifications.notification_service_factory import *
from database.house_image import HouseImage
from database.house_post import HousePost
from api_service import ApiView
import threading
import signal
import time
from timeloop import Timeloop
from datetime import timedelta
import sys

WATCH_URL = 'https://www.skelbiu.lt/skelbimai/{}?autocompleted=1&keywords=&cost_min=&cost_max=70000&space_min=80&space_max=&rooms_min=3&rooms_max=&building_type=0&year_min=&year_max=&status=0&building=0&price_per_unit_min=&price_per_unit_max=&district=0&quarter=0&streets=0&ignorestreets=0&cities=516%2C465%2C466%2C542%2C562%2C491%2C504&distance=0&mainCity=1&search=1&category_id=42&type=0&user_type=0&ad_since_min=0&ad_since_max=0&visited_page={}&orderBy=-1&detailsSearch=1'

load_dotenv()

tl = Timeloop()


def add_house_posts():
    posts = HouseScraper(WATCH_URL).get_all_posts(session)
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

    if not posts:
        return

    urls_joined = '\n\n'.join(original_urls)
    print('Added {0} new house listings!'.format(len(posts)))
    
    factory = NotificationServiceFactory()

    notification_service = factory.create("messenger", MessengerSettings(os.getenv('FB_EMAIL'), os.getenv('FB_PASSWORD')))

    notification_service.send_message()
    messenger_service.send_message('Atsirado {1} nauji skelbimai:\n {0}'.format(urls_joined, len(posts)))


def init_session():
    global database
    global session
    global api
    global api_thread

    database = DatabaseService(os.getenv('DATABASE_CONNECTOR'))
    session = database.get_session()
    api = ApiView().init()
    ApiView.register(api)
    api_thread=threading.Thread(target=api.run).start()


def commit_close_session():
    session.commit()
    session.close()
    print('Done')


@ tl.job(interval=timedelta(hours=1))
def check_for_new_posts():
    # could also be created via scraper factory
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
