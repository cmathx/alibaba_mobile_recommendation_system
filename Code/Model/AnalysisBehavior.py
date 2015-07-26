# __author__ = 'cjweffort'
# -*- coding: utf-8 -*-

def drawBehaviorMap(user_item_base_map, is_positive, positive_sample_num, negative_sample_num):
    # from PIL import Image
    if is_positive == 1:
        if positive_sample_num == 79:
            fp_user_item_behavior = open('positiveUserBehavior.csv', 'w')
        else:
            fp_user_item_behavior = open('positiveUserBehavior1.csv', 'w')
            # image = Image.new("RGB", (29 * 4, positive_sample_num))
    else:
        if negative_sample_num == 9497:
            fp_user_item_behavior = open('negativeUserBehavior.csv', 'w')
        else:
            fp_user_item_behavior = open('negativeUserBehavior1.csv', 'w')
            # image = Image.new("RGB", (29 * 4, negative_sample_num))
    watch_map = []
    is_ever_buy = {}
    for user_id in user_item_base_map:
        for item_id in user_item_base_map[user_id]:
            tag = False
            for i in xrange(0, 29):
                if user_item_base_map[user_id][item_id][i * 4 + 2] == 1 and user_item_base_map[user_id][item_id][i * 4 + 1] == 0 and \
                        user_item_base_map[user_id][item_id][i * 4 + 3] == 0:
                    tag = True
                    break
            if tag == True:
                is_ever_buy.setdefault(user_id, set())
                is_ever_buy[user_id].add(item_id)
    i = 0
    for user_id in user_item_base_map:
        for item_id in user_item_base_map[user_id]:
            if user_item_base_map[user_id][item_id][29 * 4 + 3] == is_positive and user_id in is_ever_buy and item_id in is_ever_buy[user_id]:
                ele = ''
                for j in xrange(0, 29 * 4):
                    if user_item_base_map[user_id][item_id][j] != 0:
                        ele += '1'
                        # image.putpixel([j, i], (0, 0, 0))
                    else:
                        ele += ' '
                        # image.putpixel([j, i], (255, 255, 255))
                i += 1
                watch_map.append(ele)
    watch_map.sort(reverse=True)
    fp_user_item_behavior.write('01  02  03  04  05  06  07  08  09  10  11  12  13  14  15  16  17  18  19  20  21  22  23  24  25  26  27  28  29  30\n')
    for ele in watch_map:
        fp_user_item_behavior.write('%s\n' %ele)
        # image.show()
        # if is_positive == 1:
        #     if positive_sample_num == 79:
        #         image.save('../File/PositiveUserBehaviorMap.png')
        #     else:
        #         image.save('../File/PositiveUserBehaviorMap1.png')
        # else:
        #     if negative_sample_num == 9497:
        #         image.save('../File/NegativeUserBehaviorMap.png')
        #     else:
        #         image.save('../File/NegativeUserBehaviorMap1.png')

def printSampleProcess(feature, is_positive, output_file_name):
    user_item_pair = {}
    cnt = 0
    for user_id in feature:
        for item_id in feature[user_id]:
            if feature[user_id][item_id][0] == is_positive and \
                            feature[user_id][item_id][29 + 28 * 4 + 1] == 1 and feature[user_id][item_id][29 + 28 * 4 + 3] == 1 and \
                            feature[user_id][item_id][29 + 28 * 4 + 2] == 0 and feature[user_id][item_id][29 + 28 * 4 + 4] == 0:
                user_item_pair.setdefault(user_id, set())
                user_item_pair[user_id].add(item_id)
                cnt += 1
    print cnt
    fp_positive_buy_process = open(output_file_name, 'w')
    buy_process_list = []
    for line in open('../File/tianchi_mobile_recommend_train_user.csv'):
        words = line.split(',')
        if words[0] in user_item_pair and words[1] in user_item_pair[words[0]]:
            buy_process_list.append([words[0],words[1],words[2],words[3],words[4],words[5]])
    buy_process_list.sort(key= lambda l:(l[0], l[1], l[5]), reverse=True)
    for tup in buy_process_list:
        fp_positive_buy_process.write('%s,%s,%s,%s,%s,%s' %(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5]))

