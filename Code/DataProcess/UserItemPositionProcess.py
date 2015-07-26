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
    for file_name in os.listdir(rootDir):
        file_path = os.path.join(rootDir, file_name)
        print 'start to proceed', file_path
        user_often_positon_map = getUserOftenPostion(file_path)
        print len(user_often_positon_map)
        complete_user_file_name = '../File/CompleteEverydayData/complete_%02d.csv' %days
        days += 1
        fp_complete_user_data = open(complete_user_file_name, 'w')
        for line in open(file_path, 'r'):
            words = line.split(',')
            if len(words[3]) != 0 or (len(words[3]) == 0 and words[0] not in user_often_positon_map):
                fp_complete_user_data.write('%s' %line)
            else:
                fp_complete_user_data.write('%s,%s,%s,%s,%s,%s' %(words[0], words[1], words[2],
                                                                  user_often_positon_map[words[0]][0], words[4], words[5]))

def getNoPositionUserInfo(file_name):
    not_position_user_set = set()
    for line in open(file_name, 'r'):
        words = line.split(',')
        if len(words[3]) == 0:
            not_position_user_set.add(words[0])
    print len(not_position_user_set)
    fp_lack_user_info =  open('../File/CompleteEverydayData/lackPositionUser.csv', 'w')
    for line in open(file_name, 'r'):
        words = line.split(',')
        if words[0] in not_position_user_set:
            fp_lack_user_info.write('%s' %line)

#填补从未被定为的item的位置，利用user发生交互行为最多的位置来决定(只精确到（4.9km x 4.9km）范围)
def createItemPossiblePositionReverseTable(no_position_item_id_subset):
    no_position_item_user_reverse_table = {}
    for line in open('../File/tianchi_mobile_recommend_train_user.csv', 'r'):
        words = line.split(',')
        user_id = words[0]
        item_id = words[1]
        behavior_type = words[2]
        user_geohash = words[3]
        item_category = words[4]
        time = words[5]
        if item_id in no_position_item_id_subset:# and len(user_geohash) != 0:
            no_position_item_user_reverse_table.setdefault(item_id, [user_geohash[0:5], 1])
            if no_position_item_user_reverse_table[item_id][1] == 0:
                no_position_item_user_reverse_table[item_id][0] = user_geohash[0:5]
                no_position_item_user_reverse_table[item_id][1] = 1
            else:
                if no_position_item_user_reverse_table[item_id][0] == user_geohash[0:5]:
                    no_position_item_user_reverse_table[item_id][1] += 1
                else:
                    no_position_item_user_reverse_table[item_id][1] -= 1
    return no_position_item_user_reverse_table

def distance(pos1, pos2):
    for i in xrange(0, len(pos1)):
        if pos1[i] != pos2[i]:
            return i
    return 7

def computeUserItemDistance(user_position, item_position_list):
    # if len(user_position) == 0:

    # if len(item_position_map) == 0:

    min = 8
    minGeohash = ''
    for item_position in item_position_list:
        if distance(user_position, item_position) < min:
            min = distance(user_position, item_position)
            minGeohash = item_position
    return min, minGeohash

#如果isNotPostion是True，则返回没有被定位到的item集合
#否则，返回有被定位到的item集合
def getItemPositionMap(file_name, isNotPosition):
    position_item_subset = set()
    flag = True
    for line in open(file_name, 'r'):
        if flag:
            flag = False
            continue
        words = line.split(',')
        if len(words[1]) != 0:
            position_item_subset.add(words[0])
    flag = True
    item_position_map = {}
    for line in open(file_name, 'r'):
        if flag:
            flag = False
            continue
        words = line.split(',')
        if (len(words[1]) == 0) is isNotPosition:
            if isNotPosition is False or ((isNotPosition is True) and words[0] not in position_item_subset):
                item_position_map.setdefault(words[0], set())
                item_position_map[words[0]].add(words[1])
    return item_position_map

def computeUserItemPosition(file_name, position_item_subset, no_position_item_subset):
    fp_complete_item_position_total_data = open('../File/complete_addDistance_train_user.csv', 'w')
    fp_complete_item_position_total_data.write('user_id,item_id,behavior_type,user_geohash,item_geohash,user_item_distance,item_category,time\n')
    flag = True
    for line in open(file_name, 'r'):
        if flag:
            flag = False
            continue
        words = line.split(',')
        user_id = words[0]
        item_id = words[1]
        behavior_type = words[2]
        user_geohash = words[3]
        item_category = words[4]
        time = words[5]
        #user_geohash缺失
        #user_geohash未缺失，
        if item_id in position_item_subset:
            user_item_distance, item_geohash = computeUserItemDistance(user_geohash, item_position_map[item_id])
            fp_complete_item_position_total_data.write('%s,%s,%s,%s,%s,%s,%s,%s' \
                                                   %(user_id, item_id, behavior_type, user_geohash, item_geohash, user_item_distance, item_category, time))
        else:
            fp_complete_item_position_total_data.write('%s,%s,%s,%s,,,%s,%s' \
                                                       %(user_id, item_id, behavior_type, user_geohash, item_category, time))

if __name__ == '__main__':
    # completeUserPositionInfo()
    # getNoPositionUserInfo('../File/CompleteEverydayData/complete_train_user.csv')
    #position_item_subset: item - (position1, position2, ..., position n)
    position_item_subset = getItemPositionMap('../File/tianchi_mobile_recommend_train_item.csv', False)
    print len(position_item_subset)
    no_position_item_subset = getItemPositionMap('../File/tianchi_mobile_recommend_train_item.csv', True)
    print len(no_position_item_subset)
    #no_position_item_subset: item - (position, cnt)
    no_position_item_subset = createItemPossiblePositionReverseTable(no_position_item_subset)
    print len(no_position_item_subset)
    # computeUserItemPosition('../File/CompleteEverydayData/complete_train_user.csv', position_item_subset, no_position_item_subset)