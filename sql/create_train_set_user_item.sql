drop table if exists test_set_user_item_tmp;
create table test_set_user_item(user_id STRING, item_id STRING, beh_rate1 DOUBLE, beh_rate2 DOUBLE, beh_rate3 DOUBLE, beh_rate4 DOUBLE, 
is_finalday_occur1 BIGINT, is_finalday_occur2 BIGINT, is_finalday_occur3 BIGINT, is_finalday_occur4 BIGINT, 
is_finalhalfday_occur1 BIGINT, is_finalhalfday_occur2 BIGINT, is_finalhalfday_occur3 BIGINT, is_finalhalfday_occur4 BIGINT,
final_beh_hour1 BIGINT, final_beh_hour2 BIGINT, final_beh_hour3 BIGINT, final_beh_hour4 BIGINT, final_beh_hour5 BIGINT,
first_beh_hour1 BIGINT, first_beh_hour2 BIGINT, first_beh_hour3 BIGINT, first_beh_hour4 BIGINT, first_beh_hour5 BIGINT,
final_beh_day1 BIGINT, final_beh_day2 BIGINT, final_beh_day3 BIGINT, final_beh_day4 BIGINT, final_beh_day5 BIGINT,
first_beh_day1 BIGINT, first_beh_day2 BIGINT, first_beh_day3 BIGINT, first_beh_day4 BIGINT, first_beh_day5 BIGINT,
first_last_cnt1 BIGINT, first_last_cnt2 BIGINT, first_last_cnt3 BIGINT, first_last_cnt4 BIGINT, first_last_cnt5 BIGINT, first_last_cnt6 BIGINT,
interval1 DOUBLE, interval2 DOUBLE, interval3 DOUBLE, interval4 DOUBLE, beh_days1 BIGINT, beh_days2 BIGINT, beh_days3 BIGINT, beh_days4 BIGINT, beh_days5 BIGINT,
ui_beh_ratio DOUBLE, ui_beh_day_ratio DOUBLE, is_buy BIGINT, beh_cnt1 BIGINT, beh_cnt2 BIGINT, beh_cnt3 BIGINT, beh_cnt4 BIGINT);

drop table if exists test_set_user_item;
drop table if exists recommend_set_user_item;
drop table if exists res_train_set_user_item;
drop table if exists res_test_set_user_item;
create table test_set_user_item as select * from train_set_user_item;
create table recommend_set_user_item as select * from train_set_user_item;
create table res_train_set_user_item as select * from train_set_user_item;
create table res_test_set_user_item as select * from train_set_user_item;