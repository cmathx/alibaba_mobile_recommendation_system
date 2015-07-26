drop table if exists pos1_test;
create table pos1_test_set as
    select * from test_set1 where is_buy = 1;
  
drop table if exists pos2_test_set;  
create table pos2_test_set as
    select * from(
    select * from pos1_test_set
    union all
    select * from pos1_test_set)a;

drop table if exists pos4_test_set;
create table pos4_test_set as
    select * from(
    select * from pos2_test_set
    union all
    select * from pos2_test_set)a;
    
drop table if exists pos8_test_set;
create table pos8_test_set as
    select * from(
    select * from pos4_test_set
    union all
    select * from pos4_test_set)a;
    
drop table if exists pos16_test_set;
create table pos16_test_set as
    select * from(
    select * from pos8_test_set
    union all
    select * from pos8_test_set)a;
    
drop table if exists pos32_test_set;
create table pos32_test_set as
    select * from(
    select * from pos16_test_set
    union all
    select * from pos16_test_set)a;
    
drop table if exists pos40_test_set;
create table pos40_test_set as
    select * from(
    select * from pos32_test_set
    union all
    select * from pos8_test_set)a;