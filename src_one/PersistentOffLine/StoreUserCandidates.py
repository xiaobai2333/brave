#coding=utf-8
import time

import datetime
import multiprocessing
import numpy as np
import cPickle as pickle
import logging
from src_one.filter import Collaborative_Filter
from src_one.filter import ReadData
from src_one.filter.filter import get_apriori_rulse, get_Class_Candidate
from src_one.predata.preschedule import load_data
from src_one.properties import data_path, candidate_path, thread_num, end_year, end_month, end_day

all_user_file = open(data_path + 'all_userid', 'r')
user_list = pickle.load(all_user_file)
all_user_file.close()

user_list = list(user_list)
all_len = len(user_list)
logging.info('all data length: '+str(all_len))
length = int(np.math.ceil(all_len*1.0/thread_num))
historyStarttime = (datetime.datetime(end_year, end_month, end_day) -datetime.datetime(1970, 1, 1)- datetime.timedelta(hours=8)).total_seconds()
appoint_queue, user, coach, schedule = load_data()


def storeClassCandidates(index):
    logging.info( 'dealCanditates process '+str(index)+'  start....')
    start = time.clock()

    if index == thread_num-1:
        end = all_len
    else:
        end = (index+1)*length
    subUserList = user_list[index*length: end]
    subLen =  len(subUserList)
    i = 1

    #  算法相关 需要的变量
    apriori_rules = get_apriori_rulse(historyStarttime, appoint_queue, 0.1, 0.6)
    userDict = ReadData.get_recent_user_classId_Dict(historyStarttime, appoint_queue)
    itemUser = Collaborative_Filter.getItemUserMap(userDict)
    userCandidatesMap = {}
    for user_id in subUserList:
        stime = time.clock()
        classId_candidate = get_Class_Candidate(user_id, apriori_rules, userDict, itemUser)
        userCandidatesMap[user_id] = classId_candidate
        etime =time.clock()
        # log =  'dealCandidates Process {index} :  {i}/ {subLen}   cost: {time}'.format(index=index,i=i,subLen=subLen,time=etime-stime)
        # logging.info(log)
        print 'dealCandidates Process {index} :  {i}/ {subLen}   cost: {time}'.format(index=index,i=i,subLen=subLen,time=etime-stime)
        i +=1

    resultFile = open(candidate_path + 'userCandidatesMap'+str(index), 'w')
    pickle.dump(userCandidatesMap, resultFile)
    resultFile.close()
    end = time.clock()
    log2 = 'process  {index}  end.... use time:  {time} '.format(index=index,time=end-start)
    logging.info(log2)
    # print 'process  {index}  end.... use time:  {time} '.format(index=index,time=end-start)


def merge_result():
    userCandidatesMap = {}
    for i in range(thread_num):
        result_file = open(candidate_path+'userCandidatesMap'+str(i), 'r')
        subUserCandidatesMap = pickle.load(result_file)
        # logging.info('sub {i} : {len}'.format(i=i,len=len(subUserCandidatesMap)))
        print 'sub {i} : {len}'.format(i=i, len=len(subUserCandidatesMap))
        result_file.close()
        for user_id in subUserCandidatesMap:
                userCandidatesMap[user_id]=subUserCandidatesMap[user_id]
    # logging.info('all  : {len}'.format( len=len(userCandidatesMap)))
    print 'all  : {len}'.format( len=len(userCandidatesMap))
    all_result_file = open(candidate_path+'all_userCandidates', 'w')
    pickle.dump(userCandidatesMap, all_result_file)
    all_result_file.close()


def multiProcess_BuildCandidates():
    process_list = []
    # multiprocessing.Process(target=help).start()
    # predict_candidate_score(index, slotIDs, slots_map, candidates)

    for i in range(thread_num):
        process1 = multiprocessing.Process(target=storeClassCandidates, args=(i, ))
        process_list.append(process1)
        process1.start()
    for i in range(thread_num):
        process_list[i].join()

    merge_result()

    logging.info('multiProcess_BuildCandidates process end....')
    # print 'multiProcess_BuildCandidates process end....'



if __name__ == '__main__':
    multiProcess_BuildCandidates()
