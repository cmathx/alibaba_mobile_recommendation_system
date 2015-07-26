getUserBehaviorCount <- function(data_set, n, j){
  behCnt <- rep(0, nrow(data_set))
  for(i in (30-n):29)
    behCnt <- behCnt + data_set[, (i - 1) * j]
  behCnt
}

getUserRatio <- funciton(behCnt, buyCnt){
  ratio <- buyCnt / behCnt
  tmo = mean(ratio)
  for(i in length(behCnt)){
    if(behCnt[i] == Inf)
      ratio[i] = tmp
  }
  ratio
}

getUserBehaviorCountAndRatio <- function(data_set, n){
  viewCnt <- getUserBehaviorCount(data_set, n, 0)
  colCnt <- getUserBehaviorCount(data_set, n, 1)
  CartCnt <- getUserBehaviorCount(data_set, n, 2)
  buyCnt <- getUserBehaviorCount(data_set, n, 3)
  vbRatio <- getUserRatio(viewCnt, buyCnt)
  cbRatio <- getUserRatio(viewCnt, buyCnt)
  rbRatio <- getUserRatio(viewCnt, buyCnt)
  return list(viewCnt, colCnt, cartCnt, buyCnt, vbRatio, cbRatio, rbRatio)
}

addBehaviorCountRatioFeature <- function(data_set, total_user_behavior_set){
  l1 <- getUserBehaviorCountAndRatio(total_user_behavior_set, 7)
  l2 <- getUserBehaviorCountAndRatio(total_user_behavior_set, 15)
  l3 <- getUserBehaviorCountAndRatio(total_user_behavior_set, 29)
  data_set <- cbind(data_set, l1)
  data_set <- cbind(data_set, l2)
  data_set <- cbind(data_set, l3)
  data_set
}

train_set <- addBehaviorCountRatioFeature(train_set)
test_set <- addBehaviorCountRatioFeature(test_set)
pre_recommend_set <- addBehaviorCountRatioFeature(pre_recommend_set)

beforeDaysCount <- function(data_set, n){
  cc <- rep(0, nrow(data_set))
  for(i in (3+n*4):118)
    cc <- cc + data_set[, i]
  cc
}

getLongHistoryCount <- function(data_set){
  for(i in c(7,14,28)){
    cc <- beforeDaysCount(data_set, i)
    data_set <- cbind(data_set, cc)
  }
  colnames(data_set) <- c(colnames(data_set), c('his1', 'his2', 'his3'))
  data_set
}

train_set <- getLongHistoryCount(train_set)
test_set <- getLongHistoryCount(test_set)
pre_recommend_set <- getLongHistoryCount(pre_recommend_set)

f <- beforeTwoDaysCount(base_train_set, 1)
f2 <- f == 0 & ((base_train_set[, 3] == 1 & base_train_set[, 5] == 1) | (train_set[, 13] == 1 & train_set[, 15] == 1))#??????
f1 <- f == 0 & (base_train_set[, 3] == 1 & base_train_set[, 5] == 1)
f3 <- beforeTwoDaysCount(train_set, 5)
f4 <- f3 == 0 & (train_set[, 9] == 1 & train_set[, 11] == 1)#??????
f5 <- train_set[, 9] == 1 & train_set[, 11] == 1#??????

f <- beforeTwoDaysCount(base_test_set, 1)
f1 <- t_f == 0 & ((test_set[, 9] == 1 & test_set[, 11] == 1) | (test_set[, 13] == 1 & test_set[, 15] == 1))
f1 <- f == 0 & (base_test_set[, 3] == 1 & base_test_set[, 5] == 1)
f3 <- beforeTwoDaysCount(test_set, 5)
f4 <- t_f3 == 0 & (test_set[, 9] == 1 & test_set[, 11] == 1)
f5 <- test_set[, 9] == 1 & test_set[, 11] == 1

train_set <- cbind(train_set, f)
test_set <- cbind(test_set, f)