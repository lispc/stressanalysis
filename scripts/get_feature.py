#! /usr/bin/python
# -*- coding: utf-8 -*-
import arff
import json
import jieba
import codecs
from collections import defaultdict
def init_dict(fname):
	ifile = codecs.open(fname,'r','utf-8-sig')
	feature_desc = {}
	liwc = {}
	header = 0
	for l in ifile:
		l = l.rstrip()
		if l == '%':
			header = 1 - header
			continue
		if header == 1:
			k,v = l.split('\t')
			feature_desc[int(k)]=v
			continue
		if header == 0:
			segs = l.split('\t')
			liwc[segs[0]] = map(int,segs[1:])
			continue
	return feature_desc,liwc
feature_desc,liwc = init_dict("../dict/TextMind.txt")
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
sample_text = '身边有无数的圈子。大大小小。但…自己却无论哪个圈子都无法走进…因为怕。害怕会被讨厌。我知道自己的病却又无法拯救自己…。我…到底在渴求着什么。#消沉#强迫症#社交障碍#' 
if __name__ == "__main__":
	freq = get_word_type_vec(sample_text,True)
	for k in freq:
		print feature_desc[k],":",','.join(freq[k])
