import re
from datetime import datetime

n_pattern = re.compile(r'^n\d+')  # n60 == N60
mg_pattern = re.compile(r'\d+мг')  # 150мг
g_pattern = re.compile(r'\d+г')  # 150мг

class BColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_current_time(response):
    current_time = datetime.now().strftime('%H:%M:%S %d-%m-%y')
    print(
        BColors.OKBLUE +
        '{} Processing record at {}'.format(current_time, response.url) +
        BColors.ENDC
    )


def get_current_datetime():
    return datetime.now().strftime('%H:%M:%S %d-%m-%y')


def get_correct_tags(item):
    if n_pattern.search(item):
        return item.replace('n', '№').split()

    if mg_pattern.search(item):
        return item.replace('мг', ' мг').split()

    if g_pattern.search(item):
        return item.replace('г', ' г').split()

    return item.split()

