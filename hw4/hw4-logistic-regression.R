#logistic regression - hw4
#load in libararies
library(taRifx)
#fertility data set
#http://archive.ics.uci.edu/ml/machine-learning-databases/00244/fertility_Diagnosis.txt

#set the seed for reproducible results
set.seed(2)

#use several independent vars
#colClasses=c('factor','factor','factor','factor','factor','factor','factor','factor','factor','factor')
#get a data set
fertility <- read.table('http://archive.ics.uci.edu/ml/machine-learning-databases/00244/fertility_Diagnosis.txt',sep=",",header=F)

#preserve a copy
fertile <- fertility

fertility <- fertile

#name the variables
names(fertility) <- c('season','age_group','childhood_diseases','accident_trauma','surgical_intervention','high_fevers','alcohol_consumption','smoking','hours_sitting_per_day','diagnosis')

#examine data types R assigned to data
str(fertility)

#diagnosis column is a factor
#logistic regression needs it to be numeric
#also the factors are 1 and 2 - needs to be 0,1

#it works
fertility$diagnosis <- ifelse(fertility$diagnosis=="N",0,1)

#fix data types - we have lots of categorical vars represented as numbers
fertility$season <- factor(fertility$season)
fertility$age_group <- factor(fertility$age_group)
fertility$childhood_diseases <- factor(fertility$childhood_diseases)
fertility$accident_trauma <- factor(fertility$accident_trauma)
fertility$surgical_intervention <- factor(fertility$surgical_intervention)
fertility$high_fevers <- factor(fertility$high_fevers)
fertility$alcohol_consumption <- factor(fertility$alcohol_consumption)
fertility$smoking <- factor(fertility$smoking)
fertility$hours_sitting_per_day <- factor(fertility$hours_sitting_per_day)

#linear fit
lin.fit <- lm(diagnosis ~ ., data=fertility)

lin2.fit <- lm(diagnosis ~ 0, data=fertility)

logit.fit <- glm(diagnosis ~., family='binomial', data=fertility)

summary(lm(diagnosis ~ accident_trauma + high_fevers, data=fertility))
glm(diagnosis ~ 0 + accident_trauma, family='binomial', data=fertility)

#summary of coefficients and statistical significance
summary(step(lin.fit))

summary(logit.fit)

#n-fold cv framework
#setting the seed
#well commented
#something about trends

