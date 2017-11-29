#coding=utf-8
import datetime
import Apriori
import ReadData
import time
import Collaborative_Filter

def apriori_classID(lastestTime,appointMap,minSupport=0.1 ,minConf=0.6 ):

    dataSet = ReadData.get_all_recent_class(lastestTime, appointMap)

    L, suppData = Apriori.apriori(dataSet, minSupport)

    rules =Apriori.generateRules(L, suppData, minConf)
    return rules

def get_hot_classId():
    pass

def get_his_classID(lastestTime,userID,appointMap):
    timeline = lastestTime - 60 * 60 * 24 * 45
    result = set()
    for list in appointMap[userID]:
        if list[2] > timeline and list[2] < lastestTime:
            classID = list[-2]
            result.add(classID)
    return result

def Collabrorative_classID(userID,userDict,itemUser):

    result = Collaborative_Filter.recommendByUserFC(userDict, itemUser, userID, 8)

    return result

def getCandidate(lastestTime,userID,appointMap):
    history_classID = get_his_classID(lastestTime,userID,appointMap)

    if len(history_classID)==0:
        return history_classID,set(),set()

    apriori_rules =  apriori_classID(lastestTime,appointMap,0.1 ,0.6 )
    apriori_recom=set()
    for rule in apriori_rules:
        if rule[0].issubset(history_classID):
            if not rule[1].issubset(history_classID):
                apriori_recom.update(rule[1])

    userDict = ReadData.get_recent_user_classId_Dict(lastestTime, appointMap)
    itemUser = Collaborative_Filter.getItemUserMap(userDict)
    Col_result = Collabrorative_classID(userID, userDict, itemUser)

    Col_recom_result = set()
    for item in Col_result:
        if item[1] not in history_classID:
            Col_recom_result.add(item[1])

    return history_classID, Col_recom_result,apriori_recom



def getHourOfCandidate(lastestTime,userID,appointMap):
    timeline = lastestTime - 60 * 60 * 24 * 45
    result = []
    for list in appointMap[userID]:
            if list[2] > timeline and list[2] < lastestTime:
                hour = datetime.datetime.fromtimestamp(list[2]).hour
                result.append(hour)
    return result

def getStoreOfCandidate(lastestTime,userID,appointMap):
    timeline = lastestTime - 60 * 60 * 24 * 45
    result = []
    for list in appointMap[userID]:
            if list[2] > timeline and list[2] < lastestTime:
                Store =list[1]
                result.append(Store)
    return result

def view_recent_apriori_class():
    start = time.time()
    begin = start
    appointMap = ReadData.getAppointMap()
    end = time.time()
    print '========getAppointMap() 花了 ：', str(end - start), ' s'
    start = end

    lastestTime = ReadData.get_lastest_time(appointMap)
    end = time.time()
    print '========get_lastest_time() 花了 ：', str(end - start), ' s'
    start = end

    print datetime.datetime.fromtimestamp(lastestTime)

    result = apriori_classID(lastestTime, appointMap, 0.1, 0.5)
    end = time.time()
    print '========apriori_class() 花了 ：', str(end - start), ' s'
    start = end

    print '=======总共 花了 ：', str(end - begin), ' s'

    print result

def test():
    appointMap = ReadData.getAppointMap()

    for userID in appointMap:
        lastestTime = ReadData.get_user_lastest_time(userID,appointMap)
        print userID , '========================='
        history_classID ,col_recom,apriori_recom = getCandidate(lastestTime,userID,appointMap)
        print 'history : ' , history_classID
        print 'col_recom  : ',col_recom
        print 'apriori_recom : ',apriori_recom
        print 'hour  : ',getHourOfCandidate(lastestTime,userID,appointMap)
        print 'storeID : ',getStoreOfCandidate(lastestTime,userID,appointMap)




if __name__ == '__main__':
    test()