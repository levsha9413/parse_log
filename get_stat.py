import re
import json
import argparse
import os

parser = argparse.ArgumentParser(description='Logs parser')
parser.add_argument('--path', help='Путь к файлу или папке с логами')
args = parser.parse_args()

request_pattert = re.compile(r'(?<=\")(\w+)(?= )|POST')
ip_pattern = re.compile(r'^\d+\.\d+\.\d+\.\d+')
request_url_pattern = re.compile(r'(?<=\")(.*?)(?=\")')
time_pattern = re.compile(r'(?<= )(\w+)(?=$)')

try:
    files = os.listdir(args.path)
except NotADirectoryError:
    files = [os.path.basename(args.path)]


def get_string(file):
    '''
    возвращает объект генератор для работы с большим файлом логов,
    при работе с одним файлом
    '''
    try:
        with open(f'{args.path}/{file}', "r") as logs:
            for string in logs:
                yield string
    except NotADirectoryError:
        with open(f'{args.path}', "r") as logs:
            for string in logs:
                yield string


def different_elements_counter(log_string: str, pattern, elements_dict: dict) -> dict:
    '''

    :param log_string: принимает строку лога
    :param pattern: принимает объект re содержащий регулярку для поиска элемента
    :param elements_dict: принимает словарь, в котором обновляется количество вхождений элемента
    :return: возвращает словарь в котором ключом является элемент, а значением количество вхождений элемента в лог\
    например {get:15, post:25}  и
    '''
    search_result = pattern.search(log_string)
    if search_result:
        try:
            elements_dict[search_result.group(0)] += 1
        except KeyError:
            elements_dict[search_result.group(0)] = 1
    return elements_dict


def elements_counter(requests_dict: dict):
    '''
    :param requests_dict: словарь в котором ключом является элемент, а значением количество вхождений элемента в лог
    :return: общее количество всех найденных элементов в логе
    '''
    count = 0
    for request in requests_dict:
        count = count + requests_dict[request]
    return count


def get_top3_elements(elements_dict: dict):
    '''
    считает топ 3 элементов в словаре по значениям
    :param elements_dict:
    :return:
    '''
    sorted_dict = {k: elements_dict[k] for k in sorted(elements_dict, key=elements_dict.get, reverse=True)}
    i = 0
    result_dict = {}
    for elem in sorted_dict:
        if i < 3:
            result_dict[elem] = sorted_dict[elem]
            i += 1
        else:
            break
    return result_dict


def get_requests_time(ip_patern, request_url_pattern, time_pattern, log_string, time_dict, id):
    '''
    :param time_pattern: паттерн для поиска времени в строке string
    :param log_string: строка лога
    :param time_dict: словарь в который складываются найденные элементы
    :param id: id, нужен для уникальности каждого ключа
    :param kwargs: передаются паттерны для формирования ключа
    :return: возращает слварь с элементами формата
     {"6094 213.150.254.81 GET /templates/_system/css/general.css HTTP/1.1": "9999"}
    '''
    ip = ip_patern.search(log_string)
    request_url = request_url_pattern.search(log_string)
    time = time_pattern.search(log_string)
    if ip and request_url and time:
        ip = ip.group(0)
        request_url = request_url.group(0)
        key = f"{id} {ip} {request_url}"
        time_dict[key] = int(time.group(0))
    return time_dict


for file in files:

    logs = get_string(file)

    id = 0
    ip_dict = {}
    request_dict = {}
    time_dict = {}
    for string in logs:
        ip_dict = different_elements_counter(string, ip_pattern, ip_dict)
        request_dict = different_elements_counter(string, request_pattert, request_dict)
        time_dict = get_requests_time(ip_pattern, request_url_pattern, time_pattern, string, time_dict, id)
        id += 1

    result = {'Файл логов': file,
              'Общее количество выполненных запросов': elements_counter(request_dict),
              'Количество запросов по типу': request_dict,
              'Топ 3 IP адресов, с которых были сделаны запросы': get_top3_elements(ip_dict),
              'Топ 3 самых долгих запросов': get_top3_elements(time_dict)
              }

    result_json = json.dumps(result, sort_keys=False, indent=4, ensure_ascii=False)
    print(result_json)
    with open(f'{os.path.splitext(file)[0]}.json', 'w') as file:
        file.write(result_json)
