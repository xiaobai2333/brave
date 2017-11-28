import time

import datetime

import Recommend
from src_one.filter import ReadData

def get_hour_store_Canditate(sche_time, userID, appointMap):
    hour_candidate = Recommend.getHourOfCandidate(sche_time, userID, appointMap)
    store_candidate = Recommend.getStoreOfCandidate(sche_time, userID, appointMap)
    return hour_candidate , store_candidate

def get_Class_Candidate(userID,sche_time,appointMap,apriori_rules,userDict,itemUser):

    history_classID = get_history_class_Candidate(sche_time,userID,appointMap)

    if len(history_classID) ==0:
        return history_classID,set(),set()
    col_recom = get_col_class_Candidate(history_classID,userID,userDict,itemUser)
    apriori_recom = get_apriori_classID_Candidate(apriori_rules,history_classID)


    classId_candidate  = set()
    classId_candidate.update(history_classID, col_recom, apriori_recom)


    return classId_candidate

def get_apriori_rulse(lastestTime,appointMap,minSupport=0.1 ,minConf=0.6 ):
    return Recommend.apriori_classID(lastestTime,appointMap,minSupport,minConf)


def get_history_class_Candidate(lastestTime,userID,appointMap):

    return Recommend.get_his_classID(lastestTime,userID,appointMap)

def get_apriori_classID_Candidate(apriori_rules,history_classID):
    # apriori_rules = apriori_classID(lastestTime, appointMap, 0.1, 0.6)
    apriori_recom=set()
    for rule in apriori_rules:
        if rule[0].issubset(history_classID):
            if not rule[1].issubset(history_classID):
                apriori_recom.update(rule[1])
    return apriori_recom

def get_col_class_Candidate(history_classID,userID,userDict,itemUser):
    Col_result = Recommend.Collabrorative_classID(userID,userDict,itemUser)

    Col_recom_result = set()
    for item in Col_result:
        if item[1] not in history_classID:
            Col_recom_result.add(item[1])
    return Col_recom_result




def isClassInCandidate(sche,classId_candidate):
    class_id = sche[0]

    if not class_id in classId_candidate:
        return False

    return True

def ishourStoreInCandidate(sche_time,storeId,hour_candidate,store_candidate):
    if not storeId in store_candidate:
        return False
    # sche_hour = datetime.datetime.fromtimestamp(sche_time).hour
    # if not sche_hour in hour_candidate:
    #     return False
    return True