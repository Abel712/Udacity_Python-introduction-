#!/usr/bin/python
#_*_ coding:utf8 _*_

import time
import urllib
import requests
from bs4 import BeautifulSoup
import expanddouban
import csv

category_all_list = ["剧情","爱情","喜剧","科幻","动作","悬疑","犯罪","恐怖","青春","励志","战争","文艺","黑色幽默","传记","情色","暴力","音乐","家庭"]
location_all_list = ["大陆","美国","香港","台湾","日本","韩国","英国","法国","德国","意大利","西班牙","印度","泰国","俄罗斯","伊朗","加拿大","澳大利亚","爱尔兰","瑞典","巴西","丹麦"]

#Task1,URL format:https://movie.douban.com/tag/#/?sort=S&range=9,10&tags=电影,剧情,美国
def getMovieUrl(category, location):
	if str(category) in category_all_list and str(location) in location_all_list:
		cache_string_category_location = "," + str(category) + "," + str(location)
		target_url = "https://movie.douban.com/tag/#/?sort=S&range=9,10&tags=电影" + cache_string_category_location
		#if I use：urllib.parse.urljoin('https://movie.douban.com/tag/#/?sort=S&range=9,10&tags=电影', cache_string_category_location),I get this bad result:https://movie.douban.com/tag/,剧情,日本.
	else:
		target_url = None
		print("输入有误请重新输入！")
	category_location_tran_list = [category,location]
	return target_url,category_location_tran_list

#Task2，导入enpanddouban.py已经完成。

#Task3，对整个URL分析后以字典形式返回该URL下所有影片汇总信息。
def Movie(html_from_getHtml,category_location_tran_list):
	#def_var area:
	cache_name_dict = {}
	cache_rate_dict = {}
	cache_info_link_dict = {}
	cache_cover_link_dict = {}
	cache_jump_number = 0
	m = {}
	m_cache = []
	cache_name_string_replace = ""
	#step1:从整个页面HTML编码中分离出所需部分，对所需部分进行筛选和提取。
	soup = BeautifulSoup(html_from_getHtml, "lxml")
	content_div = soup.find(class_="list-wp")
	for element in content_div.find_all("a", recursive=False):
		cache_jump_number += 1 
		for name in element.find_all(class_="title"):
			if "," not in name.string and "," not in name.string:
				cache_name_dict[cache_jump_number] = name.string
			elif ", " in name.string:
				cache_name_string_replace = name.string
				cache_name_dict[cache_jump_number] = cache_name_string_replace.replace(", ","/")
				cache_name_string_replace = ""
			elif "," in name.string:
				cache_name_string_replace = name.string
				cache_name_dict[cache_jump_number] = cache_name_string_replace.replace(",","/")
				cache_name_string_replace = ""
		for rate in element.find_all(class_="rate"):
			if rate.string == None:
				cache_rate_dict[cache_jump_number] = "9.0"
			elif rate.string != None:
				cache_rate_dict[cache_jump_number] = rate.string
		for info in content_div.find_all(class_="item"):
			#PS:在之前使用bs4的“html.parser”没有注意到<a>应该从content_div调取。
			cache_info_link_dict[cache_jump_number] = info.get("href")
		for img in element.find_all(x="movie:cover_x"):
			cache_cover_link_dict[cache_jump_number] = img.get("src")
	#step2:将所需信息提取到cache变量，而后将cache变量携带的内容写入到构造函数输出中，m变量格式为嵌套列表。
	for i in range(1,cache_jump_number+1):
		m_cache.append(cache_name_dict[i])
		m_cache.append(cache_rate_dict[i])
		if " " not in category_location_tran_list[1]:
			m_cache.append(category_location_tran_list[1])
		elif " " in category_location_tran_list[1]:
			m_cache.append(category_location_tran_list[1].replace(' ',''))
		if " " not in category_location_tran_list[0]:
			m_cache.append(category_location_tran_list[0])
		elif " " in category_location_tran_list[0]:
			m_cache.append(category_location_tran_list[0].replace(' ',''))
		m_cache.append(cache_info_link_dict[i])
		m_cache.append(cache_cover_link_dict[i])
		m[i] = m_cache
		m_cache = []
	return m,cache_jump_number

#Task4，使用Task1、2、3中的def函数汇总做成一个效果，输入("剧情","日本")，输出这个类别和地区下所有的电影信息
def task4(category,location):
	return Movie(expanddouban.getHtml(getMovieUrl(category,location)[0],getMovieUrl(category,location)[1],True)[0],expanddouban.getHtml(getMovieUrl(category,location)[0],getMovieUrl(category,location)[1],True)[1])

#Task5，提供三个组合搭配，所有信息汇总后写入movies.csv
def task5(loop_time_number=3):
	#def_var area:
	feedback_movie_information = ""
	feedback_movie_information_list = []
	print("请输入三种类型（以逗号间隔，有误输入均更正为默认搜索，即剧情，文艺，喜剧）：{}。".format("、".join(location_all_list)))
	category = str(input())
	category = category.split('，')
	if len(category) != 3:
		category = ['剧情','文艺','喜剧']	
		print("您的输入有误已更正为默认搜索，类型为{}，程序继续执行。".format(",".join(category)))
	for i in range(loop_time_number):
		if category[i] not in category_all_list:
			category = ['剧情','文艺','喜剧']	
			print("您的输入有误已更正为默认搜索，类型为{}，程序继续执行。".format(",".join(category)))
	for i in range(loop_time_number):
		for i_location in range(len(location_all_list)):
			m_cache_dict_thistime = task4(category[i],location_all_list[i_location])[0]
			for i_jump_time in range(1,task4(category[i],location_all_list[i_location])[1]+1):
				feedback_movie_information_list.append(m_cache_dict_thistime[i_jump_time])
				with open('movies.csv','w') as f:
					for i_list in range(0,len(feedback_movie_information_list)):
						f.write(str(",".join(feedback_movie_information_list[i_list]))+"\n")
	return "反馈：已将爬取内容输出到movies.csv文件中。"

#Task6，基于.csv进行分析，分析结果写入output.txt
def task6(input_csv='movies.csv'):
	#open source data file.
	with open(input_csv, 'r') as f:
	    reader = csv.reader(f)
	    movies = list(reader)
	#def_var area:
	task5_category_list = []
	task5_location0_list = []
	task5_location1_list = []
	task5_location2_list = []
	task5_location0_count_dict = {}
	task5_location1_count_dict = {}
	task5_location2_count_dict = {}
	task5_feedback_cache_cate0_percent_list = []
	task5_feedback_cache_cate1_percent_list = []
	task5_feedback_cache_cate2_percent_list = []
	#step1:创建列表，内含三种类别，从0到2排列。
	for i in range(len(movies)):
		if movies[i][3] not in task5_category_list and " " not in movies[i][3]:
			task5_category_list.append(movies[i][3])
	#step2:按照三种类别创建三个列表，每个列表含有所有该类别电影的地区。
	for i in range(len(movies)):
		if " " in movies[i][3]:
			movies[i][3] = movies[i][3].replace(' ','')
		if movies[i][3] in task5_category_list[0]:
			task5_location0_list.append(movies[i][2].replace(' ',''))
		if movies[i][3] in task5_category_list[1]:
			task5_location1_list.append(movies[i][2].replace(' ',''))
		if movies[i][3] in task5_category_list[2]:
			task5_location2_list.append(movies[i][2].replace(' ',''))
	#step3:通过字典的特性汇总三种类别下各地区的产出数量。
	for i in range(len(task5_location0_list)):
		task5_location0_count_dict[task5_location0_list[i]] = task5_location0_list.count(task5_location0_list[i])
	for i in range(len(task5_location1_list)):
		task5_location1_count_dict[task5_location1_list[i]] = task5_location1_list.count(task5_location1_list[i])
	for i in range(len(task5_location2_list)):
		task5_location2_count_dict[task5_location2_list[i]] = task5_location2_list.count(task5_location2_list[i])
	#step4:通过zip字典排序成元组类型，取出该类型最多的前三地区的数量，使用内置函数list将元组转换成列表返还到存储百分比、地区的列表中。
	task5_feedback_cache_cate0_percent_list.append(list(sorted(zip(task5_location0_count_dict.values(),task5_location0_count_dict.keys()))[-1]))
	task5_feedback_cache_cate0_percent_list.append(list(sorted(zip(task5_location0_count_dict.values(),task5_location0_count_dict.keys()))[-2]))
	task5_feedback_cache_cate0_percent_list.append(list(sorted(zip(task5_location0_count_dict.values(),task5_location0_count_dict.keys()))[-3]))
	for i in range(3):
		task5_feedback_cache_cate0_percent_list[i][0] = round((float(task5_feedback_cache_cate0_percent_list[i][0]) / float(len(task5_location0_list))) * 100,2)

	task5_feedback_cache_cate1_percent_list.append(list(sorted(zip(task5_location1_count_dict.values(),task5_location0_count_dict.keys()))[-1]))
	task5_feedback_cache_cate1_percent_list.append(list(sorted(zip(task5_location1_count_dict.values(),task5_location0_count_dict.keys()))[-2]))
	task5_feedback_cache_cate1_percent_list.append(list(sorted(zip(task5_location1_count_dict.values(),task5_location0_count_dict.keys()))[-3]))
	for i in range(3):
		task5_feedback_cache_cate1_percent_list[i][0] = round((float(task5_feedback_cache_cate1_percent_list[i][0]) / float(len(task5_location1_list))) * 100,2)

	task5_feedback_cache_cate2_percent_list.append(list(sorted(zip(task5_location2_count_dict.values(),task5_location0_count_dict.keys()))[-1]))
	task5_feedback_cache_cate2_percent_list.append(list(sorted(zip(task5_location2_count_dict.values(),task5_location0_count_dict.keys()))[-2]))
	task5_feedback_cache_cate2_percent_list.append(list(sorted(zip(task5_location2_count_dict.values(),task5_location2_count_dict.keys()))[-3]))
	for i in range(3):
		task5_feedback_cache_cate2_percent_list[i][0] = round((float(task5_feedback_cache_cate2_percent_list[i][0]) / float(len(task5_location2_list))) * 100,2)

	#step5:将以上过程的结果按要求输出。
	feedback_category0_string = "统计结果1：所选电影类别{}中，产出数量排名前三的地区有{}、{}、{}，分别占此类别总数的{}%、{}%、{}%。".format(task5_category_list[0],task5_feedback_cache_cate0_percent_list[0][1],task5_feedback_cache_cate0_percent_list[1][1],task5_feedback_cache_cate0_percent_list[2][1],task5_feedback_cache_cate0_percent_list[0][0],task5_feedback_cache_cate0_percent_list[1][0],task5_feedback_cache_cate0_percent_list[2][0]) 
	feedback_category1_string = "统计结果2：所选电影类别{}中，产出数量排名前三的地区有{}、{}、{}，分别占此类别总数的{}%、{}%、{}%。".format(task5_category_list[1],task5_feedback_cache_cate1_percent_list[0][1],task5_feedback_cache_cate1_percent_list[1][1],task5_feedback_cache_cate1_percent_list[2][1],task5_feedback_cache_cate1_percent_list[0][0],task5_feedback_cache_cate1_percent_list[1][0],task5_feedback_cache_cate1_percent_list[2][0]) 
	feedback_category2_string = "统计结果3：所选电影类别{}中，产出数量排名前三的地区有{}、{}、{}，分别占此类别总数的{}%、{}%、{}%。".format(task5_category_list[0],task5_feedback_cache_cate2_percent_list[0][1],task5_feedback_cache_cate2_percent_list[1][1],task5_feedback_cache_cate2_percent_list[2][1],task5_feedback_cache_cate2_percent_list[0][0],task5_feedback_cache_cate2_percent_list[1][0],task5_feedback_cache_cate2_percent_list[2][0]) 
	feedback_category_all_string = feedback_category0_string + "\n" + feedback_category1_string + "\n" + feedback_category2_string
	with open('output.txt','w') as f:
		f.write(feedback_category_all_string)
	return "反馈：已将统计结果输出到output.txt文件中。"

#执行区
task5()
task6()

