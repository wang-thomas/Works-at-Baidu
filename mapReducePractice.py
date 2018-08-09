#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
#
# Copyright (c) 2018 Baidu.com, Inc. All Rights Reserved
#
########################################################################

"""
File: user_eroticism_count.py
Author: zhaoshiyu01(zhaoshiyu01@baidu.com)
Date: 2018/05/30 21:24:49
"""

import os
import sys
sys.path.append(os.path.abspath("%s/../../../../" % __file__))

import re

from minekit.lib import jobs
from minekit.lib import io
from minekit.lib import table
from minekit.lib import utils

job_settings = {
    'hadoop_job_config': {
        'job_name':'${__USERDEFINE__JOB_NAME_PREFIX}' \
        '_user_eroticism_count_${__USERDEFINE__WORK_DATE}',
        'input_dirs': [
            '${__USERDEFINE__INPUT_DATA_PATH}/' \
            '[${__USERDEFINE__START_DATE},${__USERDEFINE__END_DATE}]',
            ],
        'output_dirs': [
            '${__USERDEFINE__RUNTIME_ROOT_PATH}/eroticism_count/' \
            '${__USERDEFINE__START_DATE}_${__USERDEFINE__END_DATE}'
            ],
        'job_conf': {
            'mapred.job.priority': '${__USERDEFINE__JOB_PRIORITY}',
            'mapred.job.map.capacity': '${__USERDEFINE__MAP_CAPACITY}',
            'mapred.job.reduce.capacity': '${__USERDEFINE__REDUCE_CAPACITY}',
            'mapred.reduce.tasks': '${__USERDEFINE__COUNT_REDUCE_TASKS}',
            },
        'options': [
            ('cacheArchive', '${__USERDEFINE__LIB_PATH}/python2.7.12.tar.gz#py'),
            ],
        'cmd_envs': {
            },
        },
}


map_input_cols = ['udwid', 'labels', 'source', 'time', 'title', 'domain', 'method']
map_output_cols = ['labels', 'count']
#reduce_output_cols = ['udwid', 'count']


class WordCountJob(jobs.JobBase):


    @io.input_format.stdin
    def map(self, data_iter):
        for line in data_iter:
            items = line.rstrip().split('\t')
            cats = items[1].split(" ")
            if len(items) == 7:
                for cat in cats:
                    print('%s\t%d' % (cat[0:cat.index(":")], 1))


        return data_iter

    @io.input_format.tab_split_columns(map_output_cols)
    def reduce(self, data_iter):

        def aggregate_expr_count(k, x, y):
            if x['count'] == table.aggregate_start:
                return y['count']
            elif y['count'] == table.aggregate_end:
                return x['count']
            else:
                return int(x['count']) + int(y['count'])

        data_iter = data_iter.aggregate2(
            map_output_cols[:1],
            {'count': aggregate_expr_count},
            on_exception=utils.hadoop_table_exception,
            new_schema=map_output_cols)
            #start_end_elements=('', ''))

        return data_iter


if __name__ == '__main__':
    utils.set_utf8_writer()
    job = WordCountJob(**job_settings)
    job.run()
