--线上待推荐的user_item数量85274
drop table if exists tianchi_mobile_recommendation_predict;
create table tianchi_mobile_recommendation_predict as 
    select user_id, item_id 
    from recommend_set_pred_grbt where prediction_score = '1'
    order by prediciton_score desc limit 170548;