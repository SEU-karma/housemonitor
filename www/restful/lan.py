from datetime import *
import json
from db import *


#replace with memcached later
def getdbdata(lanid, bengin, end):
	result = {}
	for record in Lan:
		result[record.time.strftime("%Y-%m-%d %H:%M:%S")] = json.loads(record.user)
	return result




def getrawdata(selectedday):
	formatday = selectedday.replace(microsecond = 0, second = 0, minute =0, hour=0)
	week = int(formatday.strftime("%W")) + 1
	weekday = int(formatday.strftime("%w"))
	monday = (weekday == 0) and formatday - timedelta(days = 6) or formatday - timedelta(days = weekday - 1) 
	sunday = monday + timedelta(days = 6)
	result = {}
	result['begin'] = monday.strftime('%Y-%m-%d %H:%M:%S')
	result['end'] = sunday.strftime('%Y-%m-%d %H:%M:%S')
	result['week'] = week

	dbdata = getdbdata(1,1,1)
	for index in range(0,6*24*7):
		#result[str(index)] = {'t':(monday + timedelta(minutes = 10) * index).strftime('%Y-%m-%d %H:%M:%S'), 'v':0}	
		t = (monday + timedelta(minutes = 10) * index).strftime('%Y-%m-%d %H:%M:%S')
		totalhit = 0
		if not dbdata.has_key(t):
			result[t] = 0
			continue
		for userindex in range(0,dbdata[t]['usernum']):
			totalhit = dbdata[t]['hitcount'][userindex] + totalhit
		totalhit = totalhit >= 15 and totalhit -15 or 0
		result[t] = totalhit 
	return result

def merge2halfhour(rawdata):
	result = {}
	result['begin'] = rawdata['begin']
	result['end'] = (datetime.strptime(rawdata['end'], ('%Y-%m-%d %H:%M:%S')) + timedelta(minutes = 30, hours = 23)).strftime('%Y-%m-%d %H:%M:%S') 
	result['week'] = rawdata['week']
	begin = datetime.strptime(rawdata['begin'], ('%Y-%m-%d %H:%M:%S')) 
	v = 0
	for index in range(0,6*24*7):
		t = (begin + timedelta(minutes = 10) * index).strftime('%Y-%m-%d %H:%M:%S')
		v = rawdata[t] + v
		if index % 3 == 2:
			formatt = (begin + timedelta(minutes = 10) * (index -2)).strftime('%Y-%m-%d %H:%M:%S') 
			result[str(index/3)] = {'t':formatt, 'v':v}
			v = 0 
	return result
	
def getweek(selectedday):
	result = merge2halfhour(getrawdata(selectedday))
	return json.dumps(merge2halfhour(getrawdata(selectedday)))

if __name__ == "__main__":

	print getweek(datetime.now())
