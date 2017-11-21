#coding=utf-8

import cPickle as pickle
import time
import datetime
import Apriori
from src_one.predata.dealOriginData import sort_trainData
appoint_queue_map_path = '/home/hhy/PycharmProjects/brave/data_11_7/appoint_queue_map'


def readAppointMap():
    file = open(appoint_queue_map_path,'r')
    appointMap = pickle.load(file)
    appointMap = sort_trainData(appointMap)
    file.close()
    for userId in appointMap:
        for list in appointMap[userId]:
            classID = list[-2]
            print classID


def getAppointMap():
    file = open(appoint_queue_map_path,'r')
    appointMap = pickle.load(file)
    appointMap = sort_trainData(appointMap)
    file.close()
    return appointMap


def get_user_recent_class(userId,time,appointMap):
    lists = appointMap[userId]
    timeline = time - 60*60*24*45
    classId_list = []
    for list in lists:
        if list[2]>timeline and list[2] <time:
            classType=list[-2]
            classId_list.append(classType)
    return classId_list


def get_all_recent_class(time ,appointMap):
    recent_class_lists = []
    for userId in appointMap:
        user_recent_class = get_user_recent_class(userId,time,appointMap)
        if(len(user_recent_class)>=3):
            recent_class_lists.append(user_recent_class)

    return recent_class_lists

def get_lastest_time(appointMap):
    result = 0
    for userId in appointMap:
        for list in  appointMap[userId]:
            if list[2]>result:
                result = list[2]

    return result

def get_user_lastest_time(userID,appointMap):
    return appointMap[userID][-1][2]

def view_recent_class():
    start = time.time()
    print datetime.datetime.fromtimestamp(start)
    appointMap = getAppointMap()
    lastestTime = get_lastest_time(appointMap)
    lists = get_all_recent_class(lastestTime, appointMap)
    for list in lists:
        print list


def get_recent_user_classId_Dict(lastestTime,appointMap):
    userDict = {}
    for userId in appointMap:
        user_classId_map = {}

        user_recent_class = get_user_recent_class(userId, lastestTime, appointMap)
        for classId in user_recent_class:
            user_classId_map[classId] =user_classId_map.get(classId,0)+1

        userDict[userId] = user_classId_map

    return userDict


if __name__ == '__main__':
    appointMan = getAppointMap()
    lastestTime = get_lastest_time(appointMan)
    get_recent_user_classId_Dict(lastestTime, appointMan)
