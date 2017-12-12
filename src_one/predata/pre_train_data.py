import cPickle as pickle
import numpy as np
import math
from keras.utils import np_utils
import datetime
# from dealOriginData import *
from src_one.predata.dealOriginData import *
from src_one.properties import data_path, padding_num
# data_path = '/home/hhy/PycharmProjects/brave/data_11_7/'
from src_one.readDataFromDatabase.get_user_rights import get_user_right
from src_one.properties import lastestUpdateUnix
appoint_queue_id = 'appoint_queue_map'
coach_map_id = 'coach_sex'
user_map_id = 'user_sex'
schedule_coach_map_id = 'schedule_coach_map'
# weather_id = 'hangzhou_weather6_9.csv'
weather_id = 'weather6_9'
# class_property_id = 'class_property.npy'


def get_weather_data():
    weather = open(data_path+weather_id, 'r')
    lines = weather.readlines()
    all_w = {}
    for line in lines:
        a = line.split(',')
        date = a[0].split('/')
        # date = datetime.date(int(date[0]), int(date[1]), int(date[2]))
        key = (int(date[1]), int(date[2]))
        all_w[key] = [int(a[1]), int(a[2]), int(a[3])]
    file_name = open(data_path+'weather6_9', 'w')
    pickle.dump(all_w, file_name)
    file_name.close()
    weather.close()


def deal_appoint_data():
    appoint_file = open(data_path+appoint_queue_id, 'r')
    appoint_queue = pickle.load(appoint_file)
    n = 0
    for key in appoint_queue.keys():
        qiandao = 0
        quxiao = 0
        for log in appoint_queue[key]:
            # if log[-1] == 2 or log[-1] == 8 or log[-1] == 9:
            if log[-1] == 4:
                qiandao += 1
            else:
                quxiao += 1
        qlv = float(qiandao)/(qiandao+quxiao)
        print '================================================'
        print 'user :', key, ' all: ', qiandao+quxiao, ' qiandao: ', qiandao, ' qiandao lv: ', qlv
        n += qiandao
    print '======================================='
    print 'qiandao : ', n


def get_coldstart_data():
    appoint_file = open(data_path + appoint_queue_id, 'r')
    appoint_queue = pickle.load(appoint_file)
    coach_file = open(data_path+coach_map_id, 'r')
    coach = pickle.load(coach_file)
    user_file = open(data_path+user_map_id, 'r')
    user = pickle.load(user_file)
    schedule_file = open(data_path+schedule_coach_map_id, 'r')
    schedule = pickle.load(schedule_file)
    weather_file = open(data_path+weather_id, 'r')
    weather = pickle.load(weather_file)
    # class_property = np.load(data_path+class_property_id)
    miss_user = set()
    coldstart_data = []
    e1 = 0
    e2 = 0
    e3 = 0
    e4 = 0
    e5 = 0
    n1 = 0
    n0 = 0
    for key in appoint_queue.keys():
        for log in appoint_queue[key]:
            user_id = key
            # print key
            sch_id = log[0]
            store_id = log[1]
            start_time = log[2]
            end_time  = log[3]
            class_id = log[4]
            # class_pro = class_property[class_map1[class_id]]
            status = log[5]
            if schedule.has_key(sch_id):
                coach_id = schedule[sch_id]
            else:
                e1 += 1
                continue
            if user.has_key(user_id):
                if user[user_id] == '':
                    e2 += 1
                    print 'user_id sex = null :', user_id
                    user_sex = 0
                else:
                    user_sex = int(user[user_id])
            else:
                e3 += 1
                print 'user_id miss :', user_id
                miss_user.add(user_id)
                user_sex = 0
            if coach.has_key(coach_id):
                if coach[coach_id] == '':
                    e4 += 1
                    print 'coach_id sex = null : ', coach_id
                    coach_sex = 0
                else:
                    coach_sex = int(coach[coach_id])
            else:
                e5 += 1
                print 'coach_id miss : ', coach_id
                coach_sex = 0
            convert_time = datetime.datetime.fromtimestamp(start_time)
            month = convert_time.month
            day = convert_time.day
            key1 = (month, day)
            tempareture_max = weather[key1][0]
            tempareture_min = weather[key1][1]
            is_rain = weather[key1][2]
            weekday = datetime.datetime.isoweekday(convert_time)
            hour = convert_time.hour
            # minute = convert_time.minute
            if status == 8 or status == 9:
                each_data = [user_sex, class_id, store_id, coach_id]
                # each_data.extend(class_pro)
                each_data.extend([coach_sex, month, day,  weekday, hour, tempareture_max, tempareture_min, is_rain, 1])
                n1 += 1
            else:
                each_data = [user_sex, class_id, store_id, coach_id]
                # each_data.extend(class_pro)
                each_data.extend([coach_sex, month, day,  weekday, hour, tempareture_max, tempareture_min, is_rain, 0])
                n0 += 1
            coldstart_data.append(each_data)
    appoint_file.close()
    coach_file.close()
    user_file.close()
    schedule_file.close()
    weather_file.close()
    print 'schedule id miss : ', e1
    print 'user_id sex = null : ', e2
    print 'user_id miss : ', len(miss_user)
    print 'coach_id sex = null : ', e4
    print 'coach_id miss : ', e5
    coldstart_data = np.array(coldstart_data)
    print 'cold start data shape : ', coldstart_data.shape
    print 'active num : ', n1
    print 'negative num : ', n0
    np.save(data_path+'coldstart_data.npy', coldstart_data)


def get_first_data():
    appoint_file = open(data_path + appoint_queue_id, 'r')
    appoint_queue = pickle.load(appoint_file)
    appoint_queue = sort_trainData(appoint_queue)
    # appoint_class_file = open(data_path + appoint_queue_class_id, 'r')
    # appoint_queue_class = pickle.load(appoint_class_file)

    # appoint_coach_file = open(data_path + appoint_queue_coach_id, 'r')
    # appoint_queue_coach = pickle.load(appoint_coach_file)

    # right_file1 = open(data_path + 'user_right', 'r')
    # user_right_list = pickle.load(right_file1)
    coach_file = open(data_path+coach_map_id, 'r')
    coach = pickle.load(coach_file)
    user_file = open(data_path+user_map_id, 'r')
    user = pickle.load(user_file)
    schedule_file = open(data_path+schedule_coach_map_id, 'r')
    schedule = pickle.load(schedule_file)
    # weather_file = open(data_path+weather_id, 'r')
    # weather = pickle.load(weather_file)
    # class_property = np.load(data_path+class_property_id)
    # user_id_map_file = open(data_path+user_id_dic, 'r')
    # user_new_id = pickle.load(user_id_map_file)
    first_data = []
    n0 = 0
    n1 = 0
    coach_id_max = 0
    store_id_max = 0
    x1 = 0
    t1 = 0
    all_users = set()
    all_coaches = set()
    test = []
    for key in appoint_queue.keys():
        for log in appoint_queue[key]:
            user_id = key
            # user_id_new = user_new_id[user_id]
            # print key
            sch_id = log[0]
            store_id = log[1]
            start_time = log[2]
            end_time  = log[3]
            class_id = log[4]
            class_id_map = class_id
            # class_pro = class_property[class_map1[class_id]]   #30 0 is class_id
            status = log[5]
            if status not in [3,4,6,8,9]:
                continue
            if schedule.has_key(sch_id):
                coach_id = schedule[sch_id]
            else:
                continue
            if user.has_key(user_id):
                # print 'user sex:', user[user_id]
                if not user[user_id].isspace() and not user[user_id] == '':
                    user_sex = int(user[user_id])
                else:
                    continue
            else:
                continue
            if coach.has_key(coach_id):
                if coach[coach_id] == '':
                    continue
                else:
                    coach_sex = int(coach[coach_id])
                    if coach_id > coach_id_max:
                        coach_id_max = coach_id
            else:
                continue
            if store_id > store_id_max:
                store_id_max = store_id
            # if user_right_list.has_key(user_id):
            #     user_right = user_right_list[user_id]
            # else:
            #     continue
            # if 2 in user_right:
            #     user_right_1 = 1
            # else:
            #     user_right_1 = 0
            # if user_right_1 == 1:
            #     all_users.add(user_id)
            all_users.add(user_id)
            all_coaches.add(coach_id)
            convert_time = datetime.datetime.fromtimestamp(start_time)
            month = convert_time.month
            day = convert_time.day
            key1 = (month, day)
            # tempareture_max = weather[key1][0]
            # tempareture_min = weather[key1][1]
            # is_rain = weather[key1][2]
            weekday = convert_time.weekday()
            weekday_sparse = np_utils.to_categorical(weekday, 7)
            # print weekday_sparse
            hour = convert_time.hour
            if hour<7 or hour>21:
                continue
            hour_sparse = np_utils.to_categorical(hour-7, 15)
            # dealed history data
            pressenP = getPresentP(user_id, start_time, appoint_queue)
            # class_pressenP = getClassPresentP(class_id, start_time, appoint_queue_class)
            # coach_pressenP = getCoachPresentP(coach_id, start_time, appoint_queue_coach)
            class_pressenP = 0
            coach_pressenP = 0
            average_appoint = get_sum_appoint(user_id, start_time, appoint_queue)
            last_week_times = get_lastweek_appoints(user_id,start_time,appoint_queue)
            last_timedelta = get_last_timedelta(user_id, start_time, appoint_queue)
            weekdayP = get_weekdayP(user_id, start_time, appoint_queue)
            hourP = get_hourP(user_id, start_time, appoint_queue)                #13
            coach_1 = get_history_coach(user_id, start_time, appoint_queue, schedule)
            if len(coach_1) <= 3:
                continue
            coach_history = coach_1 + [0 for x in range(padding_num - len(coach_1))]
            coach_history_weight = [1.0/len(coach_1) for x in range(len(coach_1))] + [0 for x in range(padding_num - len(coach_1))]
            # coach_history_weight = [math.pow(0.8, x) for x in range(len(coach_1))] + [0 for x in range(
            #     padding_num - len(coach_1))]
            store_1 = get_history_store(user_id, start_time, appoint_queue)
            store_history = store_1 + [0 for x in range(padding_num - len(store_1))]
            store_history_weight = [1.0/len(store_1) for x in range(len(store_1))] + [0 for x in range(padding_num - len(store_1))]
            # store_history_weight = [math.pow(0.8, x) for x in range(len(store_1))] + [0 for x in range(
            #     padding_num - len(store_1))]
            class_1 = get_history_class(user_id, start_time, appoint_queue)
            class_history = class_1 + [0 for x in range(padding_num - len(class_1))]
            class_history_weight = [1.0/len(class_1) for x in range(len(class_1))] + [0 for x in range(padding_num - len(class_1))]
            # class_history_weight = [math.pow(0.8, x) for x in range(len(class_1))] + [0 for x in range(
            #     padding_num - len(class_1))]
            hour_1 = get_history_time(user_id, start_time, appoint_queue)
            hour_history = hour_1 + [0 for x in range(padding_num - len(hour_1))]
            hour_history_weight = [1.0/len(hour_1) for x in range(len(hour_1))] + [0 for x in range(padding_num - len(hour_1))]
            # hour_history_weight = [math.pow(0.8, x) for x in range(len(hour_1))] + [0 for x in
            #                                                                          range(padding_num - len(hour_1))]
            week_1 = get_history_weekday(user_id, start_time, appoint_queue)
            week_history = week_1 + [0 for x in range(padding_num - len(week_1))]
            week_history_weight = [1.0/len(week_1) for x in range(len(week_1))] + [0 for x in range(padding_num - len(week_1))]
            # week_history_weight = [math.pow(0.8, x) for x in range(len(week_1))] + [0 for x in
            #                                                                          range(padding_num - len(week_1))]
            if pressenP == -1 or average_appoint == -1 or last_timedelta == -1:
                continue
            # minute = convert_time.minute
            if t1%1000 == 0:
                print t1
            t1 += 1
            each_data = [user_sex, pressenP, average_appoint, last_timedelta, last_week_times]
            each_data.extend(coach_history)
            each_data.extend(coach_history_weight)
            each_data.extend(store_history)
            each_data.extend(store_history_weight)
            each_data.extend(class_history)
            each_data.extend(class_history_weight)
            each_data.extend(hour_history)
            each_data.extend(hour_history_weight)
            each_data.extend(week_history)
            each_data.extend(week_history_weight)
            each_data.extend(weekdayP)
            each_data.extend(hourP)
            each_data.extend([class_id_map, store_id, coach_id])
            # each_data.extend(class_pro)   # 30
            # each_data.extend([coach_sex, month, day,  weekday, hour, tempareture_max, tempareture_min, is_rain, 1])
            each_data.extend([coach_sex, month, day])
            # print weekday_sparse
            each_data.extend(weekday_sparse)  # 7
            each_data.extend(hour_sparse)  # 15
            # each_data.extend([tempareture_max, tempareture_min, is_rain, 1])
            if status == 8 or status == 9:
                each_data.extend([1])
                n1 += 1
            elif status == 6 or status == 3 or status == 4:
                each_data.extend([0])
                n0 += 1
            else:
                continue

            first_data.append(each_data)

    appoint_file.close()
    coach_file.close()
    user_file.close()
    schedule_file.close()
    first_data = np.array(first_data)
    #all_user_file = open(data_path+'all_userid', 'w')
    #pickle.dump(all_users, all_user_file)
    all_coaches_file = open(data_path + 'all_coachids', 'w')
    pickle.dump(all_coaches, all_coaches_file)
    print 'all data shape : ', first_data.shape
    print 'active num : ', n1
    print 'negative num : ', n0
    print 'store max: ', store_id_max
    print 'coach max: ', coach_id_max
    print 'all users number: ', len(all_users)
    print 'all coaches number: ', len(all_coaches)
    np.save(data_path+'first_type_data.npy', first_data)
    print 'get user right from web...'
    userReal = get_user_right(all_users)
   # userReal_file = open(data_path+'all_userid', 'r')
   # userReal = pickle.load(userReal_file) 
    print 'get user right success...'
    print 'get user history by now start...'
    user_history_bynow = {}
    k = 0
    l1 = len(userReal)
    for uId in userReal:
        if k%1000==0:
            print k,' / ', l1
        k += 1
        uHis = get_user_history_bynow(uId, appoint_queue, user, coach, schedule)
        user_history_bynow[uId]=uHis
    user_history_bynow_file = open(data_path+'user_history_by_now', 'w')
    pickle.dump(user_history_bynow, user_history_bynow_file)
    user_history_bynow_file.close()
    print 'get user history by now ...'


def get_user_history_bynow(userId, appointMap, user, coach, schedule):
    user_history_bynow = []
    # class_id = sche[0]
    # store_id = sche[1]
    start_time = lastestUpdateUnix
    # coach_id = sche[3]
    user_sex = user[userId]
    # coach_sex = coach[coach_id]
    # convert_time = datetime.datetime.fromtimestamp(start_time)
    # month = convert_time.month
    # day = convert_time.day
    # weekday = convert_time.weekday()
    # weekday_sparse = np_utils.to_categorical(weekday, 7)
    # print weekday_sparse
    # hour = convert_time.hour
    # hour_sparse = np_utils.to_categorical(hour - 7, 15)
    pressenP = getPresentP(userId, start_time, appointMap)
    average_appoint = get_sum_appoint(userId, start_time, appointMap)
    last_week_times = get_lastweek_appoints(userId, start_time, appointMap)
    last_timedelta = get_last_timedelta(userId, start_time, appointMap)
    weekdayP = get_weekdayP(userId, start_time, appointMap)
    hourP = get_hourP(userId, start_time, appointMap)  # 13
    coach_1 = get_history_coach(userId, start_time, appointMap, schedule)
    user_coach_history = np.array(coach_1 + [0 for x in range(padding_num - len(coach_1))])
    user_coach_history = user_coach_history.reshape((1, user_coach_history.shape[0]))
    user_coach_weight = [1.0 / len(coach_1) for x in range(len(coach_1))] + [0 for x in
                                                                                range(padding_num - len(coach_1))]
    user_coach_weight = np.array(user_coach_weight)
    user_coach_weight = user_coach_weight.reshape((1, 1, user_coach_weight.shape[0]))
    store_1 = get_history_store(userId, start_time, appointMap)
    user_store_history = store_1 + [0 for x in range(padding_num - len(store_1))]
    user_store_history = np.array(user_store_history)
    user_store_history = user_store_history.reshape((1, user_store_history.shape[0]))
    user_store_weight = [1.0 / len(store_1) for x in range(len(store_1))] + [0 for x in
                                                                                range(padding_num - len(store_1))]

    user_store_weight = np.array(user_store_weight)
    user_store_weight = user_store_weight.reshape((1, 1, user_store_weight.shape[0]))
    class_1 = get_history_class(userId, start_time, appointMap)
    user_class_history = class_1 + [0 for x in range(padding_num - len(class_1))]
    user_class_history = np.array(user_class_history)
    user_class_history = user_class_history.reshape((1, user_class_history.shape[0]))
    user_class_weight = [1.0 / len(class_1) for x in range(len(class_1))] + [0 for x in
                                                                                range(padding_num - len(class_1))]

    user_class_weight = np.array(user_class_weight)
    user_class_weight = user_class_weight.reshape((1, 1, user_class_weight.shape[0]))
    hour_1 = get_history_time(userId, start_time, appointMap)
    user_hour_history = hour_1 + [0 for x in range(padding_num - len(hour_1))]
    user_hour_history = np.array(user_hour_history)
    user_hour_history = user_hour_history.reshape((1, user_hour_history.shape[0]))
    user_hour_weight = [1.0 / len(hour_1) for x in range(len(hour_1))] + [0 for x in
                                                                             range(padding_num - len(hour_1))]

    user_hour_weight = np.array(user_hour_weight)
    user_hour_weight = user_hour_weight.reshape((1, 1, user_hour_weight.shape[0]))
    week_1 = get_history_weekday(userId, start_time, appointMap)
    user_week_history = week_1 + [0 for x in range(padding_num - len(week_1))]
    user_week_history = np.array(user_week_history)
    user_week_history = user_week_history.reshape((1, user_week_history.shape[0]))
    user_week_weight = [1.0 / len(week_1) for x in range(len(week_1))] + [0 for x in
                                                                             range(padding_num - len(week_1))]
    user_week_weight = np.array(user_week_weight)
    user_week_weight = user_week_weight.reshape((1, 1, user_week_weight.shape[0]))
    user_basic = np.array([user_sex, pressenP, average_appoint, last_timedelta, last_week_times])
    # print user_basic.shape
    user_basic = user_basic.reshape((1, user_basic.shape[0]))
    # print user_basic.shape
    # user_weekdayp = np.sum(weekdayP * weekday_sparse, axis=0)
    # user_weekdayp = np.array(user_weekdayp)
    # user_weekdayp = user_weekdayp.reshape((1, 1))
    # user_hourP = np.sum(hourP * hour_sparse, axis=0)
    # user_hourP = np.array(user_hourP)
    # user_hourP = user_hourP.reshape((1, 1))
    # class_id = np.array(class_id)
    # class_id = class_id.reshape((1, 1))
    # store_id = np.array(store_id)
    # store_id = store_id.reshape((1, 1))
    # coach_id = np.array(coach_id)
    # coach_id = coach_id.reshape((1, 1))
    # hour = np.array(hour-7)
    # hour = hour.reshape((1, 1))
    # weekday = np.array(weekday)
    # weekday = weekday.reshape((1, 1))
    user_history_bynow.append(user_basic)
    user_history_bynow.append(user_coach_history)
    user_history_bynow.append(user_coach_weight)
    user_history_bynow.append(user_store_history)
    user_history_bynow.append(user_store_weight)
    user_history_bynow.append(user_class_history)
    user_history_bynow.append(user_class_weight)
    user_history_bynow.append(user_hour_history)
    user_history_bynow.append(user_hour_weight)
    user_history_bynow.append(user_week_history)
    user_history_bynow.append(user_week_weight)
    user_history_bynow.append(weekdayP)
    user_history_bynow.append(hourP)
    return user_history_bynow


def get_sch_map():
    appoint_file = open(data_path + appoint_queue_id, 'r')
    appoint_queue = pickle.load(appoint_file)
    sch_map = {}
    i = 1
    for key in appoint_queue.keys():
        for log in appoint_queue[key]:
            sch = log[0]
            if sch_map.has_key(sch):
                continue
            else:
                sch_map[sch] = i
                i += 1
    print i
    appoint_file.close()
    file1 = open(data_path+'scheduleMap', 'w')
    pickle.dump(sch_map, file1)


def get_sch_history(appoint_queue):
    sch_map = {}
    i = 1
    max1=0
    max2 = 0
    max3 =0
    hours = np.zeros(24)
    for key in appoint_queue.keys():
        for log in appoint_queue[key]:
            user_id = key
            # print key
            sch_id = log[0]
            store_id = log[1]
            start_time = log[2]
            end_time = log[3]
            class_id = log[4]
            convert_time = datetime.datetime.fromtimestamp(start_time)
            hour = convert_time.hour
            # print hour
            hours[hour] += 1
            c = len(get_history_class(user_id, start_time, appoint_queue))
            if c > max3:
                max3 = c
    return max3


def see_data():
    appoint_file = open(data_path + appoint_queue_id, 'r')
    appoint_queue = pickle.load(appoint_file)
    user_sch_dic = {}
    chongfu = 0
    n1 = 0
    n2 = 0
    n3 = 0
    n4 = 0
    n6 = 0
    n7 = 0
    n8 = 0
    n9 = 0
    n10 = 0
    for key in appoint_queue.keys():
        for log in appoint_queue[key]:
            user_id = key
            # print key
            sch_id = log[0]
            store_id = log[1]
            start_time = log[2]
            end_time = log[3]
            class_id = log[4]
            class_id_map = class_id
            status = log[5]
            if status == 1:
                n1+=1
            elif status ==2:
                n2+=1
            elif status == 3:
                n3+=1
            elif status == 4:
                n4+=1
            elif status == 6:
                n6+=1
            elif status == 7:
                n7+=1
            elif status == 8:
                n8+=1
            elif status == 9:
                n9+=1
            elif status == 10:
                n10+=1
            else:
                continue

    print 'n1: ', n1
    print 'n2: ', n2
    print 'n3: ', n3
    print 'n4: ', n4
    print 'n6: ', n6
    print 'n7: ', n7
    print 'n8: ', n8
    print 'n9: ', n9
    print 'n10: ', n10


def get_user_map():
    appoint_file = open(data_path + appoint_queue_id, 'r')
    appoint_queue = pickle.load(appoint_file)
    user_map = {}
    i = 0
    for key in appoint_queue.keys():
        user_map[key] = i
        i += 1
    print i
    appoint_file.close()
    file1 = open(data_path+'userIdMap', 'w')
    pickle.dump(user_map, file1)


if __name__ == '__main__':
    # get_weather_data()
    # deal_appoint_data()
    # get_coldstart_data()
    see_data()
    # get_sch_map()
    # get_sch_history()
    # see_data()
    # get_user_map()
    # right_file1 = open(data_path+'user_right', 'r')
    # user_right = pickle.load(right_file1)
    # for user_id in user_right.keys():
    #     user_r = user_right[user_id]
    #     print user_r
    #     print len(user_r)
    #     print '====================='
