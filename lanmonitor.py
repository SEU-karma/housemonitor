import sys
import time
import commands
from datetime import datetime
from db import *
import logging
from  logging.config import fileConfig
import json
fileConfig('./conf/log_config.ini')
logger=logging.getLogger('root')

def gettime():
	rawtime = datetime.now()
	scantime  = rawtime.replace(microsecond = 0, second = 0, minute = rawtime.minute-rawtime.minute%10)
	return scantime.strftime('%Y-%m-%d %H:%M:%S')


mac2user = {'FC:E9:98:96:9E:84':'gerundong-iphone','34:AB:37:16:2E:09':'sunlili-ipad', '24:A0:74:22:7D:A5':'lixianghui-ipad','68:DB:CA:E0:34:29':'sunlili-iphone', '70:81:EB:EC:FF:C0':'lixianghui-iphone','78:EB:14:91:A8:0E':'router','34:AB:37:0F:F6:42':'gerundong-ipad', '08:10:75:B5:8B:DE':'gerundong-pc'}
rawdata =  commands.getoutput('nmap -sn 192.168.1.1/24 | grep \'MAC Address\'').split('\n')
m_time = gettime()

recorddata = {}
recorddata['usernum'] = 0
recorddata['usermac'] = []
recorddata['username'] = []
recorddata['hitcount'] = []
oldrecord = None
try:
	oldrecord = Lan.get(Lan.time == m_time)
except Lan.DoesNotExist:
	oldrecord = None
if oldrecord:
	recorddata = json.loads(oldrecord.user)
	oldrecord.delete_instance()
for item in rawdata:
	m_macaddr = item.split(' ')[-2]
	if m_macaddr in recorddata['usermac']:
		index = recorddata['usermac'].index(m_macaddr)
		recorddata['hitcount'][index] = recorddata['hitcount'][index] + 1
		continue
	m_devname = mac2user.has_key(m_macaddr) and mac2user[m_macaddr] or 'unknown'
	recorddata['usernum'] = recorddata['usernum'] + 1
	recorddata['usermac'].append(m_macaddr)
	recorddata['username'].append(m_devname)
	recorddata['hitcount'].append(1)
try:
	q = Lan.insert(user = json.dumps(recorddata), lanid = '304', time = m_time)
	q.execute()
except Exception ,e:
	logger.info('fail to write db' + e)
	exit()
logger.info('write db success')



		



