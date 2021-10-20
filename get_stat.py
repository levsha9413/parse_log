import re
import json


def get_string():
    with open("./access.log", "r") as logs:
        for string in logs:
            yield string


logs = get_string()

a = 0
for string in logs:

    print(a,' ', string, end='')
    a += 1
    #if a == 5:
        #break