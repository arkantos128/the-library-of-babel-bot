import random as rnd
from random import random
from config import library
from hashlib import sha512


def to_text(num):
    if num < 0:
        sign = -1
    elif num == 0:
        return library['alphabet'][0]
    else:
        sign = 1
    num *= sign
    digits = []
    while num:
        digits.append(library['alphabet'][num % 29])
        num //= 29
    if sign < 0:
        digits.append('-')
    digits.reverse()
    return ''.join(digits)


def string_to_number(string):
    result = 0
    for x in range(len(string)):
        result += library['alphabet'].index(string[len(string) - x - 1]) * pow(29, x)
    return result


def int_to_base(x, base):
    if x < 0:
        sign = -1
    elif x == 0:
        return library['digs'][0]
    else:
        sign = 1
    x *= sign
    digits = []
    while x:
        digits.append(library['digs'][x % base])
        x //= base
    if sign < 0:
        digits.append('-')
    digits.reverse()
    return ''.join(digits)


def generate_addr():
    return [
        str(int(random() * library['wall'] + 1)),
        str(int(random() * library['shelf'] + 1)),
        str(int(random() * library['volume'] + 1)).zfill(2),
        str(int(random() * library['page'] + 1)).zfill(3)
    ]


def get_text(address, text_len):
    addr_list = address.split('-')
    hex = addr_list[0]
    if text_len == library['title_len']:
        hash_str = ''.join(addr_list[1:4])
    else:
        hash_str = ''.join(addr_list[1:])
    hash_int = int(hash_str)
    key = int(hex, 36) - (hash_int * library['mult'])
    str_36 = int(int_to_base(key, 36), 36)
    result = to_text(str_36)
    rnd.seed(result)
    while len(result) < text_len:
        result += library['alphabet'][int(random() * len(library['alphabet']))]
    return result[:text_len]


def search_page(search_str):
    addr = generate_addr()
    loc_int = int(''.join(addr))
    depth = int(random() * (library['page_len'] - len(search_str)))
    for i in range(depth):
        search_str = library['alphabet'][int(random() * len(library['alphabet']))] + search_str
    for i in range(library['page_len'] - (depth + len(search_str))):
        search_str = search_str + library['alphabet'][int(random() * len(library['alphabet']))]
    str_num = string_to_number(search_str)
    hex = int_to_base(str_num + (loc_int * library['mult']), 36)
    return '{0}-{1}-{2}-{3}-{4}'.format(hex, addr[0], addr[1], addr[2], addr[3])


def get_page(address: str):
    return get_text(address, library['page_len'])


def get_title(address: str):
    return get_text(address, library['title_len'])


def search_title(search_str: str):
    addr = generate_addr()
    loc_int = int(''.join(addr[:3]))  # w/o page
    search_str = search_str[:library['title_len']].ljust(library['title_len'])
    str_num = string_to_number(search_str)
    hex = int_to_base(str_num + (loc_int * library['mult']), 36)
    return '{0}-{1}-{2}-{3}'.format(hex, addr[0], addr[1], addr[2])


def check_address(address):
    addr_list = address.split('-')
    if len(addr_list) != 5:
        return False
    for char in addr_list[0]:
        if char not in library['digs']:
            return False
    try:
        if int(addr_list[1]) > library['wall'] or int(addr_list[2]) > library['shelf'] or \
                int(addr_list[3]) > library['volume'] or int(addr_list[4]) > library['page']:
            return False
    except:
        return False
    return True


def clear_text(text: str):
    for char in text:
        if char not in library['alphabet']:
            text = text.replace(char, '')
    return text


def ending_class(num):
    if 5 <= num <= 20:
        return 2
    num = num % 10
    if num == 1:
        return 0
    if 2 <= num <= 4:
        return 1
    if 5 <= num <= 9 or num == 0:
        return 2
