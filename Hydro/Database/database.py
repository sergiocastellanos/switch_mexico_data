#!/usr/bin/env python
# -*- coding: utf-8 -*-
from credeentials import Credentials as c
c = c()
password = c.password
user = c.user


import pandas as pd
from sqlalchemy import create_engine


BT_all = pd.read_csv('results.csv', encoding='UTF-8', delimiter = ',', dtype = {'fcode':int})

engine = create_engine('postgres://%s:%s@localhost:5433/switch_mexico'%(user,password))

BT_all.to_sql('Hello World', engine, schema='mexico', if_exists = 'replace', chunksize = 10)
