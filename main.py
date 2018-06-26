import json
import logging

import pandas as pd
import sqlalchemy as sa

from util import get_path, log


def mysql_info(config):
    with open(get_path('config', 'mysql_info.json')) as f:
        data = json.load(f)
    return data[config]


@log(logging.ERROR)
def handle(msg):
    pass


@log()
def tasks(name):
    df = pd.read_sql('select * from {}'.format(t), rel_db)
    df.to_csv(get_path('{}.csv'.format(t)), sep='|', index=False)

    dev_db.execute('''
LOAD DATA LOCAL INFILE '{0}.csv'
INTO TABLE {0}
CHARACTER SET utf8
FIELDS TERMINATED BY '|'
ENCLOSED BY '"'
LINES TERMINATED BY '\\n'
IGNORE 1 LINES'''.format(t))


rel_db = sa.create_engine('mysql+pymysql://', connect_args=mysql_info('from'))
dev_db = sa.create_engine('mysql+pymysql://', connect_args=mysql_info('to'))

for t in mysql_info('tables'):
    try:
        tasks(t)
    except Exception as e:
        handle(str(e))

