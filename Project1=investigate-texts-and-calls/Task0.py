#!/usr/bin/python
#_*_ coding:utf8 _*_

#My result:
#First record of texts, 97424 22395 texts 90365 06212 at time 01-09-2016 06:03:22
#Last record of calls, 98447 62998 calls (080)46304537 at time 30-09-2016 23:57:15, lasting 2151 seconds

import csv
with open('texts.csv', 'r', encoding='UTF-8') as f:
    reader = csv.reader(f)
    texts = list(reader)

with open('calls.csv', 'r', encoding='UTF-8') as f:
    reader = csv.reader(f)
    calls = list(reader)

texts_record_first = texts[0]
calls_record_last = calls[-1]

print("First record of texts, {} texts {} at time {}".format(
    texts_record_first[0],
    texts_record_first[1],
    texts_record_first[2]
))

print("Last record of calls, {} calls {} at time {}, lasting {} seconds".format(
    calls_record_last[0],
    calls_record_last[1],
    calls_record_last[2],
    calls_record_last[3]
))
