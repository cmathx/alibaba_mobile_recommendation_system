# __author__ = 'cjweffort'
# -*- coding: utf-8 -*-

from FeatureExtract import *
from AnalysisBehavior import *

def addTag(feature, user_item_base_map, test_user_item_buy_set):
    total_size = 0
    positive_sample_size = 0
    for user_id in feature:
        total_size += len(feature[user_id])
        for item_id in feature[user_id]:
            if user_id in test_user_item_buy_set and item_id in test_user_item_buy_set[user_id]:
                feature[user_id][item_id][0] = 1
                user_item_base_map[user_id][item_id][29 * 4 + 3] = 1
                positive_sample_size += 1
    print 'total sample size = %d, positive sample size = %d, ratio = %.2lf' %(total_size, positive_sample_size, 1.0 * total_size / positive_sample_size)
    # return [total_size, positive_sample_size, 1.0 * total_size / positive_sample_size]

def writeFeature1(user_behavior_map, output_file_name):
    fp_user_behavior = open(output_file_name, 'w')
    for user_id in user_behavior_map:
        fp_user_behavior.write('%s,' %user_id)
        for element in user_behavior_map[user_id]:
            fp_user_behavior.write(',%s' %element)
        fp_user_behavior.write('\n')

def writeFeature(user_item_behavior_map, output_file_name):
    fp_user_item_behavior = open(output_file_name, 'w')
    for user_id in user_item_behavior_map:
        for item_id in user_item_behavior_map[user_id]:
            fp_user_item_behavior.write('%s,%s' %(user_id, item_id))
            for element in user_item_behavior_map[user_id][item_id]:
                fp_user_item_behavior.write(',%s' %element)
            fp_user_item_behavior.write('\n')

def getDataSet(is_filter, start_time, end_time, ignore_days, test_set_file, feature_file, user_item_base_feature_file, user_total_feature_file, positive_num, negative_num):
    user_item_map = extractUserItemPair(id_position_map, 3, start_time, end_time, is_filter)
    user_item_base_map = baseUserItemBehavior(user_item_map, ignore_days, False)
    # user_item_total_map = baseUserItemBehavior(user_item_map, ignore_days, True)
    user_item_total_map = {}
    userItemFeature, user_item_feature_num = extractUserItemFeature(user_item_base_map)
    userFeature, user_feature_num = extractUserFeature(user_item_base_map, user_item_total_map)
    itemFeature, item_feature_num = extractItemFeature(user_item_base_map)
    feature = combineFeature(userItemFeature, user_item_feature_num, userFeature, user_feature_num, \
                             itemFeature, item_feature_num)
    print user_item_feature_num, user_feature_num, item_feature_num
    if len(test_set_file) != 0:
        test_user_item_buy_set, test_user_item_buy_set_size = userOperate(test_set_file, 4, id_position_map, is_filter)
        print 'count buy behavior occurs:%d' %test_user_item_buy_set_size
        addTag(feature, user_item_base_map, test_user_item_buy_set)
        for i in xrange(0, 2):
            drawBehaviorMap(user_item_base_map, i, positive_num, negative_num)
        printSampleProcess(feature, 1, '../File/positive_buy_process.csv')
        printSampleProcess(feature, 0, '../File/negative_buy_process.csv')
    writeFeature(feature, feature_file)
    writeFeature(user_item_base_map, user_item_base_feature_file)
    # writeFeature1(user_item_total_map, user_total_feature_file)

if __name__ == '__main__':
    id_position_map = itemIDMap('../File/tianchi_mobile_recommend_train_item.csv')
    #getTrainSet
    getDataSet(True, '2014-12-10 00', '2014-12-17 00', 2, '../File/EverydayData/01.csv', '../DataProcess/R/DataSet/feature.csv',
               '../DataProcess/R/DataSet/base_feature.csv', '../DataProcess/R/DataSet/total_user_behavior.csv', 79, 9497)
    #getTestSet
    getDataSet(True, '2014-12-11 00', '2014-12-18 00', 1, '../File/EverydayData/00.csv', '../DataProcess/R/DataSet/test_set.csv',
               '../DataProcess/R/DataSet/base_test_set.csv', '../DataProcess/R/DataSet/test_total_user_behavior.csv', 81, 9391)
    #recommendSampling
    getDataSet(True,'2014-12-12 00', '2014-12-19 00', 0, '', '../DataProcess/R/DataSet/prepare_recommend_set.csv',
               '../DataProcess/R/DataSet/base_prepare_recommend_set.csv', '../DataProcess/R/DataSet/recommend_total_user_behavior.csv', 0, 0)
