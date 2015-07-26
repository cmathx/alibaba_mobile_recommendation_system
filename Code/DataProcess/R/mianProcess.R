model <- function(train_set, test_set){
  train_set$y <- as.factor(train_set$y)
  rfModeling(train_set, test_set)
}

index_range <- c(62:65,66:69)#4:9, ,297:304  ,66:69  ,62:65  4:61  ,62:293
formula <- as.formula(paste("y ~ ", paste(colnames(train_set[index_range]), 
                                              collapse = " + ")))
model <- randomForest(formula, expand_train_set, ntree=2000,mtry=3,type="classification")
predictions <- predict(model, newdata = test_set[index_range], type = "response")
roc(test_set$y, as.numeric(predictions)-1)
table(test_set$y, predictions)
tp<-length(intersect(which(predictions==1), which(test_set$y==1)))
fp<-length(intersect(which(predictions==1), which(test_set$y==0)))
computeF1(tp, tp + fp, 473)
#model(train_set, test_set)

#rf model
library(pROC)
library(randomForest)
library(gbm)

cnt <- nrow(train_set[train_set$y==0,]) / nrow(train_set[train_set$y==1,]) / 6
expand_train_set <- increasePositiveSample(train_set, cnt)
expand_train_set$y <- as.factor(expand_train_set$y)
message('positive/negative sample ratio: ', nrow(expand_train_set[expand_train_set$y==0,])/nrow(expand_train_set[expand_train_set$y==1,]))#1.5

#rf train and predict
<<<<<<< HEAD
model <- randomForest(formula, expand_train_set, ntree=2000,mtry=3,type="classification")
predictions <- predict(model, newdata = test_set[index_range], type = "response")
=======
rf_model <- randomForest(formula, expand_train_set, ntree=2000,mtry=3,type="classification")
predictions_rf <- predict(rf_model, newdata = test_set[index_range], type = "response")
>>>>>>> 8b42681066d59045bffe040b6b0f45820782b63a
#gbm train and predict
model <- gbm(formula,data=expand_train_set,shrinkage=0.01, distribution='bernoulli',cv.folds=5, n.trees=1000,verbose=F)
best.iter <- gbm.perf(model,method='cv')
predictions <- predict(model, test_set[index_range], n.trees = best.iter, type = "response")
#logistic regression train and predict
model <- glm(formula, family = binomial, data = expand_train_set)
predictions <- predict(model, type = "response")
plot(predictions)
length(which(predictions > 0.67))
predictions[predictions > 0.67] <- 1
predictions[predictions <= 0.67] <- 0
expand_train_set<-cbind(expand_train_set,predictions)
predictions <- predict(model, newdata = test_set[index_range], type = "response")
plot(predictions)
length(which(predictions > 0.5))
predictions[predictions > 0.5] <- 1
predictions[predictions <= 0.5] <- 0
test_set <- cbind(test_set, predictions)

<<<<<<< HEAD
roc(test_set$y, as.numeric(predictions_rf)-1)
table(test_set$y, predictions_rf)
tp<-length(intersect(which(predictions_rf==1), which(test_set$y==1)))
fp<-length(intersect(which(predictions_rf==1), which(test_set$y==0)))
computeF1(tp, tp + fp, 393)
=======
roc(test_set$y, as.numeric(predictions)-1)
table(test_set$y, predictions)
tp<-length(intersect(which(predictions==1), which(test_set$y==1)))
fp<-length(intersect(which(predictions==1), which(test_set$y==0)))
computeF1(tp, tp + fp, 473)
>>>>>>> 972f41ad2af1fc238e65d04b58a152301666f6bf
#compute the value of AUC
pred <- prediction(pre, test_set$y)
performance(pred, 'auc')@y.values #auc value
perf <- performance(pred, 'tpr', 'fpr')
plot(perf)
auc(test_set$y, predictions_rf)

#recommend
cnt <- nrow(test_set[test_set$y==0,]) / 6 / nrow(test_set[test_set$y==1,])
expand_test_set <- increasePositiveSample(test_set, cnt)
expand_test_set$y <- as.factor(expand_test_set$y)
message('positive/negative sample ratio: ', nrow(expand_test_set[expand_test_set$y==0,])/nrow(expand_test_set[expand_test_set$y==1,]))
rf_model <- randomForest(formula, expand_test_set, ntree=2000,mtry=3,type="classification")
predictions_rf <- predict(rf_model, newdata = pre_recommend_set[index_range], type = "response")
pre_recommend_set$y<-predictions_rf
write.table(pre_recommend_set[pre_recommend_set$y==1,][1:2], file = 'Recommend\\user_item_based_recommend.csv', sep = ',')

#Stacked AutoEncoder
library(deepnet)
#train
dl_model <- sae.dnn.train(as.matrix(expand_train_set[index_range]), as.matrix(as.numeric(expand_train_set$y) - 1), 
                          hidden=c(100, 50, 10))
dl_model <- dbn.dnn.train(as.matrix(expand_train_set[index_range]), as.matrix(as.numeric(expand_train_set$y) - 1), 
                          hidden=c(100, 50, 100, 20, 10, 5, 5), cd = 1)
#predict by dnn
training_dnn <- nn.predict(dl_model, as.matrix(test_set[index_range]))
plot(training_dnn)
length(which(training_dnn>0.22))
training_dnn[training_dnn > 0.5] <- 1
training_dnn[training_dnn <= 0.5] <- 0
table(test_set$y, training_dnn)
predictions_dnn <- nn.predict(dl_model, as.matrix(test_set[index_range]))
plot(predictions_dnn)
length(which(predictions_dnn>0.35))
predictions_dnn[predictions_dnn > 0.35] <- 1
predictions_dnn[predictions_dnn <= 0.35] <- 0
table(test_set$y, predictions_dnn)
summary(training_dnn)
summary(predictions_dnn)
nn.test(dnn, as.matrix(test_set[index_range]), as.matrix(as.numeric(test_set$y)))
computeF1(34, 993, 473)