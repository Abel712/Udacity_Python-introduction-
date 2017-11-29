#!/usr/bin/python
#_*_ coding:utf8 _*_

#My result:
"""
The numbers called by people in Bangalore have codes:
022
040
04344
044
04546
0471
080
0821
7406
7795
7813
7829
8151
8152
8301
8431
8714
9008
9019
9035
9036
9241
9242
9341
9342
9343
9400
9448
9449
9526
9656
9738
9740
9741
9742
9844
9845
9900
9961
24.81 percent of calls from fixed lines in Bangalore are calls to other fixed lines in Bangalore.
"""

import csv
with open('texts.csv', 'r') as f:
    reader = csv.reader(f)
    texts = list(reader)
with open('calls.csv', 'r') as f:
    reader = csv.reader(f)
    calls = list(reader)

def number_called_by_bangalore(input_csv):
	#def_var area:
	number_called_by_bangalore_list = []
	#step1:create a list that get all number head.
	for i in input_csv:
		if "(080)" in i[0]:
			if "(0" in i[1] and i[1][4] == ")":
				number_called_by_bangalore_list.append(i[1][1:4])
			elif "(0" in i[1] and i[1][5] == ")":
				number_called_by_bangalore_list.append(i[1][1:5])
			elif "(0" in i[1] and i[1][6] == ")" :
				number_called_by_bangalore_list.append(i[1][1:6])
			if i[1][0] == "7" or i[1][0] == "8" or i[1][0] == "9":
				number_called_by_bangalore_list.append(i[1][0:4])
			if i[1][0:3] == "140":
				number_called_by_bangalore_list.append(i[1][0:3])
	#step2:feedback result for return part.Need transform list format(including set\sort\line by line).
	number_called_by_bangalore_list = "\n".join(sorted(set(number_called_by_bangalore_list)))
	feedback_string = "The numbers called by people in Bangalore have codes:" + "\n" +number_called_by_bangalore_list
	return feedback_string

def number_count_bangalore_bangalore(input_csv):
	#def_var area:
	number_count_bangalore_all = 0
	number_count_bangalore_bangalore = 0
	#step1:count time that two kinds of call(banaglore to all,bangalore to bangalore).
	for i in input_csv:
		if "(080)" in i[0]:
			number_count_bangalore_all += 1.0
			if "(080)" in i[1]:
				number_count_bangalore_bangalore += 1.0
	#step2:feedback result for return part.
	feedback_cache_percent = round((number_count_bangalore_bangalore / number_count_bangalore_all) * 100,2)
	feedback_string = "{} percent of calls from fixed lines in Bangalore are calls to other fixed lines in Bangalore.".format(feedback_cache_percent)
	return feedback_string

print(number_called_by_bangalore(calls))
print(number_count_bangalore_bangalore(calls))