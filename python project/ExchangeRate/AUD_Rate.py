# -*- coding: utf-8 -*-
"""
Created on Sat Feb 12 10:07:48 2022

@author: Yufei Chen
"""

import requests
import json
import xlwt
import datetime

#API Access
def request_data(url):
    req = requests.get(url) 
    content=json.loads(req.text)
    return content
#Preliminary processing data
def process_data(content):
    history_rate=content["dataset"]["data"]
    date_and_rate=history_rate[0:20]
    return date_and_rate

if __name__=='__main__':
    url_aud="http://data.nasdaq.com/api/v3/datasets/BOE/XUDLADD?api_key=GpgczptJuM9LSJmf5seK"
    content_aud=request_data(url_aud)
    list_all=process_data(content_aud)
    list_date=[]
    list_day=[]
    list_rate=[]
    #transfer date date from string to datetime and form several lists
    for i in list_all:
        list_date.append(i[0])
        list_rate.append(i[1])
    dict_rate_date=dict(zip(list_date,list_rate))
    for b in range(len(list_date)):
        list_date[b]=datetime.datetime.strptime(list_date[b], '%Y-%m-%d').date()
        
    #Trading in foreign exchange markets was suspended on Weekend
    #We nened to fill up the vacancy date data
    list_date_new=[]
    i=0
    while i <(len(list_date)-1):
        deltadate=(list_date[i]-list_date[i+1]).days
        if deltadate>1: #Judge interval date
            list_date_new.append(str(list_date[i]))
            for z in range(deltadate-1):
                list_date_new.append(str(list_date[i]-datetime.timedelta(days=(z+1))))
        else:
            list_date_new.append(str(list_date[i]))
        i=i+1
    list_date_new.append(str(list_date[len(list_date)-1]))
    list_date_new.sort() #sort list by date
    
    #Fill up the vacancy data using Friday's exchange rate
    list_rate_new=[0]*len(list_date_new)
    list_rate_new[0]=dict_rate_date[list_date_new[0]]
    v=1
    while v< len(list_date_new):
        if list_date_new[v] in dict_rate_date: 
            list_rate_new[v]=dict_rate_date[list_date_new[v]]
        else:
            dict_rate_date[list_date_new[v]]=dict_rate_date[list_date_new[v-1]]#添加新的日期（key值）和利率（value值）
        v=v+1      
    #sort date and rate list
    l_d=sorted(dict_rate_date.keys())
    l_r=[]
    for f in range(len(l_d)):
        l_r.append(dict_rate_date[l_d[f]])
    d_r_d=dict(zip(l_d,l_r))
    
    #creat excel file, write exchange rate
    #sheet1
    file=xlwt.Workbook()
    sheet1=file.add_sheet('Base_USD')
    sheet1.write(0,0,'date')
    sheet1.write(0,1,'exchange Rate')
    l_aud=len(l_d)
    for j in range(l_aud):
        sheet1.write(j+1,0,l_d[j])
        sheet1.write(j+1,1,l_r[j])
    #sheet2
    sheet2=file.add_sheet('Alert')
    sheet2.write(0,0,'date')
    sheet2.write(0,1,'Up or Down')
    sheet2.write(0,2,'Exchange rate alert')
    
    #Alert judgement
    for n in range(l_aud):
        sheet2.write(n+1,0,l_d[n])
    list_updown=[]
    list_alert=[]
    for m in range(l_aud-1):
        number=(l_r[m+1]-l_r[m])/l_r[m]
        if number>0:
            s='Up:'+str(format(number,'.4f'))
            if number>=0.01:
                a='Alert'
            else:
                a='Stable'
        if number<0:
            s='Down'+str(format(abs(number),'.4f'))
            if number<=-0.01:
                a='Alert'
            else:
                a='Stable'
        if number==0:
            s='Unchange'
            a='Stable'
        list_updown.append(s)
        list_alert.append(a)
        sheet2.write(m+1,1,list_updown[m])
        sheet2.write(m+1,2,list_alert[m])
        file.save('AUD_Rate.xls')

else:
    #API Access
    url_aud="http://data.nasdaq.com/api/v3/datasets/BOE/XUDLADD?api_key=GpgczptJuM9LSJmf5seK"
    content_aud=request_data(url_aud)
    list_all=process_data(content_aud)
    list_date=[]
    list_day=[]
    list_rate=[]
    dict_day_date={1:'Mon',2:'Tue',3:'Wed',4:'Thurs',5:'Fri',6:'Sat',7:'Sun'}
    for i in list_all:
        day_number=int(datetime.datetime.strptime(i[0], '%Y-%m-%d').strftime("%w"))
        day=dict_day_date[day_number]
        list_day.append(day)
        list_date.append(i[0])
        list_rate.append(i[1])
    dict_rate_date=dict(zip(list_date,list_rate))
    for b in range(len(list_date)):
        list_date[b]=datetime.datetime.strptime(list_date[b], '%Y-%m-%d').date()

    #Trading in foreign exchange markets was suspended on Weekend
    #We nened to fill up the vacancy date data
    list_date_new=[]
    i=0
    while i <(len(list_date)-1):
        deltadate=(list_date[i]-list_date[i+1]).days
        if deltadate>1:
            list_date_new.append(str(list_date[i]))
            for z in range(deltadate-1):
                list_date_new.append(str(list_date[i]-datetime.timedelta(days=(z+1))))
        else:
            list_date_new.append(str(list_date[i]))
        i=i+1
    list_date_new.append(str(list_date[len(list_date)-1]))
    list_date_new.sort()
    
    #Fill up the vacancy data using Friday's exchange rate
    list_rate_new=[0]*len(list_date_new)
    list_rate_new[0]=dict_rate_date[list_date_new[0]]
    v=1
    while v< len(list_date_new):
        if list_date_new[v] in dict_rate_date: 
            list_rate_new[v]=dict_rate_date[list_date_new[v]]
        else:
            dict_rate_date[list_date_new[v]]=dict_rate_date[list_date_new[v-1]]
        v=v+1
    
    #Form new date,rate, size change list and dict
    l_d=sorted(dict_rate_date.keys())
    l_r=[]
    for f in range(len(l_d)):
        l_r.append(dict_rate_date[l_d[f]])
    d_r_d=dict(zip(l_d,l_r))
   
    #Calculate the size change of exchange rate
    def rate_updown():
        l_aud=len(l_d)
        list_updown=[]
        list_alert=[]
        for m in range(l_aud-1):
            number=(l_r[m+1]-l_r[m])/l_r[m]
            if number>0:
                s='Up: '+str(format(number,'.4f'))
                if number>=0.01:
                    a='Alert'
                else:
                    a='Stable'
            if number<0:
                s='Down: '+str(format(abs(number),'.4f'))
                if number<=-0.01:
                    a='Alert'
                else:
                    a='Stable'
            if number==0:
                s='Unchange'
                a='Stable'
            list_updown.append(s)
            list_alert.append(a)
        return list_updown
    l_s=rate_updown()
    d_s_d=dict(zip(l_d,l_s))
