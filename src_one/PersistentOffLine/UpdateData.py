import sys
sys.path.append('/home/leai/brave')


import cPickle as pickle
from src_one.properties import data_path, lastestUpdateTime
from src_one.readDataFromDatabase.read_data_from_database import read_data_from_database
from src_one.predata.pre_train_data import get_first_data

print 'Start update data, please wait....'
read_data_from_database()
print 'Start merge data to train data type....'
get_first_data()
print 'Merge data to train data success...'
    
from src_one.PersistentOffLine.StoreUserCandidates import multiProcess_BuildCandidates
from src_one.trainModel.dnn_main import train_model, predict


#save latest updateTime
print '****'
print 'Update_recordTime : ',lastestUpdateTime
print '****'
lastestTimeFile = open(data_path+'lastestUpdateTime','w')
pickle.dump(lastestUpdateTime,lastestTimeFile)
lastestTimeFile.close()
def updatePersistentData():
    print 'Start update user candidates....'
    multiProcess_BuildCandidates()
    print 'Update user candidates success...'
    print 'Start train new model...'
    train_model()
    print 'Train new model success...'
    print 'Start evaluate model...'
    predict()
    print 'Update all data success...'

if __name__ == '__main__':
    updatePersistentData()
