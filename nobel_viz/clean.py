# Copyright @2016 created by wangleifan 
# Github @minfun
# !/usr/bin/env python
# !-*-encoding:utf-8-*-
import pandas as pd
import numpy as np
from pymongo import MongoClient


def get_mongo_database(db_name, host='localhost', port=27017, username=None, password=None):
    if username and password:
        mongo_url = 'mongodb://%s:%s@%s/%s' % (username, password, host, db_name)
        conn = MongoClient(mongo_url)
    else:
        conn = MongoClient(host, port)
    return conn[db_name]


def dataframe_to_mongo(df, db_name, collection, host='localhost', port=27017, username=None, password=None):
    db = get_mongo_database(db_name, host, port, username, password)
    records = df.to_dict('records')
    db[collection].insert(records)


def clean_data(df):
    df = df.replace('', np.nan)
    df_born_in = df[df.born_in.notnull()]
    df = df[df.born_in.isnull()]
    df = df.drop('born_in', axis=1)
    df.drop(df[df.year == 1809].index, inplace=True)
    df = df[~(df.name == 'Marie Curie')]
    df.loc[(df.name == u'Marie Sk\u0142odowska-Curie') & (df.year == 1911), 'nationality'] = 'France'
    df = df[~((df.name == 'Sidney Altman') & (df.year == 1990))]
    df = df.reindex(np.random.permutation(df.index))
    df = df.drop_duplicates(['name', 'year'])
    df = df.sort_index()
    df.ix[df.name == 'Alexis Carrel', 'category'] = 'Physiology or Medicine'
    df.ix[df.name == 'Ragnar Granit', 'gender'] = 'male'
    df = df[df.gender.notnull()]
    df.ix[df.name == 'Hiroshi Amano', 'date_of_birth'] = '11 September 1960'
    df.date_of_birth = pd.to_datetime(df.date_of_birth)
    df.date_of_death = pd.to_datetime(df.date_of_death, errors='coerce')
    df['award_age'] = df.year - pd.DatetimeIndex(df.date_of_birth).year
    df = df.fillna('null')
    df_born_in = df_born_in.fillna('null')
    # df = df.dropna()
    return df, df_born_in


df = pd.read_json(open('static/data/nobel_winners.json'))
df_winners_bios = pd.read_json(open('static/data/scrapy_nwinners_minibio.json'))
df_clean, df_born_in = clean_data(df)
# print '-----------clean'
# print df_clean
# print '-------------clean'
# print 'borin---------'
# print df_born_in
# print '---------borin'
dataframe_to_mongo(df_clean, 'm_nobel_prize', 'winners')
dataframe_to_mongo(df_born_in, 'm_nobel_prize', 'winners_born_in')
df_winners_all = pd.merge(df_clean, df_winners_bios, how='outer', on='link')
df_winners_all = df_winners_all.fillna('null')
dataframe_to_mongo(df_winners_all, 'm_nobel_prize', 'winners_all')
