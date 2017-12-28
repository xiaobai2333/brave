import sys
sys.path.append('/home/leai/brave')
import logging

import cPickle as pickle
from src_one.properties import data_path, lastestUpdateTime
def init_log():
    log_format = '[%(asctime)s][%(levelname)s][file:%(filename)s][line:%(lineno)s] %(message)s'
    logging.basicConfig(level=logging.DEBUG,
                        format=log_format,
                        filename=data_path+'log/merida_update.log',
                        filemode='w')
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(logging.Formatter(log_format))
    logging.getLogger('').addHandler(console)
init_log()

from src_one.readDataFromDatabase.read_data_from_database import read_data_from_database
from src_one.predata.pre_train_data import get_first_data


logging.info('Start update data, please wait....')
# read_data_from_database()
logging.info('Start merge data to train data type....')
get_first_data()
logging.info('Merge data to train data success...')
    
from src_one.PersistentOffLine.StoreUserCandidates import multiProcess_BuildCandidates
from src_one.trainModel.dnn_main import train_model, predict



#save latest updateTime
logging.info('****')
logging.info('Update_recordTime : '+str(lastestUpdateTime))
logging.info('****')
lastestTimeFile = open(data_path+'lastestUpdateTime','w')
pickle.dump(lastestUpdateTime,lastestTimeFile)
lastestTimeFile.close()


def updatePersistentData():
    logging.info('Start train new model...')
    train_model()
    logging.info('Train new model success...')
    logging.info('Start evaluate model...')
    predict()
    logging.info('Start update user candidates....')
    multiProcess_BuildCandidates()
    logging.info('Update user candidates success...')
    logging.info('Update all data success...')

if __name__ == '__main__':
    updatePersistentData()
