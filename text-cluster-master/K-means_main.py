# -*- coding: utf-8 -*-
import os
import re
from os import listdir
import jieba
from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import KMeans

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.manifold import TSNE

all_file = listdir('Data_catch/db_data')
labels = []
corpus = []
size = 500
outputDir = 'Out_data/'


def buildSW():
    '''停用词的过滤'''
    typetxt = open('stopwords.txt', encoding='utf-8')  # 停用词文档地址
    texts = ['\u3000', '\n', ' ']  # 爬取的文本中未处理的特殊字符
    '''停用词库的建立'''
    for word in typetxt:
        word = word.strip()
        texts.append(word)
    return texts


def buildWB(texts):
    '''语料库的建立'''
    for i in range(0, len(all_file)):
        filename = all_file[i]
        print(filename)
        filelabel = filename.split('.')[0]
        labels.append(filelabel)  # 名称列表
        file_add = 'Data_catch/db_data/' + filename  # 数据集地址
        doc = open(file_add, encoding='utf-8').read()
        # print(doc)
        data = jieba.cut(doc)  # 文本分词
        data_adj = ''
        delete_word = []
        for item in data:
            if item not in texts:  # 停用词过滤
                # value=re.compile(r'^[0-9]+$')#去除数字
                value = re.compile(r'^[\u4e00-\u9fa5]{2,}$')  # 只匹配中文2字词以上
                if value.match(item):
                    data_adj += item + ' '
            else:
                delete_word.append(item)
        corpus.append(data_adj)  # 语料库建立完成
    # print(corpus)
    return corpus


def countIdf(corpus):
    vectorizer = CountVectorizer()  # 该类会将文本中的词语转换为词频矩阵，矩阵元素a[i][j] 表示j词在i类文本下的词频
    transformer = TfidfTransformer()  # 该类会统计每个词语的tf-idf权值
    tfidf = transformer.fit_transform(
        vectorizer.fit_transform(corpus))  # 第一个fit_transform是计算tf-idf，第二个fit_transform是将文本转为词频矩阵
    weight = tfidf.toarray()  # 将tf-idf矩阵抽取出来，元素a[i][j]表示j词在i类文本中的tf-idf权重
    word = vectorizer.get_feature_names()  # 获取词袋模型中的所有词
    for j in range(len(word)):
        if weight[1][j] != 0:
            print(word[j], weight[1][j])
    return weight


def Kmeans(weight, clusters, correct):
    mykms = KMeans(n_clusters=clusters)
    y = mykms.fit_predict(weight)
    mykms.fit(weight)
    centoids = mykms.cluster_centers_
    predict_label = mykms.predict(weight)
    print(predict_label,centoids)
    result = []
    for i in range(0, clusters):
        label_i = []
        G5 = 0
        CY = 0
        DZ = 0
        JW = 0
        XG = 0
        for j in range(0, len(y)):
            if y[j] == i:
                label_i.append(labels[j])
                type = labels[j][0:2]
                if (type == '5G'):
                    G5 += 1
                elif (type == 'CY'):
                    CY += 1
                elif (type == 'DZ'):
                    DZ += 1
                elif (type == 'JW'):
                    JW += 1
                elif (type == 'XG'):
                    XG += 1
        max = G5
        type = '5G时代'
        if (CY > G5):
            max = CY
            type = '春运'
        if (max < DZ):
            max = DZ
            type = '廊坊4.3级地震'
        if (max < JW):
            max = JW
            type = '全国降温'
        if (max < XG):
            max = XG
            type = '香港暴动'
        correct[0] += max
        result.append('类别' + '(' + type + ')' + ':' + str(label_i))
    for i in result:
        print(i)

    tsne = TSNE(n_components=2)
    decomposition_data = tsne.fit_transform(weight)
    x = []
    y = []
    for i in decomposition_data:
        x.append(i[0])
        y.append(i[1])
    fig = plt.figure(figsize=(10, 10))
    ax = plt.axes()
    plt.scatter(x, y, c=mykms.labels_, marker='x')
    plt.xticks(())
    plt.yticks(())
    plt.show()

    return result


def output(result, outputDir, clusters):
    outputFile = 'out'
    type = '.txt'
    count = 0
    while (os.path.exists(outputDir + outputFile + type)):
        count += 1
        outputFile = 'out' + str(count)
    doc = open(outputDir + outputFile + type, 'w')
    for i in range(0, clusters):
        print(result[i], file=doc)
    print('本次分类总样本数目为:' + str(size) + ' 其中正确分类数目为:' + str(correct[0]) + ' 正确率为：' + str(correct[0] / size), file=doc)
    doc.close()


if __name__ == '__main__':
    texts = buildSW()
    corpus = buildWB(texts)
    print(corpus)
    weight = countIdf(corpus)
    clusters = 20
    correct = [0]
    result = Kmeans(weight, clusters, correct)
    output(result, outputDir, clusters)
    print('finish')
