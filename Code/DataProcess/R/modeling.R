setwd("E:\\TianChi\\alibaba_mobile_recommend_system\\Code\\DataProcess\\R")
readData <- function(train_set_file_name){
  train_set <- read.table(train_set_file_name, head = FALSE, sep = ',')
  
  colnames(train_set) <- c('user_id', 'item_id', 'y', 'item_category', 'view_rate', 'collect_rate', 'cart_rate', 'buy_rate', paste("c", 1:(7*4), sep = ""))
  
  #nrow(train_set[train_set$y==0,])/nrow(train_set[train_set$y==1,])
  train_set
}

decreaseNegativeSample <- function(train_set, random_ratio){
  positive_train_set<-subset(train_set,train_set$y==1)
  negative_train_set<-subset(train_set,train_set$y==0)
  nrow(positive_train_set)
  nrow(negative_train_set)
  #g<)e0h4f 7???
  random_data <- runif(nrow(negative_train_set), 0, 1)
  random_negative_train_set <- negative_train_set[which(random_data<=random_ratio),]
  nrow(random_negative_train_set)
  new_train_set <- rbind(random_negative_train_set, positive_train_set)
  nrow(new_train_set)
  nrow(new_train_set[new_train_set$y==0,])/nrow(new_train_set[new_train_set$y==1,])
  return (new_train_set)
}

increasePositiveSample <- function(data_set, multiple_count){
  positive_data_set<-subset(data_set,data_set$y==1)
  negative_data_set<-subset(data_set,data_set$y==0)
  nrow(positive_data_set)
  nrow(negative_data_set)
  #e"e$'f-#f 7???
  rep_data_set <- data_set
  for(i in 1:multiple_count)
    rep_data_set <- rbind(rep_data_set, positive_data_set)
  nrow(rep_data_set[rep_data_set$y==0,])/nrow(rep_data_set[rep_data_set$y==1,])
  return (rep_data_set)
}


asFactor <- function(train_set){
  train_set$y <- as.factor(train_set$y)
  return (train_set)
}


rfModeling <- function(train_set, test_set){
  #random forest
  rf_formula <- as.formula(paste0("y ~ ", paste(colnames(train_set[5:120]), 
                                                collapse = " + ")))
  rf_model <- randomForest(rf_formula, train_set, ntree=5000,mtry=11,type="classification")
  print(rf_model)
  #Predict
  predictions_rf <- predict(rf_model, newdata = test_set[5:120], type = "response")
  #compute the value of AUC
  auc(test_set$y, predictions_rf)
  table(test_set$y, predictions_rf)
}

gbdtModeling <- function(train_set, test_set){
  #gbdt
  gbm_formula <- as.formula(paste0("y ~ ", paste(colnames(new_train_set[5:124]), 
                                                 collapse = " + ")))
  gbm_model <- gbm(gbm_formula, new_train_set, distribution = "bernoulli", n.trees = 5000, 
                   bag.fraction = 0.75, cv.folds = 5, interaction.depth = 3)
  gbm_perf <- gbm.perf(gbm_model, method = "cv")
  #Predict
  predictions_gbm <- predict(gbm_model, newdata = test_set[4:7], 
                             n.trees = gbm_perf, type = "response")
  #compute the value of AUC
  auc(test_set$y, predictions_gbm)
}

computeF1 <- function(bingos, recommend_number, actual_number){
  precision <- bingos / recommend_number
  recall <- bingos / actual_number
  F1 <- 2 * precision * recall / (precision + recall)
  message(bingos, ' ', recommend_number, ' ', precision, ' ', recall, ' ', F1)
  return (list(precision, recall, F1))
}

