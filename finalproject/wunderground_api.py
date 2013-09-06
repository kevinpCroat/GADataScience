import urllib2
import StringIO
import csv
import MySQLdb
from datetime import datetime,timedelta
from dateutil import rrule
import json
#import config as cfg

#########
# 500 API CALLS PER DAY LIMIT !!!!!
########


#api call example - forecast data
#http://api.wunderground.com/api/cc09f62cc7b75ff4/hourly/q/CA/San_Francisco.json
#docs:
#http://www.wunderground.com/weather/api/d/docs?d=resources/phrase-glossary

#predict_url = 'http://api.wunderground.com/api/cc09f62cc7b75ff4/hourly/q/DC/Washington.json'

def get_date_list(num_of_days,*args):
	"""builds a date list off a specified start date using the num_of_days variable"""
	#args is a list of the start date
	#the format for this is [YYYY,MM,DD]
	#num_of_days is an int that specifies the number of days to generate after (or before the start date)
	#these days will be appened to a date_list that is returned
	
	#empty date_list
	date_list = []
	
	#turn the start_date list into a datetime object
	start_date = datetime(args[0][0],args[0][1],args[0][2]).date()

	# generate the dates with a list comprehension
	date_list = [start_date + timedelta(days=x) for x in range(0,num_of_days)]
	
	#function output is the resulting date_list
	return date_list


def init_db(cur,con,**kwargs):
	pass
	
def insert_into_db(cur,con,*args):
	
	db.executemany("REPLACE INTO " + table + " (" + ",".join(cols) + ") " + 
	    "values (" + ",".join(["%s"] * len(cols)) + ")",
	    [tuple(row[col] for col in cols) for row in data])
	
	db.commit()

def parse_dict_every_hr(weather_dict,date):

	local_weather_dict = {}
	
	#setup the values we are interested in
	weather_key_list = ['icon','conds','tempi','dewpti','hum','wspdi','visi','pressurei','precipi','fog','rain','hail','thunder','tornado']
	
	#segment the dict to just get the history section
	weather_dict = weather_dict['history']
	
	data = []
	another_list = []

	try:
		print 'date', date
		for each in weather_dict['observations']:
			
			print '*****'
			
			print 'HOUR', each['date']['hour']
			each_hour = each['date']['hour']
			#data.append(each['date']['hour'])
			
			print '#######'
			for k,v in each.iteritems():
				if k in weather_key_list:
					print k,v
					#data.append({k:v})
				#data.append({each_hour:{k:v}})
					data.append({'date':date, 'hour':each_hour,k:v })
		
		#print data
		return data

	except Exception, exc:
		print 'raise the roof. or not.'


def main():
	#put this in a config file
	API_KEY = 'cc09f62cc7b75ff4'
	
	#lets build the date_list using our start_date and the range we want to generate it for
	date_list = get_date_list(1,[2010,12,31])
	
	for date in date_list:
		history_api_url = "http://api.wunderground.com/api/%s/history_%s/q/DC/Washington.json" % (API_KEY,date.strftime("%Y%m%d"))
		response = urllib2.urlopen(history_api_url).read()
		
		
		weather_dict = json.loads(response)
		data = parse_dict_every_hr(weather_dict,date)
		
		print data
		
		#insert data into db
		#compose a data structure
		#dict		

if __name__ == "__main__":
	main()

		
		
		
