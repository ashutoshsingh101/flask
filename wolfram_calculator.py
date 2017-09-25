#!/usr/bin/env python
# -*- coding: utf-8 -*-
import wap
import json
import re
import pandas as pd
import numpy as np
import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb
np.set_printoptions(threshold=np.inf)
import difflib
import time
import assumption_extraction
import prepare_and_perform_wolfram_query
import supervise_wolfram_extraction
import sys


class wolfram_calculators:

    def __init__(self,type_of_calculator,variable_input_dict):
        self.type_of_calculator = type_of_calculator
        self.variable_input_dict = variable_input_dict

    def think_its_name(self,server,appid,input_string, medical_test_wolfram_query_flag):
        get_assumptions = assumption_extraction.get_assumptions_and_formula_variables(self.type_of_calculator)
        assumption_list = get_assumptions.extract_assumptions()
        prepare_and_perform_query = prepare_and_perform_wolfram_query.prepare_and_perform_query_with_assumptions(input_string,assumption_list,appid,server,medical_test_wolfram_query_flag,self.type_of_calculator,self.variable_input_dict)
        json_result = prepare_and_perform_query.perform_query()
        return json_result
     

    def wolfram_query_for_calculators(self,json_result,count_of_re_querying,server,appid,input_string):
        medical_test_wolfram_query_flag = False
        count_of_re_querying = count_of_re_querying + 1
        supervise_data_extraction= supervise_wolfram_extraction.supervise_extraction_of_data(json_result,medical_test_wolfram_query_flag,self.type_of_calculator)
        if count_of_re_querying < 3:
            result_dict = supervise_data_extraction.retrieving_all_pods_from_data()
            if type(result_dict) is bool:
                self.wolfram_query_for_calculators(json_result,count_of_re_querying,server,appid,input_string)
            if type(result_dict) is dict:
                return result_dict
        else:
            print('Sorry')
            return {'sorry':'no result query fail'}

    def for_calculator_operations(self):
        medical_test_wolfram_query_flag = False
        count_of_re_querying = 0
        input_test_name = ''
        server = 'http://api.wolframalpha.com/v2/query.jsp'
        appid = 'EEKVX9-HGPX4GPUWY'
        input_string = ''
         
        if int(self.type_of_calculator) == 1:
            input_string = 'weight loss'
            json_result = self.think_its_name(server,appid,input_string, medical_test_wolfram_query_flag)
        if int(self.type_of_calculator) == 2:
            input_string = 'heart disease risk'
            json_result = self.think_its_name(server,appid,input_string, medical_test_wolfram_query_flag)
            
        if  int(self.type_of_calculator) == 3:
            input_string = 'running'
            json_result = self.think_its_name(server,appid,input_string, medical_test_wolfram_query_flag)
            
        if int(self.type_of_calculator) == 4:
            input_string = 'BMI'
            json_result = self.think_its_name(server,appid,input_string, medical_test_wolfram_query_flag)
            
        if int(self.type_of_calculator) == 5:
            input_string = 'Am I too drunk to drive?'
            json_result = self.think_its_name(server,appid,input_string, medical_test_wolfram_query_flag)

        if type(json_result) is not bool:
                result_dict = self.wolfram_query_for_calculators(json_result,count_of_re_querying,server,appid,input_string)
                return result_dict
        else:
            return {'sorry':'no result json fail'}
