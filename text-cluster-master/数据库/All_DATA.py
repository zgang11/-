# -*- coding: utf-8 -*-
import os
import csv

def getFile():
    filenames = os.listdir('../sohu-20091019-20130819')
    print(filenames)
    print(len(filenames))
    for i in filenames:
        filepath = '../sohu-20091019-20130819/' + str(i)
        print("-------------------------------------------------")
        print(filepath)
        with open(filepath, 'r', encoding='utf-8') as fw:
            data = fw.read()
            data_list = data.split("\n")
            for item in data_list:
                data_rows = item.split("`1`2")
                result = {}
                if len(data_rows) > 2:
                    print(data_rows[1])
                    result['title'] = data_rows[1]
                    result['article'] = data_rows[2]
                    #print(result['title'], result['article'])
                    csv.writer(csv_obj).writerow([result['title'], result['article']])
                else:
                    continue


csv_obj = open('5_thousand_3.csv', 'w', encoding='utf-8', newline='')
csv.writer(csv_obj).writerow(['title', 'article'])
getFile()
#with open('../sohu-20091019-20130819/20091020', 'r', encoding='utf-8') as fw:
#    data = fw.read()
#    data_list = data.split("\n")
#    for item in data_list:
#        data_rows = item.split("`1`2")
#        result = {}
#        if len(data_rows) > 2:
#            print(data_rows[1])
#            result['title'] = data_rows[1]
#            result['article'] = data_rows[2]
#            #print(result['title'], result['article'])
#        else:
#            continue
        #print(data_rows)
    # print(data_list[1])
