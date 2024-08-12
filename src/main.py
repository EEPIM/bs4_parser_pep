"""Основная логика парсера."""
import logging
import re
from urllib.parse import urljoin

import requests_cache
from bs4 import BeautifulSoup
from tqdm import tqdm

from configs import configure_argument_parser, configure_logging
from constants import (
    BASE_DIR,
    DOWNLOADS_DIR,
    EXPECTED_STATUS,
    FACT_STATUS,
    LOGGING_INFO_LIST,
    MAIN_DOC_URL,
    PEP_URL
)
from exceptions import DoesNotFindTagException, EmptyResponseException
from outputs import control_output
from utils import find_tag, response_soup


def whats_new(session):
    """Парсинг обновлений."""
    whats_new_url = urljoin(MAIN_DOC_URL, 'whatsnew/')
    soup = response_soup(session, whats_new_url)
    main_div = find_tag(soup, 'section', attrs={'id': 'what-s-new-in-python'})
    div_with_ul = find_tag(main_div, 'div', attrs={'class': 'toctree-wrapper'})
    sections_by_python = div_with_ul.find_all(
        'li',
        attrs={'class': 'toctree-l1'}
    )
    results = [('Ссылка на статью', 'Заголовок', 'Редактор, автор')]
    for section in tqdm(sections_by_python):
        version_a_tag = find_tag(section, 'a')
        version_link = urljoin(whats_new_url, version_a_tag['href'])
        try:
            soup = response_soup(session, version_link)
        except EmptyResponseException:
            LOGGING_INFO_LIST.append(f'Страница {version_link} недоступна.')
            continue
        h1 = find_tag(soup, 'h1')
        dl = find_tag(soup, 'dl')
        dl_text = dl.text.replace('\n', ' ')
        results.append(
            (version_link, h1.text, dl_text)
        )
    return results


def latest_versions(session):
    """Парсинг последних версий."""
    soup = response_soup(session, MAIN_DOC_URL)
    sidebar = find_tag(soup, 'div', {'class': 'sphinxsidebarwrapper'})
    ul_tags = sidebar.find_all('ul')

    for ul in ul_tags:
        if 'All versions' in ul.text:
            a_tags = ul.find_all('a')
            break
        else:
            raise DoesNotFindTagException('Ничего не нашлось')

    results = [('Ссылка на документацию', 'Версия', 'Статус')]
    pattern = r'Python (?P<version>\d\.\d+) \((?P<status>.*)\)'

    for a_tag in a_tags:
        link = a_tag['href']
        text_match = re.search(pattern, a_tag.text)
        if text_match is not None:
            version, status = text_match.groups()
        else:
            version, status = a_tag.text, ''
        results.append(
            (link, version, status)
        )
    return results


def download(session):
    """Скачивание архивов."""
    downloads_url = urljoin(MAIN_DOC_URL, 'download.html')
    soup = response_soup(session, downloads_url)
    main_tag = find_tag(soup, 'div', attrs={'role': 'main'})
    table_tag = find_tag(main_tag, 'table', {'class': 'docutils'})
    pdf_a4_tag = find_tag(
        table_tag,
        'a',
        {'href': re.compile(r'.+pdf-a4\.zip$')}
    )
    pdf_a4_link = pdf_a4_tag['href']
    archive_url = urljoin(downloads_url, pdf_a4_link)
    filename = archive_url.split('/')[-1]
    downloads_dir = BASE_DIR / DOWNLOADS_DIR
    downloads_dir.mkdir(exist_ok=True)
    archive_path = downloads_dir / filename
    response = session.get(archive_url)

    with open(archive_path, 'wb') as file:
        file.write(response.content)

    logging.info(f'Архив был загружен и сохранён: {archive_path}')


def pep(session):
    """Парсинг версий PEP."""
    soup = response_soup(session, PEP_URL)
    all_index_section = soup.find('section', attrs={'id': 'index-by-category'})
    all_tbody = all_index_section.find_all('tbody')
    different_status = []
    for tag_tbody in all_tbody:
        all_tr = tag_tbody.find_all('tr')

        for tag_tr in all_tr:
            abbr = tag_tr.find('abbr')
            preview_status = abbr.text[1:]
            tag_a = tag_tr.find('a', class_='pep reference internal')
            href = tag_a['href']
            version_link = urljoin(PEP_URL, href)
            try:
                soup = response_soup(session, version_link)
            except EmptyResponseException:
                LOGGING_INFO_LIST.append(
                    f'Страница {version_link} недоступна.'
                )
                continue
            # response = session.get(version_link)
            # response.encoding = 'utf-8'
            # soup = BeautifulSoup(response.text, 'lxml')
            status = soup.find(
                'abbr',).text[0]

            if status != preview_status:
                different_status.append(
                    f'Несовпадающие статусы: '
                    f'{version_link} '
                    f'Статус в карточке: {EXPECTED_STATUS[status]} '
                    f'Ожидаемые статусы: {EXPECTED_STATUS[preview_status]} '
                )

            FACT_STATUS[preview_status] = FACT_STATUS.get(
                preview_status, 0
            ) + 1
    logging.info('\n'.join(different_status))
    results = [('Статус', 'Количество')]
    results.extend(FACT_STATUS.items())
    return results


MODE_TO_FUNCTION = {
    'whats-new': whats_new,
    'latest-versions': latest_versions,
    'download': download,
    'pep': pep,
}


def main():
    """Основная логика."""
    configure_logging()
    logging.info('Парсер запущен!')
    try:
        arg_parser = configure_argument_parser(MODE_TO_FUNCTION.keys())
        args = arg_parser.parse_args()
        logging.info(f'Аргументы командной строки: {args}')
        session = requests_cache.CachedSession()

        if args.clear_cache:
            session.cache.clear()

        parser_mode = args.mode
        results = MODE_TO_FUNCTION[parser_mode](session)

        if results is not None:
            control_output(results, args)
    except Exception as error:
        logging.error(error)
    finally:
        for log in LOGGING_INFO_LIST:
            logging.info(log)
        logging.info('Парсер завершил работу.')


if __name__ == '__main__':
    main()
