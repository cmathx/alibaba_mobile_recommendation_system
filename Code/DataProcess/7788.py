# __author__ = 'cjweffort'
# -*- coding: utf-8 -*-
from DataSplit import *

def extractFinalCartBehavior(file, id_position_map, filter_user_item):
    fp_final_cart_behavior = open('../File/FinalWeekCartRecommend.csv', 'w')
    fp_final_cart_behavior.write('user_id,item_id\n')
    final_cart_map = {}
    tag = True
    filter_num = 0
    for line in open(file, 'r'):
        if tag:
            tag = False
            continue
        words = line.split(',')
        if words[1] in id_position_map and int(words[2]) == 3 and \
                (words[5] >= '2014-12-18 20' or words[5] == '2014-12-18 00'):
            final_cart_map.setdefault(words[0], set())
            if (words[0] in filter_user_item and words[1] in filter_user_item[words[0]]) == False:
                final_cart_map[words[0]].add(words[1])
            else:
                filter_num += 1
    print 'filter number = %d' %filter_num
    for user_id in final_cart_map:
        for item_id in final_cart_map[user_id]:
            fp_final_cart_behavior.write('%s,%s\n' %(user_id, item_id))
    return final_cart_map

if __name__ == '__main__':
    item_id_subset = itemIDMap('../File/tianchi_mobile_recommend_train_item.csv')
    buy_user_item, buy_user_item_size = userOperate('../File/tianchi_mobile_recommend_train_user.csv', 4, item_id_subset, True)
    final_cart_map = extractFinalCartBehavior('../File/tianchi_mobile_recommend_train_user.csv', item_id_subset, buy_user_item)
    # test_user_item_buy_set, test_user_item_buy_set_size = userOperate('../File/EverydayData/00.csv', 4, item_id_subset)
    # computeRatio1(test_user_item_buy_set, final_cart_map)