import csv
import MySQLdb
import config as cfg

#can we find out the price? it could be interesting to chart money trends.

def get_bike_data():
	#get the csv data
	base_url='http://www.capitalbikeshare.com/assets/files/trip-history-data/'
	ext = '.csv'

	url_list = ['2010-4th-quarter','2011-1st-quarter','2011-2nd-quarter','2011-3rd-quarter','2011-4th-quarter', 
	'2012-1st-quarter','2012-2nd-quarter','2012-3rd-quarter','2012-4th-quarter','2013-1st-quarter','2013-2nd-quarter']

	#convert duration to HH:MM:SS
	
	#example row
	#['0h 28min. 26sec.', '11/21/2010 13:56', '11/21/2010 14:24', 'Georgia & New Hampshire Ave NW (31400)', 'Massachusetts Ave & Dupont Circle NW (31200)', 'W00830', 'Casual']
	#rental_duration,checkout_time,return_time,rental_location,return_location,bike_number,rider_type

	rental_duration_list = []

	for each_url in url_list:
		csv_url = base_url+each_url+ext
		response = urllib2.urlopen(csv_url).read()
		output = StringIO.StringIO(response)
		data = csv.reader(output)
	
		for each_row in data:
			rental_duration_list.append(each_row[0])
		
		
		print 'number of records', len(rental_duration_list)
		

		
def parse_csv(filename):
	num_rentals = 0
	with open(filename) as f:
		reader = csv.reader(f, delimiter=',')
		for each_line in reader:
			num_rentals +=1
			#print each_line
		"""	print 'trip_duration', each_line[0]
			print 'start_date', each_line[1]
			print 'end_date', each_line[2]
			print 'start_station', each_line[3]
			print 'end_station', each_line[4]
			print 'bike_num', each_line[5]
			print 'member_type', each_line[6]"""
			return each_line[0],each_line[1],each_line[2],each_line[3],each_line[4],each_line[5],each_line[6]
	#return num_rentals
	
def init_db():
	con = MySQLdb.connect(host=cfg.host,user=cfg.user,pwd=cfg.pwd,port=3306)
	cur = con.cursor()
	
	return con,cur
	
def insert_into_db(*args):
	qry = """ insert into"""
	
	sql.

def main():
	#lsetup the dir struct
	#list of filenames for iteration - could use os module for this
	dir_ = "/Users/kperko/work/data-science-class/GADataScience/finalproject/data/"
	filename = ['2010-4th-quarter','2011-1st-quarter','2011-2nd-quarter','2011-3rd-quarter','2011-4th-quarter', 
	'2012-1st-quarter','2012-2nd-quarter','2012-3rd-quarter','2012-4th-quarter','2013-1st-quarter','2013-2nd-quarter']
	ext = '.csv'
	
	#connect to the db and instantiate a connection and cursor obj
	con,cur = init_db()
	
	total_rentals = 0
	for each_file in filename:
		each_file_path = dir_+each_file+ext
		insert_into_db(parse_csv(each_file_path))
		#print each_file, rentals
		#total_rentals += rentals
	#print 'total_rentals', total_rentals
	
if __name__ == "__main__":
	main()