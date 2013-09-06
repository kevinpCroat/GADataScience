create table bike_rentals (
	row_id int not null auto_increment,
	trip_duration char(8) default null,#HH:MM:SS
	start_date datetime default null,
	end_date datetime default null,
	start_station varchar(255) default null,
	end_station varchar(255) default null,
	bike_num varchar(20) default null,
	member_type varchar(10), #Registered - annual or Monthly or Casual 1 to 5 day member
	primary key(row_id),
	index(duration),
	index(start_date),
	index(end_date),
	index(start_station),
	index(end_station),
	index(member_type) 
	);
	

drop table if exists weather_data;
create table weather_data (
	row_id int not null auto_increment primary key,
	city varchar(200) default null,
	icon varchar(200) default null,
	conds varchar(200) default null,
	tempi decimal(5,2) default null,
	dewpti decimal(5,2) default null,
	hum decimal(5,2) default null,
	wspdi decimal(5,2) default null,
	pressurei decimal(5,2) default null,
	precipi decimal(6,2) default null,
	-- pop decimal(5,2) default null,
	fog tinyint(1) default null,
	rain tinyint(1) default null,
	hail tinyint(1) default null,
	thunder tinyint(1) default null,
	tornado tinyint(1) default null,
	date_recorded datetime not null,
	hour_recorded int not null,
	date_created datetime DEFAULT CURRENT_TIMESTAMP,
	date_modified datetime default null
	);