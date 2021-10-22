import re
import json

request_pattert = re.compile(r'\"(\w+) ')
ip_pattern = re.compile(r'^\d+\.\d+\.\d+\.\d+')


def get_string():
    '''
    возвращает объект генератор для работы с большим файлом
    '''
    with open("./access.log", "r") as logs:
        for string in logs:
            yield string


logs = get_string()
ip_dict = {}
request_dict = {}


def elements_counter(log_string: str, pattern, elements_dict: dict) -> dict:
    search_result = pattern.search(log_string)
    if search_result:
        try:
            elements_dict[search_result.group(0)] += 1
        except KeyError:
            elements_dict[search_result.group(0)] = 1
    return elements_dict


a = 0
for string in logs:
    ip_dict = elements_counter(string, ip_pattern, ip_dict)

    req = request_pattert.search(string)
    if req:
        try:
            request_dict[req.group(1)] += 1
        except KeyError:
            request_dict[req.group(1)] = 1

print(len(ip_dict))
print(ip_dict)
print(request_dict)
