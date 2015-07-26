library("randomForest") 
data(iris) 
set.seed(100)  
ind=sample(2,nrow(iris),replace=TRUE，prob=c(0.8,0.2))   
iris.rf=randomForest(Species~.,iris[ind==1,],ntree=50,mtry=3)   #,nPerm=10,proximity=TRUE,importance=TRUE
print(iris.rf) 
iris.pred=predict( iris.rf,iris[ind==2,] )   
table(observed=iris[ind==2,"Species"],predicted=iris.pred )   
