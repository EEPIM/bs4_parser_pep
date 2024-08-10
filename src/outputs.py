"""Вывод."""
import csv
import datetime as dt
import logging

from prettytable import PrettyTable

from constants import BASE_DIR, DATETIME_FORMAT


def control_output(results, cli_args):
    """Выбор вывода данных."""
    output = cli_args.output
    if output == 'pretty':
        # Вывод данных в PrettyTable.
        pretty_output(results, cli_args)
    elif output == 'file':
        file_output(results, cli_args)
    else:
        default_output(results)


def default_output(results):
    """Дефолтный вывод в терминал."""
    for row in results:
        print(*row)


def pretty_output(results, cli_args):
    """Табличный вывод в терминал."""
    table = PrettyTable()

    if cli_args.mode == 'peps-versions':
        table.field_names = (
            'Статус',
            'Количество',
        )
        total = 0
        for status in results:
            table.add_row((status, results[status]))
            total += int(results[status])

        table.add_row(('Total', total))

    else:
        table.field_names = results[0]
        table.align = 'l'
        table.add_rows(results[1:])

    print(table)


def file_output(results, cli_args):
    """Вывод в файл."""
    results_dir = BASE_DIR / 'results'
    results_dir.mkdir(exist_ok=True)
    parser_mode = cli_args.mode
    now = dt.datetime.now()
    now_formatted = now.strftime(DATETIME_FORMAT)
    file_name = f'{parser_mode}_{now_formatted}.csv'
    file_path = results_dir / file_name
    with open(file_path, 'w', encoding='utf-8') as f:
        writer = csv.writer(f, dialect='unix')
        writer.writerows(results)

    logging.info(f'Файл с результатами был сохранён: {file_path}')
