ad <- read.table('/Users/kperko/work/data-science-class/GADataScience/finalproject/trip_data.csv',sep=",",header=T,colClasses = c("trips"="numeric","mnth_yr"="character"))



str(ad)
ad$mnth_yr <- as.Date(ad$mnth_yr)

library(ggplot2)

qplot(mnth_yr,trips,data=ad)
plot(ad$mnth_yr,ad$trips)
plot(density(ad$trips))

#its not a power law so logging isn't the best approach
plot(density(log(ad$trips)))

#how well does a linear model fit?
#do months explain the variation?
#.65
fit <- lm (trips ~ ., data=ad)
summary(fit)

#log it and try again
ad.log <- ad
ad$trips <- log(ad$trips)

#how well does a linear model fit? (with a logged trip num)
#do months explain the variation?
#.54
fit <- lm (trips ~ ., data=ad, poly=2)
summary(fit)

#should we exclude the inital month?
#not enough data
#startup - skew results
#remove the outlier
ad <- ad[2:33,]

fit <- lm (trips ~ ., data=ad)
summary(fit)

#get some visual representation
plot(fit)