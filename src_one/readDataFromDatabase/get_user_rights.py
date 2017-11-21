import requests
import json
import pickle
import numpy as np
from src_one.properties import data_path, url

def get_user_rights_web(user_id):
    #url = 'http://epub-gw.japis.leoao-inc.com/v1/rights/findUserStatus'
    body = dict(
        userId=user_id
    )
    response = requests.post(url=url, json=body)
    return json.loads(response.text)['result']['groupIdArr']


def get_user_right(user):
    # user_map_id = './user_map_new'
    # user_file = open(user_map_id, 'r')
    # user = pickle.load(user_file)
    user_right = {}
    usersReal = []
    i = 0
    for user_id in user:
        if i % 1000 == 0:
            print i
        i += 1
        j = get_user_rights_web(user_id)
        if 2 in j:
            usersReal.append(user_id)
       # user_right[user_id] = j
    file1 = open(data_path+'all_userid', 'w')
    pickle.dump(usersReal, file1)
    file1.close()
   # return user_right

