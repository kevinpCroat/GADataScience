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
	
def sql_insert(weather_dict):

	BATCH_SIZE = 10000
	NUM_BATCHES = len(weather_dict)/BATCH_SIZE
	REST_OF_ROWS = len(weather_dict) % BATCH_SIZE
	assert NUM_BATCHES*BATCH_SIZE+REST_OF_ROWS == len(result_set)

	for i in range(0, NUM_BATCHES):
		list_of_tuples = []
		low = i*BATCH_SIZE
		high = i*BATCH_SIZE+BATCH_SIZE

		for row in result_set[low:high]:
			list_of_tuples.append((row['month'], row['event_id'], row['uid'],row['u_created_date'],row['e_created_date'],\
			row['published'],row['end_date'],row['current_status'],row['password'],row['listed'],\
			row['locale'],row['currency'],row['referral_code'],row['channels'],row['channels_2'],\
			MySQLdb.escape_string(row['tags']),row['city'],row['state'],row['country'],row['postal_code'],\
			row['paid_buyers'],row['free_buyers'],row['paid_tix'],row['free_tix'],row['gts'],\
			row['gtf'],row['ntf'],row['ebfees'],row['salesrep']))

			SQL = """INSERT INTO fin_events_month \
	         	(month, event_id, uid,u_created_date,e_created_date,\
				published,end_date,current_status,password,listed,\
				locale,currency,referral_code,channels,channels_2,\
				tags,city,state,country,postal_code,\
				paid_buyers,free_buyers,paid_tix,free_tix,gts,\
				gtf,ntf,ebfees,salesrep)
	         	values (%s,%s,%s,%s,%s,\
						%s,%s,%s,%s,%s,\
						%s,%s,%s,%s,%s,\
						%s,%s,%s,%s,%s,\
						%s,%s,%s,%s,%s,\
						%s,%s,%s,%s)"""
		c_analytics.executemany(SQL, list_of_tuples)

	    #### Now get the remaining rows:
	list_of_tuples = []
	for row in result_set[-REST_OF_ROWS:]:
		list_of_tuples.append((row['month'], row['event_id'], row['uid'],row['u_created_date'],row['e_created_date'],\
		row['published'],row['end_date'],row['current_status'],row['password'],row['listed'],\
		row['locale'],row['currency'],row['referral_code'],row['channels'],row['channels_2'],\
		MySQLdb.escape_string(row['tags']),row['city'],row['state'],row['country'],row['postal_code'],\
		row['paid_buyers'],row['free_buyers'],row['paid_tix'],row['free_tix'],row['gts'],\
		row['gtf'],row['ntf'],row['ebfees'],row['salesrep']))

		SQL = """INSERT INTO fin_events_month \
	     	(month, event_id, uid,u_created_date,e_created_date,\
			published,end_date,current_status,password,listed,\
			locale,currency,referral_code,channels,channels_2,\
			tags,city,state,country,postal_code,\
			paid_buyers,free_buyers,paid_tix,free_tix,gts,\
			gtf,ntf,ebfees,salesrep)
	     	values (%s,%s,%s,%s,%s,\
					%s,%s,%s,%s,%s,\
					%s,%s,%s,%s,%s,\
					%s,%s,%s,%s,%s,\
					%s,%s,%s,%s,%s,\
					%s,%s,%s,%s)"""

	c_analytics.executemany(SQL, list_of_tuples)
	#commit the changes to the db
	db_analytics.commit()
	
def insert_data(con,cur,dict_w):
	qry = """ INSERT INTO weather_data (city,icon,conds,tempi,dewpti,hum,wspdi,pressurei,precipi,fog,rain,hail,thunder,
	tornado,date_recorded,hour_recorded)
	values('%s','%s','%s',%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,'%s',%s) """ % ('Washington DC', dict_w['icon'],dict_w['conds'],dict_w['tempi'],dict_w['dewpti'],\
	dict_w['hum'],dict_w['wspdi'],dict_w['pressurei'],dict_w['precipi'],dict_w['fog'],dict_w['rain'],dict_w['hail'],\
	dict_w['thunder'],dict_w['tornado'],dict_w['date'],dict_w['hour'])
	
	cur.execute(qry)
	con.commit()

def parse_dict_every_hr(con,cur,weather_dict,date):

	local_weather_dict = {}
	
	#setup the values we are interested in
	weather_key_list = ['icon','conds','tempi','dewpti','hum','wspdi','visi','pressurei','precipi','fog','rain','hail','thunder','tornado','snow']
	neg_weather_key_list = ['heatindexm','windchillm','wdire','wdird','windchilli','heatindexi','pressurem','precipm','tempm','dewptm','utcdate',\
	'wspdm','wgusti','metar','vism','wgustm']
	#segment the dict to just get the history section
	weather_dict = weather_dict['history']

	try:
		print 'date', date
		for each in weather_dict['observations']:
			
			print '*****'
			
			print 'HOUR', each['date']['hour']
			#each_hour = each['date']['hour']
			#data.append(each['date']['hour'])
			
			print '#######'
			#print each
			
			each['hour']=each['date']['hour']
			each['date']=date
			
			for key in neg_weather_key_list:
				del each[key]
				
			#for k,v in each.iteritems():
				#if k in weather_key_list:
					#print k,v
					#data.append({k:v})
			#print '######'
				#data.append({each_hour:{k:v}})
					#data.append({'date':date, 'hour':each_hour,k:v })
					
			#for k in each.iterkeys():
				#if k in weather_key_list:
					
			print each
			print '***'
			insert_data(con,cur,each)
		
		#print data
		#return each

	except Exception, exc:
		print 'raise the roof. or not.'
		print exc


def main():
	#put this in a config file
	API_KEY = 'cc09f62cc7b75ff4'
	
	con = MySQLdb.connect(user='',passwd='',db='test')
	cur = con.cursor()
	
	#lets build the date_list using our start_date and the range we want to generate it for
	date_list = get_date_list(500,[2010,12,31])
	
	for date in date_list:
		history_api_url = "http://api.wunderground.com/api/%s/history_%s/q/DC/Washington.json" % (API_KEY,date.strftime("%Y%m%d"))
		response = urllib2.urlopen(history_api_url).read()
		
		
		weather_dict = json.loads(response)
		print parse_dict_every_hr(con,cur,weather_dict,date)
		
		#insert data into db
		#compose a data structure
		#dict		

if __name__ == "__main__":
	main()

		
		
		
