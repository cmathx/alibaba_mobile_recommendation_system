drop table if exists test_set_user_set_user;
create table test_set_user_set_user as
select * from(
select a.user_id as user_id, a.item_id as item_id, 
    a.beh_rate1 as beh_rate1, a.beh_rate2 as beh_rate2, a.beh_rate3 as beh_rate3, a.beh_rate4 as beh_rate4, 
    a.is_finalday_occur1 as is_finalday_occur1, a.is_finalday_occur2 as is_finalday_occur2, a.is_finalday_occur3 as is_finalday_occur3, a.is_finalday_occur4 as is_finalday_occur4, 
	a.is_finalhalfday_occur1 as is_finalhalfday_occur1, a.is_finalhalfday_occur2 as is_finalhalfday_occur2, a.is_finalhalfday_occur3 as is_finalhalfday_occur3, a.is_finalhalfday_occur4 as is_finalhalfday_occur4,
    a.final_beh_hour1 as final_beh_hour1, a.final_beh_hour2 as final_beh_hour2, a.final_beh_hour3 as final_beh_hour3, a.final_beh_hour4 as final_beh_hour4, a.final_beh_hour5 as final_beh_hour5,
	a.first_beh_hour1 as first_beh_hour1, a.first_beh_hour2 as first_beh_hour2, a.first_beh_hour3 as first_beh_hour3, a.first_beh_hour4 as first_beh_hour4, a.first_beh_hour5 as first_beh_hour5,
	a.final_beh_day1 as final_beh_day1, a.final_beh_day2 as final_beh_day2, a.final_beh_day3 as final_beh_day3, a.final_beh_day4 as final_beh_day4, a.final_beh_day5 as final_beh_day5,
	a.first_beh_day1 as first_beh_day1, a.first_beh_day2 as first_beh_day2, a.first_beh_day3 as first_beh_day3, a.first_beh_day4 as first_beh_day4, a.first_beh_day5 as first_beh_day5,
	a.first_last_cnt1 as first_last_cnt1, a.first_last_cnt2 as first_last_cnt2, a.first_last_cnt3 as first_last_cnt3, a.first_last_cnt4 as first_last_cnt4, a.first_last_cnt5 as first_last_cnt5, a.first_last_cnt6 as first_last_cnt6,
	a.interval1 as interval1, a.interval2 as interval2, a.interval3 as interval3, a.interval4 as interval4, a.beh_days1 as beh_days1, a.beh_days2 as beh_days2, a.beh_days3 as beh_days3, a.beh_days4 as beh_days4,
	a.beh_days5 as beh_days5, a.ui_beh_ratio as ui_beh_ratio, a.ui_beh_day_ratio as ui_beh_day_ratio,
    a.beh_cnt1 as beh_cnt1, a.beh_cnt2 as beh_cnt2, a.beh_cnt3 as beh_cnt3, a.beh_cnt4 as beh_cnt4,
    b.near_buy_time1 as near_buy_time1, b.near_buy_time2 as near_buy_time2, b.near_cart_time1 as near_cart_time1, b.near_cart_time2 as near_cart_time2, b.near_contact_time1 as near_contact_time1, b.near_contact_time2 as near_contact_time2, 
	b.buy_count1 as buy_count1, b.buy_count2 as buy_count2, b.buy_count3 as buy_count3, b.buy_count4 as buy_count4, b.buy_count5 as buy_count5,
	b.cart_count1 as cart_count1, b.cart_count2 as cart_count2, b.cart_count3 as cart_count3, b.cart_count4 as cart_count4, b.cart_count5 as cart_count5,
	b.beh_count1 as beh_count1, b.beh_count2 as beh_count2, b.beh_count3 as beh_count3, b.beh_count4 as beh_count4, b.beh_count5 as beh_count5,
	b.buy_items1 as buy_items1, b.buy_items2 as buy_items2, b.buy_items3 as buy_items3, b.buy_items4 as buy_items4, b.buy_items5 as buy_items5,
	b.cart_items1 as cart_items1, b.cart_items2 as cart_items2, b.cart_items3 as cart_items3, b.cart_items4 as cart_items4, b.cart_items5 as cart_items5,
	b.beh_items1 as beh_items1, b.beh_items2 as beh_items2, b.beh_items3 as beh_items3, b.beh_items4 as beh_items4, b.beh_items5 as beh_items5,
	b.buy_days1 as buy_days1, b.buy_days2 as buy_days2, b.buy_days3 as buy_days3, b.cart_days1 as cart_days1, b.cart_days2 as cart_days2, b.cart_days3 as cart_days3, b.beh_days1 as u_beh_days1, b.beh_days2 as u_beh_days2, b.beh_days3 as u_beh_days3,
	b.buy_count_per_item as buy_count_per_item, b.beh_count_per_item as beh_count_per_item, b.user_buy_count_ratio as user_buy_count_ratio, b.user_buy_day_ratio as user_buy_day_ratio, 
	b.user_buy_items_ratio as user_buy_items_ratio, b.buy_frequency as buy_frequency,
	b.buy_flag1 as buy_flag1, b.buy_flag2 as buy_flag2, b.buy_flag3 as buy_flag3, b.buy_flag4 as buy_flag4, b.buy_flag5 as buy_flag5,
	a.is_buy as is_buy 
from test_set_user_item a left outer join test_set_user b
on a.user_id = b.user_id)aa;

drop table if exists test_set;
create table test_set as
select * from(
select a.user_id as user_id, a.item_id as item_id, 
    a.beh_rate1 as beh_rate1, a.beh_rate2 as beh_rate2, a.beh_rate3 as beh_rate3, a.beh_rate4 as beh_rate4, 
    a.is_finalday_occur1 as is_finalday_occur1, a.is_finalday_occur2 as is_finalday_occur2, a.is_finalday_occur3 as is_finalday_occur3, a.is_finalday_occur4 as is_finalday_occur4, 
	a.is_finalhalfday_occur1 as is_finalhalfday_occur1, a.is_finalhalfday_occur2 as is_finalhalfday_occur2, a.is_finalhalfday_occur3 as is_finalhalfday_occur3, a.is_finalhalfday_occur4 as is_finalhalfday_occur4,
    a.final_beh_hour1 as final_beh_hour1, a.final_beh_hour2 as final_beh_hour2, a.final_beh_hour3 as final_beh_hour3, a.final_beh_hour4 as final_beh_hour4, a.final_beh_hour5 as final_beh_hour5,
	a.first_beh_hour1 as first_beh_hour1, a.first_beh_hour2 as first_beh_hour2, a.first_beh_hour3 as first_beh_hour3, a.first_beh_hour4 as first_beh_hour4, a.first_beh_hour5 as first_beh_hour5,
	a.final_beh_day1 as final_beh_day1, a.final_beh_day2 as final_beh_day2, a.final_beh_day3 as final_beh_day3, a.final_beh_day4 as final_beh_day4, a.final_beh_day5 as final_beh_day5,
	a.first_beh_day1 as first_beh_day1, a.first_beh_day2 as first_beh_day2, a.first_beh_day3 as first_beh_day3, a.first_beh_day4 as first_beh_day4, a.first_beh_day5 as first_beh_day5,
	a.first_last_cnt1 as first_last_cnt1, a.first_last_cnt2 as first_last_cnt2, a.first_last_cnt3 as first_last_cnt3, a.first_last_cnt4 as first_last_cnt4, a.first_last_cnt5 as first_last_cnt5, a.first_last_cnt6 as first_last_cnt6,
	a.interval1 as interval1, a.interval2 as interval2, a.interval3 as interval3, a.interval4 as interval4, a.beh_days1 as beh_days1, a.beh_days2 as beh_days2, a.beh_days3 as beh_days3, a.beh_days4 as beh_days4,
	a.beh_days5 as beh_days5, a.ui_beh_ratio as ui_beh_ratio, a.ui_beh_day_ratio as ui_beh_day_ratio,
	a.beh_cnt1 as beh_cnt1, a.beh_cnt2 as beh_cnt2, a.beh_cnt3 as beh_cnt3, a.beh_cnt4 as beh_cnt4, a.beh_cnt5 as beh_cnt5,
    a.near_buy_time1 as near_buy_time1, a.near_buy_time2 as near_buy_time2, a.near_cart_time1 as near_cart_time1, a.near_cart_time2 as near_cart_time2, a.near_contact_time1 as near_contact_time1, a.near_contact_time2 as near_contact_time2, 
	a.buy_count1 as buy_count1, a.buy_count2 as buy_count2, a.buy_count3 as buy_count3, a.buy_count4 as buy_count4, a.buy_count5 as buy_count5,
	a.cart_count1 as cart_count1, a.cart_count2 as cart_count2, a.cart_count3 as cart_count3, a.cart_count4 as cart_count4, a.cart_count5 as cart_count5,
	a.beh_count1 as beh_count1, a.beh_count2 as beh_count2, a.beh_count3 as beh_count3, a.beh_count4 as beh_count4, a.beh_count5 as beh_count5,
	a.buy_items1 as buy_items1, a.buy_items2 as buy_items2, a.buy_items3 as buy_items3, a.buy_items4 as buy_items4, a.buy_items5 as buy_items5,
	a.cart_items1 as cart_items1, a.cart_items2 as cart_items2, a.cart_items3 as cart_items3, a.cart_items4 as cart_items4, a.cart_items5 as cart_items5,
	a.beh_items1 as beh_items1, a.beh_items2 as beh_items2, a.beh_items3 as beh_items3, a.beh_items4 as beh_items4, a.beh_items5 as beh_items5,
	a.buy_days1 as buy_days1, a.buy_days2 as buy_days2, a.buy_days3 as buy_days3, a.cart_days1 as cart_days1, a.cart_days2 as cart_days2, a.cart_days3 as cart_days3, a.beh_days1 as u_beh_days1, a.beh_days2 as u_beh_days2, a.beh_days3 as u_beh_days3,
	a.buy_count_per_item as buy_count_per_item, a.beh_count_per_item as beh_count_per_item, a.user_buy_count_ratio as user_buy_count_ratio, a.user_buy_day_ratio as user_buy_day_ratio, 
	a.user_buy_items_ratio as user_buy_items_ratio, a.buy_frequency as buy_frequency,
	a.buy_flag1 as buy_flag1, a.buy_flag2 as buy_flag2, a.buy_flag3 as buy_flag3, a.buy_flag4 as buy_flag4, a.buy_flag5 as buy_flag5,
	b.buy_cnt as buy_cnt, b.cart_cnt as cart_cnt, b.buy_user_cnt as buy_user_cnt, b.cart_user_cnt as cart_user_cnt, b.buy_converse_ratio as buy_converse_ratio, 
	b.per_buy as per_buy, b.buy_converse_user_ratio as buy_converse_user_ratio, b.back_user_ratio as back_user_ratio,
	b.per_cart as per_cart, b.cart_converse_user_ratio as cart_converse_user_ratio, b.back_user_cnt as back_user_cnt, b.back_user_cart_cnt as back_user_cart_cnt,
	b.final_item_beh_hour1 as final_item_beh_hour1, b.final_item_beh_hour2 as final_item_beh_hour2, b.final_item_beh_hour3 as final_item_beh_hour3, b.final_item_beh_hour4 as final_item_beh_hour4, b.final_item_beh_hour5 as final_item_beh_hour5,
	b.cart_users1 as cart_users1, b.cart_users2 as cart_users2, b.cart_users3 as cart_users3, b.cart_users4 as cart_users4, b.cart_users5 as cart_users5,
	b.buy_users1 as buy_users1, b.buy_users2 as buy_users2, b.buy_users3 as buy_users3, b.buy_users4 as buy_users4, b.buy_users5 as buy_users5,
	b.beh_users1 as beh_users1, b.beh_users2 as beh_users2, b.beh_users3 as beh_users3, b.beh_users4 as beh_users4, b.beh_users5 as beh_users5,
	b.cart_days1 as i_cart_days1, b.cart_days2 as i_cart_days2, b.cart_days3 as i_cart_days3, b.buy_days1 as i_buy_days1, b.buy_days2 as i_buy_days2, b.buy_days3 as i_buy_days3, b.beh_days1 as i_beh_days1, b.beh_days2 as i_beh_days2, b.beh_days3 as i_beh_days3,
	a.is_buy as is_buy 
from test_set_user_set_user a left outer join test_set_item b
on a.item_id = b.item_id)aa;