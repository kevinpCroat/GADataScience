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

#weather data by hour
select tempi,hum,date(date_recorded),hour_recorded from weather_data r_date group by hour_recorded,date(date_recorded);

#join
select count(br.row_id) as trips,tempi,hum,date(date_recorded),hour_recorded from weather_data wd join bike_rentals br on (hour(br.start_date)=wd.hour_recorded and date(br.start_date)=date(wd.date_recorded)) limit 10;

#join
select count(br.row_id) as trips,tempi,hum,date(date_recorded),hour_recorded from weather_data wd join bike_rentals br on (hour(br.start_date)=wd.hour_recorded and date(br.start_date)=date(wd.date_recorded))
where date(wd.date_recorded)='2013-03-01' limit 10;

#interesting
select * from bike_summary where trips > 100 order by trips,avg_trip_duration desc limit 20;

#join w/ summary table
select trips,tempi,hum,date(date_recorded) as date_trip_wthr,hour_recorded
from weather_data wd
join bike_summary bs on (trip_hour=hour_recorded and date(trip_date)=date(date_recorded))
where date(wd.date_recorded)='2013-03-01' limit 10;

#join w/ summary table
select trips,tempi,hum,date(date_recorded) as date_trip_wthr,hour_recorded
from weather_data wd
join bike_summary bs on (trip_hour=hour_recorded and date(trip_date)=date(date_recorded))
order by trips,tempi;

#interesting
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

#get the min and max data and how often weather types occur
mysql> select min(tempi) as min_temp,max(tempi) as max_temp,avg(tempi) as avg_temp,min(hum) as min_hum,max(hum) as max_hum,avg(hum) as avg_hum, min(precipi) as min_precip,max(precipi) as max_precip from weather_data;
+----------+----------+-----------+---------+---------+-----------+------------+------------+
| min_temp | max_temp | avg_temp  | min_hum | max_hum | avg_hum   | min_precip | max_precip |
+----------+----------+-----------+---------+---------+-----------+------------+------------+
|    16.00 |   105.10 | 60.232613 |    9.00 |  100.00 | 66.558899 |   -9999.00 |       1.33 |
+----------+----------+-----------+---------+---------+-----------+------------+------------+

#final approach
establish patterns
seasonality
hourly patterns
weekday/weekend patterns

set some sort of baseline
trips grow every month by x
so accounting for this - impact of weather

