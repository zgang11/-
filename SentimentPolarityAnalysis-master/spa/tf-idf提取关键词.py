# -*- coding: utf-8 -*-
import re
import jieba
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
import csv

import datetime
from multiprocessing import Process

from spa.feature_extraction import ChiSquare
from spa.tools import get_accuracy
from spa.tools import Write2File
import time as Time

import requests
from bs4 import BeautifulSoup
import pymysql
import MySQLdb

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
    with open('newsList.csv', newline='', encoding='UTF-8') as csvfile:
        rows = csv.reader(csvfile)
        for row in rows:
            doc = row[1]
            data = jieba.cut(doc)
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
        print(corpus)
        return corpus
    '''语料库的建立'''
    # for i in range(0, len(all_file)):
    #    filename = all_file[i]
    #    print(filename)
    #    filelabel = filename.split('.')[0]
    #    labels.append(filelabel)  # 名称列表
    #    file_add = 'Data_catch/db_data/' + filename  # 数据集地址
    #    doc = open(file_add, encoding='utf-8').read()
    #    print(doc)
    #    data = jieba.cut(doc)  # 文本分词
    #    data_adj = ''
    #    delete_word = []
    #    for item in data:
    #        if item not in texts:  # 停用词过滤
    #            # value=re.compile(r'^[0-9]+$')#去除数字
    #            value = re.compile(r'^[\u4e00-\u9fa5]{2,}$')  # 只匹配中文2字词以上
    #            if value.match(item):
    #                data_adj += item + ' '
    #        else:
    #            delete_word.append(item)
    #    corpus.append(data_adj)  # 语料库建立完成
    # print(corpus)
    # return corpus


def countIdf(corpus):
    vectorizer = CountVectorizer()  # 该类会将文本中的词语转换为词频矩阵，矩阵元素a[i][j] 表示j词在i类文本下的词频
    transformer = TfidfTransformer()  # 该类会统计每个词语的tf-idf权值
    tfidf = transformer.fit_transform(
        vectorizer.fit_transform(corpus))  # 第一个fit_transform是计算tf-idf，第二个fit_transform是将文本转为词频矩阵
    weight = tfidf.toarray()
    word = vectorizer.get_feature_names()  # 获取词袋模型中的所有词

    for j in range(len(word)):
        if weight[0][j] > 0.2:
            print(word[j], weight[0][j])
    return weight


def countIdf_index(corpus, index):
    vectorizer = CountVectorizer()  # 该类会将文本中的词语转换为词频矩阵，矩阵元素a[i][j] 表示j词在i类文本下的词频
    transformer = TfidfTransformer()  # 该类会统计每个词语的tf-idf权值
    tfidf = transformer.fit_transform(
        vectorizer.fit_transform(corpus))  # 第一个fit_transform是计算tf-idf，第二个fit_transform是将文本转为词频矩阵
    weight = tfidf.toarray()  # 将tf-idf矩阵抽取出来，元素a[i][j]表示j词在i类文本中的tf-idf权重
    word = vectorizer.get_feature_names()  # 获取词袋模型中的所有词
    arr = []
    for j in range(len(word)):
        if weight[index - 1][j] > 0.2:
            print(word[j], weight[index - 1][j])
            arr.append(word[j])
    return arr


class Test:
    def __init__(self, type_, train_num, test_num, feature_num, max_iter, C, k, corpus):
        self.type = type_
        self.train_num = train_num
        self.test_num = test_num
        self.feature_num = feature_num
        self.max_iter = max_iter
        self.C = C
        self.k = k
        self.parameters = [train_num, test_num, feature_num]

        # get the f_corpus
        self.train_data, self.train_labels = corpus.get_train_corpus(train_num)
        self.test_data, self.test_labels = corpus.get_test_corpus(test_num)

        # feature extraction
        fe = ChiSquare(self.train_data, self.train_labels)
        self.best_words = fe.best_words(feature_num)

        self.single_classifiers_got = False

        self.precisions = [[0, 0],  # bayes
                           [0, 0],  # maxent
                           [0, 0]]  # svm

    def set_precisions(self, precisions):
        self.precisions = precisions

    def test_knn(self):
        from spa.classifiers import KNNClassifier

        if type(self.k) == int:
            k = "%s" % self.k
        else:
            k = "-".join([str(i) for i in self.k])

        print("KNNClassifier")
        print("---" * 45)
        print("Train num = %s" % self.train_num)
        print("Test num = %s" % self.test_num)
        print("K = %s" % k)

        knn = KNNClassifier(self.train_data, self.train_labels, k=self.k, best_words=self.best_words)
        classify_labels = []

        print("KNNClassifiers is testing ...")
        for data in self.test_data:
            classify_labels.append(knn.classify(data))
        print("KNNClassifiers tests over.")

        filepath = "f_runout/KNN-%s-train-%d-test-%d-f-%d-k-%s-%s.xls" % \
                   (self.type,
                    self.train_num, self.test_num,
                    self.feature_num, k,
                    datetime.datetime.now().strftime(
                        "%Y-%m-%d-%H-%M-%S"))

        self.write(filepath, classify_labels)

    def test_bayes(self):
        print("BayesClassifier")
        print("---" * 45)
        print("Train num = %s" % self.train_num)
        print("Test num = %s" % self.test_num)

        from spa.classifiers import BayesClassifier
        bayes = BayesClassifier(self.train_data, self.train_labels, self.best_words)

        classify_labels = []
        print("BayesClassifier is testing ...")
        for data in self.test_data:
            classify_labels.append(bayes.classify(data))
        print("BayesClassifier tests over.")

        filepath = "f_runout/Bayes-%s-train-%d-test-%d-f-%d-%s.xls" % \
                   (self.type,
                    self.train_num, self.test_num, self.feature_num,
                    datetime.datetime.now().strftime(
                        "%Y-%m-%d-%H-%M-%S"))

        self.write(filepath, classify_labels, 0)

    def write(self, filepath, classify_labels, i=-1):
        results = get_accuracy(self.test_labels, classify_labels, self.parameters)
        if i >= 0:
            self.precisions[i][0] = results[10][1] / 100
            self.precisions[i][1] = results[7][1] / 100

        Write2File.write_contents(filepath, results)

    def test_maxent_iteration(self):
        print("MaxEntClassifier iteration")
        print("---" * 45)
        print("Train num = %s" % self.train_num)
        print("Test num = %s" % self.test_num)
        print("maxiter = %s" % self.max_iter)

        from spa.classifiers import MaxEntClassifier

        m = MaxEntClassifier(self.max_iter)
        iter_results = m.test(self.train_data, self.train_labels, self.best_words, self.test_data)

        filepath = "f_runout/MaxEnt-iteration-%s-train-%d-test-%d-f-%d-maxiter-%d-%s.xls" % \
                   (self.type,
                    self.train_num,
                    self.test_num,
                    self.feature_num,
                    self.max_iter,
                    datetime.datetime.now().strftime(
                        "%Y-%m-%d-%H-%M-%S"))

        results = []
        for i in range(len(iter_results)):
            try:
                results.append(get_accuracy(self.test_labels, iter_results[i], self.parameters))
            except ZeroDivisionError:
                print("ZeroDivisionError")

        Write2File.write_contents(filepath, results)

    def test_maxent(self):
        print("MaxEntClassifier")
        print("---" * 45)
        print("Train num = %s" % self.train_num)
        print("Test num = %s" % self.test_num)
        print("maxiter = %s" % self.max_iter)

        from spa.classifiers import MaxEntClassifier

        m = MaxEntClassifier(self.max_iter)
        m.train(self.train_data, self.train_labels, self.best_words)

        print("MaxEntClassifier is testing ...")
        classify_results = []
        for data in self.test_data:
            classify_results.append(m.classify(data))
        print("MaxEntClassifier tests over.")

        filepath = "f_runout/MaxEnt-%s-train-%d-test-%d-f-%d-maxiter-%d-%s.xls" % \
                   (self.type,
                    self.train_num, self.test_num,
                    self.feature_num, self.max_iter,
                    datetime.datetime.now().strftime(
                        "%Y-%m-%d-%H-%M-%S"))

        self.write(filepath, classify_results, 1)

    def test_svm(self):
        print("SVMClassifier")
        print("---" * 45)
        print("Train num = %s" % self.train_num)
        print("Test num = %s" % self.test_num)
        print("C = %s" % self.C)

        from spa.classifiers import SVMClassifier
        svm = SVMClassifier(self.train_data, self.train_labels, self.best_words, self.C)

        classify_labels = []
        print("SVMClassifier is testing ...")
        for data in self.test_data:
            classify_labels.append(svm.classify(data))
        print("SVMClassifier tests over.")

        filepath = "f_runout/SVM-%s-train-%d-test-%d-f-%d-C-%d-%s-lin.xls" % \
                   (self.type,
                    self.train_num, self.test_num,
                    self.feature_num, self.C,
                    datetime.datetime.now().strftime(
                        "%Y-%m-%d-%H-%M-%S"))

        self.write(filepath, classify_labels, 2)


def test_movie():
    from spa.corpus import MovieCorpus as Corpus

    type_ = "movie"
    train_num = 500
    test_num = 200
    feature_num = 4000
    max_iter = 10
    C = 10
    k = 13

    corpus = Corpus()

    test = Test(type_, train_num, test_num, feature_num, max_iter, C, k, corpus)

    test.test_knn()

    # test.single_multiprocess()
    # test.multiple_multiprocess()


def test_movie2():
    from spa.corpus import Movie2Corpus

    type_ = "movie2"
    train_num = 700
    test_num = 300
    feature_num = 5000
    max_iter = 100
    C = 80
    # k = 1
    k = [1, 3, 5, 7, 9, 11, 13]
    k = [1, 3, 5, 7, 9]

    corpus = Movie2Corpus()

    test = Test(type_, train_num, test_num, feature_num, max_iter, C, k, corpus)

    # test.test_knn()
    test.test_bayes()
    # test.test_maxent()
    # test.test_maxent_iteration()
    # test.test_svm()


def test_waimai():
    from spa.corpus import WaimaiCorpus

    type_ = "waimai"
    train_num = 3000
    test_num = 1000
    feature_num = 5000
    max_iter = 500
    C = 150
    k = 13
    k = [1, 3, 5, 7, 9, 11, 13]
    corpus = WaimaiCorpus()

    test = Test(type_, train_num, test_num, feature_num, max_iter, C, k, corpus)

    # test.single_multiprocess()
    # test.multiple_multiprocess()

    # test.test_knn()
    # test.test_bayes()
    # test.test_maxent()
    # test.test_maxent_iteration()
    test.test_svm()
    # test.test_multiple_classifiers()
    # test.test_multiple_classifiers2()
    # test.test_multiple_classifiers3()
    # test.test_multiple_classifiers4()


def test_waimai2():
    from spa.corpus import Waimai2Corpus

    type_ = "waimai2"
    train_num = 3000
    test_num = 1000
    feature_num = 5000
    max_iter = 100
    C = 50
    k = 1
    corpus = Waimai2Corpus()

    test = Test(type_, train_num, test_num, feature_num, max_iter, C, k, corpus)

    test.single_multiprocess()
    test.multiple_multiprocess()


def test_hotel():
    from spa.corpus import HotelCorpus

    type_ = "hotel"
    train_num = 2200
    test_num = 800
    feature_num = 5000
    max_iter = 500
    C = 150
    # k = 13
    k = [1, 3, 5, 7, 9, 11, 13]
    corpus = HotelCorpus()

    test = Test(type_, train_num, test_num, feature_num, max_iter, C, k, corpus)

    # test.test_knn()

    # test.single_multiprocess()
    # test.multiple_multiprocess()

    test.test_bayes()
    # test.test_maxent()
    # test.test_maxent_iteration()
    # test.test_svm()
    # test.test_multiple_classifiers()
    # test.test_multiple_classifiers2()
    # test.test_multiple_classifiers3()
    # test.test_multiple_classifiers4()


def test_dict(title):
    """
    test the classifier based on Sentiment Dict
    """
    print("DictClassifier")
    print("---" * 45)

    from spa.classifiers import DictClassifier

    ds = DictClassifier()

    # 对一个单句进行情感分析
    a_sentence = title  # result值: 修改前(1)/修改后(1)
    # a_sentence = "要是米饭再多点儿就好了"    # result值: 修改前(1)/修改后(0)
    # a_sentence = "要是米饭再多点儿就更好了"    # result值: 修改前(0)/修改后(0)
    # a_sentence = "不太好吃，相当难吃，要是米饭再多点儿就好了"    # result值: 修改前(1)/修改后(0)
    result = ds.analyse_sentence(a_sentence)
    return result
    print(result)

    # 对一个文件内语料进行情感分析
    # corpus_filepath = "D:/My Data/NLP/SA/waimai/positive_corpus_v1.txt"
    # runout_filepath_ = "f_runout/f_dict-positive_test.txt"
    # pos_results = ds.analysis_file(corpus_filepath, runout_filepath_, start=3000, end=4000-1)
    #
    # corpus_filepath = "D:/My Data/NLP/SA/waimai/negative_corpus_v1.txt"
    # runout_filepath_ = "f_runout/f_dict-negative_test.txt"
    # neg_results = ds.analysis_file(corpus_filepath, runout_filepath_, start=3000, end=4000-1)
    #
    # origin_labels = [1] * 1000 + [0] * 1000
    # classify_labels = pos_results + neg_results
    #
    # print(len(classify_labels))
    #
    # filepath = "f_runout/Dict-waimai-%s.xls" % (
    #     datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))
    # results = get_accuracy(origin_labels, classify_labels, [1000, 1000, 0])
    #
    # Write2File.write_contents(filepath, results)


def totalData(corpus):
    db = MySQLdb.connect(host="localhost", port=3306, user="root", passwd="123456", db="sys",
                         charset="utf8")
    cursor = db.cursor()
    with open('newsList.csv', encoding='UTF-8') as csvfile:
        rows = csv.reader(csvfile)
        i = 0
        for row in rows:
            title = row[0]
            article = row[1]
            editor = row[2]
            newssource = row[3]
            commentCount = row[4]
            time = row[5]
            neg_pos = test_dict(title)
            i = i + 1
            print(i, neg_pos)
            arr = countIdf_index(corpus, i)
            tags = arr
            str_tag = ''
            if len(tags) != 0:
                str_tag = str_tag + tags[0]
            else:
                str_tag = ''
            print(str_tag)
            # 关键词提取
            sql = "INSERT INTO article_dailydata (title,editor,newssource,commentCount,time,neg_pos,tags,article) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
            val = (title, editor, newssource, commentCount, time, neg_pos, str_tag, article)
            try:
                cursor.execute(sql, val)
                db.commit()
                print('down')
            except Exception as e:
                print(e)
                db.rollback()


if __name__ == '__main__':
    texts = buildSW()
    corpus = buildWB(texts)
    weight = countIdf(corpus)
    # test_dict()
    totalData(corpus)
    print('finish')
