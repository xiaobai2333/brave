import time
import datetime
import cPickle as pickle

trainProtocol = 'mysql'
trainAccount = 'data_group'
trainPassword = '#datagroup2'
trainIp = '121.43.184.204'
trainPort = 3307
trainClassDatabase = 'le_public_class'
trainUserDatabase = 'le_public_user'

# slot database propertiees
slotProtocol = 'mysql'
slotAccount = 'leai'
slotPassword = 'Turing0623!'
slotIp = '127.0.0.1'
slotPort = 3306
slotDatabase = 'brave'


# train data time block (read_data_from_database)
start_year = 2017
start_month = 6
start_day = 1
lastestUpdateTime = datetime.datetime.now()- datetime.timedelta(hours=24)
end_year = lastestUpdateTime.year
end_month = lastestUpdateTime.month
end_day = lastestUpdateTime.day



# data path
project_path = '/home/leai/brave/'
data_path = project_path+'data/'
candidate_path = project_path+'userClassCandidates/'
model_save_path = project_path+'model_new/'
result_path = project_path+'result/'
thread_num = 16
padding_num = 100


# user right ip
url = 'http://pub-gw.japis.leoao-inc.com/v1/rights/findUserStatus'

def get_now_date():
    global end_year, end_month, end_day
    now_date = time.localtime()
    end_year = now_date.tm_year
    end_month = now_date.tm_mon
    end_day = now_date.tm_mday


