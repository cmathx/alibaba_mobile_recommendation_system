data(iris) 
logit.fit <- glm(Species~Petal.Width+Petal.Length,
                 family = binomial(link = 'logit'),
                 data = iris[51:150,])
logit.predictions <- ifelse(predict(logit.fit) > 0,'virginica', 'versicolor')
table(iris[51:150,5],logit.predictions)

probit.fit <- glm(Species~Petal.Width+Petal.Length,
                  family = quasibinomial(link = 'probit'),
                  data = iris[51:150,])
probit.predictions <- ifelse(predict(probit.fit) >0,'virginica', 'versicolor')
table(iris[51:150,5],probit.predictions)
