drop table if exists train_set_item;
create table train_set_item(item_id STRING, buy_cnt BIGINT, cart_cnt BIGINT, buy_user_cnt BIGINT, cart_user_cnt BIGINT, buy_converse_ratio DOUBLE, 
    per_buy DOUBLE, buy_converse_user_ratio DOUBLE, back_user_ratio DOUBLE, per_cart DOUBLE, cart_converse_user_ratio DOUBLE,
    back_user_cnt BIGINT,  back_user_cart_cnt BIGINT, 
    final_item_beh_hour1 BIGINT, final_item_beh_hour2 BIGINT, final_item_beh_hour3 BIGINT, final_item_beh_hour4 BIGINT, final_item_beh_hour5 BIGINT, 
    cart_users1 BIGINT, cart_users2 BIGINT, cart_users3 BIGINT, cart_users4 BIGINT, cart_users5 BIGINT, 
    buy_users1 BIGINT, buy_users2 BIGINT, buy_users3 BIGINT, buy_users4 BIGINT, buy_users5 BIGINT, 
    beh_users1 BIGINT, beh_users2 BIGINT, beh_users3 BIGINT, beh_users4 BIGINT, beh_users5 BIGINT, 
    cart_days1 BIGINT, cart_days2 BIGINT, cart_days3 BIGINT, buy_days1 BIGINT, buy_days2 BIGINT, buy_days3 BIGINT, beh_days1 BIGINT, beh_days2 BIGINT, beh_days3 BIGINT);

drop table if exists test_set_item;
drop table if exists recommend_set_item;
drop table if exists res_train_set_item;
drop table if exists res_test_set_item;
create table test_set_item as select * from train_set_item;
create table recommend_set_item as select * from train_set_item;
create table res_train_set_item as select * from train_set_item;
create table res_test_set_item as select * from train_set_item;