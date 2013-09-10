import urllib2
import json

url_sf = "http://bayareabikeshare.com/stations/json"

response = urllib2.urlopen(url_sf).read()

bike_data = json.loads(response)

#get the dict's keys
for k in bike_data.iterkeys():
	print k
	
#stationBeanList is what we want

#its a list
type(tester['stationBeanList'])

#examine it
# oh my a list of a dicts with tuples as the values
bike_data['stationBeanList'][0]

bike_key_list = []

#get the keys. again.
for k in bike_data['stationBeanList'][0].iterkeys():
	print k
	bike_key_list.append(k)
	
#which keys are we interested in?
#['availableDocks','totalDocks','city','longitude','latitude', \
#'statusValue','testStation','stAddress1','stationName','availableBikes','location']

#this lets us put a station on the map. figure out how many bikes are available.
#we can also give it a name