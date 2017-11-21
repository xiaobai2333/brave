# encoding=utf-8


from sqlalchemy import Column, Integer, Boolean, String
from base_model import BaseModel


class Appoint(BaseModel):
    __tablename__ = 'appoint'
    id = Column(Integer, primary_key=True)
    schedule_id = Column(Integer)
    user_id = Column(Integer)
    status = Column(Integer)
    start_time = Column(Integer)
    end_time = Column(Integer)
    class_id = Column(Integer)
    class_type_id = Column(Integer)
    store_id = Column(Integer)
    city_id = Column(Integer)


class User(BaseModel):

    __tablename__ = 'u_user_info'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    sex = Column(Integer)


class Coach(BaseModel):
    __tablename__ = 'u_coach_base'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    sex = Column(Integer)


class Class(BaseModel):
    __tablename__ = 'class'
    id =Column(Integer,primary_key=True)


class Schedule(BaseModel):
    __tablename__ = 'schedule'
    id = Column(Integer, primary_key=True)
    store_id = Column(Integer)
    city_id = Column(Integer)
    start_time = Column(Integer)
    end_time = Column(Integer)
    class_id = Column(Integer)
    member_limit = Column(Integer)
    status = Column(Integer)


class Schedule_coach(BaseModel):
    __tablename__ = 'schedule_coach'
    id = Column(Integer, primary_key=True)
    schedule_id = Column(Integer)
    coach_id = Column(Integer)


class Slot(BaseModel):
    __tablename__ = 'slot'
    id = Column(Integer, primary_key=True)
    start_time = Column(Integer)
    store_id = Column(Integer)


class Candidate(BaseModel):
    __tablename__ = 'candidate'
    id = Column(Integer, primary_key=True)
    slot_id = Column(Integer)
    coach_id = Column(Integer)
    course_id = Column(Integer)
    score = Column(Integer)


class Course(BaseModel):
    __tablename__ = 'course'
    id = Column(Integer, primary_key=True)



