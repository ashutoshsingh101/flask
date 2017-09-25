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

class prepare_and_perform_query_with_assumptions:
    def __init__(self,input_string,assumption,appid,server,medical_test_wolram_query_flag,type_of_calculator,variable_input_dict ):
        self.medical_test_wolram_query_flag = medical_test_wolram_query_flag
        self.assumption = assumption
        self.input_string = input_string
        self.create_and_perform_wolfram_query = wap.WolframAlphaEngine(appid, server)
        self.query_str = self.create_and_perform_wolfram_query.CreateQuery(self.input_string)
        self.wolframalpha_query = wap.WolframAlphaQuery(self.query_str, appid)
        self.type_of_calculator = int(type_of_calculator)
        self.variable_input_dict  = variable_input_dict 
        
    def classify_formula_variables_into_subjective_or_objective(self):
        variable_list_subjective = []
        variable_list_objective = []
        for value_type_dict in self.assumption:
            if value_type_dict['type'][0] == 'FormulaVariable':
                if len(value_type_dict['value']) == 1:
                    variable_list_subjective.append(str(value_type_dict['value'][0].split('-_')[0])+'-_')
                else:
                    variable_list_objective.append(value_type_dict)
        return variable_list_subjective,variable_list_objective

    def grab_value_from_user_input_and_add_unit(self,user_input,unit):
        grabbed_value_list = re.findall(r'(\d+\.?\d*)',user_input)
        if len(grabbed_value_list) > 0:
            user_input = str(grabbed_value_list[0])+''+str(unit)
        return user_input

    def add_subjective_variables_for_blood_alcohol_content_calc(self,query_str,variable_list_subjective):
        names_of_variables_needed_in_calculator = ['numberOf drinks','time','bodyWeight']
        count = 0
        for variable_number in range(len(variable_list_subjective)):
            user_input = self.variable_input_dict[''+str(names_of_variables_needed_in_calculator[variable_number])+'']
            if re.search(r'\d+\.?\d*',user_input):
                if names_of_variables_needed_in_calculator[variable_number] == 'time':
                   user_input = self.grab_value_from_user_input_and_add_unit(user_input,'min')
                elif names_of_variables_needed_in_calculator[variable_number] == 'bodyWeight':
                   user_input = self.grab_value_from_user_input_and_add_unit(user_input,'kg')
                else:
                    user_input = re.findall(r'(\d+\.?\d*)',user_input)[0]
                count = count+1
                query_str = query_str+"&assumption="+str(variable_list_subjective[variable_number])+str(user_input)
        if count == len(variable_list_subjective):
            return query_str
        return False

    def add_subjective_variables_for_physical_exercises_calc(self,query_str,variable_list_subjective):
        print("l: "+str(len(variable_list_subjective)))
        names_of_variables_needed_in_calculator = ['speed','distance','inclination','age','height','weight','restingHeartRate']
        count = 0
        for variable_number in range(len(variable_list_subjective)):
            user_input = self.variable_input_dict[''+str(names_of_variables_needed_in_calculator[variable_number])+'']
            if names_of_variables_needed_in_calculator[variable_number] == 'restingHeartRate':
                if user_input == '':
                    user_input = '70'
            if re.search(r'\d+\.?\d*',user_input):
                if names_of_variables_needed_in_calculator[variable_number] == 'speed':
                   user_input = self.grab_value_from_user_input_and_add_unit(user_input,'kmph')
                elif names_of_variables_needed_in_calculator[variable_number] == 'distance':
                   user_input = self.grab_value_from_user_input_and_add_unit(user_input,'km')
                elif names_of_variables_needed_in_calculator[variable_number] == 'inclination':
                    user_input = self.grab_value_from_user_input_and_add_unit(user_input,'%')
                elif names_of_variables_needed_in_calculator[variable_number] == 'age':
                    user_input = self.grab_value_from_user_input_and_add_unit(user_input,'yr')
                elif names_of_variables_needed_in_calculator[variable_number] == 'height':
                    user_input = self.grab_value_from_user_input_and_add_unit(user_input,'cms')
                elif names_of_variables_needed_in_calculator[variable_number] == 'weight':
                    user_input = self.grab_value_from_user_input_and_add_unit(user_input,'kg')
                elif names_of_variables_needed_in_calculator[variable_number] == 'restingHeartRate':
                    user_input = self.grab_value_from_user_input_and_add_unit(user_input,'bpm')
                else:
                    user_input = re.findall(r'(\d+\.?\d*)',user_input)[0]
                count = count+1
                query_str = query_str+"&assumption="+str(variable_list_subjective[variable_number])+str(user_input)
        if count == len(variable_list_subjective):
            return query_str
        return False

    def add_subjective_variables_for_BMI(self,query_str,variable_list_subjective):
        names_of_variables_needed_in_calculator = ['weight','height']
        count = 0
        for variable_number in range(len(variable_list_subjective)):
            user_input = self.variable_input_dict[''+str(names_of_variables_needed_in_calculator[variable_number])+'']
            if re.search(r'\d+\.?\d*',user_input):
                if names_of_variables_needed_in_calculator[variable_number] == 'weight':
                   user_input = self.grab_value_from_user_input_and_add_unit(user_input,'kg')
                elif names_of_variables_needed_in_calculator[variable_number] == 'height':
                   user_input = self.grab_value_from_user_input_and_add_unit(user_input,'cms')
                else:
                    user_input = re.findall(r'(\d+\.?\d*)',user_input)[0]
                count = count+1
                query_str = query_str+"&assumption="+str(variable_list_subjective[variable_number])+str(user_input)
        if count == len(variable_list_subjective):
            return query_str
        return False
    def add_subjective_variables_for_weight_loss(self,query_str,variable_list_subjective):
        names_of_variables_needed_in_calculator = ['age','height','currentBodyWeight','targetBodyWeight','dailyCalorieIntake']
        count = 0
        for variable_number in range(len(variable_list_subjective)):
            user_input = self.variable_input_dict[''+str(names_of_variables_needed_in_calculator[variable_number])+'']
            if names_of_variables_needed_in_calculator[variable_number] == 'dailyCalorieIntake':
                if user_input == '':
                    count = count+1
            if re.search(r'\d+\.?\d*',user_input):
                if 'Weight' in names_of_variables_needed_in_calculator[variable_number]:
                   user_input = self.grab_value_from_user_input_and_add_unit(user_input,'kg')
                elif names_of_variables_needed_in_calculator[variable_number] == 'height':
                   user_input = self.grab_value_from_user_input_and_add_unit(user_input,'cms')
                elif names_of_variables_needed_in_calculator[variable_number] == 'age':
                   user_input = self.grab_value_from_user_input_and_add_unit(user_input,'yr')
                elif names_of_variables_needed_in_calculator[variable_number] == 'dailyCalorieIntake':
                   user_input = self.grab_value_from_user_input_and_add_unit(user_input,'Cal/day')
                else:
                    user_input = re.findall(r'(\d+\.?\d*)',user_input)[0]
                count = count+1
                query_str = query_str+"&assumption="+str(variable_list_subjective[variable_number])+str(user_input)
        if count == len(variable_list_subjective):
            return query_str
        return False

    def add_subjective_variables_for_heart_risk(self,query_str,variable_list_subjective):
        names_of_variables_needed_in_calculator = ['age', 'ldlCholesterol', 'hdlCholesterol', 'systolicBloodPressure','diastolicBloodBressure']
        count = 0
        for variable_number in range(len(variable_list_subjective)):
            user_input = self.variable_input_dict[''+str(names_of_variables_needed_in_calculator[variable_number])+'']
            if names_of_variables_needed_in_calculator[variable_number] == 'dailyCalorieIntake':
                if user_input == '':
                    count = count+1
            if re.search(r'\d+\.?\d*',user_input):
                if 'cholesterol' in names_of_variables_needed_in_calculator[variable_number]:
                   user_input = self.grab_value_from_user_input_and_add_unit(user_input,'mg/dl')
                elif 'BloodPressure' in names_of_variables_needed_in_calculator[variable_number]:
                   user_input = self.grab_value_from_user_input_and_add_unit(user_input,'mmHg')
                elif names_of_variables_needed_in_calculator[variable_number] == 'age':
                   user_input = self.grab_value_from_user_input_and_add_unit(user_input,'yr')
                else:
                    user_input = re.findall(r'(\d+\.?\d*)',user_input)[0]
                count = count+1
                query_str = query_str+"&assumption="+str(variable_list_subjective[variable_number])+str(user_input)
        if count == len(variable_list_subjective):
            return query_str
        return False
    
    def add_subjective_formula_variables_to_query(self,variable_list_subjective):
        query_str = self.query_str
        names_of_variables_needed_in_calculator = []

        if self.type_of_calculator == 1:
            query_str = self.add_subjective_variables_for_weight_loss(query_str,variable_list_subjective)
            return query_str
        if self.type_of_calculator == 2:
            query_str = self.add_subjective_variables_for_heart_risk(query_str,variable_list_subjective)
            return query_str
        if self.type_of_calculator == 3:
            query_str = self.add_subjective_variables_for_physical_exercises_calc(query_str,variable_list_subjective)
            return query_str
        if self.type_of_calculator == 4:
            query_str = self.add_subjective_variables_for_BMI(query_str,variable_list_subjective)
            return query_str
        if self.type_of_calculator == 5:
            query_str = self.add_subjective_variables_for_blood_alcohol_content_calc(query_str,variable_list_subjective)
            return query_str
        return False
         
    def add_objective_formula_variables_to_query(self,variable_list_objective,query_str):
        count = 0
        if type(query_str) is bool:
            return False
        no_of_obj_variables = len(variable_list_objective)
        variable_names_from_user = self.variable_input_dict.keys()
        for value_type_dict in variable_list_objective:
            for entry in value_type_dict['value']:
                for variable_name in variable_names_from_user:
                    if variable_name.lower() in entry.lower():
                        if ('%3A'+str(self.variable_input_dict[''+variable_name+''])).lower() in entry.lower():
                            count = count+1
                            query_str = query_str+"&assumption="+str(entry)
                            if count == no_of_obj_variables:
                                return query_str
        return False



    def prepare_query_with_formula_variables(self):
        subjective_formula_variables,objective_formula_variables = self.classify_formula_variables_into_subjective_or_objective()   
        query_str = self.add_subjective_formula_variables_to_query(subjective_formula_variables)
        query_str = self.add_objective_formula_variables_to_query(objective_formula_variables,query_str)
        return query_str

    
    def prepare_query_for_medical_tests(self):
        is_medical_test = False
        query_str = self.query_str
        for value_type_dict in self.assumption:
            for value in value_type_dict['value']:
                if 'MedicalTest' in value:
                    is_medical_test = True
                    query_str = query_str+"&assumption="+str(value)

        return query_str

    def perform_query(self):
        if self.medical_test_wolram_query_flag is False:
            query_str = self.prepare_query_with_formula_variables()
        else:
            query_str = self.prepare_query_for_medical_tests()
        if type(query_str) is str:
            result = self.create_and_perform_wolfram_query.PerformQuery(query_str)
            results = wap.WolframAlphaQueryResult(result)
            json_result= json.loads(results.JsonResult())
            return json_result
        else:
            return False