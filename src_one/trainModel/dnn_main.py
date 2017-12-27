from __future__ import division

import logging

import src_one.trainModel.dnn_classifier as dc
import numpy as np
from keras.models import load_model
#from sklearn import preprocessing
from keras.callbacks import EarlyStopping
import random
from src_one.properties import data_path, model_save_path
label_num = 1
first_type_data_name = 'first_type_data.npy'


def train_test_split(data, arr_num):
    arr = range(arr_num)
    np.random.shuffle(arr)
    train_num = int(0.9 * arr_num)
    print 'train number:', train_num
    train_data = data[arr[0:train_num], :-label_num]
    train_label = data[arr[0:train_num], -label_num:]
    test_data = data[arr[train_num:], :-label_num]
    test_label = data[arr[train_num:], -label_num:]
    np.save(data_path+'test_data.npy', test_data)
    np.save(data_path+'test_label.npy', test_label)
    return train_data, train_label, test_data, test_label


def get_data_batch(train_data):
    user_basic = train_data[:, 0:5]
    # user_basic = np.hstack((train_data[:, 0:3], train_data[:, 4:7]))
    # user_basic[:, 1:] = preprocessing.scale(user_basic[:, 1:])
    # print '============================='
    # print user_basic[0:20, 1:2]
    # print '============================='
    user_coach_history = train_data[:, 5:105]
    user_coach_weight = train_data[:, 105:205]
    print 'user_coach_weight: ', user_coach_weight.shape
    user_coach_weight = np.reshape(user_coach_weight, (user_coach_weight.shape[0], 1, user_coach_weight.shape[1]))
    print 'user_coach_weight: ', user_coach_weight.shape
    user_store_history = train_data[:, 205:305]
    user_store_weight = train_data[:, 305:405]
    print 'user_store_weight: ', user_store_weight.shape
    user_store_weight = np.reshape(user_store_weight, (user_store_weight.shape[0], 1, user_store_weight.shape[1]))
    print 'user_store_weight: ', user_store_weight.shape
    user_class_history = train_data[:, 405:505]
    user_class_weight = train_data[:, 505:605]
    print 'user_class_weight: ', user_class_weight.shape
    user_class_weight = np.reshape(user_class_weight, (user_class_weight.shape[0], 1, user_class_weight.shape[1]))
    print 'user_class_weight: ', user_class_weight.shape
    user_hour_history = train_data[:, 605:705]
    user_hour_weight = train_data[:, 705:805]
    print 'user_hour_weight: ', user_hour_weight.shape
    user_hour_weight = np.reshape(user_hour_weight, (user_hour_weight.shape[0], 1, user_hour_weight.shape[1]))
    print 'user_hour_weight: ', user_hour_weight.shape
    user_week_history = train_data[:, 805:905]
    user_week_weight = train_data[:, 905:1005]
    print 'user_week_weight: ', user_week_weight.shape
    user_week_weight = np.reshape(user_week_weight, (user_week_weight.shape[0], 1, user_week_weight.shape[1]))
    print 'user_week_weight: ', user_week_weight.shape
    user_weekdayp = train_data[:, 1005:1012]
    user_hourP = train_data[:, 1012:1027]
    # user_weekdayp = preprocessing.scale(user_weekdayp)
    class_id = train_data[:, 1027:1028]
    store_id = train_data[:, 1028:1029]
    coach_id = train_data[:, 1029:1030]   #524 is class_id
    # class_basic = train_data[:, -26:-25]   #562
    # class_basic = np.hstack((train_data[:, 539:569], train_data[:, -23:-3]))
    # class_basic = np.hstack((class_basic, train_data[:, -1:]))
    week_sparse = train_data[:, -23:-16]
    hour_sparse = train_data[:, -16:-1]
    user_weekdayp = np.sum(user_weekdayp * week_sparse, axis=1)
    user_hourP = np.sum(user_hourP * hour_sparse, axis=1)
    class_week = np.argmax(week_sparse, axis=-1)
    class_hour = np.argmax(hour_sparse, axis=-1)
    # class_basic = preprocessing.scale(class_basic)
    # class_basic[:, :32] = preprocessing.scale(class_basic[:, :32])
    # class_basic[:, -4:] = preprocessing.scale(class_basic[:, -4:])
    return [user_basic, user_coach_history, user_coach_weight, user_store_history, user_store_weight,
            user_class_history, user_class_weight, user_hour_history, user_hour_weight, user_week_history, user_week_weight,
            user_weekdayp, user_hourP, class_id, store_id, coach_id, class_hour, class_week]


def train_model():
    # ================ train_test_split =======================================================
    x_data = np.load(data_path+first_type_data_name)
    arr_num = x_data.shape[0]
    train_data, train_label, test_data, test_label = train_test_split(x_data, arr_num)
    logging.info( 'train_data :'+str(train_data.shape))
    logging.info( 'train_label :'+str(train_label.shape))
    logging.info( 'test_data :'+str(test_data.shape))
    logging.info('test_label :'+str(test_label.shape))
    # ==========================================================================================
    model = dc.build_model()
    model = dc.compile_model(model, 0.01, 0.9, 1e-6)
    model = dc.train_model(model, get_data_batch(train_data), train_label, batch=500, epoch=6, validation_split=0.05)
    # model.fit(get_data_batch(train_data), train_label, batch_size=5000, epochs=20, validation_split=0.1, callbacks=[EarlyStopping(patience=2, mode='min')])
    # model.save('../model/MLP_model_new_3.h5')
    score = model.evaluate(get_data_batch(test_data), test_label, batch_size=500)
    print model.metrics_names
    print score
    logging.info('score'+str(score))


def predict():
    # x_data = np.load(data_path + first_type_data_name, mmap_mode='r+')
    # print x_data.shape
    # arr_num = x_data.shape[0]
    # test_data, test_label, test_data1, test_label1 = train_test_split(x_data, arr_num)
    # print 'train_data :', train_data.shape
    # print 'train_label :', train_label.shape
    test_data = np.load(data_path+'test_data.npy')
    test_label = np.load(data_path+'test_label.npy')

    # test = np.load('../data_sy/test_data_98_4.npy')
    # test_data = test[:, : -label_num]
    # test_label = test[:, -label_num:]

    # test = np.load('../data_sy/test/test_all_data_negative.npy')
    # test = np.load('../data_sy/train/train/train_all_data_negative.npy')
    # arr_num = test.shape[0]
    # arr = range(arr_num)
    # np.random.shuffle(arr)
    # test_label = np.zeros((test.shape[0], 3))
    # for t in test_label:
    #     t[0] = 1
    # print test_data.shape
    #
    model = load_model(model_save_path+'DNN_model_11_7.h5')
    y_pred = model.predict(get_data_batch(test_data), batch_size=500)
    # np.save('../data_sy/chuanglifang_predict_label.npy', y_pred)
    score = model.evaluate(get_data_batch(test_data),
                           test_label, batch_size=500)
    print y_pred.shape
    print test_label.shape
    right = 0
    n_1_1 = 0
    n_1_0 = 0
    n_0_1 = 0
    n_0_0 = 0

    for i in range(y_pred.shape[0]):
        if y_pred[i]>=0.5:
            y_pred[i] = 1
            if test_label[i]==1:
                n_1_1 += 1
                right += 1
            else:
                n_0_1 += 1
        else:
            y_pred[i] = 0
            if test_label[i] == 0:
                n_0_0 += 1
                right += 1
            else:
                n_1_0 += 1

    P = right*1.0/y_pred.shape[0]
    logging.info('acc: '+str(P))
    logging.info('real 1, pred 1 : '+str(n_1_1))
    logging.info('real 1, pred 0 : '+str(n_1_0))
    logging.info('real 0, pred 1 : '+str( n_0_1))
    logging.info('real 0, pred 0 : '+ str(n_0_0))
    logging.info('chazhunlv1: '+ str(n_1_1*1.0/(n_1_1+n_1_0)))
    logging.info('chazhunlv0: '+ str(n_0_0*1.0/(n_0_1+n_0_0)))
    logging.info('zhaohuilv1: '+ str(n_1_1*1.0/(n_1_1+n_0_1)))
    logging.info('zhaohuilv0: '+ str(n_0_0*1.0/(n_1_0+n_0_0)))
    # pred = np.argmax(y_pred, axis=-1)
    g_0 = 0
    g_0_r = 0
    g_1 = 0
    g_1_r = 0
    g_2 = 0
    g_2_r = 0
    g_3 = 0
    g_3_r = 0
    g_4 = 0
    g_4_r = 0
    g_5 = 0
    g_5_r = 0
    g_6 = 0
    g_6_r = 0
    for i in range(y_pred.shape[0]):

        if y_pred[i]>=0.5:
            y_pred[i] = 1
            if test_label[i] == 1:
                if test_data[i][1] == 0:
                    g_0 += 1
                    g_0_r += 1
                elif test_data[i][1] == 1:
                    g_1 += 1
                    g_1_r += 1
                elif test_data[i][1] == 2:
                    g_2 += 1
                    g_2_r += 1
                elif test_data[i][1] == 3:
                    g_3 += 1
                    g_3_r += 1
                elif test_data[i][1] == 4:
                    g_4 += 1
                    g_4_r += 1
                elif test_data[i][1] == 5:
                    g_5 += 1
                    g_5_r += 1
                else:
                    g_6 += 1
                    g_6_r += 1
            else:
                if test_data[i][1] == 0:
                    g_0 += 1
                elif test_data[i][1] == 1:
                    g_1 += 1
                elif test_data[i][1] == 2:
                    g_2 += 1
                elif test_data[i][1] == 3:
                    g_3 += 1
                elif test_data[i][1] == 4:
                    g_4 += 1
                elif test_data[i][1] == 5:
                    g_5 += 1
                else:
                    g_6 += 1
        else:
            y_pred[i] = 0
            if test_label[i] == 0:
                if test_data[i][1] == 0:
                    g_0 += 1
                    g_0_r += 1
                elif test_data[i][1] == 1:
                    g_1 += 1
                    g_1_r += 1
                elif test_data[i][1] == 2:
                    g_2 += 1
                    g_2_r += 1
                elif test_data[i][1] == 3:
                    g_3 += 1
                    g_3_r += 1
                elif test_data[i][1] == 4:
                    g_4 += 1
                    g_4_r += 1
                elif test_data[i][1] == 5:
                    g_5 += 1
                    g_5_r += 1
                else:
                    g_6 += 1
                    g_6_r += 1
            else:
                if test_data[i][1] == 0:
                    g_0 += 1
                elif test_data[i][1] == 1:
                    g_1 += 1
                elif test_data[i][1] == 2:
                    g_2 += 1
                elif test_data[i][1] == 3:
                    g_3 += 1
                elif test_data[i][1] == 4:
                    g_4 += 1
                elif test_data[i][1] == 5:
                    g_5 += 1
                else:
                    g_6 += 1
    if g_0 == 0:
        print 'P0 :', 0
    else:
        print 'P0 :', g_0_r * 1.0 / g_0, 'num: ', g_0
    if g_1 == 0:
        print 'P1 :', 0
    else:
        print 'P1 :', g_1_r * 1.0 / g_1, 'num: ', g_1
    if g_2 == 0:
        print 'P2 :', 0
    else:
        print 'P2 :', g_2_r * 1.0 / g_2, 'num: ', g_2
    if g_3 == 0:
        print 'P3 :', 0
    else:
        print 'P3 :', g_3_r * 1.0 / g_3, 'num: ', g_3
    if g_4 == 0:
        print 'P4 :', 0
    else:
        print 'P4 :', g_4_r * 1.0 / g_4, 'num: ', g_4
    if g_5 == 0:
        print 'P5 :', 0
    else:
        print 'P5 :', g_5_r * 1.0 / g_5, 'num: ', g_5
    if g_6 == 0:
        print 'P6 :', 0
    else:
        print 'P6 :', g_6_r * 1.0 / g_6, 'num: ', g_6
    arr = range(test_data.shape[0])
    np.random.shuffle(arr)
    # real = np.argmax(test_label, axis=-1)
    # print real.shape
    # temp = np.ones((y_pred.shape[0], 1))
    # print 'temp:', temp.shape
    # print 'pred :', y_pred[:, -1:].shape
    # temp = temp - y_pred[:, -1:]
    # print 'temp:', temp.shape
    # pr = np.column_stack((real, temp))
    # print 'pr : ', pr.shape
    # np.save('../result/roc.npy', pr)
    # result = np.row_stack((real, pred))
    # result = np.transpose(result)
    # tt.evaluate_result(result)
    # np.save('../result/result.npy', result)
    print 'pre:  ', y_pred[arr[20:38]].reshape((1, 18))
    print 'real: ', test_label[arr[20:38]].reshape((1, 18))
    # print model.metrics_names
    # print score
    # diff = pred - real
    # correct = diff[diff == 0].size
    # num = test_data.shape[0]
    # accu = correct / num
    # print accu


def main():
    #train_model()
    predict()

if __name__ == '__main__':
    main()
