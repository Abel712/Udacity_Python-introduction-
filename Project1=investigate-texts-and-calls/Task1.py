#!/usr/bin/python
#_*_ coding:utf8 _*_

#My result:
#There are 570 different telephone numbers in the records.

import csv
with open('texts.csv', 'r') as f:
    reader = csv.reader(f)
    texts = list(reader)

with open('calls.csv', 'r') as f:
    reader = csv.reader(f)
    calls = list(reader)

def diff_number_counter(input_texts_list,input_calls_list):
	#def_var area:
	diff_number_list = []
	for i in input_texts_list:
		diff_number_list.append(i[0])
		diff_number_list.append(i[1])
	for i in input_calls_list:
		diff_number_list.append(i[0])
		diff_number_list.append(i[1])
	diff_number_square = set(diff_number_list)
	diff_number_counter_result = "There are {} different telephone numbers in the records.".format(len(diff_number_square))
	return diff_number_counter_result

print(diff_number_counter(texts,calls))
