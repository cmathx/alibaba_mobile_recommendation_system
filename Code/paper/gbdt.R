library("gbm")
accident_data_set <- read.delim("E:\\Competetion\\TianChi\\code\\File\\GES12_Flatfile\\PERSON.TXT")
print(sort(colnames(accident_data_set)))
#table(accident_data_set$INJSEV_IM)
table(accident_data_set$INJSEV_IM)
accident_data_set <- accident_data_set[accident_data_set$INJSEV_IM != 6, ]

for (i in 1:ncol(accident_data_set)) {
  if (sum(as.numeric(is.na(accident_data_set[, i]))) > 0) {
    num_missing <- sum(as.numeric(is.na(accident_data_set[, i])))
    print(paste0(colnames(accident_data_set)[i], ":  ", num_missing))
    
  }
}
rows_to_drop <- which(apply(accident_data_set, 1, FUN = function(X) {
  return(sum(is.na(X)) > 0)
}))
data <- accident_data_set[-rows_to_drop, ]
data$INJ_SEV <- NULL
data$INJSEV_IM <- as.numeric(data$INJSEV_IM == 4)
target <- data$INJSEV_IM

#Model
train_rows <- sample(nrow(data), round(nrow(data) * 0.5))
traindf <- data[train_rows, ]
testdf <- data[-train_rows, ]
#Train
gbm_formula <- as.formula(paste0("INJSEV_IM ~ ", paste(colnames(traindf[, -response_column]), 
                                                       collapse = " + ")))
gbm_model <- gbm(gbm_formula, traindf, distribution = "bernoulli", n.trees = 500, 
                 bag.fraction = 0.75, cv.folds = 5, interaction.depth = 3)
gbm_perf <- gbm.perf(gbm_model, method = "cv")
#Predict
predictions_gbm <- predict(gbm_model, newdata = testdf[, -response_column], 
                           n.trees = gbm_perf, type = "response")
#compute the value of AUC
auc(testdf$INJSEV_IM, predictions_gbm)

#例子2
# 加载包和数据
library(gbm)
data(PimaIndiansDiabetes2,package='mlbench')
# 将响应变量转为0-1格式
data <- PimaIndiansDiabetes2
data$diabetes <- as.numeric(data$diabetes)
data <- transform(data,diabetes=diabetes-1)
# 使用gbm函数建模
model <- gbm(diabetes~.,data=data,shrinkage=0.01,
             distribution='bernoulli',cv.folds=5,
             n.trees=3000,verbose=F)
# 用交叉检验确定最佳迭代次数
best.iter <- gbm.perf(model,method='cv')
# 预测
library(caret)
fitControl <- trainControl(method = "cv", number = 5,returnResamp = "all")
model2 <- train(diabetes~., data=data,method='gbm',distribution='bernoulli',trControl = fitControl,verbose=F,tuneGrid = data.frame(.n.trees=best.iter,.shrinkage=0.01,.interaction.depth=1))
model2