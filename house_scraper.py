import requests
import bs4
import time
import json
import re
from sqlalchemy.sql import exists
from database.house_post import HousePost


class HouseScraper:
    def __init__(self, url):
        self.get_url = url

    def get_page_count(self):
        res = requests.get(self.get_url.format(1, 1))
        soup = bs4.BeautifulSoup(res.text, 'lxml')
        page_links = soup.select('.pagination_link')
        return len(page_links)

    def get_details_urls(self):

        details_urls = {}

        # for testing range(1, 2):
        for page in range(1, self.get_page_count() + 1):
            page_url = self.get_url.format(page, page)
            res = requests.get(page_url)
            soup = bs4.BeautifulSoup(res.text, 'lxml')

            for item in soup.select('.js-cfuser-link'):
                details_urls[item['data-item-id']
                             ] = 'https://www.skelbiu.lt/' + item['href']

            time.sleep(0.2)
        return details_urls

    def getImageUrls(self, soup_page):
        all_scripts = soup_page.select('script')
        images = []

        for script in all_scripts:
            script_string = script.string

            if script_string:
                if "var images" in script_string:
                    url = re.findall(r'(full_size_src):(.+?)\s', script_string)
                    extracted_urls = [x[1] for x in url]
                    joined_urls = ','.join(extracted_urls)
                    for img in re.findall(r"'([^' ]+)'", joined_urls):
                        image = {}
                        image['image_url'] = img
                        images.append(image)
        return images

    def get_all_posts(self, session):

        houses_data_objects = []
        detail_urls = self.get_details_urls()

        for key in detail_urls.keys():
            if not session.query(exists().where(HousePost.post_inner_id == key)).scalar():
                res = requests.get(detail_urls[key])
                soup = bs4.BeautifulSoup(res.text, 'lxml')

                details_data = soup.find_all(class_='detail')

                house_data = {}
                house_data['post_inner_id'] = key
                house_data['image_urls'] = self.getImageUrls(soup)

                for detail in details_data:
                    title = detail.select('.title')[0].text.strip()
                    value = detail.select('.value')[0].text.strip()

                    if title == 'Gyvenvietė:':
                        house_data['town'] = value
                    if title == 'Gatvė:':
                        house_data['street'] = value
                    if title == 'Kamb. sk.:':
                        house_data['room_count'] = int(
                            ''.join(re.findall(r'[0-9]', value)))
                    if title == 'Metai:':
                        house_data['year'] = int(
                            ''.join(re.findall(r'[0-9]', value)))
                    if title == 'Šildymas:':
                        house_data['heating'] = value
                    if title == 'Plotas, m²:':
                        house_data['house_area'] = int(
                            ''.join(re.findall(r'[0-9]', value)))
                    if title == 'Sklypo plotas, a:':
                        house_data['land_area'] = int(
                            ''.join(re.findall(r'[0-9]', value)))

                house_data['original_url'] = detail_urls[key]
                description = soup.select('.description')
                if len(description):
                    house_data['description'] = soup.select('.description')[
                        0].text.strip()

                house_data['price'] = int(
                    ''.join(re.findall(r'[0-9]', soup.select('.price')[0].text.strip())))

                houses_data_objects.append(house_data)
                time.sleep(0.2)

        return houses_data_objects
