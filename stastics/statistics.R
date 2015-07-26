setwd("E:\\TianChi\\alibaba_mobile_recommend_system\\stastics")
view_count <- read.table('view_count.csv', head = FALSE, sep = ',')
col_count <- read.table('col_count.csv', head = FALSE, sep = ',')
cart_count <- read.table('cart_count.csv', head = FALSE, sep = ',')
buy_count <- read.table('buy_count.csv', head = FALSE, sep = ',')

beh_count <- cart_count
plot(x=beh_count$V1, y=beh_count$V4, xlab="hour", ylab="buy_ratio", type="o",lty=1, ylim=c(0,0.1), xlim=c(0,120))
     

plot(x=beh_count$V1, y=beh_count$V4, xlab="hour", ylab="buy_ratio", type="o",lty=1, ylim=c(0,0.1), xlim = c(0, 48))
par(new=TRUE)
plot(x=beh_count$V1, y=beh_count$V4, xlab="hour", ylab="buy_ratio", type="o",lty=1, ylim=c(0,0.1), xlim = c(24, 48))
par(new=TRUE)
plot(x=beh_count$V1, y=beh_count$V4, xlab="hour", ylab="buy_ratio", type="o",lty=1, ylim=c(0,0.1), xlim = c(48, 72))
par(new=TRUE)
plot(x=beh_count$V1, y=beh_count$V4, xlab="hour", ylab="buy_ratio", type="o",lty=1, ylim=c(0,0.1), xlim = c(73, 96))
par(new=TRUE)
plot(x=beh_count$V1, y=beh_count$V4, xlab="hour", ylab="buy_ratio", type="o",lty=1, ylim=c(0,0.1), xlim = c(96, 120))
par(new=TRUE)
plot(x=beh_count$V1, y=beh_count$V4, xlab="hour", ylab="buy_ratio", type="o",lty=1, ylim=c(0,0.1), xlim = c(120, 144))
par(new=TRUE)
plot(x=beh_count$V1, y=beh_count$V4, xlab="hour", ylab="buy_ratio", type="o",lty=1, ylim=c(0,0.1), xlim = c(144, 168))

