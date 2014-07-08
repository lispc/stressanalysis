#! /usr/bin/python
# -*- coding: utf-8 -*-
import arff
import json
import jieba
import re
import codecs
from collections import defaultdict
def init_dict(fname):
	ifile = codecs.open(fname,'r','utf-8-sig')
	#feature_desc = {}
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
			#feature_desc[int(k)]=v
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
def get_word_type_vec(text,verbose=False):
	if verbose:
		freq = defaultdict(list)
	else:
		freq = defaultdict(int)
	for item in jieba.cut(text):
		if item in liwc:
			for fid in liwc[item]:
				if verbose:
					freq[fid].append(item)
				else:
					freq[fid] += 1
	return freq
def analyze(text):
	t = re.sub('#.*#','',text)
	vec = get_word_type_vec(t)
	return [vec[fid] if fid in vec else 0 for fid in feature_id]
def get_arff():
	pos_f = '../../clean_data/pos.dat'
	neg_f = '../../clean_data/neg.dat'
	data = []
	for l in open(pos_f):
		data.append([True]+analyze(l.strip()))
	for l in open(neg_f):
		data.append([False]+analyze(l.strip()))
	arff.dump('data.arff',data,relation='stress',names=['is_stress']+feature_name)

sample_text = '身边有无数的圈子。大大小小。但…自己却无论哪个圈子都无法走进…因为怕。害怕会被讨厌。我知道自己的病却又无法拯救自己…。我…到底在渴求着什么。#消沉#强迫症#社交障碍#' 

if __name__ == "__main__":
	#freq = get_word_type_vec(sample_text,True)
	#for k in freq:
	#	print feature_desc[k],":",','.join(freq[k])
	get_arff()
