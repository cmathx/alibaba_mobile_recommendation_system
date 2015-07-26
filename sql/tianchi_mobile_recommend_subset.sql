drop table if exists tianchi_mobile_recommend_train_user_subset;
create table tianchi_mobile_recommend_train_user_subset as 
    select a1.user_id, a1.item_id
    from
    (
        select a.user_id, a.item_id, a.behavior_type, a.user_geohash, a.item_category, a.time
        from
        (
        select user_id, item_id, behavior_type, user_geohash, item_category, time
        from tianchi_mobile_recommend_train_user
        )a
        join
        (
        select distinct item_id
        from tianchi_mobile_recommend_train_item
        )b
        on a.item_id = b.item_id
        where b.item_id is not null
    )a1
;