from datetime import *
import json
from db import *






user_identity = {
					'gerundong-ipad':{'user':'gerundong', 'threshold': 7},
					'gerundong-iphone':{'user':'gerundong', 'threshold': 0},
					'lixianghui-ipad':{'user':'lixianghui', 'threshold': 7},
					'lixianghui-iphone':{'user':'lixianghui', 'threshold': 0},
					'sunlili-ipad':{'user':'sunlili', 'threshold': 7},
					'sunlili-iphone':{'user':'sunlili', 'threshold': 0},
				
				}


#replace with memcached later
def getdbdata(lanid, begin, end):
	result = {}
	for record in Lan.select().where(((Lan.time >= begin) & (Lan.time <= end))):
		result[record.time.strftime("%Y-%m-%d %H:%M:%S")] = json.loads(record.user)
	return result

def get_one_week_userdata_tenmin(lanid, username, begin):
	begindate = begin.replace(microsecond = 0, second = 0, minute =0, hour=0)
	enddate = begindate + timedelta(days = 6, hours = 23, minutes = 50)
	result = {}
	result['begin'] = begindate.strftime('%Y-%m-%d %H:%M:%S')
	result['end'] = enddate.strftime('%Y-%m-%d %H:%M:%S')
	result['username'] = username 
	dbdata = getdbdata(lanid, begindate, enddate)
	for index in range(0,6*24*7):
		t = (begindate + timedelta(minutes = 10) * index).strftime('%Y-%m-%d %H:%M:%S')
		totalhit = 0
		if not dbdata.has_key(t):
			result[t] = 0
			continue
		for i,v in enumerate(dbdata[t]['username']):
			if not user_identity.has_key(v):
				continue
			user = user_identity[v]['user']
			threshold = user_identity[v]['threshold']
			if user != username:
				continue
			hitcount = dbdata[t]['hitcount'][i]
			if hitcount < threshold:
				hitcount = 0
			totalhit = hitcount + totalhit
		result[t] = totalhit
	return result


def merge2halfhour(rawdata):
	result = {}
	result['username'] = rawdata['username']
	result['begin'] = rawdata['begin']
	result['end'] = (datetime.strptime(rawdata['end'], ('%Y-%m-%d %H:%M:%S')) + timedelta(minutes = 30, hours = 23)).strftime('%Y-%m-%d %H:%M:%S') 
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
	
def getweek(lanid, username, begin):
	begin = datetime.strptime('2017-02-20 00:00:00', ('%Y-%m-%d %H:%M:%S'))
	return json.dumps(merge2halfhour(get_one_week_userdata_tenmin('304', username, begin)))

if __name__ == "__main__":

	print (getweek('304', 'gerundong', 1))
