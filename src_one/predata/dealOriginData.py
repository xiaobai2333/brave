import os
import cPickle as pickle
import numpy as np
import datetime

from statsmodels.regression.tests.results import results_regression

originPath ='/home/software/leai/new_database_9_26'



# appoint_queue_map
# coach_map_new
# schedule_coach_map
# user_map_new


def readOriginData():
    dirs = os.listdir(originPath)
    for dir in dirs:
        print dir


def prepare_appointMap():
    appointPath = originPath + '/appoint_queue_map_sorted'
    appointFile = open(appointPath)
    appointMap = pickle.load(appointFile)
    appointFile.close()
    n =0
    for user_id in appointMap.keys():
        print user_id
        n+=1
        for list in appointMap[user_id]:
            print list

        print datetime.datetime.fromtimestamp(list[2]).date()
        if(n==5):
            break
        print '================================================='
    return appointMap


def sort_trainData(appointMap):
    # appointPath = originPath + '/appoint_queue_map_coach'
    # appointFile = open(appointPath)
    # appointMap = pickle.load(appointFile)
    # appointFile.close()
    n =0
    for user_id in appointMap.keys():
        n+=1
        appointMap[user_id]=sorted(appointMap[user_id], key=lambda ll:ll[2])

        # print n
    # appointPath2 = 'appoint_queue_map_coach_sorted'
    # appointFile = open(appointPath2, 'w')
    # pickle.dump(appointMap, appointFile)
    return appointMap


def getPresentP(userId, time, appiont_que_map):
    sum =0
    present =0
    start = time - 60 * 60 * 24 * 21
    for list in appiont_que_map[userId]:
        if list[2] >= start:
            if  list[2]< time:
                if list[-1]==8 or list[-1]==9:
                    present+=1
                    sum += 1
                elif list[-1] == 6 or list[-1]==3 or list[-1]==4:
                    sum += 1
            else:
                break

    if sum <=3:
        return 0
    else:
        p = (1.0 * present / sum )*100
        if p<=10:
            return 1
        elif p<=30:
            return 2
        elif p<=50:
            return 3
        elif p<=70:
            return 4
        elif p<=90:
            return 5
        else:
            return 6


def getClassPresentP(classId, time,appiont_que_map_class):
    sum =0
    present =0
    start = time - 60 * 60 * 24 * 21
    for list in appiont_que_map_class[classId]:
        if list[2] >= start:
            if  list[2]< time:
                if list[-1]==8 or list[-1]==9:
                    present+=1
                    sum += 1
                elif list[-1] == 6 or list[-1]==3 or list[-1]==4:
                    sum += 1
            else:
                break
    if sum <= 3:
        return 0
    else:
        p = (1.0 * present / sum )*100
        # return p
        if p<=10:
            return 1
        elif p<=30:
            return 2
        elif p<=50:
            return 3
        elif p<=70:
            return 4
        elif p<=90:
            return 5
        else:
            return 6


def getCoachPresentP(coachId, time,appiont_que_map_coach):
    sum =0
    present =0
    start = time - 60 * 60 * 24 * 21
    for list in appiont_que_map_coach[coachId]:
        if list[2] >= start:
            if  list[2]< time:
                if list[-1]==8 or list[-1]==9:
                    present+=1
                    sum += 1
                elif list[-1] == 6 or list[-1]==3 or list[-1]==4:
                    sum += 1
            else:
                break
    if sum <= 3:
        return 0
    else:
        p = (1.0 * present / sum )*100
        # return p
        if p<=10:
            return 1
        elif p<=30:
            return 2
        elif p<=50:
            return 3
        elif p<=70:
            return 4
        elif p<=90:
            return 5
        else:
            return 6


def get_average_appoint(userId, time,appiont_que_map):
    appoint =0
    for list in appiont_que_map[userId]:
        if  list[2]<time:
            if list[-1] == 8 or list[-1] == 9:
                appoint +=1
        else:break
    start =datetime.datetime.fromtimestamp(appiont_que_map[userId][0][2])
    end = datetime.datetime.fromtimestamp(time)
    cha = (end-start).days

    if cha==0:
        return -1
    return appoint *1.0 / cha *30


def get_sum_appoint(userId,time,appiont_que_map):
    appoint =0
    for list in appiont_que_map[userId]:
        if  list[2]<time:
            if list[-1] == 8 or list[-1] == 9:
                appoint +=1
        else:break

    return appoint


def get_lastweek_appoints(userId,time,appiont_que_map):
    start = time-60*60*24*7
    # print datetime.datetime.fromtimestamp(start)
    times = 0
    for list in appiont_que_map[userId]:
        if list[2]>start:
            if list[2]<time:
                if list[-1] == 8 or list[-1] == 9:
                    times +=1
            else:
                break
    return times


def get_average_interval(userId,time,appiont_que_map):
    start = time-60*60*24*30
    last = 0
    times = 0
    sumInterval=0
    for list in appiont_que_map[userId]:
        if list[2]>start:
            if list[2]<time:
                if list[-1] == 8 or list[-1] == 9:
                    if last ==0:
                        last = list[2]
                        continue
                    thisTime = list[2]
                    sumInterval += (datetime.datetime.fromtimestamp(thisTime)-datetime.datetime.fromtimestamp(last)).days+1
                    last = thisTime
                    times +=1
            else:
                break
    if times==0:
        return -1
    return sumInterval*1.0 / times


def get_last_timedelta(userId,time,appiont_que_map):
    last_log = []
    for list in appiont_que_map[userId]:
        if list[2]<time:
            if list[-1] == 8 or list[-1] == 9:
                last_log = list
        else:
            break
    if last_log == []:
        return -1
    last = datetime.datetime.fromtimestamp(last_log[2])
    return (datetime.datetime.fromtimestamp(time)-last).days+1


def get_weekdayP(userId,time,appiont_que_map):
    result_q = [0,0,0,0,0,0,0]
    result_y = [0,0,0,0,0,0,0]
    start = time - 60 * 60 * 24 * 30
    for list in appiont_que_map[userId]:
        if list[2] > start:
            if list[2] < time:
                if list[-1] == 8 or list[-1] == 9:
                    result_q[datetime.datetime.fromtimestamp(list[2]).weekday()] += 1
                    result_y[datetime.datetime.fromtimestamp(list[2]).weekday()] += 1
                elif list[-1] == 6 or list[-1]==3 or list[-1]==4:
                    result_y[datetime.datetime.fromtimestamp(list[2]).weekday()] += 1
                else:
                    continue
            else:
                break
    result_q = np.array(result_q)
    result_y = np.array(result_y)
    for i in range(result_y.shape[0]):
        if result_y[i] != 0:
            result_q[i] = result_q[i] * 1.0 / result_y[i]
    return result_q.tolist()


def get_hourP(userId, time, appiont_que_map):
    result_q = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    result_y = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    start = time-60*60*24*30
    for list in appiont_que_map[userId]:
        if list[2] > start:
            if list[2] < time:
                if datetime.datetime.fromtimestamp(list[2]).hour < 7 or datetime.datetime.fromtimestamp(list[2]).hour >21:
                    continue
                if list[-1] == 8 or list[-1] == 9:
                    # print str(datetime.datetime.fromtimestamp(list[2]).hour )
                    result_q[datetime.datetime.fromtimestamp(list[2]).hour - 7] += 1
                    result_y[datetime.datetime.fromtimestamp(list[2]).hour - 7] += 1
                elif list[-1] == 6 or list[-1]==3 or list[-1]==4:
                    result_y[datetime.datetime.fromtimestamp(list[2]).hour - 7] += 1
            else:
                break
    result_q = np.array(result_q)
    result_y = np.array(result_y)
    for i in range(result_y.shape[0]):
        if result_y[i] != 0:
            result_q[i] = result_q[i] * 1.0 / result_y[i]
    return result_q.tolist()


def get_history_store(userId,time,appiont_que_map):
    store = []
    start = time - 60 * 60 * 24 * 30
    for list in appiont_que_map[userId]:
        if list[2]>=start:
            if list[2] < time:
                if list[-1] == 8 or list[-1] == 9:
                    store.append(list[1])
            else:
                break

    return store


def get_history_class(userId,time,appiont_que_map):
    class_id = []
    start = time - 60 * 60 * 24 * 30
    for list in appiont_que_map[userId]:
        if list[2] >= start:
            if list[2] < time:
                if list[-1] == 8 or list[-1] == 9:
                    class_id.append(list[4])
            else:
                break
    return class_id


def get_history_coach(userId,time,appiont_que_map,schedule_coach):
    coach_ = []
    start = time - 60 * 60 * 24 * 30
    for list in appiont_que_map[userId]:
        if list[2] >= start:
            if list[2] < time:
                if list[-1] == 8 or list[-1] == 9:
                    sch_id = list[0]
                    if schedule_coach.has_key(sch_id):
                        coach_id = schedule_coach[sch_id]
                        coach_.append(coach_id)
                    else:
                        continue
            else:
                break
    return coach_


def get_history_time(userId,time,appiont_que_map):
    class_time = []
    start = time - 60 * 60 * 24 * 30
    for list in appiont_que_map[userId]:
        if list[2] >= start:
            if list[2] < time:
                if datetime.datetime.fromtimestamp(list[2]).hour < 7 or datetime.datetime.fromtimestamp(list[2]).hour > 21:
                    continue
                if list[-1] == 8 or list[-1] == 9:
                    class_datetime = datetime.datetime.fromtimestamp(list[2])
                    class_time.append(class_datetime.hour-7)
                else:
                    continue
            else:
                break
    return class_time


def get_history_weekday(userId,time,appiont_que_map):
    class_weekday = []
    start = time - 60 * 60 * 24 * 30
    for list in appiont_que_map[userId]:
        if list[2] >= start:
            if list[2] < time:
                if list[-1] == 8 or list[-1] == 9:
                    class_datetime = datetime.datetime.fromtimestamp(list[2])
                    class_weekday.append(class_datetime.weekday())
                else:
                    continue
            else:
                break
    return class_weekday

if __name__ == '__main__':
    # print 'loading data....'
    # appointMap = prepare_appointMap()
    #
    # print 'success load..'
    # print '****'
    #
    # for userId in appointMap:
    #     lists = appointMap[userId]
    #     print '====================================='
    #     print 'userID:  ' ,userId
    #
    #     for list in lists:
    #         isCome = 'No  '
    #         weekday = datetime.datetime.fromtimestamp(list[2]).weekday()
    #
    #         if list[-1] == 8 or list[-1] == 9:
    #             isCome ='Yes '
    #         print 'weekday: ',(weekday+1),'    presentP :  ',("%f" %getPresentP(userId,list[2],appointMap))\
    #             ,'    weekdayP:',('%.4f' %get_weekdayP(userId,list[2],appointMap)[weekday])  \
    #             ,'    average_interval',('%.3f'%get_average_interval(userId,list[2],appointMap))\
    #             ,'    lastTimedelta',get_last_timedelta(userId,list[2],appointMap)   \
    #             ,'   Come? ',isCome

    sort_trainData()
    # 1501669800L
    # 1501582800L
    # 1501755000Lsrc/dealOriginData.py:87
