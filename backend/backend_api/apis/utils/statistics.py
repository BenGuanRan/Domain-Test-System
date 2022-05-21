from numpy import mean, median
import pymongo
from matplotlib import pyplot
import pandas as pd

tld_score_list = []
register_score_list = []
IP_score_list = []
NS_score_list = []
CDN_score_list = []
cname_score_list = []
final_score_list = []
def operating_data_mongodb():
    try:
        con = pymongo.MongoClient('mongodb://root:#HITnist327@10.245.146.43:27077')
        return con
    except Exception as e:
        print(e)

con = operating_data_mongodb()
database = con["domain_country"]
coll = database["Chinese_domain_first_score"]
coll_2 = database["Chinese_domian_final_score"]
def get_final_score():
    finded = coll_2.find({})
    for i in finded:
        final_score_list.append(i.get('分数'))

def get_data():
    finded = coll.find({})
    for i in finded:
        tld_score = i.get('顶级域得分')
        register_score = i.get('注册商得分')
        IP_score = i.get('IP对应物理地址得分')
        NS_score = i.get('NS信息得分')
        CDN_score = i.get('CDN得分')
        cname_score = i.get('别名得分')
        if(tld_score!=0):
            tld_score_list.append(tld_score)
        if(register_score!=0):
            register_score_list.append(register_score)
        if(IP_score!=0):
            IP_score_list.append(IP_score)
        if(NS_score!=0):
            if(NS_score>=9):
                NS_score_list.append(9)
            elif(NS_score<=-8):
                NS_score_list.append(-8)
            else:
                NS_score_list.append(NS_score)
        if(CDN_score!=0):
            CDN_score_list.append(CDN_score)
        if(cname_score!=0):
            if (cname_score >= 9):
                cname_score_list.append(9)
            elif (cname_score <= -8):
                cname_score_list.append(-8)
            else:
                cname_score_list.append(cname_score)

def mean_and_medain(datalist):
    the_mean = mean(datalist)
    the_median = median(datalist)
    ret_list = [the_mean,the_median]
    return ret_list

def drawHist(s,name):
    datas = pd.Series(s)
    pyplot.hist(datas,18)
    pyplot.xlabel('Scores')
    pyplot.ylabel('Frequency')
    pyplot.title(name)
    pyplot.show()

def run():
    get_final_score()
    #print('顶级域得分平均数：',mean(tld_score_list))
    #print('顶级域得分中位数：',median(tld_score_list))
    #drawHist(register_score_list,'Register Score')
    drawHist(final_score_list, 'Final Score by CRITIC')





if __name__ == '__main__':
    run()
    con.close()