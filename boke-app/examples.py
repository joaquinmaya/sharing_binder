#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 00:16:38 2020

@author: danielmaya
"""

import random
import pandas as pd
import numpy as np

a = ['a']
b = ['b']
c = ['c']
d = ['d']
x = ['x']
y = ['y']
z = ['z']
w = ['w']
v = ['v']

a1 = ['a1']
a2 = ['a2']
a3 = ['a3']
a4 = ['a4']
a5 = ['a5']
a6 = ['a6']
a7 = ['a7']

b1 = ['b1']
b2 = ['b2']
b3 = ['b3']
b4 = ['b4']
b5 = ['b5']
b6 = ['b6']
b7 = ['b7']

c1 = ['c1']
c2 = ['c2']
c3 = ['c3']
c4 = ['c4']
c5 = ['c5']
c6 = ['c6']
c7 = ['c7']

d1 = ['d1']
d2 = ['d2']
d3 = ['d3']
d4 = ['d4']
d5 = ['d5']
d6 = ['d6']
d7 = ['d7']

dates = pd.date_range(start='2019-10-05', end='2020-02', freq='D', name='date')

cat_1 = a*20 + b*30 + c*40 + d*30

cat_2 = x*3+y*2+z*8+w*7 + x*10+y*4+w*16 + x*10+y*11+z*4+w*10+v*5 + x*10+y*5+v*15
 
cat_3 = a1*5+a2*6+a3*3+a4*6 + b1*2+b2*4+b3*10+b4*14 + c1*10+c2*12+c3*8+c4*5+c5*5 + d1*10+d2*15+d3*5
random.seed(1)
m_1 = random.sample(range(0, 500), 120)
random.seed(2)  
m_2 = random.sample(range(0, 500), 120)
random.seed(3)
m_3 = random.sample(range(0, 500), 120)

d = {'date': dates, 'cat_1': cat_1, 'cat_2': cat_2, 'cat_3': cat_3, 'm1': m_1, 'm2': m_2, 'm3': m_3}

df = pd.DataFrame(d)
df = df.set_index('date').sort_index()

v1 = 'a'
v2 = 'y'
v3 = 'a1'



