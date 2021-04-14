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
                               r'(?P<request_path>.+) HTTP\/(?P<http_version>.+)" (?P<status_code>\d+) '
                               r'(?P<response_size>.*) "(?P<referrer>.*)" "(?P<user_agent>.*)" "-"'))
        # В качестве аргумента указываем ссылку на лог
        # python manage.py parser http://www.almhuette-raith.at/apache-log/access.log
        def add_arguments(self, parser):
            parser.add_argument('log_url', type=str, action='store', help='url')


        def handle(self, **options):
            # кидаем ГЕТ-запрос на URL и получаем данные до тех пор, пока окно открыто
            response = requests.get(options['log_url'], stream=True)
            # если ответ не (200-299) то вызываем исключение с ответом номера ошибки
            if not response.ok:
                raise CommandError(f'URL status code: {response.status_code}')

            # С помощью tqdm создаем визульное отображение парсинга
            # В progress_bar сохраняем размер отправленного получателю тела объекта в байтах и преобразуем в int
            with tqdm(total=int(response.headers['Content-Length'])) as progress_bar:
                not_ended_line = None  # Переменная необходима, чтобы перенести незаконченную строку на следующий цикл
                log_entry_list = list() # В списке будут хранится отпарсенные данные которые пойдут в БД

            # Это делается для того, чтобы предотвратить загрузку всего ответа в память сразу
            # если размер ответа равен 1000, а chunk_size установлен на 100, мы разделим ответ на десять частей.
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk: # bool = True
                        for line in chunk.decode('utf-8').splitlines(): # Преобразуем байты в строку
                            #и разобьем на множество строк, возвращая их списком
                            try:
                                if not_ended_line: # если регулярка совпала?
                                    line = not_ended_line + line
                                # Ищем совпадения регулярный выражении в каждой строке и при их обнаружении возращаем
                                # словарь из {название группы : совпадение}
                                data = self.LOG_REGEX.match(line).groupdict()

                                #Преобразуем словарь в список, чтобы потом сохранить в модель через bulk_create
                                log_entry_list.append(LogEntry(ip=data['ip'],
                                                               user_id=data['user_id'],
                                                               user_name=data['user_name'],
                                                               date=data['date'],
                                                               method=data['method'],
                                                               request_path=data['request_path'],
                                                               http_version=data['http_version'],
                                                               status_code=data['status_code'],
                                                               response_size=data['response_size'] if data[
                                                                   'response_size'].isdigit() else 0,
                                                               referrer=data['referrer'],
                                                               user_agent=data['user_agent']
                                                               ))

                                not_ended_line = None  # Должна быть всегда None, если регулярка успешно совпала

                                # если длина списка превышает, то сохраняем что есть и чистим, чтобы не убивать память
                                if len(log_entry_list) == 1_000_000:
                                    LogEntry.objects.bulk_create(log_entry_list)
                                    log_entry_list.clear()

                            except AttributeError:  # В случае несовпадения регулярки, строку переносим на другой цикл
                                if not not_ended_line:
                                    not_ended_line = line

                        progress_bar.update(len(chunk))


                if log_entry_list:
                    LogEntry.objects.bulk_create(log_entry_list)
            
            self.stdout.write(self.style.SUCCESS('Custom command logparser completed'))