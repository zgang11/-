from cosSim import cosSim
from os import listdir
import numpy as np

all_file = listdir('../Data_catch/db_data')
data = []
sim = cosSim()


def dataDB():
    for i in range(0, len(all_file)):
        filename = all_file[i]
        # print(filename)
        file_add = '../Data_catch/db_data/' + filename  # 数据集地址
        doc = open(file_add, encoding='utf-8').read()
        filename = 'db_data/' + str(i) + '.txt'
        with open(filename, 'w', encoding='utf-8') as fh:
            fh.write(doc)
        data.append(doc)
        # print(filename)

    return data


def create_docSimilarity(data):
    data_list = [[0 for i in range(500)] for j in range(500)]
    for i in range(0, len(data)):
        for j in range(0, len(data)):
            a = []
            a.append(data[i])
            a.append(data[j])
            r = sim.CalcuSim(a)
            data_list[i][j] = r
            print(data_list)
            print(i, j, r)

    print(data_list)
    np.save('data_list.npy', data_list)
    return data_list


if __name__ == '__main__':
    data = dataDB()
    data_list = create_docSimilarity(data)
    np.save('data_list1.npy', data_list)
