import cPickle as pickle
import numpy as np
import math
import operator
from keras.utils import np_utils
from keras.models import load_model
import datetime
from src_one.predata.dealOriginData import *
from src_one.properties import padding_num
user_map_id = 'user_map_new'
# data_path = '/home/software/leai/new_database_9_26/'
schedule_coach_map_id = 'schedule_coach_map'
coach_map_id = 'coach_map_new'


def merge_data(sche, user_history):
    class_id = sche[0]
    store_id = sche[1]
    start_time = sche[2]
    coach_id = sche[3]
    user_basic = user_history[0]
    user_coach_history = user_history[1]
    user_coach_weight = user_history[2]
    user_store_history = user_history[3]
    user_store_weight = user_history[4]
    user_class_history = user_history[5]
    user_class_weight = user_history[6]
    user_hour_history = user_history[7]
    user_hour_weight = user_history[8]
    user_week_history = user_history[9]
    user_week_weight = user_history[10]
    # user_sex = user[userId]
    # # coach_sex = coach[coach_id]
    convert_time = datetime.datetime.fromtimestamp(start_time)
    # # month = convert_time.month
    # # day = convert_time.day
    weekday = convert_time.weekday()
    weekday_sparse = np_utils.to_categorical(weekday, 7)
    # # print weekday_sparse
    hour = convert_time.hour
    hour_sparse = np_utils.to_categorical(hour - 7, 15)
    # pressenP = getPresentP(userId, start_time, appointMap)
    # average_appoint = get_sum_appoint(userId, start_time, appointMap)
    # last_week_times = get_lastweek_appoints(userId, start_time, appointMap)
    # last_timedelta = get_last_timedelta(userId, start_time, appointMap)
    # weekdayP = get_weekdayP(userId, start_time, appointMap)
    weekdayP = user_history[11]
    # hourP = get_hourP(userId, start_time, appointMap)  # 13
    hourP = user_history[12]
    # coach_1 = get_history_coach(userId, start_time, appointMap, schedule)
    # user_coach_history = np.array(coach_1 + [0 for x in range(padding_num - len(coach_1))])
    # user_coach_history = user_coach_history.reshape((1, user_coach_history.shape[0]))
    # user_coach_weight = [1.0 / len(coach_1) for x in range(len(coach_1))] + [0 for x in
    #                                                                             range(padding_num - len(coach_1))]
    # user_coach_weight = np.array(user_coach_weight)
    # user_coach_weight = user_coach_weight.reshape((1, 1, user_coach_weight.shape[0]))
    # store_1 = get_history_store(userId, start_time, appointMap)
    # user_store_history = store_1 + [0 for x in range(padding_num - len(store_1))]
    # user_store_history = np.array(user_store_history)
    # user_store_history = user_store_history.reshape((1, user_store_history.shape[0]))
    # user_store_weight = [1.0 / len(store_1) for x in range(len(store_1))] + [0 for x in
    #                                                                             range(padding_num - len(store_1))]
    #
    # user_store_weight = np.array(user_store_weight)
    # user_store_weight = user_store_weight.reshape((1, 1, user_store_weight.shape[0]))
    # class_1 = get_history_class(userId, start_time, appointMap)
    # user_class_history = class_1 + [0 for x in range(padding_num - len(class_1))]
    # user_class_history = np.array(user_class_history)
    # user_class_history = user_class_history.reshape((1, user_class_history.shape[0]))
    # user_class_weight = [1.0 / len(class_1) for x in range(len(class_1))] + [0 for x in
    #                                                                             range(padding_num - len(class_1))]
    #
    # user_class_weight = np.array(user_class_weight)
    # user_class_weight = user_class_weight.reshape((1, 1, user_class_weight.shape[0]))
    # hour_1 = get_history_time(userId, start_time, appointMap)
    # user_hour_history = hour_1 + [0 for x in range(padding_num - len(hour_1))]
    # user_hour_history = np.array(user_hour_history)
    # user_hour_history = user_hour_history.reshape((1, user_hour_history.shape[0]))
    # user_hour_weight = [1.0 / len(hour_1) for x in range(len(hour_1))] + [0 for x in
    #                                                                          range(padding_num - len(hour_1))]
    #
    # user_hour_weight = np.array(user_hour_weight)
    # user_hour_weight = user_hour_weight.reshape((1, 1, user_hour_weight.shape[0]))
    # week_1 = get_history_weekday(userId, start_time, appointMap)
    # user_week_history = week_1 + [0 for x in range(padding_num - len(week_1))]
    # user_week_history = np.array(user_week_history)
    # user_week_history = user_week_history.reshape((1, user_week_history.shape[0]))
    # user_week_weight = [1.0 / len(week_1) for x in range(len(week_1))] + [0 for x in
    #                                                                          range(padding_num - len(week_1))]
    # user_week_weight = np.array(user_week_weight)
    # user_week_weight = user_week_weight.reshape((1, 1, user_week_weight.shape[0]))
    # user_basic = np.array([user_sex, pressenP, average_appoint, last_timedelta, last_week_times])
    # # print user_basic.shape
    # user_basic = user_basic.reshape((1, user_basic.shape[0]))
    # # print user_basic.shape
    user_weekdayp = np.sum(weekdayP * weekday_sparse, axis=0)
    user_weekdayp = np.array(user_weekdayp)
    user_weekdayp = user_weekdayp.reshape((1, 1))
    user_hourP = np.sum(hourP * hour_sparse, axis=0)
    user_hourP = np.array(user_hourP)
    user_hourP = user_hourP.reshape((1, 1))
    class_id = np.array(class_id)
    class_id = class_id.reshape((1, 1))
    store_id = np.array(store_id)
    store_id = store_id.reshape((1, 1))
    coach_id = np.array(coach_id)
    coach_id = coach_id.reshape((1, 1))
    hour = np.array(hour-7)
    hour = hour.reshape((1, 1))
    weekday = np.array(weekday)
    weekday = weekday.reshape((1, 1))
    return [user_basic, user_coach_history, user_coach_weight, user_store_history, user_store_weight,
            user_class_history, user_class_weight, user_hour_history, user_hour_weight, user_week_history,
            user_week_weight,
            user_weekdayp, user_hourP, class_id, store_id, coach_id, hour, weekday]


def get_score(model, data):
    comeinP = model.predict(data, batch_size=1, )
    return comeinP


def sort_class(class_score):
    class_score_list = sorted(class_score.iteritems(), key=operator.itemgetter(1), reverse=True)
    return class_score_list

