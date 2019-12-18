import numpy as np
import matplotlib.pyplot as plt


# Initialize center函数通过使用numpy库的 zeros函数和random.uniform函数，随机选取 了k个数据做聚类中心，
# 并将结果存放在 了k个数据做聚类中心，并将结果存放在 Numpy的Array对象centers中
def InitCenters(dataSet, k):
    numSample, dim = dataSet.shape  # 获得数组的维度
    centers = np.zeros((k, dim))
    for i in range(k):
        index = int(np.random.uniform(0, numSample))  # 随机得到k个质心
        centers[i, :] = dataSet[index, :]
    print(centers)
    return centers


# Dist2Centers这个函数用来计算一个数据点到所有 聚类中心的距离，将其存放在dis2cents中返回
def Dist2Centers(sample, centers):
    k = centers.shape[0]
    dis2cents = np.zeros(k)
    for i in range(k):
        dis2cents[i] = np.sqrt(np.sum(np.power(sample - centers[i, :], 2)))
        return dis2cents


def kmeans(dataSet, k, iterNum):
    numSamples = dataSet.shape[0]
    iterCount = 0
    # clusterAssignment保存着样本属于哪个数据集
    clusterAssignment = np.zeros(numSamples)
    clusterChanged = True
    # 初始化中心点
    centers = InitCenters(dataSet, k)
    while clusterChanged and iterCount < iterNum:
        # 遍历每个样本
        for i in range(numSamples):
            dis2cent = Dist2Centers(dataSet[i, :], centers)
            minIndex = np.argmin(dis2cent)
            # 更新所属的类
            if clusterAssignment[i] != minIndex:
                clusterChanged = True
                clusterAssignment[i] = minIndex
        # 更新中心点
        for j in range(k):
            pointsInCluster = dataSet[np.nonzero(clusterAssignment[:] == j)[0]]
            centers[j:] = np.mean(pointsInCluster, axis=0)
    print("聚类完成")
    return centers, clusterAssignment


def showCluster(dataSet, k, centers, clusterAssignment):
    numSamples, dim = dataSet
    mark = ['or', 'ob', 'og', 'om']
    # 画出所有样本
    for i in range(numSamples):
        markIndex = int(clusterAssignment[i])
        plt.plot(dataSet[i, 0], dataSet[i, 1], mark[markIndex])
    mark = ['Dr', 'Db', 'Dg', 'Dm']
    # 画中心点
    for i in range(k):
        plt.plot(centers[i, 0], centers[i, 1], mark[i], markersize=17)
    plt.show()


def main():
    # 第一步：加载数据
    print("第一步：加载数据")
    dataSet = []
    dataSetFile = open('stopwords.txt', 'r', encoding='utf-8')
    for line in dataSetFile:
        lineArr = line.strip().split('\t')
        print(lineArr)
        dataSet.append([float(lineArr[1]), float(lineArr[2])])
    # 第二步：聚类
    print("第二步：聚类")
    dataSet = np.mat(dataSet)
    k = 4  # k为分成几类的参数
    centers_result, clusterAssignment_result = kmeans(dataSet, k, 100)
    # 第三步：展示结果
    print("第三步：展示结果")
    showCluster(dataSet, k, centers_result, clusterAssignment_result)


main()


