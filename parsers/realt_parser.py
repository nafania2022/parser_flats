import requests
from bs4 import BeautifulSoup
from db.data import Flat
import re
from datetime import datetime
from parsers.parser_standat import ParserStandart
import traceback
import logging
import sentry.sentry_logger as sentry_logger


class RealtParser(ParserStandart):

    def get_parser_name(self):        
        return 'realt'
    
    def get_url(self,page_from=1):
        resp = requests.get(
                f'https://realt.by/sale/flats/?page={page_from}',
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}
            )
        return BeautifulSoup(resp.content, 'html.parser')
    

    def get_all_last_flats_links(self, page_from=1, page_to=2):
        flat_links = []
        if page_to == 'last':            
            html = self.get_url(1)
            raw_last_page = html.find_all('option')
            list_page= []
            for page in raw_last_page:
                list_page.append(page.text)
            page_to = int(list_page[-1])
        else:
            page_to = page_to     

        while page_from < page_to:            
            html = self.get_url(page_from)
            for a in html.find_all('a', href=True, class_='teaser-title'):
                flat_links.append(a['href'])
            print(f'Загружено {page_from} из {page_to} ')
            page_from += 1
        ready_links = list(filter(lambda el: 'object' in el, flat_links))
        return ready_links

    def enrich_links_to_flats(self, links):
        flats = []
        try:
            for counter, link in enumerate(links):
                resp = requests.get(link)
                html = BeautifulSoup(resp.content, 'html.parser')
                title = html.find('h1', class_='order-1').text.strip()
                raw_price = html.find('h2', class_='w-full')
                if raw_price is not None:
                    price = int(re.sub('[^0-9]', '', raw_price.text.strip()))
                else:
                    price = 0
                raw_price_meter = html.find('p', class_='w-full').find('span', class_='mr-1.5').text.strip()
                if raw_price_meter is not None:
                    price_meter = int(re.sub('[^0-9]', '', raw_price_meter))
                else:
                    price_meter = 0
                city = html.find('div', class_='md:-order-1').find('a').text.replace("г.", "").lower().strip()
                description = html.find('section', class_='bg-white').text.strip()
                try:
                    date = datetime.strptime(html.find('span', class_='mr-1.5').text.strip(), '%d.%m.%Y')
                except Exception as e:
                    date = datetime.now()
                try:
                    images = set()
                    image_divs = html.find_all("div", {"class": "swiper-slide"})
                    for img_div in image_divs:
                        for img in list(filter(lambda el: el is not None and (el[:4] == 'http' and 'user' in el),
                                            map(lambda el2: el2['src'], img_div.findAll("img")))):
                            images.add(img)
                    images = list(images)
                except Exception as e:
                    logging.error(f'Не удалось загрузить картинку. : {traceback.format_exc()}')
                    images = []
                flats.append(Flat(
                    link=link,
                    title=title,
                    price=price,
                    price_meter=price_meter,
                    city=city,
                    description=description,
                    date=date,
                    reference=self.get_parser_name(),
                    images=images
                ))
                print(f'Спаршено {counter} из {len(links)}')
            return flats
        except Exception as e:
            logging.error(f'Не удалось спарсить квартиру. {traceback.format_exc()}')    
        return flats
            

# links = RealtParser().get_all_last_flats_links()
# RealtParser().enrich_links_to_flats(links)

