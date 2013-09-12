#need to pull the data out of the db
#requires packages
install.packages('RMySQL')

#imports
library(RMySQL)
library(ggplot2)


con <- dbConnect(MySQL(),user="", password="",dbname="test", host="localhost")
         
result <- dbSendQuery(con, "select date_recorded,tempi,dewpti from weather_data;")
data <- fetch(result, n=30000)

#examine the data structure
str(data)

#turn date_recorded into date
data$date_recorded <- as.Date(data$date_recorded)

#verify that it worked
str(data)

#visualize it
qplot(date_recorded,tempi,color=tempi,data=data, geom=c("point", "smooth"))

#option one
ggplot(data, aes(date_recorded)) + geom_line(aes(y = tempi, colour = "temp")) + geom_line(aes(y = dewpti, colour = "dewpt"))

#option two
melt_data <- melt(data, id="date_recorded")
ggplot(data=melt_data, aes(x=date_recorded, y=value, colour=variable)) + geom_line()

#clear the result_set before closing the connection
dbClearResult(result_set)
dbDisconnect(con)

# always close the connection
on.exit(dbDisconnect(con))

#does dewpt explain temperature?
#plot the regression
fit <- lm (tempi ~ dewpti, data=data)
summary(fit)
layout(matrix(c(1,2,3,4),2,2))
plot(fit)