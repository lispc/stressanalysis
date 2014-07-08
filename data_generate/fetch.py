#! /usr/bin/python
import pymongo
import sys
ip = "166.111.139.100"
cli = pymongo.MongoClient(ip)
table = cli.weibo_ajay.weibo_status_3_11_update
cnt = 0
limit = 1700000
#ofile = sys.stdout
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

