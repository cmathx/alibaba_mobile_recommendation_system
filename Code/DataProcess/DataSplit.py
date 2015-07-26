# __author__ = 'cjweffort'
# -*- coding: utf-8 -*-

def itemIDMap(item_file):
    fp_item_data = open(item_file, 'r')
    id_position_map = {}
    tag = True
    for line in fp_item_data:
        if tag:
            tag = False
            continue
        line = line.split(',')
        item_id = line[0]
        item_position = line[1]
        id_position_map.setdefault(item_id, item_position)
    return id_position_map

def generateUserItemDataSet(user_file, id_positin_map):
    fp_user_item_data = open('../File/user_item_data.csv', 'w')
    fp_user_data = open(user_file, 'r')
    tag = True
    for line in fp_user_data:
        if tag:
            tag = False
            continue
        words = line.split(',')
        fp_user_item_data.write('%s,%s,%s,%s,%s,%s,%s' %(words[0], words[1], words[2], words[3], words[4], id_positin_map[words[1]], words[5]))

#分割数据集
def dataSetSplit(user_ori_file, id_position_map):
    fp_ori_data = open(user_ori_file, 'r')
    fp_train_data = open('../File/user_train_data_last_week.csv', 'w')
    fp_test_data = open('../File/user_test_data.csv', 'w')
    item_id_set = set()
    tag = True
    for line in fp_ori_data:
        if tag:
            tag = False
            continue
        words = line.split(',')
        item_id = words[1]
        time = words[5]
        if time >= '2014-12-18 00':
            fp_test_data.write('%s' %line)
        elif time >= '2014-12-17 00':
            fp_train_data.write('%s' %line)
        item_id_set.add(item_id)
    return len(item_id_set)

#获取user，item，category集合
def userAndItemList(file, version, id_position_map):
    fp_user_data = open(file, 'r')
    user_set = set()
    item_set = set()
    category_set = set()
    # tag = True
    for line in fp_user_data:
        # if tag:
        #     tag = False
        #     continue
        words = line.split(',')
        if(version == 0 or (version != 0 and version == int(words[2]))):
            if words[1] in id_position_map:#待定
                user_set.add(words[0])
                item_set.add(words[1])
                category_set.add(words[4])
    return user_set, item_set, category_set

#计算user-item序列总数
def userOperate(file, version, id_position_map, is_filter):
    fp_user_data = open(file, 'r')
    user_item_map = {}
    tag = True
    for line in fp_user_data:
        if tag:
            tag = False
            continue
        words = line.split(',')
        user_id = words[0]
        item_id = words[1]
        behavior_type = words[2]
        if version == 0 or (version != 0 and version == int(behavior_type)):
            user_item_map.setdefault(user_id, set())
            if is_filter:
                if item_id in id_position_map: #待定
                    user_item_map[user_id].add(item_id)
            else:
                user_item_map[user_id].add(item_id)
    user_item_map_size = 0
    for user in user_item_map:
        user_item_map_size += len(user_item_map[user])
    return user_item_map, user_item_map_size

#计算user-item行为的比率
def computeRatio1(map1, map2):
    total = 0
    cnt = 0
    for user_id in map2:
        for item_id in map2[user_id]:
            total += 1
            if user_id in map1 and item_id in map1[user_id]:
                cnt += 1
    print '(%d,%d,%.2lf)' %(cnt, total, 1.0 * cnt / total * 100)
    # return cnt#返回命中条数，即在map2中出现的map1条数
    return cnt, total

#计算user，item的比率
def computeRatio2(set1, set2):
    total = 0
    cnt = 0
    for val in set2:
        total += 1
        if val in set1:
            cnt += 1
    print cnt, total, 1.0 * cnt / total

if __name__ == '__main__':
    id_position_map = itemIDMap('../File/tianchi_mobile_recommend_train_item.csv')
    print len(id_position_map)#item_id总数
    # generateUserItemDataSet('../File/tianchi_mobile_recommend_train_user.csv', id_position_map)
    total_item_count = dataSetSplit('../File/tianchi_mobile_recommend_train_user.csv', id_position_map)
    # print total_item_count #2914411个item，待推荐445623个item
    """
    ""分析user-item行为
    """
    #所有用户发生行为的item总数（不重复）共4579324个，浏览共4570440个，加入收藏夹共212286个，加入购物车共288212个，购买的共100337个
    #所有用户最后一天发生行为item总数（不重复）共162934个，浏览共162289个，加入收藏夹共6720个，加入购物车共9936个，购买item总数共3252个
    #考虑一个月之前的，对应的比率各33.51%，33.33%，4.95%，20.05%，3.84%
    #考虑最近一周的，对应的比率各29.52%，29.34%，3.84%，17.65%，2.28%
    #考虑最近3天的，对应的比率各25.83%，25.61%，2.83%，15.41%，0.98%
    #（对于商品子集而言）所有用户发生行为的item总数（不重复）共516829个，浏览共516049个，加入收藏夹共18820个，加入购物车共31394个，购买的共13185个
    #（对于商品子集而言）所有用户最后一天发生行为的item总数（不重复）共19021个，浏览共18944个，加入收藏夹共619个，加入购物车共1308个，购买item总数共473个
    #对应的比率各34.25%，34.25%，4.65%，20.30%，3.60%
    #考虑最近一周的，对应的比率各30.23%，30.23%，4.44%，17.12%，2.11%
    #考虑最近3天的，对应的比率各23.89%，23.89%，3.59%，14.16%，1.06%
    test_user_item_map, test_user_item_map_size = userOperate('../File/user_test_data.csv', 4, id_position_map)
    for i in xrange(0, 5):
        train_user_item_map, train_user_item_map_size = userOperate('../File/user_train_data_last_week.csv', i, id_position_map)
        computeRatio1(train_user_item_map, test_user_item_map)
        print 'train data: user_item_numbers = %d' %train_user_item_map_size
        print 'test data: user_item_numbers = %d' %test_user_item_map_size
    """
    ""分析user，item行为
    """
    #训练数据中用户数9992个，发生浏览行为的9992个，加入收藏夹的6793个，加入购物车的8649个，购买的8823个
    #测试数据中用户数6676个，发生浏览行为的6676个，加入收藏夹的1547个，加入购物车的2375个，购买的1606个
    #训练数据中item数2841247个，发生浏览行为的2835284个，加入收藏夹的193087个，加入购物车的256119个，购买的90749个
    #测试数据中item数144920个，发生浏览行为的144332个，加入收藏夹的6662个，加入购物车的9796个，购买的3202个
    #（对于商品子集而言）训练数据中用户数9894个，发生浏览行为的9893个，加入收藏夹的3207个，加入购物车的4904个，购买的4446个
    #（对于商品子集而言）测试数据中用户数2206个，发生浏览行为的2204个，加入收藏夹的241个，加入购物车的437个，购买的288个
    #（对于商品子集而言）训练数据中item数306660个，发生浏览行为的306163个，加入收藏夹的16655个，加入购物车的27053个，购买的11540个
    #（对于商品子集而言）测试数据中item数17246个，发生浏览行为的17171个，加入收藏夹的615个，加入购物车的1290个，购买的468个
    # test_user_set, test_item_set, test_category_set = userAndItemList('../File/user_test_data.csv', 4, id_position_map)
    # for i in xrange(0, 5):
    #     train_user_set, train_item_set, train_category_set = userAndItemList('../File/user_train_data_last_week.csv', i, id_position_map)
    #     computeRatio2(train_user_set, test_user_set)
    #     computeRatio2(train_item_set, test_item_set)
    #     computeRatio2(train_category_set, test_category_set)
    #     print 'train data: user_numbers = %d item_numbers = %d, category_numbers = %d' %(len(train_user_set), len(train_item_set), len(train_category_set))
    #     print 'test data: user_numbers = %d item_numbers = %d, category_numbers = %d' %(len(test_user_set), len(test_item_set), len(test_category_set))
        # test data: user_numbers = 288 item_numbers = 468, category_numbers = 164
    # computeRatio(train_user_item_buy_map, test_user_item_map)
    # last_week_user_item_cart_map = userOperate('../File/user_train_data_last_week.csv', 3, id_position_map)
