# -*- coding: utf-8 -*-
# coding: unicode_escape
import pandas as pd


def read_Data():
    data_list_100000 = []
    data = open('5_thousand_3.csv', 'r', encoding='utf8')
    data_list = data.readlines()
    for item in data_list:
        item = item.split(',')
        data_list_100000.append(item[0])
        print(item[0])
    return data_list_100000




def getUniqueItems(iterable):
    seen = set()
    result = []
    for item in iterable:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result


def getDB(result):
    i = 1
    #print(result)
    for item in result:
        filename = 'db_data/' + 'XW' + '(' + str(i) + ')' + '.txt'
        i = i + 1
        with open(filename, 'w', encoding='utf8') as fh:
            fh.write(item)


if __name__ == '__main__':
    a1 = read_Data()
    print(len(a1))
    b = getUniqueItems(a1)
    getDB(b)

