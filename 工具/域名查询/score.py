import pymongo
import pandas as pd
import numpy as np
def operating_data_mongodb():
    try:
        con = pymongo.MongoClient('mongodb://root:#HITnist327@10.245.146.43:27077')
        return con
    except Exception as e:
        print(e)

def get_Matrix(coll):
    finded = coll.find({})
    data1 = []
    count = 0
    for i in finded:
        A1 = i.get("注册商得分")
        A2 = i.get("顶级域得分")
        A3 = i.get("NS信息得分")
        if(A3>9):
            A3 = 9
        elif(A3<-8):
            A3=-8
        A4 = i.get("别名得分")
        if(A4>9):
            A4=9
        elif(A4<-8):
            A4=-8
        A5 = i.get("IP对应物理地址得分")
        A6 = i.get("CDN得分")
        list = [A1,A2,A3,A4,A5,A6]
        data1.append(list)
        count += 1
    return data1




def CRITIC(DataMatrix):
    data1 = np.array(DataMatrix)
    data2 = data1
    [m, n] = data2.shape
    #指标标准化
    index = np.arange(n)
    for j in index:
        d_max = 9
        d_min = -8
        data2[:, j] = (data1[:, j] - d_min) / (d_max - d_min)
    # 对比性
    the = np.std(data2, axis=0)
    # 矛盾性
    data3 = list(map(list, zip(*data2)))  # 矩阵转置
    r = np.corrcoef(data3)  # 求皮尔逊相关系数
    f = np.sum(1 - r, axis=1)
    # 信息承载量
    c = the * f
    # 计算权重
    w = c / sum(c)
    return w


def score_for_one_domain(i):
    name = i.get('域名')
    A1 = i.get("注册商得分")
    A2 = i.get("顶级域得分")
    A3 = i.get("NS信息得分")
    if (A3 > 9):
        A3 = 9
    elif (A3 < -8):
        A3 = -8
    A4 = i.get("别名得分")
    if (A4 > 9):
        A4 = 9
    elif (A4 < -8):
        A4 = -8
    A5 = i.get("IP对应物理地址得分")
    A6 = i.get("CDN得分")
    CRITIC_weight = [0.047889125197668136,0.351345749646376,0.2112867083266102,0.047860375100039806,0.2563689702800858,0.08524907144921996]
    AHP_weight = [0.54468497,0.02222055,0.11310587,0.04492874,0.14546515,0.12959472]
    weight = []
    for i in range (0,6) :
        weight.append((CRITIC_weight[i] + AHP_weight[i]) / 2)
    final_score = round(A1*weight[0]+A2*weight[1]+A3*weight[2]+A4*weight[3]+A5*weight[4]+A6*weight[5],2)

    return final_score


if __name__ == '__main__':
    '''
    DataMatrix = get_Matrix()
    CRITIC_weight = list(CRITIC(DataMatrix))
    print(CRITIC_weight)
    subjrctive_weight = [0.167,0.167,0.167,0.167,0.167,0.167]
    final_weight = []
    for i in range (0,6):
        final_weight.append((CRITIC_weight[i]+subjrctive_weight[i])/2)
    score()
    con.close()
    '''


