import cPickle as pickle
from src_one.predata.dealOriginData import sort_trainData
from src_one.properties import data_path
appoint_queue_id = 'appoint_queue_map'
schedule_coach_map_id = 'schedule_coach_map'
coach_map_id = 'coach_sex'
user_map_id = 'user_sex'


def load_data():
    appoint_file = open(data_path + appoint_queue_id, 'r')
    appoint_queue = pickle.load(appoint_file)
    appoint_queue = sort_trainData(appoint_queue)
    user_file = open(data_path + user_map_id, 'r')
    user = pickle.load(user_file)
    coach_file = open(data_path + coach_map_id, 'r')
    coach = pickle.load(coach_file)
    schedule_file = open(data_path + schedule_coach_map_id, 'r')
    schedule = pickle.load(schedule_file)
    appoint_file.close()
    user_file.close()
    coach_file.close()
    schedule_file.close()
    return appoint_queue, user, coach, schedule


def get_schedules(class_id_list, coach_id_list, store_id, start_time):
    schedules = []
    for coach_id in coach_id_list:
        for class_id in class_id_list:
            schedules.append([class_id, store_id, start_time, coach_id])
    return schedules


def get_candidate_schedules(candidates, slot_id, sch_t, storeId):
    schedules = []
    if not candidates.has_key(slot_id):
        return schedules
    for candidate in candidates[slot_id]:
        coach_id = candidate[0]
        class_id = candidate[1]
        candidate_id = candidate[2]
        schedules.append([class_id, storeId, sch_t, coach_id, candidate_id])
    return schedules


