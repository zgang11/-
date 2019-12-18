import pandas as pd


def read_Data():
    data = pd.read_csv('data_cluster/newsList.csv', encoding='utf8').astype(str)
    i = 1
    for title, content in zip(data['title'], data['article']):
        content_data = content.replace('[', '').replace(']', '').replace("'", '').replace(',', '')
        filename = 'db_data/' + 'QT' + '(' + str(i) + ')' + '.txt'
        i = i + 1
        with open(filename, 'w', encoding='utf8') as fh:
            fh.write(title + '\n' + content_data)
        print(filename)
    # print(data)


if __name__ == '__main__':
    read_Data()
