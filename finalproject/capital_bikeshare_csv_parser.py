print 'importing modules'
import csv
import MySQLdb
from datetime import datetime
import re
#import config as cfg

#can we find out the price? it could be interesting to chart money trends.
		
#YYYY-MM-DD
def insert_data(con,cur,rental_list):
	""" inserts the bike share data into a db """
	
	qry = """ INSERT INTO bike_rentals (trip_duration,start_date,end_date,start_station,start_terminal,end_station,
	end_terminal,bike_num,member_type)
	values('%s','%s','%s',"%s",'%s',"%s",'%s','%s','%s') """ % (rental_list[0],rental_list[1], \
	rental_list[2],rental_list[3],rental_list[4],rental_list[5],rental_list[6],rental_list[7],rental_list[8])

	cur.execute(qry)
	con.commit()
	

def date_fmt(date_str):
	"""input a date string and returns a datetime object"""
	
	pos = [n.start() for n in re.finditer(r"/",date_str)]
	space = date_str.find(' ')
	colon = date_str.find(':')
	
	date_obj = datetime(int(date_str[pos[1]+1:pos[1]+5]),int(date_str[0:pos[0]]),int(date_str[pos[0]+1:pos[1]]),int(date_str[space+1:colon]),int(date_str[colon+1:]))
	#date_obj = datetime(int(date_str[6:10]),int(date_str[0:char_pos_list[0]]),int(date_str[3:5]),int(date_str[11:13]),int(date_str[14:16]))
	
	return date_obj


def terminal_fmt(station):
	""" extracts and removes the termainl from a station str"""
	
	terminal = station[station.find('(')+1:station.find(')')]
	station = station[::-1][8:][::-1]
	
	return station,terminal


def parse_csv(con,cur,filename):
	""" input a csv, parse it, process it, return consistent data for a db insert"""
	
	with open(filename) as f:
		reader = csv.reader(f, delimiter=',')
		reader.next()
		for each_line in reader:
			"""print 'trip_duration', each_line[0]
			print 'start_date', each_line[1]
			print 'end_date', each_line[2]
			print 'start_station', each_line[3]
			print 'end_station', each_line[4]
			print 'bike_num', each_line[5]
			print 'member_type', each_line[6]"""
			'1/1/2011 0:00'
			
			each_line = [each.strip() for each in each_line]
			
			#parsing logic for inconsistent csv structure
			# <3 data inconsistency
			try:
				if filename[70:] in ['2012-1st-quarter.csv','2012-2nd-quarter.csv']:
					start_date = date_fmt(each_line[2])
					end_date = date_fmt(each_line[5])
				
					line = [each_line[0],start_date,end_date,each_line[3],each_line[4],each_line[6],each_line[7],each_line[8],each_line[9]]
					#return line
					insert_data(con,cur,line)
			
				elif filename[70:] in ['2010-4th-quarter.csv','2011-1st-quarter.csv','2011-2nd-quarter.csv','2011-3rd-quarter.csv','2011-4th-quarter.csv']:
					start_date = date_fmt(each_line[1])
					end_date = date_fmt(each_line[2])
					start_station,start_terminal = terminal_fmt(each_line[3])
					end_station,end_terminal = terminal_fmt(each_line[4])
				
					line = [each_line[0],start_date,end_date,start_station,start_terminal,end_station,end_terminal,each_line[5],each_line[6]]
					#return line
					insert_data(con,cur,line)
					
				else:
					start_date = date_fmt(each_line[1])
					end_date = date_fmt(each_line[4])
				
					line = [each_line[0],start_date,end_date,each_line[2],each_line[3],each_line[5],each_line[6],each_line[7],each_line[8]]
					#return line
					insert_data(con,cur,line)
					
			except Exception, ie:
					print 'houston, we have a problem: ', ie
					print 'filename: ', filename
					print 'data: ', each_line
					
		#return line


def init_db():
	""" instantiate and return the db and cur objects"""
	
	#con = MySQLdb.connect(host=cfg.host,user=cfg.user,passwd=cfg.pwd,db=cfg.db,port=3306)
	con = MySQLdb.connect(user='',passwd='',db='test')
	cur = con.cursor()
	
	return con,cur


def main():
	
	#runtime: ~24 mins for 4.1M records
	#list of filenames for iteration - could use os module for this
	dir_ = "/Users/kperko/work/data-science-class/GADataScience/finalproject/data/"
	filename = ['2010-4th-quarter','2011-1st-quarter','2011-2nd-quarter','2011-3rd-quarter','2011-4th-quarter', 
	'2012-1st-quarter','2012-2nd-quarter','2012-3rd-quarter','2012-4th-quarter','2013-1st-quarter','2013-2nd-quarter']
	ext = '.csv'
	
	try:
	#connect to the db and instantiate a connection and cursor obj
		con,cur = init_db()
		
		print 'loading data'
		
		for each_file in filename:
			each_file_path = dir_+each_file+ext
			parse_csv(con,cur,each_file_path)
			#insert_data(con,cur,parse_csv(each_file_path))
			
	except Exception, exc:
		print 'exception issued: ', exc

if __name__ == "__main__":
	main()