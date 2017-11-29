#!/usr/bin/python
#_*_ coding:utf8 _*_

#My result:
#(080)33251027 spent the longest time, 90456 seconds, on the phone during September 2016.

import csv
with open('texts.csv', 'r') as f:
    reader = csv.reader(f)
    texts = list(reader)

with open('calls.csv', 'r') as f:
    reader = csv.reader(f)
    calls = list(reader)

def number_during_time_max(input_calls_list):
	#def_var area:
	number_during_time = {}
	cache_spent_time = 0
	feedback_cache_number = ""
	feedback_cache_time = ""
	#step1:create a dict include number and number's spent time.
	for i in input_calls_list:
		if i[0] not in number_during_time:
			number_during_time[i[0]] = i[3]
			#print(number_during_time)
		elif i[0] in number_during_time:
			number_during_time[i[0]] = str(int(number_during_time[i[0]]) + int(i[3]))
		if i[1] not in number_during_time:
			number_during_time[i[1]] = i[3]
		elif i[1] in number_during_time:
			number_during_time[i[1]] = str(int(number_during_time[i[1]]) + int(i[3]))
	#step2:get the max dict's values by loop dict.
	for i_keys,i_values in number_during_time.items():
		if int(i_values) >= cache_spent_time:
			cache_spent_time = int(i_values)
			feedback_cache_number = i_keys
			feedback_cache_time = i_values
	#step3:feedback result for return part.
	feedback_string = "{} spent the longest time, {} seconds, on the phone during September 2016.".format(feedback_cache_number,feedback_cache_time)
	return feedback_string

print(number_during_time_max(calls))
