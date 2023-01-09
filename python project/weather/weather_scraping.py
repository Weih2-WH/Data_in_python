#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 18 16:09:17 2022

@author: chichenl
"""

import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import os
import csv

from importlib.machinery import SourceFileLoader
wd = SourceFileLoader("weather_data",(os.path.join(os.path.dirname(__file__), 'weather_data.py'))).load_module()

URL = 'https://www.timeanddate.com/weather/australia/adelaide/historic?month=2&year=2022'

#for storing params value to sent to url
data = {'hd': '20220201',}

date_list=[]
monthly_data=[]

#get date value from web's dropdown list
def get_datelist():
    global date_list
    page = requests.get(URL,params=data)
    soup = bs(page.content, "html.parser")
    dates = soup.find('select', id='wt-his-select')
    for i in dates:
        date_list.append(i['value'])

#get daily table and return as dataframe
def get_table(soup):
    tr = soup.find('table', id='wt-his').find_all('tr')[2:-1]
    daily_data=[]
    #clean time data
    for line in tr:
        hour_data=[]
        for th in line.find_all('th'):
            hour_data.append(th.text)
        for td in line.find_all('td'):
            hour_data.append(td.text)
        hour_data=hour_data[0:1]+hour_data[2:5]+hour_data[6:7]
        hour_data[1]=hour_data[1][:2]
        daily_data.append(hour_data)   
    date=daily_data[0][0][8:]
    daily_data[0][0]=daily_data[0][0][:8]
    daily_data.insert(0,date)
    #list of list to dataframe
    daily_df = pd.DataFrame.from_records(daily_data[1:])
    daily_df.columns = ["Time", "Temperature", "Weather", "Wind", "Humidity"]
    
    return daily_df

#write list of dataframe as several csv file in folder data
def write_df_csvs():
    for data in monthly_data:
        filename = os.path.dirname(__file__)+ '/data/' +data.name + '.csv'
        data.to_csv(filename)

#write date_dict to csv file
def write_dict():
    date_dict={k: v for v,k in enumerate(date_list)}
    with open(os.path.join(os.path.dirname(__file__), 'date_dict.csv'), 'w') as f:
        writer = csv.writer(f)
        for key, value in date_dict.items():
           writer.writerow([key, value])

#re-scrape & clean data, called from weather UI
def update_data():
    print('updating...')
    with requests.Session() as s:
        get_datelist()
        for i in date_list:
            data['hd']=i
            page = s.get(URL,params=data)
            soup = bs(page.content, "html.parser")
            table = get_table(soup)
            table.name=i
            monthly_data.append(table)
        #update new data to csv 
        write_df_csvs()
        write_dict()
        wd.update_alert()

