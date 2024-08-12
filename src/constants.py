"""Константы."""
from pathlib import Path


BASE_DIR = Path(__file__).parent
MAIN_DOC_URL = 'https://docs.python.org/3/'
PEP_URL = 'https://peps.python.org/'
LOG_DIR = BASE_DIR / 'logs'
LOG_FILE = LOG_DIR / 'parser.log'
LOGGING_INFO_LIST = []
RESULTS_DIR = 'results'
DOWNLOADS_DIR = 'downloads'
LOG_FORMAT = '"%(asctime)s - [%(levelname)s] - %(message)s"'
DT_FORMAT = '%d.%m.%Y %H:%M:%S'
DATETIME_FORMAT = '%Y-%m-%d_%H-%M-%S'
MODE_PRETTY = 'pretty'
MODE_FILE = 'file'
FACT_STATUS = {
    'A': 0,
    'D': 0,
    'F': 0,
    'P': 0,
    'R': 0,
    'S': 0,
    'W': 0,
    '': 0,
}
EXPECTED_STATUS = {
    'A': ('Active', 'Accepted'),
    'D': ('Deferred',),
    'F': ('Final',),
    'P': ('Provisional',),
    'R': ('Rejected',),
    'S': ('Superseded',),
    'W': ('Withdrawn',),
    '': ('Draft', 'Active'),
}
