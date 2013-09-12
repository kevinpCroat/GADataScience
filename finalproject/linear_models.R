#need to pull the data out of the db
#requires packages
install.packages('RMySQL')

#imports
library(RMySQL)
library(ggplot2)

#setup the mysql connection
con <- dbConnect(MySQL(),user="", password="",dbname="test", host="localhost")
         
#grab the weather data
result <- dbSendQuery(con, "select date_recorded,tempi,dewpti from weather_data;")
bike_data <- fetch(result, n=30000)

#examine the data structure
str(bike_data)

#turn date_recorded into date
bike_data$date_recorded <- as.Date(bike_data$date_recorded)

#verify that it worked
str(bike_data)

#visualize it
qplot(date_recorded,tempi,color=tempi,data=bike_data, geom=c("point", "smooth"))

#option one
ggplot(bike_data, aes(date_recorded)) + geom_line(aes(y = tempi, colour = "temp")) + geom_line(aes(y = dewpti, colour = "dewpt"))

#option two
melt_data <- melt(bike_data, id="date_recorded")
ggplot(data=melt_data, aes(x=date_recorded, y=value, colour=variable)) + geom_line()


#does dewpt explain temperature?
#plot the regression
fit <- lm (tempi ~ dewpti, data=data)
summary(fit)
layout(matrix(c(1,2,3,4),2,2))
plot(fit)


#clear the result_set before closing the connection
dbClearResult(result)

#grab the bike_share data
result <- dbSendQuery(con, "select * from bike_summary;")
weather_data <- fetch(result, n=100000)

#examine it
str(data)
data$trip_date <- as.Date(data$trip_date)

#
result <- dbSendQuery(con, "select * from bike_rentals;")
bd2 <- fetch(result, n=4000000)


#disconnect from db
dbDisconnect(con)

