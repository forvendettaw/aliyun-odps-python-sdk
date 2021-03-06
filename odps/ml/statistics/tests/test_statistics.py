# encoding: utf-8
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

from __future__ import print_function

from odps.df import DataFrame
from odps.config import options
from odps.ml.utils import TEMP_TABLE_PREFIX
from odps.ml.statistics import *
from odps.ml.tests.base import MLTestBase, tn

IONOSPHERE_TABLE = tn('pyodps_test_ml_ionosphere')
IRIS_TABLE = tn('pyodps_test_ml_iris')
IONOSPHERE_PRINCOMP_TABLE = tn('pyodps_test_ml_iono_princomp')
IONOSPHERE_FEATURE_STATS = tn('pyodps_test_ml_iono_feature_stats')
IONOSPHERE_REPLACE_WOE = tn('pyodps_test_ml_iono_replace_woe')
IONOSPHERE_QUANTILE_TABLE = tn('pyodps_test_ml_iono_quantile')


class TestStatistics(MLTestBase):
    def setUp(self):
        super(TestStatistics, self).setUp()
        self.create_ionosphere(IONOSPHERE_TABLE)

    def test_histograms(self):
        options.runner.dry_run = True

        ds = DataFrame(self.odps.get_table(IONOSPHERE_TABLE)).roles(label='class')
        histograms(ds, _cases=self.gen_check_params_case({
            'outputTableName': TEMP_TABLE_PREFIX + 'histograms_0_2_res',
            'selectedColNames': ','.join('a%02d' % i for i in range(1, 35)),
            'intervalNum': '10', 'inputTableName': IONOSPHERE_TABLE}))

    def test_t_test(self):
        options.runner.dry_run = True

        ds = DataFrame(self.odps.get_table(IONOSPHERE_TABLE)).roles(label='class')
        t_test(ds, x_col='a04', _cases=self.gen_check_params_case(
            {'mu': '0', 'outputTableName': TEMP_TABLE_PREFIX + 't_test_0_2_res', 'confidenceLevel': '0.95',
             'xTableName': IONOSPHERE_TABLE, 'alternative': 'two.sided', 'xColName': 'a04'}))
        t_test(ds, x_col='a04', y_col='a05', _cases=self.gen_check_params_case(
            {'yTableName': IONOSPHERE_TABLE, 'yColName': 'a05', 'mu': '0',
             'outputTableName': TEMP_TABLE_PREFIX + 't_test_0_3_res', 'confidenceLevel': '0.95',
             'xTableName': IONOSPHERE_TABLE, 'alternative': 'two.sided', 'xColName': 'a04'}))

    def test_chisquare(self):
        options.runner.dry_run = True

        df = DataFrame(self.odps.get_table(IONOSPHERE_TABLE))
        chi_square(df, x_col=df.a01, y_col='class', _cases=self.gen_check_params_case(
            {'yColName': 'class', 'xColName': 'a01', 'outputDetailTableName': 'tmp_pyodps_ml_chi_square_0_1_res_2',
             'outputTableName': 'tmp_pyodps_ml_chi_square_0_1_res_1',
             'inputTableName': tn('pyodps_test_ml_ionosphere')}))

    def test_cov(self):
        options.runner.dry_run = True

        df = DataFrame(self.odps.get_table(IONOSPHERE_TABLE)).roles(label='class')
        covariance(df, _cases=self.gen_check_params_case(
            {'outputTableName': 'tmp_pyodps_ml_covariance_0_2_res',
             'selectedColNames': ','.join('a%02d' % i for i in range(1, 35)),
             'inputTableName': tn('pyodps_test_ml_ionosphere')}))

    def test_mat_pearson(self):
        options.runner.dry_run = True

        df = DataFrame(self.odps.get_table(IONOSPHERE_TABLE)).roles(label='class')
        matrix_pearson(df, _cases=self.gen_check_params_case(
            {'outputTableName': 'tmp_pyodps_ml_matrix_pearson_0_2_res',
             'selectedColNames': ','.join('a%02d' % i for i in range(1, 35)),
             'inputTableName': tn('pyodps_test_ml_ionosphere')}))

    def test_quantile(self):
        options.runner.dry_run = True

        df = DataFrame(self.odps.get_table(IONOSPHERE_TABLE)).roles(label='class')
        qt = quantile(df, _cases=self.gen_check_params_case(
            {'inputTableName': tn('pyodps_test_ml_ionosphere'), 'outputTableName': tn('pyodps_test_ml_iono_quantile'),
             'colName': ','.join('a%02d' % i for i in range(1, 35)),
             'N': '100'}))
        qt.persist(IONOSPHERE_QUANTILE_TABLE)
