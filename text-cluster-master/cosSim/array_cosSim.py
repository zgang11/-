import numpy as np


def create_docSim():
    data = np.load('data_list.npy')
    average_docSimilarity = []
    for i in range(0, 100):
        # print(data[i])
        sim = 0
        for j in range(0, 100):
            sim = data[i][j] + sim
            # print(sim)
            # print(i, j)
        sim = sim / 100
        average_docSimilarity.append(sim)
    # print(average_docSimilarity)
    return average_docSimilarity


def create_coreDoc(docSim):
    coreDoc = []
    for i in range(0, 100):
        core_item = []
        if docSim[i] > 0.80:
            core_item.append(docSim[i])
            core_item.append(i)
            #print(core_item)
            coreDoc.append(core_item)
    #print(coreDoc)
    return coreDoc

def create_center(coreDoc):
    docSimilarity = np.load('data_list.npy')
    center = []
    center.append(coreDoc[0])
    coreDoc.pop(0)
    center.append(coreDoc[5])
    coreDoc.pop(5)
    center.append(coreDoc[5])
    coreDoc.pop(5)
    center.append(coreDoc[4])
    coreDoc.pop(4)
    center.append(coreDoc[0])
    coreDoc.pop(0)
    print(coreDoc)
    print(center)
    print(docSimilarity[27][15])
    print(docSimilarity[27][18])
    print(docSimilarity[27][19])
    print(docSimilarity[27][27])
    print(docSimilarity[27][45])






if __name__ == '__main__':
   docSim = create_docSim()
   coreDoc =  create_coreDoc(docSim)
   create_center(coreDoc)
