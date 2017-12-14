import logging

import sqlalchemy
from new_database import Slot, Candidate, Course
import cPickle as pickle
import time
from src_one.properties import slotProtocol, slotAccount, slotPassword, slotIp, slotPort, slotDatabase, data_path


def init(database):
    protocol = slotProtocol
    account = slotAccount
    password = slotPassword
    ip = slotIp
    port = slotPort
    # database = 'le_public_class'
    db_url = '{protocol}://{account}:{passwd}@{ip}:{port}/{database}?charset=utf8'.format(
        protocol=protocol, account=account, passwd=password, ip=ip, port=port, database=database)
    engine = sqlalchemy.create_engine(db_url, echo=False)
    session = sqlalchemy.orm.sessionmaker(bind=engine)(expire_on_commit=False)
    return session


def get_slots():
    database = slotDatabase
    session = init(database)
    slots = session.query(Slot).all()
    slot_map = {}
    for slot in slots:
        slot_id = slot.id
        # print slot.start_time
        slot_start_time = int(time.mktime(slot.start_time.timetuple()))
       # print slot_start_time
        # print slot_start_time
        slot_store_id = slot.store_id
        slot_map[slot_id] = [slot_start_time, slot_store_id]
    slot_file = open(data_path+'slots', 'w')
    pickle.dump(slot_map, slot_file)
    slot_file.close()
    print 'slot num: ', len(slot_map.keys())
    session.close()
    return slot_map


def read_slots_only():
    database = slotDatabase
    session = init(database)
    slots = session.query(Slot).all()
    slot_map = {}
    candidate_map = {}
    for slot in slots:
        slot_id = slot.id
        # print slot.start_time
        slot_start_time = int(time.mktime(slot.start_time.timetuple()))
        # print slot_start_time
        # print slot_start_time
        slot_store_id = slot.store_id
        slot_course_id = slot.course_id
        slot_coach_id = slot.coach_id
        slot_map[slot_id] = [slot_start_time, slot_store_id]
        if not candidate_map.has_key(slot_id):
            candidate_map[slot_id] = []
        candidate_map[slot_id].append([slot_coach_id, slot_course_id, 1])
    # slot_file = open(data_path + 'slots', 'w')
    # pickle.dump(slot_map, slot_file)
    # slot_file.close()
    print 'slot num: ', len(slot_map.keys())
    session.close()
    return slot_map, candidate_map


def get_candicate():
    database = slotDatabase
    session = init(database)
    candidates = session.query(Candidate).all()
    candidate_map = {}
    n = 0
    for candidate in candidates:
        candidate_id = candidate.id
        candidate_coach_id = candidate.coach_id
        candidate_course_id = candidate.course_id
        candidate_slot_id = candidate.slot_id
        if not candidate_map.has_key(candidate_slot_id):
            candidate_map[candidate_slot_id] = []
        candidate_map[candidate_slot_id].append([candidate_coach_id, candidate_course_id, candidate_id])
        n += 1
    candidate_file = open(data_path+'candidates', 'w')
    pickle.dump(candidate_map, candidate_file)
    candidate_file.close()
    session.close()
    print 'candidates num: ', len(candidate_map.keys())
    print 'all schedule num: ', n
    return candidate_map


def get_course():
    print 'start read courses from database...'
    database = slotDatabase
    session = init(database)
    courses = session.query(Course).all()
    all_coures = []
    for key in courses:
        all_coures.append(key.id)
    courses_file = open(data_path+'courses', 'w')
    pickle.dump(all_coures, courses_file)
    # print len(all_coures)
    print 'get courses success'
    courses_file.close()
    session.close()
    return all_coures


def writeback_databse(sch_score):
    database = slotDatabase
    session = init(database)
    query = session.query(Candidate)
    # query.update({Candidate.score: 0})
    # result_file = open(data_path+'all_result', 'r')
    # sch_score = pickle.load(result_file)
    # result_file.close()
    i = 0
    length = len(sch_score.keys())
    for slot_id in sch_score:
        for candicate_id in sch_score[slot_id]:
            query.filter(Candidate.id==candicate_id).update({Candidate.score: sch_score[slot_id][candicate_id]})
        logging.info('process: {i}/ {length}'.format(i=i,length=length))
        i += 1
    logging.info('write back database success....')
    session.close()


def writeback_slot(sch_score):
    database = slotDatabase
    session = init(database)
    query = session.query(Slot)
    # query.update({Candidate.score: 0})
    # result_file = open(data_path+'all_result', 'r')
    # sch_score = pickle.load(result_file)
    # result_file.close()
    i = 0
    length = len(sch_score.keys())
    for slot_id in sch_score:
        for candicate_id in sch_score[slot_id]:
            query.filter(Slot.id == slot_id).update({Slot.score: sch_score[slot_id][candicate_id]})
        logging.info('process: {i}/ {length}'.format(i=i, length=length))
        i += 1
    logging.info('write back database success....')
    session.close()


def read_data_for_predict():
    print 'read slot data start......'
    # slots = get_slots()
    slots, candicates= read_slots_only()
    print 'read slot data success....'
    print 'read candicates start.....'
    # candicates = get_candicate()
    print 'read candicates success....'
    return slots, candicates

if __name__ == '__main__':
    writeback_databse()

