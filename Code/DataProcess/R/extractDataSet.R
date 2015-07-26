increase_positive_model <- function(train_set, test_set, increase_count){
  expand_train_set <- increasePositiveSample(train_set, increase_count)
  expand_train_set$y <- as.factor(expand_train_set$y)
  rfModeling(expand_train_set, test_set)
}

decrease_negative_model <- function(train_set, test_set, decrease_ratio){
  lower_train_set <- decreaseNegativeSample(train_set, decrease_ratio)
  lower_train_set$y <- as.factor(lower_train_set$y)
  rfModeling(lower_train_set, test_set)
}

setwd("E:\\TianChi\\alibaba_mobile_recommend_system\\Code\\DataProcess\\R")

train_set <- read.table('DataSet\\new\\feature.csv', head = FALSE, sep = ',')
test_set <- read.table('DataSet\\new\\test_set.csv', head = FALSE, sep = ',')
pre_recommend_set <- read.table('DataSet\\new\\prepare_recommend_set.csv', head = FALSE, sep = ',')

base_train_set <- read.table('DataSet\\new\\base_feature.csv', head = FALSE, sep = ',')
base_test_set <- read.table('DataSet\\new\\base_test_set.csv', head = FALSE, sep = ',')
base_pre_recommend_set <- read.table('DataSet\\new\\base_prepare_recommend_set.csv', head = FALSE, sep = ',')

# train_set <- addFeature(train_set)
# test_set <- addFeature(test_set)
# pre_recommend_set <- addFeature(pre_recommend_set)
colnames <- c('user_id', 'item_id', 'y', paste("vc", 1:(29*2), sep = ""), paste("rate", 1:(29*8), sep = ""), 'hour', 'category', 'user_geohash', 
<<<<<<< HEAD
              paste("u", 1:22, sep = ""), paste("i", 1:14, sep = ""))
=======
              paste("u", 1:25, sep = ""), paste("i", 1:14, sep = ""))
>>>>>>> 972f41ad2af1fc238e65d04b58a152301666f6bf
colnames(train_set) <- colnames
colnames(test_set) <- colnames
colnames(pre_recommend_set) <- colnames
colnames <- c('user_id', 'item_id', paste("c", 1:(4*29), sep = ""), 'categoty', 'user_geohash', 'hour', 'y')
colnames(base_train_set) <- colnames
colnames(base_test_set) <- colnames
colnames(base_pre_recommend_set) <- colnames

nrow(train_set[train_set$y==0,])/nrow(train_set[train_set$y==1,])
#???????????????
lower_train_set <- decreaseNegativeSample(train_set, 0.028)
nrow(lower_train_set[lower_train_set$y==0,])/nrow(lower_train_set[lower_train_set$y==1,])
lower_train_set$y <- as.factor(lower_train_set$y)

total_predicitons_rf <- rep(0, nrow(test_set))
classificaiton_model_num <- 0
for(i in 1:24){
  message(i, ' round start')
  train_set_file_name <- sprintf('DataSet\\feature%02d.csv', i)
  #DataSet\\feature01.csv'
  train_set <- readData(train_set_file_name)
  if(train_01_ratio$V3[i] > 140)
    next
  classificaiton_model_num <- classificaiton_model_num + 1
  cnt <- nrow(train_set[train_set$y==0,]) / 1.5 / nrow(train_set[train_set$y==1,])
  expand_train_set <- increasePositiveSample(train_set, cnt)
  expand_train_set$y <- as.factor(expand_train_set$y)
  message('positive/negative sample ratio: ', nrow(expand_train_set[expand_train_set$y==0,])/nrow(expand_train_set[expand_train_set$y==1,]))
  rf_model <- randomForest(rf_formula, expand_train_set, ntree=500,mtry=2,type="classification")
  predictions_rf <- predict(rf_model, newdata = test_set[index_range], type = "response")
  table(test_set$y, predictions_rf)
  tp<-length(intersect(which(predictions_rf==1), which(test_set$y==1)))
  fp<-length(intersect(which(predictions_rf==1), which(test_set$y==0)))
  computeF1(tp, tp + fp, 473)
  total_predicitons_rf <- total_predicitons_rf + as.numeric(predictions_rf) - 1
}

tp<-length(intersect(which(total_predicitons_rf>11), which(test_set$y==1)))
fp<-length(intersect(which(total_predicitons_rf>11), which(test_set$y==0)))
computeF1(tp, tp + fp, 473)