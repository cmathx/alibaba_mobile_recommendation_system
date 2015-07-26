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


addFeature <- function(data_set){
  data_set <- addViewAndCartFeature(data_set)
  data_set <- addBehaviorOccurs(data_set)
  data_set <- addBehaviorRatio(data_set)
  data_set
}
