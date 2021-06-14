"""Ядро парсера. """

from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from beer_parser.exceptions import ThereAreNoLinksForParsing, ThereAreNoProducts


class BaseParser:
    """Базовый класс для парсера"""

    def __init__(self, base_catalog_url):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 ('
                          'KHTML, like Gecko) Chrome/90.0.4430.212 YaBrowser/21.5.2.644 '
                          'Yowser/2.5 Safari/537.36'
        }

        self.links = []
        self.main_catalog = base_catalog_url
        self.products = []
        self.soup = None

    def download_page(self, url: str):
        """Реализует загрузку страницы через requests. """

        response = requests.get(url, headers=self.headers)
        response.raise_for_status()

        return response.content.decode('utf-8')

    def get_ready_page(self, url: str):
        """Загружает страницу и возвращает BeautifulSoup. """

        page = self.download_page(url)
        soup = self.make_soup(page)
        return soup


    def make_soup(self, page_content):
        """Превращает контент в объект BeautifulSoup. """

        return BeautifulSoup(page_content, 'html.parser')

    def parse_links(self):
        """Парсим главный каталог, чтобы собрать ссылки. """

        page = self.get_ready_page(self.main_catalog)
        links_soup = page.select('.menu .item_level2 a')

        for link in links_soup:
            self.links.append(
                    urljoin(self.main_catalog, link['href']),
            )
        print(self.links)

    def parse_products(self):
        """Парсим товары. """

        if not self.links:
            raise ThereAreNoLinksForParsing

        for link in self.links:
            page = self.get_ready_page(link)
            items = page.select('div.catalogitem')

            if not items:
                raise ThereAreNoProducts

            for item in items:
                title = item.find('div', class_='desc').get_text(strip=True)
                price = item.find('div', class_='normalprice').get_text(strip=True)
                images = item.find("img")["src"]

                self.products.append({
                    'title': title,
                    'price': price,
                    'images': images
                })

    def save_to_file(self):
        with open(f'parse_1.txt', 'a') as file:
            for product in self.products:
                file.write(
                    f'{product["title"]} -> Prise: {product["price"]} -> '
                    f'scr: https://mastergradus.ru{product["images"]}\n'
                )
