from datetime import datetime

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
