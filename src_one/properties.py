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
lastestUpdateUnix = int(time.time())-24*60*60
end_year = lastestUpdateTime.year
end_month = lastestUpdateTime.month
end_day = lastestUpdateTime.day



# data path
project_path = 'C:/Users/wjy/Desktop/leai/brave/'
data_path = project_path+'data/'
candidate_path = project_path+'userClassCandidates/'
model_save_path = project_path+'model_new/'
result_path = project_path+'result/'
thread_num = 16
padding_num = 100


# user right ip
url = 'http://pub-gw.japis.leoao-inc.com/v1/rights/findUserStatus'



