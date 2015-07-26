# __author__ = 'cjweffort'
# -*- coding: utf-8 -*-

import datetime
import DataSplit

def timeSparse(time_string):
    words = time_string.split('-')
    words1 = words[2].split(' ')
    year = int(words[0])
    month = int(words[1])
    day = int(words1[0])
    hour = int(words1[1])
    return year, month, day, hour

def dataSplitByDay(user_ori_file):
    date = datetime.datetime(2014, 12, 18)
    fp_ori_data = open(user_ori_file, 'r')
    file_point_map = {}
    for i in xrange(0, 31):
        output_file = '../File/EverydayData/%02d.csv' %i
        file_point_map[i] = open(output_file, 'w')
    tag = True
    cnt = 0
    for line in fp_ori_data:
        if cnt % 100 == 0:
            print cnt
        cnt += 1
        if tag:
            tag = False
            continue
        words = line.split(',')
        item_id = words[1]
        time = words[5]
        year1, month1, day1, hour1 = timeSparse(time)
        date1 = datetime.datetime(year1, month1, day1)
        interval = int((date - date1).days)
        # if file_point_map.has_key(interval) == False:
        #     output_file = '%02d.csv' %interval
        #     fp_output = open(output_file, 'w')
        #     file_point_map[interval] = fp_output
        file_point_map[interval].write('%s' %line)

if __name__ == '__main__':
    #分割文件为31个文件，每天一个文件
<<<<<<< HEAD
    # dataSplitByDay('../File/tianchi_mobile_recommend_train_user.csv')
    # dataSplitByDay('../File/complete_addDistance_train_user.csv')
    id_position_map = DataSplit.itemIDMap('../File/tianchi_mobile_recommend_train_item.csv')
=======
    dataSplitByDay('../File/tianchi_mobile_recommend_train_user.csv')
    # dataSplitByDay('../File/complete_addDistance_train_user.csv')
    # id_position_map = DataSplit.itemIDMap('../File/tianchi_mobile_recommend_train_item.csv')
>>>>>>> 972f41ad2af1fc238e65d04b58a152301666f6bf
    # id_position_map = DataSplit.itemIDMap('../File/train_user_complete_by_userInfo.csv')
    """
    ""分析每天的user-item行为
    """
    import os
    total_user_item_behavior_list = [[0 for i in xrange(0, 8)] for i in xrange(0, 5)]
    rootDir = '../File/EverydayData/'
    for cnt in xrange(0, 1):
        print 'process %02d' %cnt
        tag = 0
        ii = 0
        for file_name in os.listdir(rootDir):
            file_path = os.path.join(rootDir, file_name)
            if tag < cnt:
                tag += 1
                continue
            print '%s proceed begin %d %d %d' %(file_path, ii, tag, cnt)
            if ii == 0:
                test_user_item_map, test_user_item_map_size = DataSplit.userOperate(file_path, 4, id_position_map, True)
            elif ii <= 7:
                for i in xrange(1, 5):
                    everyday_user_item_map, everyday_user_item_map_size = DataSplit.userOperate(file_path, i, id_position_map, True)
                    print 'behavior %d' %i
                    # print 'train data: user_item_numbers = %d' %everyday_user_item_map_size
                    bingos, total = DataSplit.computeRatio1(everyday_user_item_map, test_user_item_map)
                    # print '(%d,%d,%.2lf)' %(bingos, everyday_user_item_map_size, 100.0 * bingos / everyday_user_item_map_size)
                    total_user_item_behavior_list[i][ii] += bingos
            else:
                break
            ii += 1
            tag += 1
    # test_user_item_map, test_user_item_map_size = DataSplit.userOperate('../File/user_test_data.csv', 4, id_position_map)
    # print 'test data: user_item_numbers = %d' %test_user_item_map_size
    # import os
    # rootDir = '../File/EverydayData/'
    # total_user_item_behavior_list = []
    # for file_name in os.listdir(rootDir):
    #     user_item_behavior_list = []
    #     file_path = os.path.join(rootDir, file_name)
    #     print file_path
    #     for i in xrange(1, 5):
    #         everyday_user_item_map, everyday_user_item_map_size = DataSplit.userOperate(file_path, i, id_position_map)
    #         print 'behavior %d' %i
    #         print 'train data: user_item_numbers = %d' %everyday_user_item_map_size
    #         bingos, total = DataSplit.computeRatio1(everyday_user_item_map, test_user_item_map)
    #         print '(%d,%d,%.2lf)' %(bingos, everyday_user_item_map_size, 100.0 * bingos / everyday_user_item_map_size)
    #         user_item_behavior_list.append(bingos)
    #     total_user_item_behavior_list.append(user_item_behavior_list)
    cmap = {}
    # cmap[0] = 'occur_in_contact_behavior.csv'
    cmap[1] = 'occur_in_view_behavior.csv'
    cmap[2] = 'occur_in_collect_behavior.csv'
    cmap[3] = 'occur_in_cart_behavior.csv'
    cmap[4] = 'occur_in_buy_behavior.csv'
    for i in xrange(1, 5):
        time_behavior_file = '../File/' + ('%s' %cmap[i])
        fp_time_behavior = open(time_behavior_file, 'w')
        for j in xrange(1, 8):
            # total_user_item_behavior_list[i][j] /= 24.0
            fp_time_behavior.write('%d,' %total_user_item_behavior_list[i][j])
        fp_time_behavior.write('\n')
