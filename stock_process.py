# -*- coding: utf-8 -*-
"""
Created on Sat Apr 08 15:11:39 2017

@author: Liyi Li
Stock data
"""

import glob
import pandas as pd

#############################
#read stock data
############################
path ="D:/lly/2017spring-big_data/group_project/stcok_lly" # use your path
allFiles = glob.glob(path + "/AAPL_1m.csv")
frame = pd.DataFrame()
list_ = []
for file_ in allFiles:
    df = pd.read_csv(file_,sep=";",thousands=',',index_col=None, header=0)
    list_.append(df)
frame = pd.concat(list_)
#check the head
frame.head(n = 5)
#list names of frame
list(frame)

#get rid of one column, 0: row; 1: column
#frame = frame.drop('volume', 1)

#change name of columns
frame = frame.rename(index=str, columns={"volume,,,,": "volume"})
frame['timestamp'] = pd.to_datetime(frame['timestamp'])

######################
#read script data
###################
path_script ="D:/lly/2017spring-big_data/group_project/script_lly" # use your path
allFiles_script = glob.glob(path_script + "/TRY*.csv")
frame_script = pd.DataFrame()
list_script = []
for script in allFiles_script:
    df_1 = pd.read_csv(script,index_col=None, header=0)
    list_script.append(df_1)
frame_script = pd.concat(list_script)

#get a list of headers of pd
list(frame_script)
#get rid of one column, 0: row; 1: column
#frame_script = frame_script.drop('Unnamed: 6', 1)

#conbinme date and time into timestamp
frame_script["timestamp"] = pd.to_datetime(frame_script['date'] + ' ' + frame_script['time'])

frame_script.head(n=5)

######################
#use timestamp of frame_script to query 180 timestamp of frame
#####################
import datetime, time
import re

start = 0
end = 0
from datetime import timedelta
one_day = timedelta(days = 1)
three_day = timedelta(days = 3)

for i, row in frame_script.iterrows():
    #   print the script info    
    print row["timestamp"]

    #   get the date, time and weekday infomation of script
    date_flag = row["timestamp"].date()
    week_flag = row["timestamp"].weekday()
    hour_flag = row["timestamp"].hour
    minute_flag = row["timestamp"].minute
    
    #   if script time is invalid, set it to the closest valid time
        #   if it is before 9:30 AM, set it to 9:30 AM
    if (hour_flag < 9 or hour_flag == 9 and minute_flag < 30):
        hour_flag = 9
        minute_flag = 30
        #   if it is after 4:00 PM, set it to 4:00 PM
    if (hour_flag > 16 or hour_flag == 16 and minute_flag > 0):
        hour_flag = 16
        minute_flag = 0
        
    #   if script day is weekend, set it to the closest Monday 9:30 AM
    if (week_flag > 4):
        hour_flag = 9
        minute_flag = 30
        date_flag = date_flag + one_day
        if week_flag == 5:
            date_flag = date_flag + one_day
        week_flag = 0
    
    #   Initialize the start time and the end time (±2 hour)    
    hour_limit_end = hour_flag + 2
    minute_limit_end = minute_flag
    date_limit_end = date_flag
    hour_limit_start = hour_flag - 2
    minute_limit_start = minute_flag
    date_limit_start = date_flag
    
    #   if script time is before 11:30 AM, revise the start time    
    if (hour_flag < 11 or hour_flag == 11 and minute_flag < 30):
        minute_limit_start = (minute_flag + 30) % 60
        date_limit_start = date_flag - one_day
        if week_flag == 0:
            date_limit_start = date_flag - three_day
        if (minute_flag < 30):
            hour_limit_start = 4 + hour_flag
        else:
            hour_limit_start = 5 + hour_flag
    #   if script time is after 2:00 PM, revise the end time
    elif (hour_flag > 14 or hour_flag == 14 and minute_flag > 0):
        minute_limit_end = (minute_flag + 30) % 60
        date_limit_end = date_flag + one_day
        if week_flag == 4:
            date_limit_end = date_flag + three_day
        if (minute_flag < 30):
            hour_limit_end = hour_flag - 5
        else:
            hour_limit_end = hour_flag - 4
        
    #   find all data points that fit the script's requirement 
        #   find the first index of the result
    while (1):
        now = frame.iloc[[start]]
        date_now = now["timestamp"][0].date()
        hour_now = now["timestamp"][0].hour
        minute_now = now["timestamp"][0].minute
        if (date_now < date_limit_start or
            date_now == date_limit_start and hour_now < hour_limit_start or
            date_now == date_limit_start and hour_now == hour_limit_start and minute_now < minute_limit_start):
            start = start + 1
            if (start > end):
                end = start
        else:
            break
        #   find the last index of the result
    while (1):
        now = frame.iloc[[end]]
        date_now = now["timestamp"][0].date()
        hour_now = now["timestamp"][0].hour
        minute_now = now["timestamp"][0].minute
        if (date_now < date_limit_end or
            date_now == date_limit_end and hour_now < hour_limit_end or
            date_now == date_limit_end and hour_now == hour_limit_end and minute_now < minute_limit_end):
            end = end + 1
            #   print the data point
            print now
            with open("D:/lly/2017spring-big_data/group_project/script_lly/timeseries_1.csv", 'a') as f:
                now.to_csv(f, header=False)
        else:
            break

##################################
#don't forget add id symbol nr timestamp open	high	low close volume for csv file
################################  




