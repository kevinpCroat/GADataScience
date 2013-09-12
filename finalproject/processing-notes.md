#Final Project
## Weather Data Analysis on Bike Sharing Patterns in Washington DC
### by Kevin Perko


#next steps:
munge the data
check with csv to make sure data didnt get messed up on insert
if valid
1 we have 30k rows with invalid trip duration values
calculate trip duration using start_date and end_date
OR OR
convert existing trip duration values into a integer represented by seconds
this will make your life easier for modeling

grep the files and pass the grep output to wc -l to find the number of occurrences
if it matches its just the dirty data
somewhere along the line it got whack
at to do about trip duration values that dont align with start_date and end_date values?
can we just get ride of this data? 30k rows.

#data quality

examined the data. looks good. trip duration seems to be the most accurate field.
start date and end date are not recorded at the second level
so trips under 1m dont register

For 0h 0m 0s there are 144 records in csv provided by capital bikeshare vs 130 in db. Acceptable.

-- no trips meet this condition of having a trip length >1m
select substr(trip_duration,4,1),trip_duration,row_id,start_date,start_terminal,end_terminal from bike_rentals where start_date=end_date and substr(trip_duration,4,1)>0 and trip_duration!="0h 0m 0s" order by year(start_date),month(start_date);

-- get a distinct count of all the different ways of formatting trip_duration
select trip_duration,length(trip_duration) from bike_rentals group by length(trip_duration);

#process
1. get the data from wunderground and capital bikeshare
2. set up the virtual environment which has numerical libraries installed
	2a. I did it the hard way (gcc compiler, numpy, pylab, scipy, etc) but if you go with an anacondo distro its all packaged nicely. highly recommended. 
3. source /Users/kperko/work/data-science-class/venv/bin/activate

#pytables
to get pytables working:
pip install numexpr
sudo pip install git+https://github.com/PyTables/PyTables.git@v.3.0.0#egg=tables
sudo pip install Cython

#install hdf5
http://www.underworldproject.org/downloads.html
unix build instructions:
http://www.underworldproject.org/documentation/HDF5Download.html

#considerations
account for time series
plot the data

-- number of rentals by month in time
select count(*) as rentals,year(start_date),month(start_date) from bike_rentals group by year(start_date),month(start_date);

#rentals per hour
select count(*) as trips,hour(start_date),sum(trip_duration_seconds)/count(*) as avg_trip_length_seconds from bike_rentals group by hour(start_date);

	#summary table

	create table bike_summary
	select count(*) as trips,hour(start_date) as trip_hour,date(start_date) as trip_date,
	avg(trip_duration_seconds) as avg_trip_duration,sum(trip_duration_seconds)/count(*) as avg_trip_length_seconds
	from bike_rentals 
	group by hour(start_date),date(start_date);

	-- add index for columns
	alter table bike summary add index(trip_hour,trip_date);

##weather data by hour
select tempi,hum,date(date_recorded),hour_recorded from weather_data r_date group by hour_recorded,date(date_recorded);

##join
select count(br.row_id) as trips,tempi,hum,date(date_recorded),hour_recorded from weather_data wd join bike_rentals br on (hour(br.start_date)=wd.hour_recorded and date(br.start_date)=date(wd.date_recorded)) limit 10;

##join
select count(br.row_id) as trips,tempi,hum,date(date_recorded),hour_recorded from weather_data wd join bike_rentals br on (hour(br.start_date)=wd.hour_recorded and date(br.start_date)=date(wd.date_recorded))
where date(wd.date_recorded)='2013-03-01' limit 10;

##interesting
select * from bike_summary where trips > 100 order by trips,avg_trip_duration desc limit 20;

##join w/ summary table
select trips,tempi,hum,date(date_recorded) as date_trip_wthr,hour_recorded
from weather_data wd
join bike_summary bs on (trip_hour=hour_recorded and date(trip_date)=date(date_recorded))
where date(wd.date_recorded)='2013-03-01' limit 10;

##join w/ summary table
select trips,tempi,hum,date(date_recorded) as date_trip_wthr,hour_recorded
from weather_data wd
join bike_summary bs on (trip_hour=hour_recorded and date(trip_date)=date(date_recorded))
order by trips,tempi;

##interesting
select * from bike_summary 
select trips,tempi,hum,date(date_recorded) as date_trip_wthr,hour_recorded
from weather_data wd
join bike_summary bs on (trip_hour=hour_recorded and date(trip_date)=date(date_recorded))
 limit 10;

#how to define "weather"
What constitutes good weather? 
Break out the components:
  temperature
  conditions (humidity,rain,clouds,wind,fog)
  severe conditions (thunders,rain,hail)

Could these be pushed into a PCA? That way, weather becomes a single real number, that indicates
how ideal the conditions are for biking (imho) on any given day.

#Weather Data Analysis
##Frequency and Analysis


	mysql> select min(tempi) as min_temp,max(tempi) as max_temp,avg(tempi) as avg_temp,min(hum) as min_hum,
	max(hum) as max_hum,avg(hum) as avg_hum, min(precipi) as min_precip,max(precipi) as max_precip from weather_data;
	
	+----------+----------+-----------+---------+---------+-----------+------------+------------+
	| min_temp | max_temp | avg_temp  | min_hum | max_hum | avg_hum   | min_precip | max_precip |
	+----------+----------+-----------+---------+---------+-----------+------------+------------+
	|    16.00 |   105.10 | 60.232613 |    9.00 |  100.00 | 66.558899 |   -9999.00 |       1.33 |
	+----------+----------+-----------+---------+---------+-----------+------------+------------+


What does this tell us? 
First, we have a wide amount of variance in all of our metrics and we need to clean the precipi field
so that the min is 0, not -9999.00.

####Data Cleaning
Determine the number of rows to clean:

	mysql> select count(*),precipi from weather_data group by precipi order by count(*) desc limit 5;
	+----------+---------+
	| count(*) | precipi |
	+----------+---------+
	|      467 |    0.02 |
	|      899 |    0.01 |
	|     3038 |    0.00 |
	|    22756 |-9999.00 |
	+----------+---------+

We can read the data dictionary, but for us, its either raining or it's not, so we can move this value to 0. 

	mysql> update weather_data set precipi = 0.00 where precipi=-9999.00;
	Query OK, 22756 rows affected (0.23 sec)
	Rows matched: 22756  Changed: 22756  Warnings: 0
	
	select min(tempi) as min_temp,max(tempi) as max_temp,avg(tempi) as avg_temp,min(hum) as min_hum, max(hum) as max_hum,avg(hum) as avg_hum, min(precipi) as min_precip,max(precipi) as max_precip,avg(precipi) as avg_precipi from weather_data;
	+----------+----------+-----------+---------+---------+-----------+------------+------------+-------------+
	| min_temp | max_temp | avg_temp  | min_hum | max_hum | avg_hum   | min_precip | max_precip | avg_precipi |
	+----------+----------+-----------+---------+---------+-----------+------------+------------+-------------+
	|    16.00 |   105.10 | 60.232613 |    9.00 |  100.00 | 66.558899 |       0.00 |       1.33 |    0.009175 |
	+----------+----------+-----------+---------+---------+-----------+------------+------------+-------------+

That's better!

Wait, we left out fog,rain,hail,thunder and tornado!

They are binary values, which means they are between 0 and 1. Let's count them to see how often they occur,
and if we have any unwanted values, like -9999 :).

	mysql> select count(*),round(count(*)/(select count(*) from weather_data),2) as pct_frequency,fog,rain,hail,thunder,tornado
	 from weather_data group by fog,rain,hail,thunder,tornado order by count(*);

	+----------+---------------+------+------+------+---------+---------+
	| count(*) | pct_frequency | fog  | rain | hail | thunder | tornado |
	+----------+---------------+------+------+------+---------+---------+
	|        1 |          0.00 |    0 |    1 |    1 |       0 |       0 |
	|        4 |          0.00 |    0 |    1 |    1 |       1 |       0 |
	|        9 |          0.00 |    1 |    1 |    0 |       1 |       0 |
	|       11 |          0.00 |    1 |    1 |    0 |       0 |       0 |
	|      143 |          0.00 |    0 |    0 |    0 |       1 |       0 |
	|      181 |          0.01 |    1 |    0 |    0 |       0 |       0 |
	|      510 |          0.02 |    0 |    1 |    0 |       1 |       0 |
	|     3290 |          0.11 |    0 |    1 |    0 |       0 |       0 |
	|    24867 |          0.86 |    0 |    0 |    0 |       0 |       0 |
	+----------+---------------+------+------+------+---------+---------+


This tells us that the weather is mostly decent in WDC, but oddly enough,
rain, hail and thunder occur more frequently than just rain and hail. Add
in fog and you double the number of occurrences from 4 to 9. 

The most interesting weather types to look at here are rain and rain+thunder
because they occur frequently enough that we have a chance at measuring their impact.
It also tells me that, if weather is indeed important to the decision to rent a bike,
we should see significant differences in bike rentals on a Tuesday at 5pm when it's not raining,
versus a Tuesday at 5pm when it is raining, assuming similar conditions. 

###Temperature Frequency Distribution

Let's bucketize the weather based on its distrubtion:
	
	#Distribution of temps by freqncy
	select count(*),tempi from weather_data group by(tempi);

	mysql> select 
	sum(if(tempi>10 and tempi<=30,1,0)) as bucket_30, 'count' as measure,
	sum(if(tempi>30 and tempi<=50,1,0)) as bucket_50,'count' as measure,
	sum(if(tempi>50 and tempi<=70,1,0)) as bucket_70,'count' as measure,
	sum(if(tempi>70 and tempi<=90,1,0)) as bucket_90,'count' as measure,
	sum(if(tempi>90 and tempi<=100,1,0)) as bucket_110,'count' as measure
	from weather_data
	UNION ALL
	select
	round(sum(if(tempi>10 and tempi<=30,1,0))/(select count(*) from weather_data),2) as bucket_30_pct,'pct' as measure,
	round(sum(if(tempi>30 and tempi<=50,1,0))/(select count(*) from weather_data),2) as bucket_50_pct,'pct' as measure,
	round(sum(if(tempi>50 and tempi<=70,1,0))/(select count(*) from weather_data),2) as bucket_70_pct,'pct' as measure,
	round(sum(if(tempi>70 and tempi<=90,1,0))/(select count(*) from weather_data),2) as bucket_90_pct,'pct' as measure,
	round(sum(if(tempi>90 and tempi<=100,1,0))/(select count(*) from weather_data),2) as bucket_110_pct,'pct' as measure
	from weather_data;
	
	+-----------+---------+-----------+---------+-----------+---------+-----------+---------+------------+---------+
	| bucket_30 | measure | bucket_50 | measure | bucket_70 | measure | bucket_90 | measure | bucket_110 | measure |
	+-----------+---------+-----------+---------+-----------+---------+-----------+---------+------------+---------+
	|    783.00 | count   |   9013.00 | count   |   9186.00 | count   |   9414.00 | count   |     590.00 | count   |
	|      0.03 | pct     |      0.31 | pct     |      0.32 | pct     |      0.32 | pct     |       0.02 | pct     |
	+-----------+---------+-----------+---------+-----------+---------+-----------+---------+------------+---------+


Here we can see that 93% of the weather occurs between 30 and 90 degrees F in Washington, DC. 


If we look at the percentage of weather patterns within each month we expose trends weather seasonality.

	mysql> select
	month(date_recorded),
	round(sum(if(tempi>10 and tempi<=30,1,0))/count(*),2) as bucket_30_pct,
	round(sum(if(tempi>30 and tempi<=50,1,0))/count(*),2) as bucket_50_pct,
	round(sum(if(tempi>50 and tempi<=70,1,0))/count(*),2) as bucket_70_pct,
	round(sum(if(tempi>70 and tempi<=90,1,0))/count(*),2) as bucket_90_pct,
	round(sum(if(tempi>90 and tempi<=100,1,0))/count(*),2) as bucket_110_pct
	from weather_data
	group by month(date_recorded);

We're making progress understanding our weather patterns, but what would be excellent is the ability
to have a single real number, normalized from 0 to 1, that represents the idea of weather.

###Let's get some domain expertise:
http://www.shorstmeyer.com/wxfaqs/humidity/humidity.html

####tl;dr Dew point is a better measure of whether or not the air feels sticky than humidity is.

	Dew Point  						                     Relative Humidity
	Temp. °F	       Human Perception	                   Air Temp 90°F	
	 ---------------------------------------------------------------                          
	75°+	      |   Extremely uncomfortable, oppressive  |  62%
	70° - 74°	  |   Very Humid, quite uncomfortable	   |  52% - 60%
	65° - 69°	  |   Somewhat uncomfortable          	   |  44% - 52%
	60° - 64°	  |   OK for most	                       |  37% - 46%
	55° - 59°	  |   Comfortable	                       |  31% - 41%
	50° - 54°	  |   Very comfortable	                   |  31% - 37%
	49° or lower  |	  Western US a bit dry to some	       |  30%


Including dewpoint:

	select min(tempi) as min_temp,max(tempi) as max_temp,avg(tempi) as avg_temp,min(hum) as min_hum, max(hum) as max_hum,avg(hum) as avg_hum, min(precipi) as min_precip,max(precipi) as max_precip,avg(precipi) as avg_precipi,min(dewpti) min_dewpt,max(dewpti) max_dewpt,avg(dewpti) avg_dewpt from weather_data;
	
	+----------+----------+-----------+---------+---------+-----------+------------+------------+-------------+-----------+-----------+-----------+
	| min_temp | max_temp | avg_temp  | min_hum | max_hum | avg_hum   | min_precip | max_precip | avg_precipi | min_dewpt | max_dewpt | avg_dewpt |
	+----------+----------+-----------+---------+---------+-----------+------------+------------+-------------+-----------+-----------+-----------+
	|    16.00 |   105.10 | 60.232613 |    9.00 |  100.00 | 66.558899 |       0.00 |       1.33 |    0.009175 |     -8.00 |     81.00 | 47.759564 |
	+----------+----------+-----------+---------+---------+-----------+------------+------------+-------------+-----------+-----------+-----------+


We need to create a temp table that lets us join weather and number of bike trips per hour,
since the assumption is that weather can explain at least some the variance in bike trips.
Additionally, I would expect that time of day, weekend/weekday/holiday will also have an impact
that we will need to control for. 

To control for these variables we'll include them in the regression model so that their covariates
are part of the model. We also want to say that Winter is not the same as summer and may build
different models to explain different seasons.

In reality there are certainly variables that I'm not controlling for, called residual confounding,
but this approach should be solid enough. 


#final approach
establish patterns
seasonality
hourly patterns
weekday/weekend patterns

set some sort of baseline
trips grow every month by x
so accounting for this - impact of weather

