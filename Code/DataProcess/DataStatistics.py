# __author__ = 'cjweffort'
# -*- coding: utf-8 -*-

import DataSplit

def UserFocusCategory():
    fp_total_data = open('../File/tianchi_mobile_recommend_train_user.csv', 'r')
    user_category_map = {}
    tag = True
    for line in fp_total_data:
        if tag:
            tag = False
            continue
        words = line.split(',')
        if int(words[2]) == 4:
            user_category_map.setdefault(words[0], set())
            user_category_map[words[0]].add(words[4])
    return user_category_map

def ItemInformationAnalysis(item_file):
    fp_item_data = open(item_file, 'r')
    category_item_map = {}
    item_geohash_map = {}
    tag = True
    for line in fp_item_data:
        if tag:
            tag = False
            continue
        words = line.split(',')
        category_item_map.setdefault(words[2], set())
        category_item_map[words[2]].add(words[0])
        item_geohash_map.setdefault(words[0], set())
        item_geohash_map[words[0]].add(words[1])
    return category_item_map, item_geohash_map

def compute(map_set):
    total_cnt = 0
    cnt = 0
    min_cnt = 100000
    max_cnt = -1
    for element in map_set:
        if len(map_set[element]) < min_cnt:
            min_cnt = len(map_set[element])
        if len(map_set[element]) > max_cnt:
            max_cnt = len(map_set[element])
        if(len(map_set[element]) != 0):
            cnt += 1
        total_cnt += len(map_set[element])
    print 'cnt = %d, total_cnt = %d' %(cnt, total_cnt)
    print 'min, max, avg are %d, %d, %.2lf' %(min_cnt, max_cnt, 1.0 * total_cnt / cnt)

#提取出所有的item信息
def extractItemInformation():
    fp_data = open('../File/tianchi_mobile_recommend_train_user.csv', 'r')
    category_item_set = {}
    item_geohash_set = {}
    tag = True
    for line in fp_data:
        if tag:
            tag = False
            continue
        words = line.split(',')
        category_item_set.setdefault(words[4], set())
        category_item_set[words[4]].add(words[1])
        item_geohash_set.setdefault(words[1], set())
        item_geohash_set[words[1]].add(words[3])
    fp_item_info = open('../File/tianchi_mobile_recommend_train_total_item.csv', 'w')
    fp_item_info.write('item_id,item_geohash,item_category\n')
    for category in category_item_set:
        for item in category_item_set[category]:
            for geohash in item_geohash_set[item]:
                fp_item_info.write('%s,%s,%s\n' %(item, geohash, category))
    return category_item_set, item_geohash_set

#计算缺失的geohash数量
def positionHash(item_id_geohash_map):
    print len(item_id_geohash_map)
    cnt = 0
    hash_length_map = {}
    for item in item_id_geohash_map:
        if len(item_id_geohash_map[item]) == 0:
            cnt += 1
        for geohash in item_id_geohash_map[item]:
            # print len(geohash)
            hash_length_map.setdefault(len(geohash), 0)
            hash_length_map[len(geohash)] += 1
    print cnt
    for hash_length, cnt1 in hash_length_map.items():
        print hash_length, cnt1

def userPosition():
    fp_data = open('../File/tianchi_mobile_recommend_train_user.csv', 'r')
    user_position_set = {}
    tag = True
    for line in fp_data:
        if tag:
            tag = False
            continue
        words = line.split(',')
        user_position_set.setdefault(words[0], set())
        user_position_set[words[0]].add(words[3])
    return user_position_set

# def distance(dis1, dis):


#计算用户总数量，item总数量，
#对于商品子集而言，用户总数量，item总数量，
#用户关注的category
#关注位置hash值(user位置，item位置)

if __name__ == '__main__':
    # id_position_map = DataSplit.itemIDMap('../File/tianchi_mobile_recommend_train_item.csv')
    # user_set, item_set, category_set = DataSplit.userAndItemList('../File/tianchi_mobile_recommend_train_user.csv', 0, id_position_map)
    # print 'number of users, item and category are %d %d %d' %(len(user_set), len(item_set), len(category_set))
    # user_category_set = UserFocusCategory()
    category_item_set, item_geohash_set = ItemInformationAnalysis('../File/tianchi_mobile_recommend_train_item.csv')
    compute(category_item_set)
    compute(item_geohash_set)
    # category_item_total_set, item_geohash_total_set = extractItemInformation()
    # positionHash(item_geohash_set)
    user_position_set = userPosition()
    compute(user_position_set)
