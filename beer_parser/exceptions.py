"""Кастомные исключения. """


class ThereAreNoLinksForParsing(Exception):
    """Исключение, которое выбрасывается, когда список ссылок пустой (нечего парсить). """


class ThereAreNoProducts(Exception):
    """Исключение, которое выбрасывается, когда на странице нет товаров (нечего парсить). """
