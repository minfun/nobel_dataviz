# Copyright @2016 created by wangleifan 
# Github @minfun
# !/usr/bin/env python
# !-*-encoding:utf-8-*-
URL_PREFIX = 'api'
MONGO_DBNAME = 'm_nobel_prize'
DOMAIN = {'winners_all':
              {'item_title': 'winners_all',
               'schema':
                   {'nationality': {'type': 'string'},
                    'category': {'type': 'string'},
                    'name': {'type': 'string'},
                    'year': {'type': 'integer'},
                    'gender': {'type': 'string'},
                    'mini_bio': {'type': 'string'}
                    },
                'url': 'winners'
                 }
            }
X_DOMAINS = '*'
HATEOAS = False
PAGINATION = False
