# -*- coding: utf-8 -*-
import os
import re
from os import listdir
import jieba
from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import KMeans
from gensim.models import word2vec
from gensim import models

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.manifold import TSNE

all_file = listdir('../数据库/db_data')
labels = []
corpus = []
size = 500
outputDir = 'Out_data/'
fileSegWordDonePath = 'corpusSegDone_1.txt'


def buildSW():
    '''停用词的过滤'''
    typetxt = []  # 停用词文档地址
    texts = ['\u3000', '\n', ' ']  # 爬取的文本中未处理的特殊字符
    '''停用词库的建立'''
    for word in typetxt:
        word = word.strip()
        texts.append(word)
    return texts


def buildWB(texts):
    '''语料库的建立'''
    output = open('all_cut_data.txt', 'w', encoding='utf-8')
    for i in range(0, len(all_file)):
        filename = all_file[i]
        filelabel = filename.split('.')[0]
        labels.append(filelabel)  # 名称列表
        file_add = '../数据库/db_data/' + filename  # 数据集地址
        doc = open(file_add, encoding='utf-8').read()
        data = jieba.cut(doc)  # 文本分词
        FullData = ' '.join(data)
        output.writelines(FullData)
        corpus.append(FullData)
        data_adj = ''
        delete_word = []
        #for item in data:
        #    print(item)
        #    print('------------------------')
        #    #if item not in texts:  # 停用词过滤
        #        # value=re.compile(r'^[0-9]+$')#去除数字
        #        value = re.compile(r'^[\u4e00-\u9fa5]{2,}$')  # 只匹配中文2字词以上
        #        if value.match(item):
        #            data_adj += item + ' '
        #    else:
        #        delete_word.append(item)
        #corpus.append(data_adj)  # 语料库建立完成
    #print(corpus)
    return corpus


def countIdf(corpus):
    vectorizer = CountVectorizer()  # 该类会将文本中的词语转换为词频矩阵，矩阵元素a[i][j] 表示j词在i类文本下的词频
    count_vector = vectorizer.fit_transform(corpus)
    transformer = TfidfTransformer()  # 转换Tf矩阵
    tfidf = transformer.fit_transform(count_vector)  # 将TF转换成Tf-Idf
    #arr = tfidf.toarray()
    word = vectorizer.get_feature_names()
    #transformer = TfidfTransformer()  # 该类会统计每个词语的tf-idf权值
    #tfidf = transformer.fit_transform(
    #    vectorizer.fit_transform(corpus))  # 第一个fit_transform是计算tf-idf，第二个fit_transform是将文本转为词频矩阵
    #word = vectorizer.get_feature_names()  # 获取词袋模型中的所有词

    #with open(fileSegWordDonePath, 'w', encoding='utf-8') as fw:
    #    i = 0
    #    for j in range(len(word)):
    #        if weight[1][j] != 0:
    #            i = i + 1
    #            print(i)
    #            print(word[j], weight[1][j])
    #            fw.write(word[j])
    #            fw.write('\n')
    return word


def main():
    num_features = 100  # Word vector dimensionality
    min_word_count = 1  # Minimum word count
    num_workers = 10  # Number of threads to run in parallel
    context = 5  # Context window size
    downsampling = 1e-3  # Downsample setting for frequent words
    sentences = word2vec.Text8Corpus("all_cut_data.txt")
    model = word2vec.Word2Vec(sentences, workers=num_workers, size=num_features, min_count=min_word_count,
                              window=context, sg=1, sample=downsampling)
    model.init_sims(replace=True)
    # 保存模型，供日後使用
    model.save("data_corpus.model")


if __name__ == '__main__':
    #texts = buildSW()
    #corpus = buildWB(texts)
    #print(corpus)
    #print(len(corpus))
    #weight = countIdf(corpus)
    #print(weight)
    #print(len(weight))
    main()
    model = models.Word2Vec.load('data_corpus.model')
    result = model.most_similar('增速', topn=10)
    print(result)