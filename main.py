#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 16:42:55 2020

@author: danielmaya
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from bokeh.io import output_file, show,curdoc
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool, Select, CustomJS,RadioButtonGroup
from bokeh.layouts import widgetbox,row,column
from bokeh.models import Slider
from bokeh.models.annotations import Title
from bokeh.models.widgets import DatePicker
from bokeh.models.ranges import Range1d
from datetime import date
import datetime
import examples

curdoc().clear()

df = examples.df
k = 3

categories = list(df.columns)[0:k]
measures=list(df.columns)[k:]
aggregations=['count','sum']

def get_df(data,widgets):
    '''This function takes the DF data and filter it according to the values of
    the keys in the widgets dictionary'''
    widgets_nall={c:v for c,v in widgets.items() if 'All' not in v}
    dfplot=data.loc[data[widgets_nall.keys()].isin(widgets_nall.values()).all(axis=1),:]
    return dfplot


min_date = date(2019, 10, 5)
max_date = date(2020, 2, 2)
delta = max_date - min_date


initial_date = DatePicker(title='From',min_date=date(2019,10,5),max_date=date(2020,2,2),value=date(2019,10,5))
final_date = DatePicker(title='To',min_date=date(2019,10,5),max_date=date(2020,2,2),value=date(2020,2,2))

source2 = ColumnDataSource(data = {'x' : list(df.groupby('cat_1').m1.sum()), 'y' : list(df.groupby('cat_1').m1.sum().index)})

res_button= RadioButtonGroup(labels=["All selection", "Slider value"], active=0)
selects = [Select(title=cat, options=['All '+cat+'s']+df[cat].unique().tolist(), value='All '+cat+'s') for cat in categories]
select_m=Select(title='Measures', options=measures, value=measures[0])
agg_select=Select(title='Aggregation', options=aggregations, value='sum')
var_select = Select(title='Variable', options=categories, value='cat_1')
slider = Slider(title='Day',start=1, end=delta.days, step=1, value=1)
frequency= Select(title='Frequency',options=['M','D'],value='D')

p = figure(title='sum by days',y_range=list(df.groupby('cat_1').m1.sum().index), x_range=(0, 9000), plot_height=700, y_axis_label='cat_1')
p.hbar(right='x', y='y', height=0.2 ,source=source2)  

hover = HoverTool(tooltips=[('sum', '@x')])
p.add_tools(hover)    


def main_callback(attr, old, new):
    '''This functions performs the general callback of the app. It sets the values of the filters, and 
    the range dates given by the user, and creates a new data source according to them'''
    selects_mod = [select.value for select in selects]
    widgets = dict(zip(categories, selects_mod))
    measure=select_m.value
    new_var = var_select.value
    x = initial_date.value
    y = final_date.value
    freq=frequency.value
    #slider = Slider(title='Day', start=x.day, end=(y-x).days, value=x.day)
    new_slice = slider.value
    if x and y:
        x = pd.to_datetime(x)
        y = pd.to_datetime(y)
        
        dfplot = get_df(df, widgets)
        dfplot = dfplot[(dfplot.index.date >= x ) & (dfplot.index.date <= y)]
        
        new_date = x + datetime.timedelta(days=new_slice)   
        slider.end=(y-x).days
        p.y_range.factors = []
        new_source = {'x' : list(dfplot.loc[str(new_date): str(new_date)].groupby(new_var).m1.sum()), 'y' : list(dfplot.loc[str(new_date): str(new_date)].groupby(new_var).m1.sum().index)}
        source2.data = new_source  
        p.y_range.factors = list(dfplot.groupby(new_var).sum().index)
#        t=Title()
#        t.text='count on'+str(new_date)
        p.title.text='count on'+' '+ str(new_date.month)+ '-' + str(new_date.day)+'-'+str(new_date.year)

def freq_callback(attr,new,old):
    selects_mod = [select.value for select in selects]
    widgets = dict(zip(categories, selects_mod))
    new_var = var_select.value
    x = initial_date.value
    y = final_date.value
    freq=frequency.value
    measure=select_m.value
    agg=agg_select.value
    new_slice = slider.value
    res=res_button.active
    
    p.yaxis.axis_label = new_var
    
    if res==1:
        if x and y:
            x = pd.to_datetime(x)
            y = pd.to_datetime(y)
            
            dfplot = get_df(df, widgets)
            dfplot = dfplot[(dfplot.index.date >= x ) & (dfplot.index.date <= y)]
            
            new_date = x + datetime.timedelta(days=new_slice)   
            
            p.y_range.factors = []
            if freq=='M':
                slider.end=12
                slider.title='month'
                df1=dfplot.groupby([new_var,pd.Grouper(freq=freq)])[measure].agg(agg).reset_index()
                new_source = {'x' : list(df1[df1.date.apply(lambda x:x.month)==new_slice].set_index(new_var)[measure]),
                              'y' : list(df1[df1.date.apply(lambda x:x.month)==new_slice].set_index(new_var).index)}
                source2.data = new_source  
                hover.tooltips=[(agg,'@x')]
                p.y_range.factors = list(dfplot.groupby(new_var).agg(agg).index)
    #        t=Title()
    #        t.text='count on'+str(new_date)
                p.title.text=agg+' of '+measure+' on'+' month:  '+ str(new_slice)
                if agg=='sum':
                    p.x_range.end=9000
                else:
                    p.x_range.end=100
            else:
                slider.end=(y-x).days
                slider.title='day'
                df1=dfplot.groupby([new_var,pd.Grouper(freq=freq)])[measure].agg(agg).reset_index()
                new_source = {'x' : list(dfplot.loc[str(new_date): str(new_date)].groupby(new_var)[measure].agg(agg)), 
                              'y' : list(dfplot.loc[str(new_date): str(new_date)].groupby(new_var)[measure].agg(agg).index)}
                source2.data = new_source 
                hover.tooltips=[(agg,'@x')]
                p.y_range.factors = list(dfplot.groupby(new_var).agg(agg).index)
    #        t=Title()
    #        t.text='count on'+str(new_date)
                p.title.text=agg+' of ' +measure+' on'+' '+ str(new_date.month)+ '-' + str(new_date.day)+'-'+str(new_date.year)
                if agg=='sum':
                    p.x_range.end=9000
                else:
                    p.x_range.end=100
    else:
        if x and y:
            x = pd.to_datetime(x)
            y = pd.to_datetime(y)
            
            dfplot = get_df(df, widgets)
            dfplot = dfplot[(dfplot.index.date >= x ) & (dfplot.index.date <= y)]
            
            new_date = x + datetime.timedelta(days=new_slice)   
            
            p.y_range.factors = []
            new_source = {'x' : list(dfplot.groupby(new_var)[measure].agg(agg)), 
                          'y' : list(dfplot.groupby(new_var)[measure].agg(agg).index)}
            source2.data = new_source
            hover.tooltips=[(agg,'@x')]
            p.y_range.factors = list(dfplot.groupby(new_var).agg(agg).index)
    #        t=Title()
    #        t.text='count on'+str(new_date)
            p.title.text='Total '+ agg+' of '+measure+' on selected dates'
            if agg=='sum':
                p.x_range.end=9000
            else:
                p.x_range.end=100
            # print(dfplot.groupby(new_var)[measure].agg(agg))
            
    #         if freq=='M':
    #             slider.end=12
    #             slider.title='month'
    #             df1=dfplot.groupby([new_var,pd.Grouper(freq=freq)])[measure].agg(agg).reset_index()
    #             new_source = {'x' : list(df1.set_index(new_var)[measure]),
    #                           'y' : list(df1.set_index(new_var).index)}
    #             source2.data = new_source  
    #             p.y_range.factors = list(dfplot.groupby(new_var).agg(agg).index)
    # #        t=Title()
    # #        t.text='count on'+str(new_date)
    #             p.title.text='Total '+ agg+' of '+measure+' on selected dates by month'
    #             if agg=='sum':
    #                 p.x_range.end=9000
    #             else:
    #                 p.x_range.end=100
    #             print(dfplot.groupby([new_var,pd.Grouper(freq=freq)])[measure].agg(agg))    
    #         else:
    #             slider.end=(y-x).days
    #             slider.title='day'
    #             df1=dfplot.groupby([new_var,pd.Grouper(freq=freq)])[measure].agg(agg).reset_index()
    #             new_source = {'x' : list(dfplot.groupby(new_var)[measure].agg(agg)), 
    #                           'y' : list(dfplot.groupby(new_var)[measure].agg(agg).index)}
    #             source2.data = new_source  
    #             p.y_range.factors = list(dfplot.groupby(new_var).agg(agg).index)
    # #        t=Title()
    # #        t.text='count on'+str(new_date)
    #             p.title.text='Total '+ agg+' of '+measure+' on selected dates by day'
    #             if agg=='sum':
    #                 p.x_range.end=9000
    #             else:
    #                 p.x_range.end=100
    #             print(dfplot.groupby(new_var)[measure].agg(agg))

#def slider_callback(attr,old,new):
#     
#    selects_mod = [select.value for select in selects]
#    widgets = dict(zip(categories, selects_mod))
#    new_var = var_select.value
#    x = initial_date.value
#    y = final_date.value
#    value=slider.value
#    dfplot = get_df(df, widgets)
#    new_date = min_date + datetime.timedelta(days=value)
#    new_data = {'x': list(dfplot.loc[str(new_date): str(new_date)].groupby(new_var).m1.sum()),
#                              'y': list(dfplot.loc[str(new_date): str(new_date)].groupby(new_var).m1.sum().index)}
#    #p.x_range.end=dfplot.groupby(['ws_date','description']).leads.count().reset_index().leads.max()+10
#    source2.data=new_data
        
                            
initial_date.on_change('value',freq_callback)    
final_date.on_change('value',freq_callback) 
slider.on_change('value', freq_callback)  
frequency.on_change('value',freq_callback) 
select_m.on_change('value',freq_callback)
agg_select.on_change('value',freq_callback)
res_button.on_change('active',freq_callback)
for select in selects:
    select.on_change('value', freq_callback)
var_select.on_change('value', freq_callback)

layout=row(column(res_button,var_select, initial_date, final_date,frequency, slider,agg_select, select_m, selects[0], selects[1], selects[2]), p)


curdoc().add_root(layout)

