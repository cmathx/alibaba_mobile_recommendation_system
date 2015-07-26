setwd("E:\\Competetion\\TianChi\\DataProcess\\R")

readData <- function(){
  train_set <- read.table('feature.csv', head = FALSE, sep = ',')
  test_set <- read.table('test_set.csv', head = FALSE, sep = ',')
  colnames(train_set) <- c('user_id', 'item_id', 'y', 'item_category', 'view_rate', 'collect_rate', 'cart_rate', 'buy_rate', paste("c", 1:(29*4), sep = ""))
  colnames(test_set) <- c('user_id', 'item_id', 'y', 'item_category', 'view_rate', 'collect_rate', 'cart_rate', 'buy_rate', paste("c", 1:(29*4), sep = ""))
  nrow(train_set[train_set$y==0,])/nrow(train_set[train_set$y==1,])
  return (train_set)
}

decreaseNegativeSample <- function(train_set, ratio){
  positive_train_set<-subset(train_set,train_set$y==1)
  negative_train_set<-subset(train_set,train_set$y==0)
  nrow(positive_train_set)
  nrow(negative_train_set)
  #缩小负样�?
  random_data <- runif(nrow(negative_train_set), 0, 1)
  random_negative_train_set <- negative_train_set[which(random_data<=ratio),]
  nrow(random_negative_train_set)
  new_train_set <- rbind(random_negative_train_set, positive_train_set)
  nrow(new_train_set)
  nrow(new_train_set[new_train_set$y==0,])/nrow(new_train_set[new_train_set$y==1,])
  return (new_train_set)
}

increasePositiveSample <- function(train_set, cnt){
  positive_train_set<-subset(train_set,train_set$y==1)
  negative_train_set<-subset(train_set,train_set$y==0)
  nrow(positive_train_set)
  nrow(negative_train_set)
  #增大正样�?
  rep_train_set <- train_set
  for(i in 1:cnt)
    rep_train_set <- rbind(rep_train_set, positive_train_set)
#   nrow(rep_train_set[rep_train_set$y==0,])/nrow(rep_train_set[rep_train_set$y==1,])
  rep_train_set
}


asFactor <- function(train_set){
  train_set$y <- as.factor(train_set$y)
}


rfModeling <- funciton(train_set, test_set){
  #random forest
  rf_formula <- as.formula(paste0("y ~ ", paste(colnames(train_set[5:8]), 
                                                collapse = " + ")))
  rf_model <- randomForest(rf_formula, train_set, ntree=500,mtry=2,type="classification")
  print(rf_model)
  #Predict
  predictions_rf <- predict(rf_model, newdata = test_set[5:8], type = "response")
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
