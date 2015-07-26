# __author__ = 'cjweffort'
# -*- coding: utf-8 -*-

from DataProcess.DataSplit import *

def extractUserItemPair(id_position_map, extract_behavior_type, start_time, end_time, is_filter):
    user_item_map = {}
    tag = True
    for line in open('../File/tianchi_mobile_recommend_train_user.csv', 'r'):
        if tag:
            tag = False
            continue
        words = line.split(',')
        '''
        设置提取的user-item对的时间（最近一周）,只考虑商品子集
        '''
        if is_filter:
            if words[1] in id_position_map  and int(words[2]) == extract_behavior_type and words[5] >= start_time and words[5] < end_time:
                user_item_map.setdefault(words[0], set())
                user_item_map[words[0]].add(words[1])
        else:
            if int(words[2]) == extract_behavior_type and words[5] >= start_time and words[5] < end_time:
                user_item_map.setdefault(words[0], set())
                user_item_map[words[0]].add(words[1])
    total = 0
    for user_id in user_item_map:
        total += len(user_item_map[user_id])
    print '待分析user-item对数量：%d' %total
    return user_item_map

'''
''ignore_cnt:不计算的天数，对于train_set而言，历史信息不包括最近的两天，对于test_set而言，历史信息不包括前一天
''base_feature_num:基本的特征数量，一般设置为29*4
''consider_day:历史信息的天数，一般设置为29
''返回用户对于商品每天各种行为发生次数，商品所属类别，用户所在位置
'''
def baseUserItemBehavior(user_item_map, ignore_cnt, is_extract_total_behavior):
    """
    提取购物车，浏览，收藏，购买行为的时间评分，商品类别
    待定：行为点击发生次数，时间评分函数制定，user和item位置，user浏览的所有item和商品子集中item的关联性
    用户特征～用户点击量，用户加入购物车量，用户购买量，用户收藏量，用户购买时间间隔，用户购买点击比率，用户购买收藏比率，用户购买加入购物车比率(所有指标按照时间重复累计，一天，三天，7天，半个月，一个月)
    品牌特征～品牌被用户点击量，品牌点击的用户数，品牌被用户购买数，品牌购买的用户数，品牌被用户收藏数，品牌收藏的用户数，品牌被用户加入购物车数，品牌加入购物车的用户数，各种比率(按照时间累计统计)
    用户品牌特征～用户品牌点击量，购买量，收藏量，加入购物车量，四种行为时间评分，各种比率(时间累计统计)
    交叉特征～用户品牌点击量/用户总点击量，用户品牌购买量/用户总购买量，用户品牌收藏量/用户收藏量，用户品牌加入购物车量/用户加入购物车量
    位置特征～用户品牌的距离(用户位置估计-根据使用品牌位置估计，品牌位置缺失-根据用户位置估计，用户位置缺失-根据用户已有的位置估计)
    """
    #4*29个特征：用户每天的点击次数，3个特征：行为发生的时间点，item类别，用户位置，最后一列：正负样本标记
    consider_days = 29
    base_feature_num = 29 * 4
    tag = 0
    user_item_behavior_map = {}
    rootDir = '../File/CompleteEverydayData/complete_by_userInfo/'#EverydayData/'
    import os
    days = 0
    for file_name in os.listdir(rootDir):
        if tag < ignore_cnt:
            tag += 1
            continue
        days += 1
        if days > consider_days:
            break
        file_path = os.path.join(rootDir, file_name)
        print 'analysis %s begin' %file_path
        with open(file_path, 'r') as f:
            for line in f:
                words = line.split(',')
                user_id = words[0]
                item_id = words[1]
                behavior_type = words[2]
                user_geohash = words[3]
                item_geohash = words[4]
                user_item_distance = words[5]
                if len(user_item_distance) == 0 or int(user_item_distance) == -1:
                    user_item_distance = 0
                else:
                    user_item_distance = int(user_item_distance)
                item_category = words[6]
                time = words[7].split(' ')[1]
                if is_extract_total_behavior == False:
                    if user_id in user_item_map and item_id in user_item_map[user_id]:#确保user_id和item_id在待分析的user-item对中
                        user_item_behavior_map.setdefault(user_id, {})
                        user_item_behavior_map[user_id].setdefault(item_id, [0 for i in xrange(0, base_feature_num + 5)])
                        user_item_behavior_map[user_id][item_id][(days - 1) * 4 + int(behavior_type) - 1] += 1  #item occurs per day
                        user_item_behavior_map[user_id][item_id][base_feature_num] = item_category
                        user_item_behavior_map[user_id][item_id][base_feature_num + 1] = user_geohash
                        user_item_behavior_map[user_id][item_id][base_feature_num + 2] = int(time)
                        if user_item_behavior_map[user_id][item_id][base_feature_num + 3] == 0:
                            user_item_behavior_map[user_id][item_id][base_feature_num + 3] = user_item_distance
                else:
                    user_item_behavior_map.setdefault(user_id, [0 for i in xrange(0, base_feature_num)])
                    user_item_behavior_map[user_id][(days - 1) * 4 + int(behavior_type) - 1] += 1  #item occurs per day
    return user_item_behavior_map

'''
''提取用户品牌特征
'''
def extractUserItemFeature(user_item_behavior_map):
    """
    用户品牌特征：1-4*49:四种行为历史信息的时间评分
    1-4：四种行为时间评分，5-8：四种行为出现次数，9-11：三种行为对购买行为比率，12-15:四种行为出现天数，16-18：三种行为出现天数对购买天数比率,
                19,20,21:浏览、收藏、购物车同时购买次数，22,23,24:浏览、收藏、购物车未当天购买次数,25,26,27：浏览、收藏、购物车同时购买次数/未当天购买比率
    """
    #29：用户最近几天同时浏览和加入购物车天数，4*29：时间评分，3：用户行为发生时间点，item类别，用户位置
    weight = []
    view_weight = [1.0, 85.0/37, 85.0/24, 85.0/19, 85.0/14, 85.0/13, 85.0/11]
    collect_weight = [1.0, 7.0/3, 7.0/2, 7.0, 7.0, 7.0, 7.0]
    cart_weight = [1.0, 39.0/14, 39.0/8, 39.0/5, 39.0/4, 39.0/3, 39.0/3]
    buy_weight = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
    weight.append(view_weight)
    weight.append(collect_weight)
    weight.append(cart_weight)
    weight.append(buy_weight)
    print 'extract user item feature begin'
    user_item_view_cart_notBuy_feature_num = 2*5
    user_item_rate_feature_num = 8*5
    user_item_count_num = 8*5
    user_item_feature_num = user_item_view_cart_notBuy_feature_num + user_item_rate_feature_num + user_item_count_num + 4
    user_item_feature = {}
    for user_id in user_item_behavior_map:
        for item_id in user_item_behavior_map[user_id]:
            user_item_feature.setdefault(user_id, {})
            user_item_feature[user_id].setdefault(item_id, [0 for i in xrange(0, user_item_feature_num)])
            for i in xrange(0, 5):
                if user_item_behavior_map[user_id][item_id][i * 4] != 0 and \
                    user_item_behavior_map[user_id][item_id][i * 4 + 2] != 0 and \
                        user_item_behavior_map[user_id][item_id][i * 4 + 1] == 0 and \
                        user_item_behavior_map[user_id][item_id][i * 4 + 3] == 0:# and \
                    if user_item_behavior_map[user_id][item_id][4 * 29 + 2] >= 19:
                        user_item_feature[user_id][item_id][2 * i] = 1#user_item_behavior_map[user_id][item_id][i - 1] + 1
                    else:
                        user_item_feature[user_id][item_id][2 * i + 1] = 1
            for i in xrange(0, 5):
                for j in xrange(0, 4):
                    for k in xrange(0,  i + 1):
                        if user_item_behavior_map[user_id][item_id][4 * k + j] != 0:
                            if user_item_behavior_map[user_id][item_id][4 * 29 + 2] >= 19:
                                if k < 5:
                                    user_item_feature[user_id][item_id][8 * i + j + user_item_view_cart_notBuy_feature_num] += 1.0 / (2 * k + 1)
                                else:
                                    user_item_feature[user_id][item_id][8 * i + j + user_item_view_cart_notBuy_feature_num] -= 1.0 * k / (2 * k + 1)
                            else:
                                if k < 5:
                                    user_item_feature[user_id][item_id][8 * i + 4 + j + user_item_view_cart_notBuy_feature_num] += 1.0 / (2 * k + 3)
                                else:
                                    user_item_feature[user_id][item_id][8 * i + 4 + j + user_item_view_cart_notBuy_feature_num] -= 1.0 * k / (2 * k + 3)
            for i in xrange(0, 5):
                for j in xrange(0, 4):
                    for k in xrange(0, i + 1):
                        if user_item_behavior_map[user_id][item_id][4 * k + j] != 0:
                            if user_item_behavior_map[user_id][item_id][4 * 29 + 2] >= 19:
                                user_item_feature[user_id][item_id][8 * i + j + user_item_view_cart_notBuy_feature_num + user_item_rate_feature_num] += 1.0 * user_item_behavior_map[user_id][item_id][4 * k + j]
                            else:
                                user_item_feature[user_id][item_id][8 * i + 4 + j + user_item_view_cart_notBuy_feature_num + user_item_rate_feature_num] += 1.0 * user_item_behavior_map[user_id][item_id][4 * k + j]
            # sum = [0 for i in xrange(0, 3 * 5)]
            # cnt = [0 for i in xrange(0, 3 * 5)]
            # for i in xrange(0, 5):
            #     for j in xrange(0, 3):
            #         if user_item_behavior_map[user_id][item_id][4 * i + 3] != 0:
            #             user_item_feature[user_id][item_id][user_item_view_cart_notBuy_feature_num + user_item_ratio_feature_num + 3 * i + j] = \
            #                 user_item_behavior_map[user_id][item_id][4 * i + j] / user_item_behavior_map[user_id][item_id][4 * i + 3]
            #             sum[3 * i + j] += user_item_behavior_map[user_id][item_id][4 * i + j] / user_item_behavior_map[user_id][item_id][4 * i + 3]
            #             cnt[3 * i + j] += 1
            # for i in xrange(0, 5):
            #     for j in xrange(0, 3):
            #         if user_item_behavior_map[user_id][item_id][4 * i + 3] == 0:
            #             user_item_feature[user_id][item_id][user_item_view_cart_notBuy_feature_num + user_item_ratio_feature_num + 3 * i + j] = 1.0 * sum[3 * i + j] / cnt[3 * i + j]
            user_item_feature[user_id][item_id][user_item_rate_feature_num + user_item_view_cart_notBuy_feature_num + user_item_count_num] = user_item_behavior_map[user_id][item_id][4 * 29 + 2]
            user_item_feature[user_id][item_id][user_item_rate_feature_num + user_item_view_cart_notBuy_feature_num + user_item_count_num + 1] = user_item_behavior_map[user_id][item_id][4 * 29]
            user_item_feature[user_id][item_id][user_item_rate_feature_num + user_item_view_cart_notBuy_feature_num + user_item_count_num + 2] = user_item_behavior_map[user_id][item_id][4 * 29 + 1]
            user_item_feature[user_id][item_id][user_item_rate_feature_num + user_item_view_cart_notBuy_feature_num + user_item_count_num + 3] = user_item_behavior_map[user_id][item_id][4 * 29 + 3]
    cnt = 0
    sum = 0
    for user_id in user_item_feature:
        for item_id in user_item_feature[user_id]:
            if user_item_feature[user_id][item_id][user_item_rate_feature_num + user_item_view_cart_notBuy_feature_num + 3] != 0:
                sum += user_item_feature[user_id][item_id][user_item_rate_feature_num + user_item_view_cart_notBuy_feature_num + 3]
                cnt += 1
    print 'the number of non-missing position is %d' %cnt
    for user_id in user_item_feature:
        for item_id in user_item_feature[user_id]:
            if user_item_feature[user_id][item_id][user_item_rate_feature_num + user_item_view_cart_notBuy_feature_num + 3] == 0:
                user_item_feature[user_id][item_id][user_item_rate_feature_num + user_item_view_cart_notBuy_feature_num + 3] = 1.0 * sum / cnt
    return user_item_feature, user_item_feature_num

'''
''提取用户特征
'''
def extractUserFeature(user_item_behavior_map, user_item_total_map):
    '''
    ''用户特征～用户点击量，用户加入购物车量，用户购买量，用户收藏量，用户购买时间间隔，用户购买点击比率，用户购买收藏比率，用户购买加入购物车比率(0-4,5-7)
    (所有指标按照时间重复累计，一天，三天，7天，半个月，一个月)
    '''
    #7个特征：四种行为用户交互数量，用户对于4种行为发生的次数，转化率
    print 'extract user feature begin'
    user_feature_num = 15
    user_feature = {}
    sumRatio = [0 for i in xrange(0, user_feature_num)]
    cnt = [0 for i in xrange(0, user_feature_num)]
    # ratio_cnt = [0 for i in xrange(0, 3)]
    for user_id in user_item_behavior_map:
        user_feature.setdefault(user_id, [0 for i in xrange(0, user_feature_num)])
        for item_id in user_item_behavior_map[user_id]:
            for j in xrange(0, 4):
                for i in xrange(0, 29):
                    if user_item_behavior_map[user_id][item_id][4 * i + j] != 0:
                        user_feature[user_id][j] += 1.0
                        user_feature[user_id][j + 11] += 1.0 / (i + 1)
                    user_feature[user_id][j + 4] += user_item_behavior_map[user_id][item_id][4 * i + j]
        for i in xrange(8, 11):
            if user_feature[user_id][i - 4] != 0:
                user_feature[user_id][i] = user_feature[user_id][7] / user_feature[user_id][i - 4]
                sumRatio[i] += user_feature[user_id][7] / user_feature[user_id][i - 4]
                cnt[i] += 1
    for user_id in user_feature:
        for i in xrange(8, 11):
            if user_feature[user_id][i] == 0:
                user_feature[user_id][i] = sumRatio[i] / cnt[i]
    # for user_id in user_item_behavior_map:
    #         for i in xrange(15, 19):
    #             user_feature[user_id][i] = user_item_total_map[user_id][i]
    #         for i in xrange(19, 22):
    #             if user_item_total_map[user_id][i - 4] != 0:
    #                 user_feature[user_id][i] = user_item_total_map[user_id][18] / user_item_total_map[user_id][i - 4]
    #                 sumRatio[i] += user_feature[user_id][18] / user_feature[user_id][i - 4]
    #                 cnt[i] += 1
    # for user_id in user_feature:
    #     for i in xrange(19, 22):
    #         if user_feature[user_id][i] == 0:
    #             user_feature[user_id][i] = sumRatio[i] / cnt[i]
    return user_feature, user_feature_num

'''
''提取品牌特征
'''
def extractItemFeature(user_item_behavior_map):
    '''
    ''品牌特征～品牌被用户点击量，品牌点击的用户数，品牌被用户购买数，品牌购买的用户数，品牌被用户收藏数，品牌收藏的用户数，品牌被用户加入购物车数，品牌加入购物车的用户数，各种比率
    (按照时间累计统计)
    '''
    #7个特征：用户四种行为发生次数，转化率；7个特征：四种行为有多少个用户进行过，转化率
    print 'extract item feature begin'
    item_feature_num = 14
    item_feature = {}
    sumRatio = [0 for i in xrange(0, item_feature_num)]
    cnt = [0 for i in xrange(0, item_feature_num)]
    for user_id in user_item_behavior_map:
        for item_id in user_item_behavior_map[user_id]:
            item_feature.setdefault(item_id, [0 for i in xrange(0, item_feature_num)])
            is_occur = [0 for i in xrange(0, 4)]
            for j in xrange(0, 4):
                for i in xrange(0, 29):
                    item_feature[item_id][j] += user_item_behavior_map[user_id][item_id][4 * i + j]#品牌被用户交互的行为数量
                    if user_item_behavior_map[user_id][item_id][4 * i + j] != 0:
                        is_occur[j] = 1
            for i in xrange(0, 4):
                if is_occur[i] == 1:
                    item_feature[item_id][i + 4] += 1#品牌用户交互数量
    for item_id in item_feature:
        for i in xrange(8, 11):
            if item_feature[item_id][i - 8] != 0:
                item_feature[item_id][i] = item_feature[item_id][3] / item_feature[item_id][i - 8]
                sumRatio[i] += item_feature[item_id][3] / item_feature[item_id][i - 8]
                cnt[i] += 1
        for i in xrange(11, 14):
            if item_feature[item_id][i - 7] != 0:
                item_feature[item_id][i] = item_feature[item_id][7] / item_feature[item_id][i - 7]
                sumRatio[i] += item_feature[item_id][7] / item_feature[item_id][i - 7]
                cnt[i] += 1
    for item_id in item_feature:
        for i in xrange(8, 14):
            if item_feature[item_id][i] == 0:
                item_feature[item_id][i] = sumRatio[i] / cnt[i]
    return item_feature, item_feature_num

def combineFeature(userItemFeature, user_item_feature_num, userFeature, user_feature_num, \
           itemFeature, item_feature_num):
    feature_num = user_item_feature_num + user_feature_num + item_feature_num
    feature = {}
    for user_id in userItemFeature:
        for item_id in userItemFeature[user_id]:
            feature.setdefault(user_id, {})
            feature[user_id].setdefault(item_id, [0 for i in xrange(1 + feature_num)])
            for i in xrange(0, user_item_feature_num):
                feature[user_id][item_id][1 + i] = userItemFeature[user_id][item_id][i]
            for i in xrange(0, user_feature_num):
                feature[user_id][item_id][1 + user_item_feature_num + i] = userFeature[user_id][i]
            for i in xrange(0, item_feature_num):
                feature[user_id][item_id][1 + user_item_feature_num + user_feature_num + i] = itemFeature[item_id][i]
    print 'extract feature end'
    return feature

