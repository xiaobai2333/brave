# coding=utf-8
from __future__ import division
from __future__ import print_function
from base_model import BaseMemoryModel, Model, BaseModel
from sqlalchemy import Column, Integer, Float, DateTime, func, Boolean
import datetime
import sqlalchemy
import sqlalchemy.orm
import numpy as np
import logging
import cPickle as pickle
from new_database import Appoint, User, Coach, Class, Schedule, Schedule_coach
from read_data_for_predict import get_course
# vim ~/.my.cnf
# [mysqld]
# max_heap_table_size = 1024M
#
# sudo service mysql restart

# 课程id映射表：  (数据库对应的id： class_property表对应的id)
session_maker = sqlalchemy.orm.sessionmaker()
# data_path = '../../data_11_7/'
from src_one.properties import trainProtocol, trainAccount, trainPassword, trainIp, trainPort, trainClassDatabase, trainUserDatabase, start_year, start_month, start_day, end_year, end_month, end_day, data_path, \
    cities


#  远程数据库
def init(database):
    protocol = trainProtocol
    account = trainAccount
    password = trainPassword
    ip = trainIp
    port = trainPort
    # database = 'le_public_class'
    db_url = '{protocol}://{account}:{passwd}@{ip}:{port}/{database}?charset=utf8'.format(
        protocol=protocol, account=account, passwd=password, ip=ip, port=port, database=database)
    engine = sqlalchemy.create_engine(db_url, echo=False)
    session = sqlalchemy.orm.sessionmaker(bind=engine)(expire_on_commit=False)
    return session


#  本地数据库
def init_db():
    protocol = 'mysql'
    account = 'leai'
    password = 'leai123'
    ip = '127.0.0.1'
    port = 3306
    database = 'brave'
    db_url = '{protocol}://{account}:{passwd}@{ip}:{port}/{database}?charset=utf8'.format(
        protocol=protocol, account=account, passwd=password, ip=ip, port=port, database=database)
    engine = sqlalchemy.create_engine(db_url, echo=False)
    # Model.metadata.drop_all(engine)
    Model.metadata.create_all(engine)
    session_maker.configure(bind=engine)
    session = session_maker(expire_on_commit=False)
    return session


def datetime_to_timestamp(time):
    origin_time = datetime.datetime(1970, 1, 1)
    return int((time - origin_time - datetime.timedelta(hours=8)).total_seconds())


# ===================  所有课程表：杭州、6月-10月、指定课程   =====================================================================
def get_all_schedule():
    database = trainClassDatabase
    session = init(database)
    schedule = session.query(Schedule_coach).all()
    num = len(schedule)
    session.close()
    # print('All schedules number: ', num)
    logging.info('All schedules number: '+str(num))
    sch_map = {}
    for sch in schedule:
        sch_map[sch.schedule_id] = sch.coach_id
    file = open(data_path+'schedule_coach_map', 'w')
    pickle.dump(sch_map, file)
    file.close()
    return sch_map


# ===================  预约表：杭州、6月-10月、指定课程 键为user_id =========================================================
def get_appoint_map(courses):
    #courses_file = open(data_path+'courses', 'r')
    #courses = pickle.load(courses_file)
    #courses_file.close()
    #courses = get_course()
    # print (courses)
    database = trainClassDatabase
    session = init(database)
    schedule = session.query(Appoint).filter(Appoint.city_id.in_(cities),
                                             Appoint.class_type_id == 1,
                                             Appoint.class_id.in_(courses),
                                             Appoint.start_time >= datetime_to_timestamp(
                                                 datetime.datetime(start_year, start_month, start_day)),
                                             Appoint.end_time <= datetime_to_timestamp(
                                                  datetime.datetime(end_year, end_month, end_day))).all()
    num = len(schedule)
    # print('All appoints number: ', num)
    logging.info('All appoints number: '+str(num))
    session.close()
    sch_map = {}
    for sch in schedule:
        if not sch_map.has_key(sch.user_id):
            sch_map[sch.user_id] = []
        sch_map[sch.user_id].append([sch.schedule_id, sch.store_id, sch.start_time, sch.end_time, sch.class_id,
                                     sch.status])
    file1 = open(data_path+'appoint_queue_map', 'w')
    pickle.dump(sch_map, file1)
    file1.close()
   # session.close()
    return sch_map


# ===================  预约表：杭州、6月-10月、指定课程 键为class_id =========================================================
def get_appoint_map_class(start_month, start_day, end_month, end_day):
    database = trainClassDatabase
    session = init(database)
    schedule = session.query(Appoint).filter(Appoint.city_id.in_(cities),
                                             Appoint.class_type_id == 1,
                                             Appoint.start_time >= datetime_to_timestamp(
                                                 datetime.datetime(2017, start_month, start_day)),
                                             Appoint.end_time <= datetime_to_timestamp(
                                                  datetime.datetime(2017, end_month, end_day))).all()
    session.close()
    num = len(schedule)
    print(num)
    sch_map = {}
    for sch in schedule:
        if not sch_map.has_key(sch.class_id):
            sch_map[sch.class_id] = []
        sch_map[sch.class_id].append([sch.schedule_id, sch.store_id, sch.start_time, sch.end_time, sch.user_id,
                                     sch.status])
    file1 = open('../data/appoint_queue_map_class', 'w')
    pickle.dump(sch_map, file1)
    file1.close()
    return sch_map


# ===================  预约表：杭州、6月-10月、指定课程 键为coach_id =========================================================
def get_appoint_map_coach(start_month, start_day, end_month, end_day):
    database = trainClassDatabase
    session = init(database)
    schedule = session.query(Appoint).filter(Appoint.city_id.in_(cities),
                                             Appoint.class_type_id == 1,
                                             Appoint.start_time >= datetime_to_timestamp(
                                                 datetime.datetime(2017, start_month, start_day)),
                                             Appoint.end_time <= datetime_to_timestamp(
                                                  datetime.datetime(2017, end_month, end_day))).all()
    num = len(schedule)
    print(num)
    file = open('../data_new/schedule_coach_map', 'r')
    schedule_coach = pickle.load(file)
    sch_map = {}
    for sch in schedule:
        if not schedule_coach.has_key(sch.schedule_id):
            continue
        coach_id = schedule_coach[sch.schedule_id]
        if not sch_map.has_key(coach_id):
            sch_map[coach_id] = []
        sch_map[coach_id].append([sch.schedule_id, sch.store_id, sch.start_time, sch.end_time, sch.class_id,
                                     sch.status])
    file1 = open('../data/appoint_queue_map_coach', 'w')
    pickle.dump(sch_map, file1)
    file1.close()
    return sch_map


# ===================  用户表：杭州、6月-10月、指定课程   =====================================================================
def get_user_map(appoint_map):
    # file2 = open('../data/appoint_queue_map')
    # appoint_map = pickle.load(file2)
    database = trainUserDatabase
    session = init(database)
    user = []
    user.extend(appoint_map.keys())
    # user.extend(queue_map.keys())
    schedule = session.query(User).filter(User.user_id.in_(user)).all()
    num = len(schedule)
    session.close()
    # print('All users number: ', num)
    logging.info('All users number: '+str(num))
    sch_map = {}
    for sch in schedule:
        sch_map[sch.user_id] = sch.sex
    file1 = open(data_path+'user_sex', 'w')
    pickle.dump(sch_map, file1)
    file1.close()
    return sch_map


# ===================  coach表：杭州、6月-8月、指定课程   =====================================================================
def get_coach_map():
    database = trainUserDatabase
    session = init(database)
    schedule = session.query(Coach).all()
    num = len(schedule)
    # print('All coaches number: ', num)
    logging.info('All coaches number: '+str(num))
    session.close()
    sch_map = {}
    for sch in schedule:
        sch_map[sch.id] = sch.sex
    file1 = open(data_path+'coach_sex', 'w')
    pickle.dump(sch_map, file1)
    file1.close()
    return sch_map


def read_data_from_database():
    print('read data from database start....')
    print('start time: 2017-', start_month, '-', start_day)
    print('end time: 2017-', end_month, '-', end_day)
    get_all_schedule()
    print('get schedule_coach success...')
    print('get course start...')
    courses = get_course()
    print('get course success...')
    get_appoint_map(courses)
    print('get appoint_map success...')
    file1 = open(data_path + 'appoint_queue_map', 'r')
    appoint_map = pickle.load(file1)
    print(len(appoint_map))
    get_user_map(appoint_map)
    print('get user sex success...')
    get_coach_map()
    print('get coach sex success...')
    print('read data from database end....')

if __name__ == '__main__':
    # start_year = 2017
    # start_month = 6
    # start_day = 1
    # end_year = 2017
    # end_month = 11
    # end_day = 7
    read_data_from_database()
