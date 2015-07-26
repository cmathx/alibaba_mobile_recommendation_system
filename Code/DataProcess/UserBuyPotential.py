# __author__ = 'cjweffort'
# -*- coding: utf-8 -*-
import DataSplit

def userBuyAppetite(user_ori_file, type, id_position_map):
    fp_user_item = open(user_ori_file, 'r')
    user_item_map = {}
    # tag = True
    for line in fp_user_item:
        # if tag:
        #     tag = False
        #     continue
        words = line.split(',')
        if int(words[2]) == type and words[1] in id_position_map:
            user_item_map.setdefault(words[0], {})
            user_item_map[words[0]].setdefault(words[1], 0)
            user_item_map[words[0]][words[1]] += 1
    count_map = {}
    count_user_item_map = {}
    for user in user_item_map:
        for item, cnt in user_item_map[user].items():
            count_map.setdefault(cnt, 0)
            count_map[cnt] += 1
            count_user_item_map.setdefault(cnt, {})
            count_user_item_map[cnt].setdefault(user, set())
            count_user_item_map[cnt][user].add(item)
    # for cnt in count_map:
    #     print 'the number of behavior which occurs %d is %d' %(cnt, count_map[cnt])
    return count_map, count_user_item_map

if __name__ == '__main__':
    id_position_map = DataSplit.itemIDMap('../File/tianchi_mobile_recommend_train_item.csv')
    test_user_item_map, test_user_item_map_size = DataSplit.userOperate('../File/user_test_data.csv', 4, id_position_map)
    fp_behavior_occur_count = open('../File/AnalysisResult/behavior_occur_count.csv', 'w')
    total1 = 0
    for i in xrange(1, 5):
        fp_behavior_occur_count.write('behavior type is %d: \n' %i)
        count_map, count_user_item_map = userBuyAppetite('../File/user_train_data.csv', i, id_position_map)
        total = 0
        for cnt in count_map:
            # print count_map[cnt], len(count_user_item_map[cnt])
            bingos, test_set_num = DataSplit.computeRatio1(count_user_item_map[cnt], test_user_item_map)
            fp_behavior_occur_count.write('behavior occurs = %d, in train data(%d,%d,%.2lf), in test data(%d,%d,%.2lf)\n' \
                                          %(cnt, bingos, count_map[cnt], 100.0 * bingos / count_map[cnt], bingos, test_set_num, 100.0 * bingos / test_set_num))
            total += bingos
            # total1 += len(count_user_item_map[cnt])
        fp_behavior_occur_count.write('%d\n' %total)
        print i, total
        # fp_behavior_occur_count.write('\n')
        # for cnt in count_map:
        #     fp_behavior_occur_count.write('%d,' %count_map[cnt])
        # fp_behavior_occur_count.write('\n')
    print total1
