# __author__ = 'cjweffort'
# -*- coding: utf-8 -*-

def countPositionBehavior(user_data_file, position_file, position_count_file, is_user_position):
    user_data = []
    fp_user_position = open(position_file, 'w')
    fp_user_position_count = open(position_count_file, 'w')
    user_position_map = {}
    for line in open(user_data_file, 'r'):
        words = line.split(',')
        user_id = words[0]
        if is_user_position:
            user_geohash = words[3]
        else:
            user_geohash = words[1]
        user_position_map.setdefault(user_id, set())
        user_position_map[user_id].add(user_geohash[0:5])
    for user_id in user_position_map:
        fp_user_position_count.write('%d\n' %(len(user_position_map[user_id])))
        for user_geohash in user_position_map[user_id]:
            user_data.append([user_id, user_geohash])
    user_data.sort(key=lambda  l:(l[0]), reverse=True)
    for tup in user_data:
        # if len(tup[1]) == 0:
        #     continue
        tag = True
        for ele in tup:
            if tag:
                tag = False
                fp_user_position.write('%s' %(ele))
            else:
                fp_user_position.write(' %s' %(ele))
        fp_user_position.write('\n')

def sortByUserTime(user_data_file):
    user_data = []
    for line in open(user_data_file, 'r'):
        words = line.split(',')
        user_id = words[0]
        user_position = words[3]
        user_data.append([user_id, user_position])
    user_data.sort(key=lambda l:(l[0]), reverse=True)
    fp_user_time = open('../File/sort_user_time_data.csv', 'w')
    for tup in user_data:
        fp_user_time.write('%s,%s\n' %(tup[0], tup[1]))

if __name__ == '__main__':
    # countPositionBehavior('../File/tianchi_mobile_recommend_train_user.csv', '../File/userPosition.csv',
    #                      '../File/userPositionCount.csv', True)
    # countPositionBehavior('../File/tianchi_mobile_recommend_train_item.csv', '../File/itemPosition.csv',
    #                       '../File/itemPositionCount.csv', False)
    sortByUserTime('../File/tianchi_mobile_recommend_train_user.csv')
