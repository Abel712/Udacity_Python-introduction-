#!/usr/bin/python
#_*_ coding:utf8 _*_

#My result:
"""
These numbers could be telemarketers:
(022)37572285
(022)65548497
(022)68535788
(022)69042431
(040)30429041
(044)22020822
(0471)2171438
(0471)6579079
(080)20383942
(080)25820765
(080)31606520
(080)40362016
(080)60463379
(080)60998034
(080)62963633
(080)64015211
(080)69887826
(0821)3257740
1400481538
1401747654
1402316533
1403072432
1403579926
1404073047
1404368883
1404787681
1407539117
1408371942
1408409918
1408672243
1409421631
1409668775
1409994233
74064 66270
78291 94593
87144 55014
90351 90193
92414 69419
94495 03761
97404 30456
97407 84573
97442 45192
99617 25274
"""

import csv
with open('texts.csv', 'r') as f:
    reader = csv.reader(f)
    texts = list(reader)
with open('calls.csv', 'r') as f:
    reader = csv.reader(f)
    calls = list(reader)

def catch_telemarketing(input_calls_csv,input_texts_csv):
	#def_var area:
	matchlist_number_callans_textinc_textans = []
	feedback_cache_list = []
	feedback_cache_string = ""
	#step1:create a list that get call_ans_number \ text_inc_number \ text_ans_number,and then,transform this list become a set square.
	for i in input_calls_csv:
		matchlist_number_callans_textinc_textans.append(i[1])
	for i in input_texts_csv:
		matchlist_number_callans_textinc_textans.append(i[0])
		matchlist_number_callans_textinc_textans.append(i[1])
	matchlist_number_callans_textinc_textans = set(matchlist_number_callans_textinc_textans)
	#print(matchlist_number_callans_textinc_textans)
	#step2:match call_inc_number and matchlist,pop matched number into a feedback list.
	for i in input_calls_csv:
		if i[0] not in matchlist_number_callans_textinc_textans:
			feedback_cache_list.append(i[0])
	#step3:feedback result for return part.Need transform list format(including set\sort\line by line).
	feedback_cache_string = "\n".join(sorted(set(feedback_cache_list)))
	feedback_string = "These numbers could be telemarketers: " + "\n" + feedback_cache_string
	return feedback_string
print(catch_telemarketing(calls,texts))

