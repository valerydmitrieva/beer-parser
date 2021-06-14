"""Запуск парсера. """
from beer_parser.core import BaseParser


def main():
    parser = BaseParser('https://hootch.ru/')
    parser.parse_links()
    parser.parse_products()
    parser.save_to_file()


if __name__ == '__main__':
    main()