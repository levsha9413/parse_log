import re
import json


get_pattern = re.compile(r'GET')
post_pattern = re.compile(r'POST')
put_pattern = re.compile(r'PUT')
delete_pattern = re.compile(r'DELETE')

def get_string():
    '''
    возвращает объект генератор для работы с большим файлом
    '''
    with open("./access.log", "r") as logs:
        for string in logs:
            yield string

logs = get_string()

get_request_count = 0
post_request_count = 0
put_request_count = 0
delete_request_count = 0
for string in logs:
    if get_pattern.search(string):
        get_request_count += 1
    elif post_pattern.search(string):
        post_request_count += 1
    elif put_pattern.search(string):
        put_request_count += 1
    elif delete_pattern.search(string):
        delete_request_count +=1

print(f'GET={get_request_count}\nPOST={post_request_count}\nPUT={put_request_count}\nDELETE={delete_request_count}')
print(f'Requests count={get_request_count+post_request_count+put_request_count+delete_request_count}')
