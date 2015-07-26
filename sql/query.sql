--以最后3天加入购物车的行为作为训练数据
--以最后1天浏览的行为作为训练数据

--train_set_user_item
--总样本：1288826 正样本：19394
--        7468449         29139     用户购买过:364928  用户收藏过:411555  
--                                    会再购买:1666      会再购买:5117

--test_set_user_item
--总样本：1260813 正样本：19029
--        7288614         27902

--recommend_set_user_item
--总样本：1229089
--        6882339

-- select count(*) from train_set_user_item;
-- select count(*) from train_set_user_item where is_buy = 1;

-- select count(*) from test_set_user_item;
-- select count(*) from test_set_user_item where is_buy = 1;

-- select count(*) from recommend_set_user_item;

--12月18日购买的user_item数量168476
-- select count(*) from
-- (
--     select distinct user_id, item_id
--     from tianchi_mobile_recommend_train_user_subset
--     where time >= '2014-12-18 00' and behavior_type = 4
-- )a;

select count(*) from train_set_user_item where buy_rate != 0 and is_buy = 1;