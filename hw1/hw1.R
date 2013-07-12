
# data dict: http://archive.ics.uci.edu/ml/machine-learning-databases/autos/imports-85.names
# data: http://archive.ics.uci.edu/ml/machine-learning-databases/autos/imports-85.data

#clear workspace
rm(list = ls())

#load packages
library(MASS)
library(ggplot2)
library(taRifx)

#load in data
auto <- read.csv("/Users/kperko/work/data-science-class/hw1/dataset/imports-85.data", header=F)

#get structure that R imposed
str(auto)

#name columns
names(auto) <- c("symboling","normalized-losses","make","fuel_type","aspiration","num_of_doors","body_style","drive_wheels","engine_location","wheel_base", "length", "width", "height", "curb_weight", "engine_type", "num_of_cylinders", "engine_size", "fuel_system", "bore", "stroke", "compression_ratio", "horsepower", "peak_rpm", "city_mpg", "highway_mpg", "price")

#copy df for manipulation
auto.s <- auto

#remove rows
myvars <- names(auto.s) %in% c("symboling","normalized-losses","bore","stroke")
auto.s <- auto.s[!myvars]
str(auto.s)

#turn factors into numbers
#I tried a lot of other functions like as.numeric(levels(column)) but they didn't work
auto.s$horsepower <- destring(auto.s$horsepower)
auto.s$price <- destring(auto.s$price)
auto.s$peak_rpm <- destring(auto.s$peak_rpm)

#plot it
#looks like a power law
qplot(city_mpg,price,color=engine_size,data=auto.s)
# linear
qplot(engine_size,price,color=engine_size,data=auto.s)

#closer to linear but not as good as engine size
qplot(log(city_mpg),log(price),color=engine_size,data=auto.s)

#remove na's
auto.s <- na.omit(auto.s)

#throwing everything in the model
#the indep vars explain 95% of the variance in the price
fit.a <- lm(price ~., data=auto.s)
summary(fit.a)
plot(fit.a)

#.61 r-squared
fit.a1 <- lm(price ~ num_of_cylinders, data=auto.s)
summary(fit.a1)
plot(fit.a1)

#.7725 rsquared for make
fit.b <- lm(price ~ make, data=auto.s)
summary(fit.b)
plot(fit.b)

#.78 r squared
fit <- lm(price ~ city_mpg + engine_size + body_style, data=auto.s)
summary(fit)

#.76 r squared for one var
fit <- lm(price ~ engine_size, data=auto.s)
summary(fit)

#adding polynomials
fit2 <- lm(price ~ poly(engine_size,degree=2), data=auto.s)
summary(fit2)

fit3 <- lm(price ~ poly(engine_size,degree=3), data=auto.s)
summary(fit3)

fit8 <- lm(price ~ poly(engine_size,degree=8), data=auto.s)
summary(fit8)

fit16 <- lm(price ~ poly(engine_size,degree=16), data=auto.s)
summary(fit16)

#.903 r squared for 2 vars, make and curb weight
fit.c <- lm(price ~ curb_weight + make, data=auto.s)
summary(fit.c)
plot(fit.c)

#ridge regression
#dont think I did this correctly
fit.c.r <- lm.ridge(price ~ curb_weight + engine_size, data=auto.s,lambda=seq(0,.1,.001))
summary(fit.c.r)

plot(lm.ridge(price ~ curb_weight + engine_size, data=auto.s,lambda=seq(0,.1,.001)))
