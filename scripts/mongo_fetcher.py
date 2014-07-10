#! /usr/bin/python
import pymongo
import sys
import subprocess
import signal
import os
ip = "166.111.139.96"
cli = pymongo.MongoClient(ip)
table = cli.weibo_Test.weibo_status
class Alarm(Exception):
    pass
def alarm_handler(signum, frame):
    raise Alarm
signal.signal(signal.SIGALRM, alarm_handler)
def get_weibo_by_uid(uid,limit=100,timeout=10,min_limit=50):#TODO min_limit
	if table.find({"user.id":uid}).count() >= min_limit:
		return list(table.find({"user.id":uid}).limit(limit))
	devnull = open(os.devnull,"wb")
	signal.alarm(timeout)
	try:
		p = subprocess.Popen(['java', '-jar', '../WeiboCrawler/WeiboCrawler_fat.jar', str(uid)],stdout=devnull,stderr=devnull,shell=False)
		p.wait()
		signal.alarm(0)  # reset the alarm
	except Alarm:
		print "timeout"
		pass
	#return [item for item in table.find({"user.id":uid}).limit(limit)]
	return list(table.find({"user.id":uid}).limit(limit))
if __name__ == "__main__":
	uid = 2696095571
	if len(sys.argv) == 2:
		uid = int(sys.argv[1])
	print get_weibo_by_uid(uid,2,100)
'''
ofile = open("all","w")
for item in table.find():
	try:
		cnt += 1
		if cnt>=limit:
			break
		if item.get('retweeted_status'):
			continue
		ofile.write(str(item['user']['id'])+'\t')
		ofile.write(item['text'].encode('utf-8'))
		ofile.write('\t'+item['created_at']+'\n')
	except:
		print >>sys.stderr,item
ofile.close()
'''

