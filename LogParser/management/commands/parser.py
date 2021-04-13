import os
import re
import requests

from django.core.management.base import BaseCommand, CommandError
from tqdm import tqdm

from LogParser.models import LogEntry
    class Command(BaseCommand):
        help = 'command for parsing a log and save it to data ( get a url for argument)'
    # Комплируем в переменную LOG_REGEX регулярки для парса строки по типу
    # После такой компиляции можно использовать переменную для обнаружения в строке по всем регуляркам сразу
    # 13.66.139.0 - - [19/Dec/2020:13:57:26 +0100] "GET /index HTTP/1.1" 200 32653 "-" "Mozilla/5.0" "-"
        LOG_REGEX = re.compile(
            os.getenv('LOG_REGEX', r'(?P<ip>.+) (?P<user_id>.+) (?P<user_name>.+) \[(?P<date>.+)\] "(?P<method>.+) '
                               r'\(?P<request_path>.+) HTTP\/(?P<http_version>.+)" (?P<status_code>\d+) '
                               r'(?P<response_size>.*) "(?P<referrer>.*)" "(?P<user_agent>.*)" "-"'))
        


