#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 18 21:39:09 2022

@author: chichenl
"""
import tkinter as tk
from tkinter import ttk
import pandas as pd
import os
import csv
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import time
#%%
# imports weather scraping and data module
from importlib.machinery import SourceFileLoader
ws = SourceFileLoader("weather_scraping",(os.path.join(os.path.dirname(__file__), 'weather_scraping.py'))).load_module()
wd = SourceFileLoader("weather_data",(os.path.join(os.path.dirname(__file__), 'weather_data.py'))).load_module()

#read data_dict from csv
with open(os.path.join(os.path.dirname(__file__), 'date_dict.csv')) as file:
    reader = csv.reader(file)
    date_dict = dict(reader)

#read month daily data from several csv from data folder
data=[]
for key in date_dict:
    filename = os.path.dirname(__file__)+ '/data/' +key+ '.csv'
    tmp_df=pd.read_csv(filename)
    tmp_df.name=key
    tmp_df.drop(tmp_df.columns[0], axis=1, inplace=True)
    data.append(tmp_df)

#clean up data for histogram
chart_data2=[]
for i in range(len(data)):
    date=str(int(data[i].name[-2:]))
    length=len(data[i])
    temp=int(data[i].loc[length//2]['Temperature'])
    chart_data2.append([date,temp])
df2 = pd.DataFrame(chart_data2,columns=['Date','Temperature'])


class Window:
    def __init__(self, master):
        # configure the root window
        master.title('Weather Monthly Data')
        master.geometry('600x550')
        master.pack_propagate(False)
        master.resizable(0,0)
        
        # Frame for Control
        self.frame_control=tk.LabelFrame(master)
        #self.frame_control.place(height=36, width=265, relx=0,y=0)
        self.frame_control.place(height=36, width=265, relx=0,y=0)
        # Frame for TreeView
        self.frame_tv=tk.LabelFrame(master, text='Weather Data')
        self.frame_tv.place(height=250, width=600, x=0, y=36)
        # Frame for LineChart
        self.frame_chart=tk.LabelFrame(master,text='Monthly Temperature Histogram')
        self.frame_chart.place(height=260, width=600, x=0,y=290)
        self.plot()

        # TreeView Widget
        self.tv=ttk.Treeview(self.frame_tv)
        self.tv.place(relheight=1, relwidth=1)
        self.treescrolly=tk.Scrollbar(self.frame_tv, orient='vertical', command=self.tv.yview)
        self.tv.configure(yscrollcommand=self.treescrolly.set)
        self.treescrolly.pack(side="right", fill="y")

        # Combo Box Widget for selecting date
        self.drop = ttk.Combobox(self.frame_control,values=list(date_dict.keys()),width=8)
        self.drop.place(relx=0.02, rely=0.1)
        self.drop.current(0)
        
        # Buttons
        self.select_button = tk.Button(self.frame_control, text = "Select", command = self.show_tree)
        self.select_button.place(relx=0.42, rely=0)
        self.record_button = tk.Button(self.frame_control, text = "Record", command = self.record_to_csv)
        self.record_button.place(relx=0.69, rely=0)
        self.update_button = tk.Button(master, text = "Update Data", command=self.update)
        self.update_button.place(relx=0.8, y=3)

    # Plotting histogram
    def plot(self):
        figure = plt.Figure(figsize=(6, 4), dpi=100)
        figure_canvas = FigureCanvasTkAgg(figure, self.frame_chart)
        NavigationToolbar2Tk(figure_canvas,self.frame_chart)
        axes = figure.add_subplot()
        axes.bar(df2['Date'], df2['Temperature'])
        axes.set_ylabel('Temperature')
        figure_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    # Clear TreeView
    def clear_tree(self):
        self.tv.delete(*self.tv.get_children())

    # Change TreeView Data(Daily data Table)
    def show_tree(self):
        clicked=self.drop.get()
        index = int(date_dict[clicked])
        df = data[index]
        self.clear_tree()
        self.tv['column']=list(df.columns)
        self.tv['show']='headings'
        for column in self.tv['columns']:
            self.tv.heading(column, text=column)
            self.tv.column(column, minwidth=0, width=100, stretch=tk.NO)
        self.tv.column('#3', minwidth=0, width=180,  stretch=tk.NO)
        df_rows=df.to_numpy().tolist()
        for row in df_rows:
            self.tv.insert('','end',values=row)
        return None
    
    # Record current day mid-day temperature & weather to csv
    def record_to_csv(self):
        #call write_record from weather_data.py
        clicked=self.drop.get()
        wd.write_record(clicked)
        return None
    
    #re-scrape & clean data
    def update(self):
        tic = time.perf_counter()
        ws.update_data()
        toc = time.perf_counter()
        print(f"Update in {toc - tic:0.4f} seconds")
        # new window after finishing update
        # Toplevel object which will be treated as a new window
        self.newWindow = tk.Toplevel()
        self.newWindow.title(' ')
        # sets the geometry of toplevel
        self.newWindow.geometry("150x50")
        # A Label widget to show in toplevel
        self.text = tk.Label(self.newWindow,text ="Data Update Finished").place(relx=0.1, rely=0.1)
        return None
    
    def button_method(self):
        #run this when button click to close window
        self.master.destroy()   
        
def main(): #run mianloop 
    root = tk.Tk()
    app = Window(root)
    root.mainloop()
    return None

if __name__ == '__main__':
    main()