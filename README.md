# Проект парсинга документации Python

Проект парсит информацию об обновлениях, ссылки на версии обновлений, их скачивание, а так же парсит количество PEPов.

### Авторы:

Евгений

### Стэк:

Python, bs4, request, tqdm

### Как запустить проект:

Форкнуть и клонировать репозиторий.

```
git@github.com:EEPIM/bs4_parser_pep.git
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

```
source env/bin/activate
```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Перейти в папку src и запустить проект. Команда для запуска парсера PEP в качестве примера:

```
python main.py pep --output pretty
```

```
где, --output pretty - режим вывода в красивой таблице в командную строку.
```
