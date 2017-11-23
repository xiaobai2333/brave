from keras.layers.core import Dense, Lambda, Activation
from keras.regularizers import l2
from keras.layers import Embedding, Input, Dense, Flatten, Dropout
from keras.layers.normalization import BatchNormalization
from keras.layers.merge import concatenate, dot
from keras.optimizers import Adagrad, Adam, SGD, RMSprop
from keras.models import Sequential, Model
import time
from src_one.properties import padding_num, model_save_path
from keras import backend as K
model_name = 'DNN_model_11_7.h5'
num1 = padding_num
coach_history_num = num1
store_history_num = num1
class_history_num = num1
hour_history_num = num1
week_history_num = num1


def build_model(nums=[5000, 500, 1500, 16, 7],
                out_embedding=[16, 16, 16, 8, 8],
                reg_embedding=[0.000, 0.000, 0.000, 0.00, 0.000, 0.00, 0.0, 0.0],
                mlp_layers=[2048, 1024, 512, 256, 64],
                # mlp_layers=[1024, 512, 256],
                mlp_reg=[0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.00, 0.000]):
    num_coaches = nums[0]
    num_store = nums[1]
    num_classes = nums[2]
    num_hours = nums[3]
    num_weeks = nums[4]
    num_layers = len(mlp_layers)        # Number of layers in the MLP

    # ====================== Input user basic data  ===============================================================
    user_basic = Input(shape=(5,), dtype='float32', name='user_basic')

    # ======================= coach embedding ========================================================
    coach_embedding = Embedding(input_dim=num_coaches, output_dim=out_embedding[0], name='coach_embedding',
                                embeddings_regularizer=l2(reg_embedding[0]), input_length=None)

    # =======================Input user coach history=====================================================
    user_coach_history = Input(shape=(coach_history_num,), dtype='int32', name='user_coach_history')
    user_coach_history_embedding = coach_embedding(user_coach_history)

    # ====================== Input user coach history weight =============================================
    user_coach_weight = Input(shape=(1, coach_history_num,), dtype='float32', name='user_coach_weight')

    # ======================= user coach history averge =================================================
    user_coach_history_averge = dot([user_coach_weight, user_coach_history_embedding], axes=(2, 1))
    user_coach_history_flatten = Flatten()(user_coach_history_averge)

    # ======================= store embedding ========================================================
    store_embedding = Embedding(input_dim=num_store, output_dim=out_embedding[1], name='store_embedding',
                                embeddings_regularizer=l2(reg_embedding[1]), input_length=None)

    # =======================Input user store history=====================================================
    user_store_history = Input(shape=(store_history_num,), dtype='int32', name='user_store_history')
    user_store_history_embedding = store_embedding(user_store_history)

    # ====================== Input user store history weight =============================================
    user_store_weight = Input(shape=(1, store_history_num,), dtype='float32', name='user_store_weight')

    # ======================= user store history averge =================================================
    user_store_history_averge = dot([user_store_weight, user_store_history_embedding], axes=(2, 1))
    user_store_history_flatten = Flatten()(user_store_history_averge)

    # ======================= class embedding ========================================================
    class_embedding = Embedding(input_dim=num_classes, output_dim=out_embedding[2], name='class_embedding',
                                embeddings_regularizer=l2(reg_embedding[2]), input_length=None)

    # =======================Input user class history=====================================================
    user_class_history = Input(shape=(class_history_num,), dtype='int32', name='user_class_history')
    user_class_history_embedding = class_embedding(user_class_history)

    # ====================== Input user class history weight =============================================
    user_class_weight = Input(shape=(1, class_history_num,), dtype='float32', name='user_class_weight')

    # ======================= user class history averge =================================================
    user_class_history_averge = dot([user_class_weight, user_class_history_embedding], axes=(2, 1))
    user_class_history_flatten = Flatten()(user_class_history_averge)

    # ======================= hours embedding ========================================================
    hour_embedding = Embedding(input_dim=num_hours, output_dim=out_embedding[3], name='hour_embedding',
                                embeddings_regularizer=l2(reg_embedding[3]), input_length=None)

    # =======================Input user hour history=====================================================
    user_hour_history = Input(shape=(hour_history_num,), dtype='int32', name='user_hour_history')
    user_hour_history_embedding = hour_embedding(user_hour_history)

    # ====================== Input user hour history weight =============================================
    user_hour_weight = Input(shape=(1, hour_history_num,), dtype='float32', name='user_hour_weight')

    # ======================= user hour history averge =================================================
    user_hour_history_averge = dot([user_hour_weight, user_hour_history_embedding], axes=(2, 1))
    user_hour_history_flatten = Flatten()(user_hour_history_averge)

    # ======================= week embedding ========================================================
    week_embedding = Embedding(input_dim=num_weeks, output_dim=out_embedding[4], name='week_embedding',
                                embeddings_regularizer=l2(reg_embedding[4]), input_length=None)

    # =======================Input user week history=====================================================
    user_week_history = Input(shape=(week_history_num,), dtype='int32', name='user_week_history')
    user_week_history_embedding = week_embedding(user_week_history)

    # ====================== Input user week history weight =============================================
    user_week_weight = Input(shape=(1, week_history_num,), dtype='float32', name='user_week_weight')

    # ======================= user week history averge =================================================
    user_week_history_averge = dot([user_week_weight, user_week_history_embedding], axes=(2, 1))
    user_week_history_flatten = Flatten()(user_week_history_averge)

    # ====================== Input user weekdayP data  ===============================================================
    user_weekdayp = Input(shape=(1,), dtype='float32', name='user_weekdayp')

    # ====================== Input user weekdayP data  ===============================================================
    user_hourp = Input(shape=(1,), dtype='float32', name='user_hourp')

    # ======================= input class ids =========================================================
    class_id = Input(shape=(1,), dtype='int32', name='class_id')

    # ======================= class id embedding ======================================================
    class_em = class_embedding(class_id)

    # ======================= class id flatten ========================================================
    class_id_flatten = Flatten()(class_em)

    # ======================= input store id ============================================================
    store_id = Input(shape=(1,), dtype='int32', name='store_id')

    # ======================= store embedding ========================================================
    store_id_embedding = store_embedding(store_id)

    # ====================== store flatten ===========================================================
    store_id_flatten = Flatten()(store_id_embedding)

    # ====================== input coach id ============================================================
    coach_id = Input(shape=(1,), dtype='int32', name='coach_id')

    # ====================== coach embedding ===========================================================
    coach_id_embedding = coach_embedding(coach_id)
    # ====================== coach flatten ============================================================
    coach_id_flatten = Flatten()(coach_id_embedding)

    # ====================== input hour id ============================================================
    hour_id = Input(shape=(1,), dtype='int32', name='hour_id')

    # ====================== hour embedding ===========================================================
    hour_id_embedding = hour_embedding(hour_id)
    # ====================== hour flatten ============================================================
    hour_id_flatten = Flatten()(hour_id_embedding)

    # ====================== input week id ============================================================
    week_id = Input(shape=(1,), dtype='int32', name='week_id')

    # ====================== week embedding ===========================================================
    week_id_embedding = week_embedding(week_id)
    # ====================== week flatten ============================================================
    week_id_flatten = Flatten()(week_id_embedding)

    # ======================= input class basic imformation  ============================================
    # class_basic = Input(shape=(1,), dtype='float32', name='class_basic')

    # ====================== concatenate feature ===========================================================
    vector = concatenate([user_basic, user_coach_history_flatten, user_store_history_flatten, user_class_history_flatten,
                          user_hour_history_flatten, user_week_history_flatten,
                          user_weekdayp, user_hourp, class_id_flatten, store_id_flatten, coach_id_flatten, hour_id_flatten, week_id_flatten])
    # vector = concatenate(
    #     [user_basic, user_coach_history_flatten, user_store_history_flatten, user_class_history_flatten,
    #      user_weekdayp, class_id_flatten, store_id_flatten, coach_id_flatten])

    # ====================== MLP layers ======================================================================
    for idx in range(0, num_layers):
        bn = BatchNormalization()
        vector = bn(vector)
        layer = Dense(units=mlp_layers[idx], kernel_regularizer=l2(mlp_reg[idx]), name='layer%d' % (idx+1))
        vector = layer(vector)
        activation = Activation(activation='relu')
        vector = activation(vector)
        # dropout = Dropout(0.1)
        # vector = dropout(vector)

    # ===================== Final prediction layer ===========================================================
    # prediction = Dense(3, activation='softmax', name='prediction')(vector)
    prediction = Dense(1, activation='sigmoid', name='prediction')(vector)
    # ===================== Model build ======================================================================
    model = Model(input=[user_basic, user_coach_history, user_coach_weight, user_store_history, user_store_weight,
                         user_class_history, user_class_weight, user_hour_history, user_hour_weight, user_week_history, user_week_weight,
                         user_weekdayp, user_hourp, class_id, store_id, coach_id, hour_id, week_id],
                  output=prediction)
    # model = Model(input=[user_basic, user_coach_history, user_coach_weight, user_store_history, user_store_weight,
    #                      user_class_history, user_class_weight, user_weekdayp, class_id, store_id, coach_id],
    #               output=prediction)
    print model.summary()
    return model
    # ========================================================================================================


def compile_model(model, learning_rate, momentum, decay):
    # sgd = SGD(lr=learning_rate, momentum=momentum, decay=decay, nesterov=True)
    # model.compile(optimizer=sgd, loss='categorical_crossentropy', metrics=['accuracy'])
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    print 'model build successed...'
    return model


def train_model(model, train_data, train_label, batch, epoch, validation_split):
    start_time = time.clock()
    model.fit(train_data, train_label, batch_size=batch, epochs=epoch, validation_split=validation_split)
    end_time = time.clock()
    train_time = end_time-start_time
    print "model training successed, use time: ", train_time
    model.save(model_save_path+model_name)
    return model
