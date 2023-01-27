from datetime import datetime
import pytz


class clr:
    HEADER = '\033[95m'
    INFO = '\033[93m'
    CYAN = '\033[96m'
    OK = '\033[92m'
    FAIL = '\033[91m'
    BOLD = '\033[1m'
    ENDC = '\033[0m'


def print_info(code, m=None):
    print(f'{clr.INFO}{datetime.now(pytz.timezone("Europe/Paris")).strftime("%H:%M")} | <{code}>{clr.ENDC} {m}')


def print_err(code, error):
    print(f'{clr.FAIL}Error: <{code}> {error}{clr.ENDC}')
