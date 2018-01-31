# import json
from pprint import pprint


def log(*args):
    if len(args) == 1:
        pprint(*args)
    else:
        print(*args)


def str_stream(string: str):
    ignore = (' ', '\n', '\r', '\t')
    for i in string:
        if i not in ignore:
            yield i


def str_from_ss(ss: str_stream):
    s = []
    for char in ss:
        if char == '"':
            return ''.join(s)
        else:
            s.append(char)


def key_from_ss(ss: str_stream):
    char = next(ss)
    if char == '"':
        key = str_from_ss(ss)
        if next(ss) == ':':
            return key
    log('read key error')
    return


def num_from_ss(ss: str_stream, first_num: str):
    num = [str(i) for i in range(10)]
    num.append('.')
    s = [first_num]
    for char in ss:
        if char not in num:
            str_s = ''.join(s)
            if '.' in str_s:
                return float(str_s), char
            else:
                return int(str_s), char
        else:
            s.append(char)


def bool_from_ss(ss: str_stream, first_char):
    if first_char == 't':
        b, bool_str = True, 'rue'
    else:
        b, bool_str = False, 'alse'
    for char in bool_str:
        if char != next(ss):
            log('read bool error')
    else:
        return b


def value_from_ss(ss: str_stream):
    char = next(ss)
    if char == '"':
        value = str_from_ss(ss)
        log(value)
        tail_char = next(ss)

    elif char in [str(i) for i in range(10)]:
        value, tail_char = num_from_ss(ss, char)
        log(value)

    elif char in ('t', 'f'):
        value = bool_from_ss(ss, char)
        tail_char = next(ss)

    elif char == '{':
        value = dict_from_ss(ss)
        tail_char = next(ss)

    elif char == '[':
        value = list_from_ss(ss)
        tail_char = next(ss)

    return value, tail_char


def read_kv(d: dict, ss: str_stream):
    key = key_from_ss(ss)
    value, tail_char = value_from_ss(ss)

    d[key] = value
    if tail_char == ',':
        return read_kv(d, ss)
    elif tail_char == '}':
        return d
    else:
        log('make dict error')


def dict_from_ss(ss: str_stream):
    d = dict()
    return read_kv(d, ss)


def read_item(ls: list, ss: str_stream):
    item, tail_char = value_from_ss(ss)
    ls.append(item)
    if tail_char == ',':
        return read_item(ls, ss)
    elif tail_char == ']':
        return ls
    else:
        log('read item error')


def list_from_ss(ss: str_stream):
    ls = list()
    return read_item(ls, ss)


def load(string: str):
    ss = str_stream(string)
    char = next(ss)
    if char == '{':
        return dict_from_ss(ss)
    elif char == '[':
        return list_from_ss(ss)
    else:
        log('error')


if __name__ == '__main__':
    test = '''{
     "aa": 1,
     "bb": "Python",
     "cc": 2.5,
     "dd": true,
     "e": {"f": 1},
     "f": [
        "g",
        "h"
     ]
}
    '''
    # test = '[1, 2, 3]'
    d = load(test)
    log(d)
