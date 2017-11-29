#coding=utf-8
import sys
sys.path.append('/home/leai/brave')
from src_one.filter import Collaborative_Filter
from src_one.filter import ReadData

import logging
from src_one.filter.filter import  get_apriori_rulse, get_hour_store_Canditate, \
    get_Class_Candidate, ishourStoreInCandidate, isClassInCandidate, ishourStoreInCandidateProbabilities
from src_one.score.single_scroe import merge_data, get_score
from src_one.predata.preschedule import load_data,  get_candidate_schedules
from src_one.readDataFromDatabase.read_data_for_predict import writeback_databse, read_data_for_predict
from keras.models import load_model
import multiprocessing
import time
import datetime
#from progressbar import *
import numpy as np
import cPickle as pickle
from src_one.properties import data_path, model_save_path, candidate_path, result_path, thread_num

def init_log():
    log_format = '[%(asctime)s][%(levelname)s][file:%(filename)s][line:%(lineno)s] %(message)s'
    logging.basicConfig(level=logging.DEBUG,
                        format=log_format,
                        filename=data_path+'log/predict.log',
                        filemode='w')
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(logging.Formatter(log_format))
    logging.getLogger('').addHandler(console)

init_log()



file_date = open(data_path+'lastestUpdateTime')
lastestUpdateTime = pickle.load(file_date)
logging.info('****')
logging.info('lastestUpdateTime : '+str(lastestUpdateTime))
logging.info('****')
file_date.close()
end_day =lastestUpdateTime.day
end_month = lastestUpdateTime.month
end_year= lastestUpdateTime.year

model_name = model_save_path+'DNN_model_11_7.h5'
userCandidate_files_path = candidate_path+'all_userCandidates'
all_user_file = open(data_path + 'all_userid', 'r')
user_list = pickle.load(all_user_file)
all_user_file.close()
user_list = list(user_list)
all_coaches_file = open(data_path + 'all_coachids', 'r')
coach_id_list = pickle.load(all_coaches_file)
all_coaches_file.close()
userCandidates_file = open(userCandidate_files_path,'r')
userCandidates = pickle.load(userCandidates_file)
userCandidates_file.close()
appoint_queue, user, coach, schedule = load_data()
historyStarttime = (datetime.datetime(end_year, end_month, end_day) -datetime.datetime(1970, 1, 1)- datetime.timedelta(hours=8)).total_seconds()
# class_id_list = [x for x in range(45)]
#right_file1 = open(data_path + 'user_right', 'r')
#user_right_list = pickle.load(right_file1)
#right_file1.close()
# sche_time = 1505037600 + 2 * 60 * 60
# start_time_list = [sche_time]
# store_id_list = [26]
all_list = []
# thread_num = 20
for c in range(thread_num):
    all_list.append({})

#slot_file = open(data_path+'slots', 'r')
#slots = pickle.load(slot_file)
#slot_file.close()

#candidate_file = open(data_path+'candidates', 'r')
#candidates = pickle.load(candidate_file)
#candidate_file.close()
slots, candidates = read_data_for_predict()
slotIDs = candidates.keys()
all_len = len(user_list)
length = int(np.math.ceil(all_len*1.0/thread_num))


def predict_candidate_score(index,slots, candidates):
    logging.info('process '+str(index)+ 'start....')
    start = time.clock()
    model = load_model(model_name)

    if index == thread_num-1:
        end = all_len
    else:
        end = (index+1)*length
    slot_Score = {}
    subUserList = user_list[index*length: end]
    subLen =  len(subUserList)
    i = 1


    time_filter = 0
    time_predict = 0
    for user_id in subUserList:
        stime = time.clock()
        hour_candidate , store_candidate = get_hour_store_Canditate(historyStarttime, user_id, appoint_queue)
        classId_candidate = userCandidates[user_id]
        etime =time.clock()
        time_filter += etime-stime
        for slot_id in slotIDs:
            sch_t = slots[slot_id][0]
            storeId = slots[slot_id][1]

            if not ishourStoreInCandidateProbabilities(sch_t,storeId ,  hour_candidate,store_candidate):
                continue

            schedules_list = get_candidate_schedules(candidates, slot_id, sch_t, storeId)
            if not slot_Score.has_key(slot_id):
                slot_Score[slot_id] = {}

            for schedule1 in schedules_list:
                sch = schedule1[:4]
                candidateid = schedule1[4]
                if isClassInCandidate(sch, classId_candidate):
                   # data = merge_data(sch, user_id, appoint_queue, user, coach, schedule)
                   # singleScore = get_score(model, data)
                    if slot_Score[slot_id].has_key(candidateid):
                       # slot_Score[slot_id][candidateid] += singleScore[0][0]
                        slot_Score[slot_id][candidateid] += 1
                    else:
                       # slot_Score[slot_id][candidateid] = singleScore[0][0]
                        slot_Score[slot_id][candidateid] = 1
        etime2 = time.clock()
        time_predict += etime2 - etime
        if i%100 == 0:
            logging.info('Process  {index} :  {i} / {subLen}'.format(index=index, i=i, subLen=subLen))
        i +=1
    logging.info('Process'+str(index)+'  ===  filterTime : '+str(time_filter)+'   predictTime : '+str(time_predict))
    file_score = open(result_path + 'sch_score_sorted'+str(index), 'w')
    pickle.dump(slot_Score, file_score)
    file_score.close()
    end = time.clock()
    logging.info('process*'+str(index)+ ' end....'+'use time: '+str(end-start))


def process_predict():
    process_list = []
    # multiprocessing.Process(target=help).start()
    # predict_candidate_score(index, slotIDs, slots_map, candidates)

    for i in range(thread_num):
        process1 = multiprocessing.Process(target=predict_candidate_score, args=(i,  slots, candidates))
        process_list.append(process1)
        process1.start()

    for i in range(thread_num):
        process_list[i].join()

    logging.info('main process end....')


def main():
    start = time.clock()
    logging.info('start.....')
    process_predict()
    logging.info('==================')
    logging.info('end......')
    logging.info('merge start...')
    sch_score = merge_result()
    logging.info('merge over....')
    end = time.clock()
    logging.info('use time: '+str(end-start))
    logging.info('write back database...')
    writeback_databse(sch_score)
    logging.info('write success...')


def merge_result():
    result_map = {}
    for i in range(thread_num):
        result_file = open(result_path+'sch_score_sorted'+str(i), 'r')
        sch_score = pickle.load(result_file)
        result_file.close()
        for slot_id in sch_score:
            if not result_map.has_key(slot_id):
                result_map[slot_id] = {}
            for candidate_id in sch_score[slot_id]:
                if not result_map[slot_id].has_key(candidate_id):
                    result_map[slot_id][candidate_id]=sch_score[slot_id][candidate_id]
                else:
                    result_map[slot_id][candidate_id] += sch_score[slot_id][candidate_id]
    logging.info('all : '+str(len(result_map)))
    for slot_id in result_map:
        logging.info(' slot id : {slot_id}============================='.format(slot_id=slot_id))
        for candidate_id in result_map[slot_id]:
            logging.info('candidate_id: {candidate_id}, score: {score}'.format(candidate_id=candidate_id,score=result_map[slot_id][candidate_id]))
            logging.info('-------')
    all_result_file = open(result_path+'all_result', 'w')
    pickle.dump(result_map, all_result_file)
    all_result_file.close()
    return result_map


def see_result():
    subResultList = []
    for i in range(thread_num):
        result_file = open(result_path+'sch_score_sorted'+str(i), 'r')
        sch_score = pickle.load(result_file)
       # print len(sch_score)
        subResultList.append(sch_score)
        result_file.close()

    all_result_file = open(result_path + 'all_result', 'r')
    all_result = pickle.load( all_result_file)
    all_result_file.close()
    i = 0
    name = []
    for slot_id in slotIDs:
        print ' slot id : ', slot_id, '============================='
        if all_result.has_key(slot_id):
            for candidateid in all_result[slot_id]:
                for subResult in subResultList:
                    if subResult.has_key(slot_id) and subResult[slot_id].has_key(candidateid):
                        print 'score : ',subResult[slot_id][candidateid]

                print '******'
                print 'sum : ' , all_result[slot_id][candidateid]
                print '++++++++++++++++++++++'
        else:
            name.append(slot_id)
            i += 1;
    print 'slot miss : ', i
    for n in name:
        print 'miss : ', n


if __name__ == '__main__':
    main()
    # merge_result()
    # see_result()
    # predict_score(0)
    # file_score = open(data_path + 'sch_score', 'r')
    # sch_score = pickle.load(file_score)
    # sch_score_list = sort_class(sch_score)
    # for item in sch_score_list:
    #     sch = item[0]
    #     score = item[1]
    #     print 'class id: ', sch[0], '  store_id: ', sch[1], '  coach_id: ', sch[3], '  score: ', score
    #     print '============================================================================================='
    # file1 = open(data_path + 'sch_score_sorted', 'w')
    # pickle.dump(sch_score_list, file1)
    # file1.close()
    # candidate_file = open('../../data_11_7/candidates', 'r')
    # candidate_map = pickle.load(candidate_file)
    # candidate_file.close()
    # for key in candidate_map:
    #     for x in candidate_map[key]:
    #         print x[1]
