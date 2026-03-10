#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 10 10:06:25 2026

@author: dalaislydon
"""

import pandas as pd
dataframe = pd.read_csv('CTD_data.dat' , sep = '\t')
print(dataframe.head())