#coding=utf-8
import pymongo

def operating_data_mongodb():
    try:
        con = pymongo.MongoClient('mongodb://root:#HITnist327@10.245.146.43:27077')
        return con
    except Exception as e:
        print(e)

con = operating_data_mongodb()
database = con["domain_country"]
coll=database["try"]
save_coll = database["1000-5000_first_score"]
country_point_dict={"NULL":0,None:0,'CN': 9, 'China': 9, '中国': 9, 'US': -8, 'United States': -8, '美国': -8, 'DE': 6, 'Germany': 6, '德国': 6, 'GB': -1, 'United Kingdom': -1, '英国': -1, 'FR': 5.9, 'France': 5.9, '法国': 5.9, 'RU': 8.3,'Russian Federation':8.3, 'Russian': 8.3, '俄罗斯': 8.3, 'CN(HK)': 9, 'Hong Kong': 9, '香港': 9, '中国香港': 9, 'SC': -8, '美国卡罗莱纳洲': -8, 'KR': 4.2, 'Korea': 4.2, '韩国': 4.2, 'JP': -3.6, 'Japan': -3.6, '日本': -3.6, 'GER': 6, 'AU': 0.1, 'Australia': 0.1, '澳大利亚': 0.1, 'ID': 5.1, '印度尼西亚': 5.1, 'IN': 2.2, 'India': 2.2, '印度': 2.2}
def get_inform_of_one_domain(domain):
    #列表为空其值为NULL
    finaldict = {}
    domain_coin_dict = {}
    domain_coin_dict.update({"域名":domain})
    finded = coll.find({"域名":domain})[0]
    tld_country = finded.get("顶级域所属国家")
    if country_point_dict.get(tld_country) == None:
        domain_coin_dict.update({'顶级域得分': 0})
    else:
        domain_coin_dict.update({'顶级域得分':country_point_dict.get(tld_country)})
    #顶级域所处国家值
    if finded.get("注册商所属国家"):
        register_country = finded.get("注册商所属国家")     #注册商所处国家值
        if country_point_dict.get(register_country) == None:
            domain_coin_dict.update({'注册商得分': 0})
        else:
            domain_coin_dict.update({'注册商得分': country_point_dict.get(register_country)})
    else:
        domain_coin_dict.update({'注册商得分': 0})
    IP_country = finded.get("IP所处国家")               #IP所处国家列表
    IP_coin = 0
    for ip in  IP_country:
        if(ip != None) and (ip != 'NULL'):
            if country_point_dict.get(ip) != None:
                IP_coin = IP_coin + country_point_dict.get(ip)/len(IP_country)

    domain_coin_dict.update({'IP对应物理地址得分': IP_coin})
    NS_result_list = finded.get("NS服务器信息")
    NS_inform_dict = {}                                 #两个字典记录NS层级关系和NS服务器与国家对应信息
    NS_relation_dict = {}
    for NS_result in NS_result_list:
        if not NS_result.get("解析它的NS服务器域名") in NS_inform_dict:
            NS_inform_dict.update({NS_result.get("解析它的NS服务器域名"):[NS_result.get("NS服务器所属国家"),NS_result.get("NS服务器所处国家")]})
    i_list = []
    for NS_result in NS_result_list:
        if NS_result.get("域名") ==domain:
            i_list.append(NS_result.get("解析它的NS服务器域名"))
    NS_relation_dict.update({domain:i_list})
    for i in NS_inform_dict:
        i_list = []
        for NS_result in NS_result_list:
            if NS_result.get("域名") == i:
               i_list.append( NS_result.get("解析它的NS服务器域名"))
        if i_list:
            NS_relation_dict.update({i:i_list})
    NS_weight_dict = ns_weight_get(NS_relation_dict, domain)
    NS_coin = 0
    for ns in NS_inform_dict:
        ns_place_coin = 0
        ns_place_list = NS_inform_dict.get(ns)[1]
        for ns_place in ns_place_list:
            if country_point_dict.get(ns_place) != None:
                ns_place_coin =ns_place_coin + country_point_dict.get(ns_place)/len(ns_place_list)
            else:
                pass

        if ns_place_coin != None:
            if country_point_dict.get(NS_inform_dict.get(ns)[0]) !=None:
                NS_coin += NS_weight_dict.get(ns)*(0.3 * country_point_dict.get(NS_inform_dict.get(ns)[0]) + 0.7 * (ns_place_coin))  # 得到NS得分
            else:
                NS_coin += NS_weight_dict.get(ns) * ( 0.7 * (ns_place_coin))  # 得到NS得分

    domain_coin_dict.update({"NS信息得分":NS_coin})
    cdn_country = finded.get("CDN服务商信息").get("对应的国家")   #CDN所属国家列表
    CDN_coin = 0
    if len(cdn_country) != 0:
        for cdn_c in cdn_country:
            if country_point_dict.get(cdn_c) != None:
                CDN_coin += country_point_dict.get(cdn_c)/len(cdn_country)
            else:
                pass
    domain_coin_dict.update({"CDN得分":CDN_coin})
    CNAME_coin = 0
    if finded.get("别名") != None:
        cname_country_list = finded.get("别名对应注册商国家")
        cname_register_country_list = []#别名注册商国家列表
        for i in cname_country_list:
            for key in i:
                cname_register_country_list.append(i.get(key))
        if not cname_register_country_list:
            cname_register_country_list.append("NULL")
        for j in cname_register_country_list:
            if country_point_dict.get(j)!=None:
                CNAME_coin += (country_point_dict.get(j)/2)/len(cname_register_country_list)
            else:
                pass
        if(finded.get("别名的NS服务器信息")):       #下面计算每个别名的NS得分
            cname_ns_result_dict_list = finded.get("别名的NS服务器信息")
            for cname_ns_dict in cname_ns_result_dict_list:
                cname = list(cname_ns_dict.keys())[0]
                cname_ns_dict_list = cname_ns_dict.get(cname)
                cname_NS_inform_dict = {}  # 两个字典记录NS层级关系和NS服务器与国家对应信息
                cname_NS_relation_dict = {}
                for cname_NS_result in cname_ns_dict_list:
                    if not cname_NS_result.get("解析它的NS服务器域名") in cname_NS_inform_dict:
                        cname_NS_inform_dict.update(
                            {cname_NS_result.get("解析它的NS服务器域名"): [cname_NS_result.get("NS服务器所属国家"), cname_NS_result.get("NS服务器所处国家")]})
                i_list = []
                for cname_NS_result in cname_ns_dict_list:
                    if cname_NS_result.get("被解析的域名") == cname:
                        i_list.append(cname_NS_result.get("解析它的NS服务器域名"))
                cname_NS_relation_dict.update({cname: i_list})
                for i in cname_NS_inform_dict:
                    i_list = []
                    for cname_NS_result in cname_ns_dict_list:
                        if cname_NS_result.get("被解析的域名") == i:
                            i_list.append(cname_NS_result.get("解析它的NS服务器域名"))
                    if i_list:
                        cname_NS_relation_dict.update({i: i_list})
                cname_NS_weight_dict = ns_weight_get(cname_NS_relation_dict, cname)
                one_cname_NS_coin = 0
                for ns in cname_NS_inform_dict:
                    cname_ns_place_coin = 0
                    cname_ns_place_list = cname_NS_inform_dict.get(ns)[1]
                    for cname_ns_place in cname_ns_place_list:
                        if country_point_dict.get(cname_ns_place) != None:
                            cname_ns_place_coin = cname_ns_place_coin + country_point_dict.get(cname_ns_place) / len(cname_ns_place_list)
                        else:
                            pass
                    if cname_ns_place_coin != None:
                        if cname_NS_weight_dict.get(ns) != None:
                            if country_point_dict.get(cname_NS_inform_dict.get(ns)[0]) != None:
                                one_cname_NS_coin += cname_NS_weight_dict.get(ns) * (0.3 * country_point_dict.get(cname_NS_inform_dict.get(ns)[0]) + 0.7 * (cname_ns_place_coin))
                            else:
                                one_cname_NS_coin += cname_NS_weight_dict.get(ns) * (0.7 * (cname_ns_place_coin))
                CNAME_coin += (one_cname_NS_coin/2)/len(cname_ns_result_dict_list)         #算出了别名的得分
        domain_coin_dict.update({"别名得分":CNAME_coin})
    else:
        domain_coin_dict.update({"别名得分":CNAME_coin})
    finaldict = {domain : domain_coin_dict}
    return finaldict

def inform_to_score(domain,informdict):
    #列表为空其值为NULL
    finaldict = {}
    domain_coin_dict = {}
    domain_coin_dict.update({"域名":domain})
    finded = informdict
    tld_country = finded.get("顶级域所属国家")
    if country_point_dict.get(tld_country) == None:
        domain_coin_dict.update({'顶级域得分': 0})
    else:
        domain_coin_dict.update({'顶级域得分':country_point_dict.get(tld_country)})
    #顶级域所处国家值
    if finded.get("注册商所属国家"):
        register_country = finded.get("注册商所属国家")     #注册商所处国家值
        if country_point_dict.get(register_country) == None:
            domain_coin_dict.update({'注册商得分': 0})
        else:
            domain_coin_dict.update({'注册商得分': country_point_dict.get(register_country)})
    else:
        domain_coin_dict.update({'注册商得分': 0})
    IP_country = finded.get("IP所处国家")               #IP所处国家列表
    IP_coin = 0
    for ip in  IP_country:
        if(ip != None) and (ip != 'NULL'):
            if country_point_dict.get(ip) != None:
                IP_coin = IP_coin + country_point_dict.get(ip)/len(IP_country)

    domain_coin_dict.update({'IP对应物理地址得分': IP_coin})
    NS_result_list = finded.get("NS服务器信息")
    NS_inform_dict = {}                                 #两个字典记录NS层级关系和NS服务器与国家对应信息
    NS_relation_dict = {}
    for NS_result in NS_result_list:
        if not NS_result.get("解析它的NS服务器域名") in NS_inform_dict:
            NS_inform_dict.update({NS_result.get("解析它的NS服务器域名"):[NS_result.get("NS服务器所属国家"),NS_result.get("NS服务器所处国家")]})
    i_list = []
    for NS_result in NS_result_list:
        if NS_result.get("域名") ==domain:
            i_list.append(NS_result.get("解析它的NS服务器域名"))
    NS_relation_dict.update({domain:i_list})
    for i in NS_inform_dict:
        i_list = []
        for NS_result in NS_result_list:
            if NS_result.get("域名") == i:
               i_list.append( NS_result.get("解析它的NS服务器域名"))
        if i_list:
            NS_relation_dict.update({i:i_list})
    NS_weight_dict = ns_weight_get(NS_relation_dict, domain)
    NS_coin = 0
    for ns in NS_inform_dict:
        ns_place_coin = 0
        ns_place_list = NS_inform_dict.get(ns)[1]
        for ns_place in ns_place_list:
            if country_point_dict.get(ns_place) != None:
                ns_place_coin =ns_place_coin + country_point_dict.get(ns_place)/len(ns_place_list)
            else:
                pass

        if ns_place_coin != None:
            if country_point_dict.get(NS_inform_dict.get(ns)[0]) !=None:
                NS_coin += NS_weight_dict.get(ns)*(0.3 * country_point_dict.get(NS_inform_dict.get(ns)[0]) + 0.7 * (ns_place_coin))  # 得到NS得分
            else:
                NS_coin += NS_weight_dict.get(ns) * ( 0.7 * (ns_place_coin))  # 得到NS得分

    domain_coin_dict.update({"NS信息得分":NS_coin})
    cdn_country = finded.get("CDN服务商信息").get("对应的国家")   #CDN所属国家列表
    CDN_coin = 0
    if len(cdn_country) != 0:
        for cdn_c in cdn_country:
            if country_point_dict.get(cdn_c) != None:
                CDN_coin += country_point_dict.get(cdn_c)/len(cdn_country)
            else:
                pass
    domain_coin_dict.update({"CDN得分":CDN_coin})
    CNAME_coin = 0
    if finded.get("别名") != None:
        cname_country_list = finded.get("别名对应注册商国家")
        cname_register_country_list = []#别名注册商国家列表
        for i in cname_country_list:
            for key in i:
                cname_register_country_list.append(i.get(key))
        if not cname_register_country_list:
            cname_register_country_list.append("NULL")
        for j in cname_register_country_list:
            if country_point_dict.get(j)!=None:
                CNAME_coin += (country_point_dict.get(j)/2)/len(cname_register_country_list)
            else:
                pass
        if(finded.get("别名的NS服务器信息")):       #下面计算每个别名的NS得分
            cname_ns_result_dict_list = finded.get("别名的NS服务器信息")
            for cname_ns_dict in cname_ns_result_dict_list:
                cname = list(cname_ns_dict.keys())[0]
                cname_ns_dict_list = cname_ns_dict.get(cname)
                cname_NS_inform_dict = {}  # 两个字典记录NS层级关系和NS服务器与国家对应信息
                cname_NS_relation_dict = {}
                for cname_NS_result in cname_ns_dict_list:
                    if not cname_NS_result.get("解析它的NS服务器域名") in cname_NS_inform_dict:
                        cname_NS_inform_dict.update(
                            {cname_NS_result.get("解析它的NS服务器域名"): [cname_NS_result.get("NS服务器所属国家"), cname_NS_result.get("NS服务器所处国家")]})
                i_list = []
                for cname_NS_result in cname_ns_dict_list:
                    if cname_NS_result.get("被解析的域名") == cname:
                        i_list.append(cname_NS_result.get("解析它的NS服务器域名"))
                cname_NS_relation_dict.update({cname: i_list})
                for i in cname_NS_inform_dict:
                    i_list = []
                    for cname_NS_result in cname_ns_dict_list:
                        if cname_NS_result.get("被解析的域名") == i:
                            i_list.append(cname_NS_result.get("解析它的NS服务器域名"))
                    if i_list:
                        cname_NS_relation_dict.update({i: i_list})
                cname_NS_weight_dict = ns_weight_get(cname_NS_relation_dict, cname)
                one_cname_NS_coin = 0
                for ns in cname_NS_inform_dict:
                    cname_ns_place_coin = 0
                    cname_ns_place_list = cname_NS_inform_dict.get(ns)[1]
                    for cname_ns_place in cname_ns_place_list:
                        if country_point_dict.get(cname_ns_place) != None:
                            cname_ns_place_coin = cname_ns_place_coin + country_point_dict.get(cname_ns_place) / len(cname_ns_place_list)
                        else:
                            pass
                    if cname_ns_place_coin != None:
                        if cname_NS_weight_dict.get(ns) != None:
                            if country_point_dict.get(cname_NS_inform_dict.get(ns)[0]) != None:
                                one_cname_NS_coin += cname_NS_weight_dict.get(ns) * (0.3 * country_point_dict.get(cname_NS_inform_dict.get(ns)[0]) + 0.7 * (cname_ns_place_coin))
                            else:
                                one_cname_NS_coin += cname_NS_weight_dict.get(ns) * (0.7 * (cname_ns_place_coin))
                CNAME_coin += (one_cname_NS_coin/2)/len(cname_ns_result_dict_list)         #算出了别名的得分
        domain_coin_dict.update({"别名得分":CNAME_coin})
    else:
        domain_coin_dict.update({"别名得分":CNAME_coin})
    finaldict = {domain : domain_coin_dict}
    return finaldict







def ns_weight_get(NS_relation_dict,domain):     #两个字典记录NS层级关系和NS服务器与国家对应信息
    main_list = list(set(NS_relation_dict.get(domain)))
    NS_weight_dict = {}
    for level_1 in  main_list:
        if NS_relation_dict.get(level_1) != None:
            level_2_list = list(set(NS_relation_dict.get(level_1)))
            level_1_weight =  (0.5 / len(main_list))
            if(NS_weight_dict.get(level_1)):
                total_level_1_weight = level_1_weight + NS_weight_dict.get(level_1)
            else:
                total_level_1_weight = level_1_weight
            NS_weight_dict.update({level_1: total_level_1_weight})
            for level_2 in level_2_list:
                if NS_relation_dict.get(level_2) != None:
                    level_3_list = list(set(NS_relation_dict.get(level_2)))
                    level_2_weight = (level_1_weight/2*len(level_2_list))
                    if (NS_weight_dict.get(level_2)):
                        total_level_2_weight = level_2_weight + NS_weight_dict.get(level_2)
                    else:
                        total_level_2_weight = level_2_weight
                    NS_weight_dict.update({level_2:total_level_2_weight})
                    for level_3 in level_3_list:
                        if NS_relation_dict.get(level_3) != None:
                            level_4_list = list(set(NS_relation_dict.get(level_3)))
                            level_3_weight = (level_2_weight / 2 * len(level_3_list))
                            NS_weight_dict.update({level_3: level_3_weight})
                            for level_4 in level_4_list:
                                if NS_relation_dict.get(level_4)!= None:
                                    level_5_list = list(set(NS_relation_dict.get(level_4)))
                                    level_4_weight = (level_3_weight / 2 * len(level_4_list))
                                    NS_weight_dict.update({level_4: level_4_weight})
                                    for level_5 in level_5_list:
                                        level_5_weight = (level_4_weight / len(level_5_list))
                                        NS_weight_dict.update({level_5:level_5_weight})
                                else:
                                    level_4_weight = (level_3_weight / len(level_4_list))

                                    if (NS_weight_dict.get(level_4)):
                                        total_level_4_weight = level_4_weight + NS_weight_dict.get(level_4)
                                    else:
                                        total_level_4_weight = level_4_weight
                                    NS_weight_dict.update({level_4: total_level_4_weight})
                        else:
                            level_3_weight = (level_2_weight / len(level_3_list))
                            if (NS_weight_dict.get(level_3)):
                                total_level_3_weight = level_3_weight + NS_weight_dict.get(level_3)
                            else:
                                total_level_3_weight = level_3_weight
                            NS_weight_dict.update({level_3: total_level_3_weight})
                else:
                    level_2_weight = (level_1_weight / len(level_2_list))
                    if (NS_weight_dict.get(level_2)):
                        total_level_2_weight = level_2_weight + NS_weight_dict.get(level_2)
                    else:
                        total_level_2_weight = level_2_weight
                    NS_weight_dict.update({level_2: total_level_2_weight})
        else:
            level_1_weight = (1 / len(main_list))
            if (NS_weight_dict.get(level_1)):
                total_level_1_weight = level_1_weight + NS_weight_dict.get(level_1)
            else:
                total_level_1_weight = level_1_weight
            NS_weight_dict.update({level_1: total_level_1_weight})
    return NS_weight_dict


def save_to_db(final_dict):
    name = list(final_dict.keys())[0]
    score_dict = final_dict.get(name)
    save_coll.insert_one(score_dict)


def operate():
    finded = coll.find({})
    whole_list = []
    count = 0
    for i in finded:
        try:
            whole_list.append(i.get('域名'))
        except Exception as e:
            print(e)
        count+=1
        if count==5000:
            break
    whole_list = whole_list[1000:]

    print('共'+str(count)+"个域名")
    count_2 = 0
    for domain in whole_list:
        print(domain)
        count_2 += 1
        print(count_2/count)
        one_dict = get_inform_of_one_domain(domain)
        #except Exception as e:
            #print(e)
        try:
            save_to_db(one_dict)
        except Exception as e:
            print(e)
            print("储存失败")
    con.close()






if __name__ == '__main__':
    operate()



