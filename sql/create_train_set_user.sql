drop table if exists train_set_user;
create table train_set_user(user_id STRING, near_buy_time1 BIGINT, near_buy_time2 BIGINT, near_cart_time1 BIGINT, near_cart_time2 BIGINT, near_contact_time1 BIGINT, near_contact_time2 BIGINT,
    buy_count1 BIGINT, buy_count2 BIGINT, buy_count3 BIGINT, buy_count4 BIGINT, buy_count5 BIGINT, cart_count1 BIGINT, cart_count2 BIGINT, cart_count3 BIGINT, cart_count4 BIGINT, cart_count5 BIGINT, beh_count1 BIGINT, beh_count2 BIGINT, beh_count3 BIGINT, beh_count4 BIGINT, beh_count5 BIGINT,
    buy_items1 BIGINT, buy_items2 BIGINT, buy_items3 BIGINT, buy_items4 BIGINT, buy_items5 BIGINT, cart_items1 BIGINT, cart_items2 BIGINT, cart_items3 BIGINT, cart_items4 BIGINT, cart_items5 BIGINT, beh_items1 BIGINT, beh_items2 BIGINT, beh_items3 BIGINT, beh_items4 BIGINT, beh_items5 BIGINT,
    buy_days1 BIGINT, buy_days2 BIGINT, buy_days3 BIGINT, cart_days1 BIGINT, cart_days2 BIGINT, cart_days3 BIGINT, beh_days1 BIGINT, beh_days2 BIGINT, beh_days3 BIGINT, 
    buy_count_per_item DOUBLE, beh_count_per_item DOUBLE, user_buy_count_ratio DOUBLE, user_buy_day_ratio DOUBLE, user_buy_items_ratio DOUBLE, buy_frequency DOUBLE,
    buy_flag1 BIGINT, buy_flag2 BIGINT, buy_flag3 BIGINT, buy_flag4 BIGINT, buy_flag5 BIGINT);

drop table if exists test_set_user;
drop table if exists recommend_set_user;
drop table if exists res_train_set_user;
drop table if exists res_test_set_user;
create table test_set_user as select * from train_set_user;
create table recommend_set_user as select * from train_set_user;
create table res_train_set_user as select * from train_set_user;
create table res_test_set_user as select * from train_set_user;