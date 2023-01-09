#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 19 11:19:48 2022

@author: weihuang
"""
from tkinter import ttk  
from tkinter import *
from tkinter.messagebox import *
import pandas as pd
import datetime  as dt
import matplotlib as mat
import tkcalendar
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os

def alert():
    #the number of case
    data = pd.read_csv(r'https://covid19.who.int/WHO-COVID-19-global-data.csv')
    df = pd.DataFrame(data, columns= ['Date_reported','Country','New_cases','Cumulative_cases','New_deaths','Cumulative_deaths'])
    Casefile = os.path.dirname(__file__)+ '/caseNumber.csv'
    df.to_csv(Casefile,index=False)
    case = pd.read_csv(Casefile)
    today = dt.date.today()
    date0 = str(today - dt.timedelta(days=1))
    date1 = str(today - dt.timedelta(days=2))
    alertfile = os.path.normpath(os.path.join(os.path.dirname(__file__), '../alert_sheet.csv'))
    calander = pd.read_csv (alertfile)
    user_country = 'Australia'
    for d in calander.Date:
        try:
            date0 = str(dt.datetime.strptime(d,'%Y-%m-%d').date() - dt.timedelta(days=1))
            date1 = d
            date0_case = int(case.New_cases[(case.Date_reported == date0) & (case.Country == user_country)].values)
            date1_case = int(case.New_cases[(case.Date_reported == date1) & (case.Country == user_country)].values)
            mark = ''
            if date0_case == date1_case:
                mark = 'Even'
            elif date0_case < date1_case:
                mark = 'Up'
            elif date0_case > date1_case:
                mark = 'Down'
            calander.Covid_alert[calander.Date == date1] = mark
        except:
            calander.Covid_alert[calander.Date == date1] = "No record"
    calander.to_csv(alertfile,index=False)
        


class COVIDMain(object):
    def __init__(self, master=None):
        self.root = master #定義內部變量root
        self.root.geometry('1000x800+200+200') #設置窗口大小
        self.root.resizable(width=True, height=True)
        self.loadData()
        self.modify()
        self.chartData()
        self.createPage()
        
    def loadData(self):
        #the number of case
        data = pd.read_csv(r'https://covid19.who.int/WHO-COVID-19-global-data.csv')
        df = pd.DataFrame(data, columns= ['Date_reported','Country','New_cases','Cumulative_cases','New_deaths','Cumulative_deaths'])
        Casefile = os.path.dirname(__file__)+ '/caseNumber.csv'
        df.to_csv(Casefile,index=False)
        
        #the number of case per 100,000 population
        data = pd.read_csv(r'https://covid19.who.int/WHO-COVID-19-global-table-data.csv')
        df = pd.DataFrame(data, columns= ['Name','Cases - cumulative total per 100000 population','Deaths - cumulative total per 100000 population'])
        popultionfile = os.path.dirname(__file__)+ '/populationCase.csv'
        df.to_csv(popultionfile,index=False,header=['Country','Cumulative_cases','Cumulative_deaths'])
        
        #the date vable for the page
        self.case = pd.read_csv(Casefile)
        self.population = pd.read_csv(popultionfile)
        self.country = sorted(list(set(self.case.Country)))
        today = dt.date.today()
        self.date = str(today)
        self.date0 = str(today - dt.timedelta(days=1))
        self.date1 = str(today - dt.timedelta(days=2))
        self.date2 = str(today - dt.timedelta(days=7))
        
    def chartData(self):
        #Data structures
        #population data
        self.cum_case = str(self.population.Cumulative_cases[self.population.Country.isnull()].values)
        self.cum_deaths = str(self.population.Cumulative_deaths[self.population.Country.isnull()].values)
        
        #chart data
        num = ['Australia','China','India','Japan','The United Kingdom'] 
        n = len(num) 
        #new case
        self.fig_new_case = mat.pyplot.figure(figsize=(10,2),dpi = 100)
        for i in range(n):
            dfs = self.case[(self.case['Country']==num[i]) & (self.case.Date_reported >= self.date2)]  
            mat.pyplot.plot(dfs.Date_reported,dfs.New_cases,label=num[i])
            mat.pyplot.legend(bbox_to_anchor=(1,0),loc=3,borderaxespad=0,prop={'size': 6})
        mat.pyplot.title('New Case for each country')
        mat.pyplot.xlabel('Date',size=10)
        mat.pyplot.ylabel('Number',size=10)
        
        #new death
        self.fig_new_deaths = mat.pyplot.figure(figsize=(10,2),dpi = 100)
        for i in range(n):
            dfs = self.case[(self.case['Country']==num[i]) & (self.case.Date_reported >= self.date2)]  
            mat.pyplot.plot(dfs.Date_reported,dfs.New_deaths,label=num[i])
            mat.pyplot.legend(bbox_to_anchor=(1,0),loc=3,borderaxespad=0,prop={'size': 6})
        mat.pyplot.title('New Deaths for each country')
        mat.pyplot.xlabel('Date',size=10)
        mat.pyplot.ylabel('Number',size=10)
        
    def createPage(self):
        self.page = Frame(self.root)
        self.page.pack()
        Label(self.page,text='Please choose the date range and country: ' ).grid(row=1,column=1,stick=W)
        Label(self.page,text= 'Start date' ).grid(row=2,column=1,stick=W)
        self.date_start = tkcalendar.DateEntry(self.page)
        self.date_start.grid(row=3,column=1,stick=W)
        self.date_end = tkcalendar.DateEntry(self.page)
        Label(self.page,text= 'End date' ).grid(row=2,column=2,stick=W)
        self.date_end.grid(row=3,column=2,stick=W)
        Label(self.page,text= 'Country' ).grid(row=2,column=3,stick=W)
        self.country_list = ttk.Combobox(self.page,values=self.country)
        self.country_list.grid(row=3,column=3,stick=W)
        Button(self.page,text='Submit',command=self.dateCheck).grid(row=4,column=3,stick=W)
        Label(self.page,text=self.date0+'World Cumulative Cases - total per 100000 population \n '+self.cum_case ).grid(row=5,column=1,columnspan=3,stick=W+E+N+S)
        Label(self.page,text=self.date0+'World Cumulative Deaths - total per 100000 population \n '+self.cum_deaths ).grid(row=6,column=1,columnspan=3,stick=W+E+N+S)
        Label(self.page,text='New Cases for each country '+self.date2+' to '+self.date0 ).grid(row=7,column=1,stick=W)
        FigureCanvasTkAgg(self.fig_new_case,self.page).get_tk_widget().grid(row=8,column=1,columnspan=3,stick=W)
        Label(self.page,text='New Deaths for each country '+self.date2+' to '+self.date0 ).grid(row=9,column=1,stick=W)
        FigureCanvasTkAgg(self.fig_new_deaths,self.page).get_tk_widget().grid(row=10,column=1,columnspan=3,stick=W)
        
    def modify(self):
        try:
            alertfile = os.path.normpath(os.path.join(os.path.dirname(__file__), '../alert_sheet.csv'))
            calander = pd.read_csv (alertfile)
            user_country = 'Australia'
            date0_case = int(self.case.New_cases[(self.case.Date_reported == self.date0) & (self.case.Country == user_country)].values)
            date1_case = int(self.case.New_cases[(self.case.Date_reported == self.date1) & (self.case.Country == user_country)].values)
            mark = 'UP'
            if date0_case == date1_case:
                mark = 'Even'
            elif date0_case < date1_case:
                mark = 'Down'
            calander.Covid_alert[calander.Date == self.date0] = mark
            calander.to_csv(alertfile,index=False)
        except:
            showinfo(title='Error', message='Data source did not provide the '+self.date0+' data')

    
    def dateCheck(self):
        start = self.date_start.get_date()
        end = self.date_end.get_date()
        country_choose = self.country_list.get()
        dates = []
        diff = (end-start).days
        for i in range(diff+1):
            day = start + dt.timedelta(days=i)
            dates.append(day)            
        if len(dates) > 2 :
            if len(country_choose) > 0:
                self.setData()
            else:
                showinfo(title='Error', message='Make sure pick a country!')
        else:
            showinfo(title='Error', message='Make sure the end date is later than start date!')
            
    def setData(self):
        Userfile = os.path.dirname(__file__)+ '/User.csv'
        self.User = pd.read_csv (Userfile)
        self.User.user_start = str(self.date_start.get_date())
        self.User.user_end = str(self.date_end.get_date())
        self.User.user_country = str(self.country_list.get())
        import pathlib
        print(pathlib.Path(__file__).parent.absolute())
        self.User.to_csv(Userfile,index=False)
        self.page.destroy()
        COVIDSed(self.root)



class COVIDSed(object):
    def __init__(self, master=None):
        self.root = master #定義內部變量root
        self.root.geometry('1000x800+200+200') #設置窗口大小
        self.root.resizable(width=True, height=True)
        self.loadData()
        self.chartData()
        self.createPage()
        
    def loadData(self):
        #the date vable for the page
        Userfile = os.path.dirname(__file__)+ '/User.csv'
        Casefile = os.path.dirname(__file__)+ '/caseNumber.csv'
        popultionfile = os.path.dirname(__file__)+ '/populationCase.csv'
        self.case = pd.read_csv(Casefile)
        self.population = pd.read_csv(popultionfile)
        self.user = pd.read_csv(Userfile)
        self.user_start = str(self.user.user_start.values).replace(r"'",'').replace(r"[",'').replace(r"]",'')
        self.user_end = str(self.user.user_end.values).replace(r"'",'').replace(r"[",'').replace(r"]",'')
        self.user_country = str(self.user.user_country.values).replace(r"'",'').replace(r"[",'').replace(r"]",'')
        
    def chartData(self):
        #Data structures
        #population data
        self.user_case = str(self.case.Cumulative_cases[(self.case.Country == self.user_country) & (self.case.Date_reported == self.user_end) ].values)
        self.user_deaths = str(self.case.Cumulative_deaths[(self.case.Country == self.user_country) & (self.case.Date_reported == self.user_end)].values)
        
        #chart data
        #new case
        self.user_new_case = mat.pyplot.figure(figsize=(10,2),dpi = 100)
        self.dfs = self.case[(self.case['Country']==self.user_country) & (self.case.Date_reported >= self.user_start)& (self.case.Date_reported <= self.user_end)]  
        mat.pyplot.plot(self.dfs.Date_reported,self.dfs.New_cases,label=self.user_country)
        mat.pyplot.legend(bbox_to_anchor=(1,0),loc=3,borderaxespad=0,prop={'size': 6})
        mat.pyplot.title('New Case for '+self.user_country)
        mat.pyplot.xlabel('Date',size=10)
        mat.pyplot.ylabel('Number',size=10)
        
        #new death
        self.user_new_deaths = mat.pyplot.figure(figsize=(10,2),dpi = 100)
        dfs = self.case[(self.case['Country']==self.user_country) & (self.case.Date_reported >= self.user_start)& (self.case.Date_reported <= self.user_end)]  
        mat.pyplot.plot(dfs.Date_reported,dfs.New_deaths,label=self.user_country)
        mat.pyplot.legend(bbox_to_anchor=(1,0),loc=3,borderaxespad=0,prop={'size': 6})
        mat.pyplot.title('New Deaths for '+self.user_country)
        mat.pyplot.xlabel('Date',size=10)
        mat.pyplot.ylabel('Number',size=10)
        
    def createPage(self):
        self.page = Frame(self.root)
        self.page.pack()
        Label(self.page,text=self.user_end+' '+self.user_country+ ' '+' Cumulative Cases \n'+self.user_case ).grid(row=1,column=1,columnspan=3,stick=W+E+N+S)
        Label(self.page,text=self.user_end+' '+self.user_country+ ' '+' Cumulative Deaths \n '+self.user_deaths ).grid(row=2,column=1,columnspan=3,stick=W+E+N+S)
        Label(self.page,text='New Cases for '+self.user_country+' '+self.user_start+' to '+self.user_end ).grid(row=3,column=1,stick=W)
        FigureCanvasTkAgg(self.user_new_case,self.page).get_tk_widget().grid(row=4,column=1,columnspan=3,stick=W)
        Label(self.page,text='New Deaths for  '+self.user_country+' '+self.user_start+' to '+self.user_end ).grid(row=5,column=1,stick=W)
        FigureCanvasTkAgg(self.user_new_deaths,self.page).get_tk_widget().grid(row=6,column=1,columnspan=3,stick=W)
        Button(self.page,text='Record',command=self.record).grid(row=7,column=1,stick=W)
    
    def record(self):
        datafile = os.path.normpath(os.path.join(os.path.dirname(__file__), '../data_sheet.csv'))
        calander = pd.read_csv (datafile)
        for i in self.dfs.Date_reported:
            number = str(self.dfs.New_cases[self.dfs.Date_reported == i].values).replace(r"[",'').replace(r"]",'')
            calander.covid[calander.date == i] = self.user_country+','+number
        calander.to_csv(datafile,index=False)

        
def main(): #run mianloop 
    root = Tk()
    root.title('Detail Data of COVID19')
    COVIDMain(root)
    root.mainloop()
    return None
        
if __name__ == '__main__':
        main()
         
         
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        