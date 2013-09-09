import MySQLdb

def init_db():
	""" instantiate and return the db and cur objects"""
	
	#con = MySQLdb.connect(host=cfg.host,user=cfg.user,passwd=cfg.pwd,db=cfg.db,port=3306)
	con = MySQLdb.connect(user='',passwd='',db='test')
	cur = con.cursor()
	
	return con,cur
	
def extract_rows(cur,year):
	qry = """ select row_id,trip_duration from bike_rentals where year(start_date) = %s""" % year
	cur.execute(qry)
	result = cur.fetchall()
	
	return result
	
def convert_str_to_int(row_id,trip_duration):
	""" converts the string version of 0h 0m 0s to an int that represents time in seconds"""
	
	hour = trip_duration[0:trip_duration.find('h')]
	minute = trip_duration[trip_duration.find(' ')+1:trip_duration.find('m')]
	sec_slice = trip_duration[trip_duration.find(' ')+1:]
	sec = sec_slice[sec_slice.find(' ')+1:sec_slice.find('s')]
	
	hour = int(hour) * 3600
	minute = int(minute) * 60
	total_seconds = hour + minute + int(sec)
	
	#print 'hms: ', hour, minute, sec
	return row_id,total_seconds
	
def update_rows(con,cur,row_id,total_seconds):
	
	qry = """ INSERT IGNORE INTO bike_rentals (row_id,trip_duration_seconds)
	values (%s,%s)
	ON DUPLICATE KEY UPDATE trip_duration_seconds=VALUES(trip_duration_seconds) """ % (row_id,total_seconds)
	
	cur.execute(qry)
	con.commit()
	


def main():
	#runtime: 2264.96 seconds
	con,cur = init_db()
	
	year = ['2010','2011','2012','2013']
	
	for each_yr in year:
		result = extract_rows(cur,each_yr)
	
		for each in result:
			row_id,total_seconds = convert_str_to_int(each[0],each[1])
			update_rows(con,cur,row_id,total_seconds)


if __name__=="__main__":
	main()