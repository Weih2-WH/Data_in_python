#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 19 14:55:34 2022

@author: chichenl
"""

import csv
import os
import pandas as pd

#read data_dict from csv
with open(os.path.join(os.path.dirname(__file__), 'date_dict.csv')) as file:
    reader = csv.reader(file)
    date_dict = dict(reader)

#read month daily data from several csv from data folder
data=[]
for key in date_dict:
    filename = os.path.dirname(__file__)+ '/data/' +key+ '.csv'
    #only use temperature & weather, reading these two col are enought
    data.append(pd.read_csv(filename,usecols= ['Temperature','Weather']))

#data_sheet and alert_sheet belong to main folder
record_filename = os.path.normpath(os.path.join(os.path.dirname(__file__), '../data_sheet.csv'))
alert_filename = os.path.normpath(os.path.join(os.path.dirname(__file__), '../alert_sheet.csv'))
csv_data = []
header = []

#judge weather condition from temperature
def weather_alert(temp):
    if(temp>25):
        return 'Hot'
    if(temp>10):
        return 'Cool'
    return 'Cold'

#read in original data from csv
def read_ori(f):
    #clear list before reading in data
    csv_data.clear()
    with open(f, 'r', newline='') as fin:
        csvreader = csv.reader(fin)
        global header
        header = next(csvreader)
        for row in csvreader:
            csv_data.append(row)           
    return None

#write back the updated data in list csv_data to csv
def write_updated(f):
    with open(f, 'w', newline="") as fout:
        csvwriter = csv.writer(fout) 
        csvwriter.writerow(header)
        csvwriter.writerows(csv_data)
        
#write record(temperature & weather) to csv
#can be called from weather UI record button
def write_record(rdate):
    #read in original data to make sure no other data is missed
    read_ori(record_filename)
    for row in csv_data:
        date=row[0]
        date=date[:4]+date[5:7]+date[8:]
        #if date is what is selected
        if(date==rdate):
            index=int(date_dict[date])
            length=len(data[index])
            temp=data[index].loc[length//2]['Temperature']
            weather=data[index].loc[length//2]['Weather']
            #update the weather data cell
            row[2]=str(temp)+'C, '+weather
    #write back the updated data
    write_updated(record_filename)   

#write alert to csv
#can be called from main UI
def update_alert():
    #read in original data to make sure no other data is missed
    read_ori(alert_filename)
    for row in csv_data:
        date=row[0]
        date=date[:4]+date[5:7]+date[8:]
        #check if data is available
        if date in date_dict:
            index=int(date_dict[date])
            length=len(data[index])
            temp=data[index].loc[length//2]['Temperature']
            alert=weather_alert(int(temp))
            #update the weather alert cell
            row[2]=alert
    #write back the updated data
    write_updated(alert_filename)  
