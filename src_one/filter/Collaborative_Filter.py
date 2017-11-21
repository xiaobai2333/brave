# -*-coding=utf-8 -*-

import math
import ReadData

# 计算余弦距离
def getCosDist(user1, user2):
    sum_x = 0.0
    sum_y = 0.0
    sum_xy = 0.0
    for key in user1:
        if key in user2:
            sum_x += user1[key] * user1[key]
            sum_y += user2[key] * user2[key]
            sum_xy += user1[key] * user2[key]

    for key1 in user1:
        if key1 not in user2:
            sum_x += user1[key1] * user1[key1]

    for key2 in user2:
        if key2 not in user1:
            sum_y += user2[key2] * user2[key2]


    if sum_xy == 0.0:
        return 0
    demo = math.sqrt(sum_x * sum_y)
    return sum_xy / demo

# 生成课程-用户字典
def getItemUserMap(userDict):
    itemUser = {}
    for user in userDict:
        user_classId_dict = userDict[user]

        for class_Id in user_classId_dict:
            if class_Id in itemUser:
                itemUser[class_Id].append(user)
            else:
                itemUser[class_Id] = [user]
    return itemUser


# 计算与指定用户最相近的邻居
def recommendByUserFC(userDict,itemUser, userId, k=10):

    # 找邻居
    neighbors = getNearestNeighbor(userId, userDict, itemUser)[:k]
    # print '他的neighbors : '
    # print neighbors
    # print 'neighbors:'
    # for neighbor in neighbors:
    #     print 'classID : ', userDict[neighbor[1]]
    # 建立推荐字典
    recommand_dict = {}
    for neighbor in neighbors:

        user_classId = userDict[neighbor[1]]
        for classId in user_classId:
            if classId not in recommand_dict:
                recommand_dict[classId] = neighbor[0]
            else:
                recommand_dict[classId] += neighbor[0]

                # 建立推荐列表
    recommand_list = []
    for key in recommand_dict:
        recommand_list.append([recommand_dict[key], key])
    recommand_list.sort(reverse=True)
    return recommand_list


# 使用UserFC进行推荐，输入：文件名,用户ID,邻居数量
def getNearestNeighbor(userId, userDict, itemUser):
    neighbors = []
    for item in userDict[userId]:
        for neighbor in itemUser[item]:
            if neighbor != userId and neighbor not in neighbors:
                neighbors.append(neighbor)
    neighbors_dist = []

    for neighbor in neighbors:
        dist = getCosDist(userDict[userId], userDict[neighbor])
        neighbors_dist.append([dist, neighbor])
    neighbors_dist.sort(reverse=True)

    return neighbors_dist


def test():
    appointMap = ReadData.getAppointMap()
    for user in appointMap:
        lastestTime = ReadData.get_user_lastest_time(user,appointMap)
        userDict = ReadData.get_recent_user_classId_Dict(lastestTime, appointMap)

        itemUser = getItemUserMap(userDict)
        print 'userID : ',user
        print 'his classID : ',userDict[user]
        print recommendByUserFC(userDict, itemUser, user, 8)


# 从这里开始运行
if __name__ == '__main__':
    test()

