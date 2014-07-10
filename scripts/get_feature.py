#! /usr/bin/python
# -*- coding: utf-8 -*-
import arff
import sys
import json
import jieba
import re
import codecs
from collections import defaultdict
import liblinearutil as svm
sample_text = '身边有无数的圈子。大大小小。但…自己却无论哪个圈子都无法走进…因为怕。害怕会被讨厌。我知道自己的病却又无法拯救自己…。我…到底在渴求着什么。#消沉#强迫症#社交障碍#' 
def init_dict(fname):
	ifile = codecs.open(fname,'r','utf-8-sig')
	features = []
	liwc = {}
	header = 0
	for l in ifile:
		l = l.rstrip()
		if l == '%':
			header = 1 - header
			continue
		if header == 1:
			k,v = l.split('\t')
			features.append((int(k),v))
			continue
		if header == 0:
			segs = l.split('\t')
			liwc[segs[0]] = map(int,segs[1:])
			continue
	return features,liwc
features,liwc = init_dict("../dict/TextMind.txt")
feature_desc = dict(features)
feature_name = [desc for i,desc in features]
feature_id = [i for i,desc in features]
def init_model(filename="liblinear.model"):
	return svm.load_model(filename)
#model = init_model()
def get_word_type_vec(text,verbose=False):
	token_num = 0
	if verbose:
		freq = defaultdict(list)
	else:
		freq = defaultdict(int)
	for item in jieba.cut(text):
		token_num += 1
		if item in liwc:
			for fid in liwc[item]:
				if verbose:
					freq[fid].append(item)
				else:
					freq[fid] += 1
	return freq,token_num
def analyze(text):
	t = re.sub('#.*?#','',text)
	vec,token_num = get_word_type_vec(t)
	total = token_num
	if total == 0:
		return None
	return [1.0/total]+[vec[fid]/float(total) if fid in vec else 0 for fid in feature_id]
pos_f = '../../clean_data/pos.dat'
neg_f = '../../clean_data/neg.dat'
def get_arff_and_svm():
	data = []
	for l in open(pos_f):
		fvec = analyze(l.strip())
		if fvec:
			data.append(fvec+[True])
	for l in open(neg_f):
		fvec = analyze(l.strip())
		if fvec:
			data.append(fvec+[False])
	arff.dump('data.arff',data,relation='stress',names=['token_num']+feature_name+['is_stress'])
	svm_ofile = open("data.svm","w")
	for ins in data:
		line = "+1 " if ins[-1] else "-1 "
		dict_line = [str(index+1)+":"+str(ins[index]) for index in range(0,len(ins)-1) if ins[index]!=0]
		svm_ofile.write(line+" ".join(dict_line)+"\n")
	svm_ofile.close()
def prefict_from_text(text=sample_text):
	res = svm.predict([],[analyze(text)],model)
	print res
	return res[2][0][0]/2+0.5
if __name__ == "__main__":
	get_arff_and_svm()
	#if len(sys.argv) == 2:
	#	print prefict_from_text(sys.argv[1])
	#else:
	#	print prefict_from_text()
