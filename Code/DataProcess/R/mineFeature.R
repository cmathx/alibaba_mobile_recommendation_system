addViewAndCartFeature <- function(data_set){
  view_and_cart <- rep(0, nrow(data_set))
  for(ii in 1:29){
    for(i in 1:nrow(data_set)){
      flag <- 0
      if(data_set[i, 8 + (ii - 1) * 4 + 1] > 0 & data_set[i, 8 + (ii - 1) * 4 + 3] > 0)
        flag <- 1
      #for(j in 1:7){
      #  if(train_set[i,8 + (j - 1) * 4 + 1] > 0 & train_set[i,8 + (j - 1) * 4 + 3] > 0){
      #    flag <- 1
      #    break
      #  }
      #}
      if(flag > 0)
        view_and_cart[i] <- view_and_cart[i] + flag
    }
    #print(table(train_set$y, feature_valid))
  }
  data_set <- cbind(data_set, view_and_cart)
  data_set
}

addBehaviorOccurs <- function(data_set){
  for(k in 1:4){
    behavior_occurs <- rep(0, nrow(data_set))
    for(j in 1:29)
      behavior_occurs <- behavior_occurs + data_set[, 8 + (j - 1) * 4 + k]
    data_set <- cbind(data_set, behavior_occurs)
  }
  data_set
}

addBehaviorRatio <- function(data_set){
  buy_view_ratio <- rep(0, nrow(data_set))
  cart_view_ratio <- rep(0, nrow(data_set))
  collect_view_ratio <- rep(0, nrow(data_set))
  for(i in 1:nrow(data_set)){
    if(data_set[i, 8 + 4 * 29 + 1 + 1] != 0)#view_buy_ratio
      buy_view_ratio[i] <- data_set[i, 8 + 4 * 29 + 1 + 4] / data_set[i, 8 + 4 * 29 + 1 + 1]
    if(data_set[i, 8 + 4 * 29 + 3 + 1] != 0)#cart_buy_ratio
      cart_view_ratio[i] <- data_set[i, 8 + 4 * 29 + 1 + 4] / data_set[i, 8 + 4 * 29 + 1 + 3]
    if(data_set[i, 8 + 4 * 29 + 2 + 1] != 0)#collect_buy_ratio
      collect_view_ratio[i] <- data_set[i, 8 + 4 * 29 + 1 + 4] / data_set[i, 8 + 4 * 29 + 1 + 2]
  }
  for(i in 1:nrow(data_set)){
    if(buy_view_ratio[i] != 0) buy_view_ratio[i] = mean(buy_view_ratio)
    if(cart_view_ratio[i] != 0) cart_view_ratio[i] = mean(cart_view_ratio)
    if(collect_view_ratio[i] != 0) collect_view_ratio[i] = mean(collect_view_ratio)
  }
  data_set <- cbind(cbind(cbind(data_set, buy_view_ratio), cart_view_ratio), collect_view_ratio)
  data_set
}

addBehaviorCount <- function(data_set, extra_feature_num){
  for(i in 1:29){
    behavior_count <- rep(0, nrow(data_set))
    start_index <- extra_feature_num
    for(j in i:29){
      behavior_count <- behavior_count + data_set[, start_index + (i - 1) * 4]
    }
    data_set <- cbind(data_set, behavior_count)
  }
  data_set
}

addHistoryCount <- function(data_set){
  cc<-rep(0, nrow(data_set))
  for(i in (3+4*5):ncol(data_set))
    cc <- cc + data_set[,i]
  data_set<-cbind(data_set, cc)
  data_set<-cbind(data_set,data_set$)
  data_set
}

addNearlyViewCart <- function(data_set){
  for(i in 1:5)
    data_set<-cbind(data_set, data_set[, 3+4+(i-1)*4+1] + data_set[,3+4+(i-1)*4+3])
  data_set
}

addViewCartNotBuy <- function(data_set){
  data_set <- cbind(data_set, data_set$rate1 != 0 & data_set$rate3 != 0 & data_set$rate4 == 0)
  data_set
}

addFeature <- function(data_set){
  data_set <- addViewCartNotBuy(data_set)
  data_set
}

train_set <- addFeature(train_set)
test_set <- addFeature(test_set)

colnames <- c('user_id', 'item_id', 'y', paste("rate", 1:(4), sep = ""), paste("c", 1:(29*4), sep = ""), 
              'his', paste("view_cart", 1:5, sep = ""), 'cc', 'r')

train_set<-cbind(train_set,train_set$his==0&train_set$view_cart1==2&train_set$c4==0)
test_set<-cbind(test_set,test_set$his==0&test_set$view_cart1==2&test_set$c4==0)

colnames <- c('user_id', 'item_id', 'y', paste("rate", 1:4, sep = ""),  paste("occurs", 1:4, sep = ""), paste("occurs_ratio", 1:3, sep = ""),
              paste("occur_days", 1:4, sep = ""), paste("occur_days_ratio", 1:3, sep = ""), 
              paste('buy_beh', 1:3, sep = ""), paste("not_buy_beh", 1:3, sep = ""), paste("buy_beh_ratio", 1:3, sep = ""),
              paste("c", 1:(29*4), sep = ""), paste("view", 1:(29), sep = ""), paste("collect", 1:(29), sep = ""), paste("cart", 1:(29), sep = ""), paste("buy", 1:(29), sep = ""))
colnames(train_set) <- colnames
colnames(test_set) <- colnames
colnames(pre_recommend_set) <- colnames