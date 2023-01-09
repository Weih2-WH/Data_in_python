"""
Created on Fri Feb 25 10:03:09 2022


@author: Yufei Chen
"""

from tkinter import *
import pandas as pd
import tkinter as tk
from tkinter import ttk
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.pylab import mpl
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import AUD_Rate as audr
import os

def alert():
    list_alert=audr.rate_updown()
    alert_filename = os.path.normpath(os.path.join(os.path.dirname(__file__), '../alert_sheet.csv'))
    dataalert=pd.read_csv(alert_filename)
    list_da=dataalert['Date'][0:23]
    dict_alert=dict(zip(list_da,range(len(list_da))))
    dict_ad=dict(zip(audr.l_d, list_alert))
    
    for i in list_da:
        dataalert.iloc[dict_alert[i],3]=dict_ad[i]
    dataalert.to_csv(alert_filename,index=False)

#record_filename = os.path.normpath(os.path.join(os.path.dirname(__file__), '../data_sheet.csv'))
#alert_filename = os.path.normpath(os.path.join(os.path.dirname(__file__), '../alert_sheet.csv'))


class Application:

    def __init__(self, master):
        master.title('Exchange Rate : USD/AUD')
        master.geometry('600x550')
        master.pack_propagate(False)
        master.resizable(0,0)
        # Frame for Control
        self.frame_control=tk.LabelFrame(master)
        self.frame_control.place(height=36, width=265, relx=0,y=0)
        
        #TreeView
        self.frame_tv=tk.LabelFrame(master, text='USD/AUD Exchange Rate')
        self.frame_tv.place(height=250, width=600, x=0, y=36)
        
        #LineChart
        self.frame_chart=tk.LabelFrame(master,text='Exchange Rate in Last Seven Days')
        self.frame_chart.place(height=260, width=600, x=0,y=290)
        self.plot()
        
        #TreeView 
        self.tv=ttk.Treeview(self.frame_tv)
        self.tv.place(relheight=1, relwidth=1)
        self.treescrolly=tk.Scrollbar(self.frame_tv, orient='vertical', command=self.tv.yview)
        self.tv.configure(yscrollcommand=self.treescrolly.set)
        self.treescrolly.pack(side="right", fill="y")
        self.treeview()

        #Initial Dropdown Menu Text
        global clicked
        clicked = tk.StringVar()
        clicked.set(str(audr.l_d[0]))
        drop = tk.OptionMenu(self.frame_control, clicked, *audr.l_d ).place(x=0, rely=0.1) 
        
        #Record Button
        self.record_button = tk.Button(self.frame_control, text = "Record", command=self.record_method)
        self.record_button.place(relx=0.69, rely=0)
        
    def plot(self):
        figure = plt.Figure(figsize=(6, 4), dpi=75)
        figure_canvas = FigureCanvasTkAgg(figure, self.frame_chart)
        NavigationToolbar2Tk(figure_canvas,self.frame_chart)
        axes = figure.add_subplot()
        axes.plot(audr.l_d[21:28],audr.l_r[21:28])
        axes.set_ylabel('USD/AUD')
        figure_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
            
    # Exchage Rate Data Table
    def treeview(self):
        ac=('1','2','3')
        c=['Date', 'Exchange Rate', 'Size Change']
        self.tv['column']=ac
        self.tv['show']='headings'
        list_updown=audr.rate_updown()
        daterate=[]
        list_unit=[]
        for a in range(len(list_updown)):
            list_unit=[audr.l_d[a],audr.l_r[a],list_updown[a]]
            daterate.append(list_unit)
        for i in range(len(c)):
            self.tv.column(ac[i],width=40,anchor='center')
            self.tv.heading(ac[i],text=c[i])
        for row in daterate:
                self.tv.insert('','end',values=row)

    #Record date, exchange rate, size change
    def record_method(self):
        dict_date_rate=audr.d_r_d
        dict_date_sizechange=audr.d_s_d
        dict_index=dict(zip(audr.l_d, range(len(audr.l_d))))
        record_date=clicked.get()
        record_rate=dict_date_rate[record_date]
        record_sizechange=dict_date_sizechange[str(record_date)]
        
        #write data in data_sheet.csv
        record_filename = os.path.normpath(os.path.join(os.path.dirname(__file__), '../data_sheet.csv'))
        datad=pd.read_csv(record_filename)
        list_dd=datad['date']
        dict_dd=dict(zip(list_dd,range(len(list_dd))))
        datad.iloc[dict_dd[record_date],4]=record_rate
        datad.to_csv(record_filename,index=False)


    def button_method(self):
            self.master.destroy()   

         
         
def main(): 
    root = Tk()
    app = Application(root)
    root.mainloop()
    return None

if __name__ == '__main__':
    main()
