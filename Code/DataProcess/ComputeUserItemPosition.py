# __author__ = 'cjweffort'
# -*- coding: utf-8 -*-

from GetItemPossiblePosition import *
from CompleteUserPosition import *

def getNoPositionUserInfo(file_name):
    not_position_user_set = set()
    for line in open(file_name, 'r'):
        words = line.split(',')
        if len(words[3]) == 0:
            not_position_user_set.add(words[0])
    print 'the number of users with no position:%d' %(len(not_position_user_set))
    fp_lack_user_info =  open('../File/lackPositionUser.csv', 'w')
    for line in open(file_name, 'r'):
        words = line.split(',')
        if words[0] in not_position_user_set:
            fp_lack_user_info.write('%s' %line)

def distance(pos1, pos2):
    if len(pos1) == 0 or len(pos2) == 0:
        return -1
    # print '%d %d' %(len(pos1), len(pos2))
    for i in xrange(0, 5):
        if pos1[i] != pos2[i]:
            return i
    return 5

def computeUserItemDistance(user_position, item_position_list):
    #用户位置信息、所购买的商品位置列表信息为空，则不进行处理，用户和商品的距离依然保持为空
    if len(user_position) == 0:
        return -1
    if len(item_position_list) == 0:
        return -1
    min = 8
    minGeohash = ''
    for item_position in item_position_list:
        if distance(user_position, item_position) < min:
            min = distance(user_position, item_position)
            minGeohash = item_position
    return min, minGeohash

def computeUserItemPosition(file_name, item_position_map):
    fp_complete_item_position_total_data = open('../File/complete_addDistance_train_user.csv', 'w')
    fp_complete_item_position_total_data.write('user_id,item_id,behavior_type,user_geohash,item_geohash,user_item_distance,item_category,time\n')
    cnt = 0
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
        if len(user_geohash) != 0 and item_id in item_position_map and len(item_position_map[item_id]) != 0:#用户位置信息不为空，商品线下位置信息不全部为空，用户商品位置可以计算
            user_item_distance, item_geohash = computeUserItemDistance(user_geohash, item_position_map[item_id])
            fp_complete_item_position_total_data.write('%s,%s,%s,%s,%s,%d,%s,%s' \
                                                   %(user_id, item_id, behavior_type, user_geohash, item_geohash, user_item_distance, item_category, time))
            cnt += 1
        else:
            fp_complete_item_position_total_data.write('%s,%s,%s,%s,,,%s,%s' \
                                                       %(user_id, item_id, behavior_type, user_geohash, item_category, time))
    print 'no-mission position records: %d' %cnt

if __name__ == '__main__':
    #利用商品位置信息补全用户位置信息

    #positing_item_position_map: item - (position1, position2, ..., position n)
    #利用用户位置信息补全商品位置信息
    positing_item_position_map = getItemPositionMap('../File/tianchi_mobile_recommend_train_item.csv', False)
    print len(positing_item_position_map)
    no_positing_item_position_map = getItemPositionMap('../File/tianchi_mobile_recommend_train_item.csv', True)
    print len(no_positing_item_position_map)
    #no_position_item_subset: item - (position, cnt)
    no_positing_item_position_map = createItemPossiblePositionReverseTable('../File/tianchi_mobile_recommend_train_user.csv', no_positing_item_position_map)
    print len(no_positing_item_position_map)
    item_position_map = combineItemPosition(positing_item_position_map, no_positing_item_position_map)
    #利用用户位置信息补全用户缺失的位置信息
    #用户当天所在位置是唯一的，根据当天已有的位置信息补全缺失的位置信息
    completeUserPositionInfo()
    #../File/train_user_complete_by_userInfo.csv - 利用用户位置信息补全后用户详细信息
    getNoPositionUserInfo('../File/train_user_complete_by_userInfo.csv')
    computeUserItemPosition('../File/train_user_complete_by_userInfo.csv', item_position_map)