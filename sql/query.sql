--�����3����빺�ﳵ����Ϊ��Ϊѵ������
--�����1���������Ϊ��Ϊѵ������

--train_set_user_item
--��������1288826 ��������19394
--        7468449         29139     �û������:364928  �û��ղع�:411555  
--                                    ���ٹ���:1666      ���ٹ���:5117

--test_set_user_item
--��������1260813 ��������19029
--        7288614         27902

--recommend_set_user_item
--��������1229089
--        6882339

-- select count(*) from train_set_user_item;
-- select count(*) from train_set_user_item where is_buy = 1;

-- select count(*) from test_set_user_item;
-- select count(*) from test_set_user_item where is_buy = 1;

-- select count(*) from recommend_set_user_item;

--12��18�չ����user_item����168476
-- select count(*) from
-- (
--     select distinct user_id, item_id
--     from tianchi_mobile_recommend_train_user_subset
--     where time >= '2014-12-18 00' and behavior_type = 4
-- )a;

select count(*) from train_set_user_item where buy_rate != 0 and is_buy = 1;