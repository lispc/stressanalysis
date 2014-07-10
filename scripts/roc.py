f = 0
t = 0
fp = 0
fn = 0
tp = 1
tn = 1
lineno = 0
for l in open("tail_roc"):
	lineno += 1
	v = l.rstrip().split()[0]
	pre = float(l.rstrip().split()[1])
	if v == '-1':
		if pre>0:
			fp += 1
		else:
			tn += 1
	elif v == '+1':
		if pre>0:
			tp += 1
		else:
			fn += 1
	else:
		print "err",v
	print float(fp+tn)/(18576.0),float(tp+fn)/(28426.0)
'''
predict 13645 minus
predict 33357 pos
fact 28426 pos
fact 18576 pos
'''
