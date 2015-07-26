# __author__ = 'cjweffort'
# -*- coding: utf-8 -*-

#获取用户最经常呆的位置(只精确到（4.9km x 4.9km）范围)
def getUserOftenPostion(file_name):
    user_often_postion = {}
    for line in open(file_name, 'r'):
        words = line.split(',')
        user_id = words[0]
        user_geohash = words[3]
        if len(user_geohash) != 0:
            user_often_postion.setdefault(user_id, [user_geohash[0:5], 1])
            if user_often_postion[user_id][1] == 0:
                user_often_postion[user_id][0] = user_geohash[0:5]
                user_often_postion[user_id][1] = 1
            else:
                if user_often_postion[user_id][0] == user_geohash[0:5]:
                    user_often_postion[user_id][1] += 1
                else:
                    user_often_postion[user_id][1] -= 1
    return user_often_postion

#用户当天的的位置信息由当天所在的最多的位置决定
#用户当天没有被定位到，则位置由一个月所在的最多的位置决定
#用户从来没有被定位到，则由所买的item的位置决定
def completeUserPositionInfo():
    rootDir = '../File/EverydayData/'
    days = 0
    import os
    complete_total_user_file_name = '../File/train_user_combine_everyday_complete_by_userInfo.csv'
    fp_complete_total_user_data = open(complete_total_user_file_name, 'w')
    for file_name in os.listdir(rootDir):
        file_path = os.path.join(rootDir, file_name)
        print 'start to proceed', file_path
        user_often_positon_map = getUserOftenPostion(file_path)
        print len(user_often_positon_map)
        complete_user_file_name = '../File/CompleteEverydayData/complete_by_userInfo/%02d.csv' %days
        days += 1
        fp_complete_user_data = open(complete_user_file_name, 'w')
        for line in open(file_path, 'r'):
            words = line.split(',')
            if len(words[3]) != 0 or (len(words[3]) == 0 and words[0] not in user_often_positon_map):
                fp_complete_user_data.write('%s' %line)
                fp_complete_total_user_data.write('%s' %line)
            else:
                fp_complete_user_data.write('%s,%s,%s,%s,%s,%s' %(words[0], words[1], words[2],
                                                                  user_often_positon_map[words[0]][0], words[4], words[5]))
                fp_complete_total_user_data.write('%s,%s,%s,%s,%s,%s' %(words[0], words[1], words[2],
                                                                  user_often_positon_map[words[0]][0], words[4], words[5]))
    user_often_positon_map = getUserOftenPostion('../File/train_user_combine_everyday_complete_by_userInfo.csv')
    fp_complete_total_user_data = open('../File/train_user_complete_by_userInfo.csv', 'w')
    for line in open('../File/train_user_combine_everyday_complete_by_userInfo.csv', 'r'):
            words = line.split(',')
            if len(words[3]) != 0 or (len(words[3]) == 0 and words[0] not in user_often_positon_map):
                fp_complete_total_user_data.write('%s' %line)
            else:
                fp_complete_total_user_data.write('%s,%s,%s,%s,%s,%s' %(words[0], words[1], words[2],
                                                                  user_often_positon_map[words[0]][0], words[4], words[5]))