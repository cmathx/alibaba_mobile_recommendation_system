drop table if exists tianchi_mobile_recommendation_predict;
create table tianchi_mobile_recommendation_predict as 
    select a1.user_id, a1.item_id
    from
    (
        select a.user_id, a.item_id
        from
        (
        select user_id, item_id
        from tianchi_mobile_recommend_train_user
        where time >= '2014-12-18 00' and behavior_type = 3
        group by user_id, item_id
        )a
        join
        (
        select distinct item_id
        from tianchi_mobile_recommend_train_item
        )b
        on a.item_id = b.item_id
        where b.item_id is not null
    )a1
    --join
    --(
    --select user_id, item_id
    --from tianchi_lbs.tianchi_mobile_recommend_train_user
    --where behavior_type = 4
    --)b1
    --on a1.user_id = b1.user_id and a1.item_id = b1.item_id
    --where b1.user_id is null and b1.item_id is null
;
