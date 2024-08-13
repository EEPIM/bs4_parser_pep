"""Перехват ошибок."""
import logging

from bs4 import BeautifulSoup

from exceptions import ParserFindTagException
from requests import RequestException


def get_response(session, url, encoding='utf-8'):
    """Перехват ошибки RequestException."""
    try:
        response = session.get(url)
        response.encoding = encoding
        return response
    except RequestException:
        raise RequestException('Страница недоступна')


def find_tag(soup, tag, attrs=None):
    """Перехват ошибки поиска тегов."""
    searched_tag = soup.find(tag, attrs=(attrs or {}))
    if searched_tag is None:
        error_msg = f'Не найден тег {tag} {attrs}'
        logging.error(error_msg)
        raise ParserFindTagException(error_msg)
    return searched_tag


def response_soup(session, url, features='lxml'):
    """Получение кода страницы."""
    response = get_response(session, url)
    return BeautifulSoup(response.text, features=features)
