# -*- coding: utf-8 -*-
"""
Created on Tue Feb 15 20:26:01 2022

@author: Sharon Shih
"""
from tkinter import *
#import tkinter as tk 
import pandas as pd
import openpyxl as xl
from tkinter import ttk,filedialog
import COVID.COVIDMain
import os

from importlib.machinery import SourceFileLoader

audr=SourceFileLoader("AUD_Rate",(os.path.dirname(__file__)+'/ExchangeRate/AUD_Rate.py')).load_module()
rm=SourceFileLoader("rate_main",(os.path.dirname(__file__)+'/ExchangeRate/rate_main.py')).load_module()

w = SourceFileLoader("weather",(os.path.dirname(__file__)+'/weather/weather.py')).load_module()
wd = SourceFileLoader("weather_data",(os.path.dirname(__file__)+'/weather/weather_data.py')).load_module()

wd.update_alert()

rm.alert()

#put in covid data
COVID.COVIDMain.alert()


root=Tk()
#draw the scene
root.geometry('1100x500') 
root.title('my_user_interface')
my_frame=Frame(root)
my_frame.pack(pady=20)

my_tree =ttk.Treeview(my_frame)
#function of opening other csv file
def file_open():
   global filename
   filename=filedialog.askopenfilename(
       initialdir=os.path.dirname(__file__),
       title="Open A File",
       filetypes=(("excel files","*.csv"),("all files","*.*")))
   
   if filename:
        try:
             filename=r"{}".format(filename)
             df=pd.read_csv(filename)
        except ValueError:
            my_label.config(text="file couldn't be opened")
        except FileNotFoundError:
             my_label.config(text="file couldn't be found")
   #Clear old treeview
   clear_tree()
   df.fillna("", inplace=True) 
   
   #Set up new treeview
   my_tree["column"]=list(df.columns)
   my_tree["show"]="headings"
   # loop thru column list for headers
   for column in my_tree["column"]:
       my_tree.heading(column,text=column)
   #put data in treeview
   df_rows=df.to_numpy().tolist()    
   for row in df_rows:
       my_tree.insert("","end",values=row)
  #pack the treeview finally
   my_tree.pack()


#open alert file first in the interface
def show_alert():
    filename='alert_sheet.csv'
    if filename:
         try:
              filename=r"{}".format(filename)
              df=pd.read_csv(filename)
         except ValueError:
             my_label.config(text="file couldn't be opened")
         except FileNotFoundError:
              my_label.config(text="file couldn't be found")
    #Clear old treeview
    clear_tree()
    df.fillna("", inplace=True) 

    #Set up new treeview
    my_tree["column"]=list(df.columns)
    my_tree["show"]="headings"
    # loop thru column list for headers
    for column in my_tree["column"]:
        my_tree.heading(column,text=column)
    #put data in treeview
    df_rows=df.to_numpy().tolist()    
    for row in df_rows:
        my_tree.insert("","end",values=row)
    my_tree.pack()

def clear_tree():
    my_tree.delete(*my_tree.get_children())

def set_cell_value(event): #double click to edit the table
    
    for item in my_tree.selection():
        
        item_text = my_tree.item(item, "values")
    # output the selected cell's value
    column= my_tree.identify_column(event.x)# row
    row = my_tree.identify_row(event.y)  # column
    cn = int(str(column).replace('#',''),16)
    rn = int(str(row).replace('I',''),16)
    entryedit = Text(root,width=10+(cn-1)*16,height = 1)
    entryedit.place(x=16+(cn-1)*130, y=6+rn*20)
    def saveedit():
        my_tree.set(item, column=column, value=entryedit.get(0.0, "end"))
        df.iloc[rn-1,cn-1]=entryedit.get(0.0, "end")

        df.to_excel(filename,index=(False)) 
        print(df.iloc[6,2])
        entryedit.destroy()
        okb.destroy()
    okb = ttk.Button(root, text='OK', width=4, command=saveedit)
    okb.place(x=90+(cn-1)*242,y=2+rn*20)
    
def sav():

    global filename
    df.to_excel(filename,index=(False)) 
    print (filename)




# Add a menu
my_menu=Menu(root)
root.config(menu=my_menu)
#Add menu dropdown
file_menu=Menu(my_menu,tearoff=False)
my_menu.add_cascade(label="Open File",menu=file_menu)
file_menu.add_command(label="Open",command=file_open)
#button for mac users
my_menubtn=ttk.Button(root, text="Open File", width=20,command=file_open)
my_menubtn.pack()
#show the table
show_alert()


my_tree.bind('<Double-1>', set_cell_value)

my_label=Label(root,text='')
my_label.pack(pady=20)

#==========================================================================

#weather button
weatherbtn = ttk.Button(root, text="weather", width=20, command=w.main)
weatherbtn.pack()

#exchange button
exchangebtn = ttk.Button(root, text="exchange rate", width=20,command=rm.main)
exchangebtn.pack()


#covid button
covidbtn = ttk.Button(root, text="covid", width=20, command=COVID.COVIDMain.main)
covidbtn.pack()


root.mainloop()