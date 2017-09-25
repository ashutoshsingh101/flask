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


class extract_weight_loss_data:
    def __init__(self,pods_list):
        self.pods_list = pods_list

    def convert_to_camel_case(self,string):
        string_list = string.strip().split(' ')
        if len(string_list) > 1:
            for index in range(1,len(string_list)):
                string_list[index] = string_list[index].title()
            camel_case_string = ''
            for item in string_list:
                camel_case_string = camel_case_string+str(item)
            return camel_case_string
        else:
            return string.strip()
    
    def extract_data_out_of_pod_regimen_duration(self,pod_item):
        found = False
        parameter_dict = {}
        for inner_pod_list in pod_item:
            if type(inner_pod_list) is list and inner_pod_list[0] == 'subpod':
                for subpod_item in inner_pod_list:
                    if type(subpod_item) is list and subpod_item[0] == 'plaintext':
                        data = str(subpod_item[1])

                        parameter_dict.update({"regimenDuration":data.replace('\n',' ')})
                        parameters_list = re.findall(r'(\d+\s*Cal/day)|(\d+\s*month\s*\d+\s*days)|(\d+\s*kg)',data)

                        parameter_dict.update({"calorieIntake":str(parameters_list[0][0])})
                        parameter_dict.update({"toLoseWeight":str(parameters_list[2][2])})
                        if 'month' in parameters_list[1][1]:
                            months_days = re.findall(r'(\d+)',parameters_list[1][1])
                            parameter_dict.update({"timeInDays":str(int(months_days[0])*30+int(months_days[1]))})
                        else:
                            months_days = re.findall(r'(\d+)',parameters_list[1][1])
                            parameter_dict.update({"timeInDays":str(months_days[0])})
                        return parameter_dict               
        return found
    def extract_data_out_of_pod_maintain_bodyweight(self,pod_item):
        found = False
        maintain_bodyweight_table_dict = {}
        for inner_pod_list in pod_item:
            if type(inner_pod_list) is list and inner_pod_list[0] == 'subpod':
                for subpod_item in inner_pod_list:
                    if type(subpod_item) is list and subpod_item[0] == 'plaintext':
                        maintain_bodyweight_table_rows = subpod_item[1].split('\n')
                        for row_index in range(1,len(maintain_bodyweight_table_rows)):
                            row_data_list = str(maintain_bodyweight_table_rows[row_index]).split(' | ')
                            if len(row_data_list) == 3:
                                maintain_bodyweight_table_dict.update({''+self.convert_to_camel_case(str(row_data_list[0]))+'':{'weight':''+str(row_data_list[1])+'','calorieIntake':''+str(row_data_list[2])+''}})
        
        if len(maintain_bodyweight_table_dict.keys()) >=2:
            return maintain_bodyweight_table_dict   
        return found

    def extract_data_from_required_pods(self):
        found = False
        found_2 = False
        for pod_item in self.pods_list:
            if type(pod_item) is list:
                for inner_pod_list in pod_item:
                    if inner_pod_list[0] == 'title':
                        if 'Weight loss regimen duration' in inner_pod_list[1] or 'Nominal required regimen duration' in inner_pod_list[1]:
                            parameter_dict = self.extract_data_out_of_pod_regimen_duration(pod_item)
                        if 'Caloric intake to maintain body weight' in inner_pod_list[1]:
                            maintain_bodyweight_table_dict = self.extract_data_out_of_pod_maintain_bodyweight(pod_item)
                            maintain_bodyweight_table_dict.update(parameter_dict)
                            return maintain_bodyweight_table_dict 
        return found

class extract_heart_risk_data:
    
    def __init__(self,pods_list):
        self.pods_list = pods_list

    def extract_data_out_of_pod_10year_risk(self,pod_item):
        found = False
        heart_risk_data = {}
        for inner_pod_list in pod_item:
            if type(inner_pod_list) is list and inner_pod_list[0] == 'subpod':
                for subpod_item in inner_pod_list:
                    if type(subpod_item) is list and subpod_item[0] == 'plaintext':
                        data = str(subpod_item[1].split('\n')[0])
                        heart_risk_data.update({"heartRisk":data})
                        percentage_data = re.findall(r'(\d+.?\d*%)',data)
                        if '%' in percentage_data[0]:
                            value = re.findall(r'(\d+.?\d*)',percentage_data[0])
                            heart_risk_data.update({"valueInPercentage":str(value[0])})
                            return heart_risk_data                
        return found

    def extract_data_from_required_pods(self):
        for pod_item in self.pods_list:
            if type(pod_item) is list:
                for inner_pod_list in pod_item:
                    if inner_pod_list[0] == 'title':
                        if '10-year risk of developing coronary heart disease' in inner_pod_list[1]:
                            heart_risk_data = self.extract_data_out_of_pod_10year_risk(pod_item)
                            return heart_risk_data 




class extract_physical_excercises_data:
    def __init__(self,pods_list):
        self.pods_list = pods_list

    def convert_to_camel_case(self,string):
        string_list = string.strip().split(' ')
        if len(string_list) > 1:
            for index in range(1,len(string_list)):
                string_list[index] = string_list[index].title()
            camel_case_string = ''
            for item in string_list:
                camel_case_string = camel_case_string+str(item)
            return camel_case_string
        else:
            return string.strip()

    def extract_data_out_of_pod_metabolic_activities(self,pod_item):
        found = False
        metabolic_activities_table_dict = {}
        for inner_pod_list in pod_item:
            if type(inner_pod_list) is list and inner_pod_list[0] == 'subpod':
                for subpod_item in inner_pod_list:
                    if type(subpod_item) is list and subpod_item[0] == 'plaintext':
                        metabolic_activities_table_rows =  subpod_item[1].split('\n')
                        for row in metabolic_activities_table_rows:
                            columns = row.split('|')
                            if len(columns) >= 2 :
                                found = True
                                metabolic_activities_table_dict.update({''+self.convert_to_camel_case(columns[0])+'':''+columns[1].strip()+''})
        if found is True:
            return metabolic_activities_table_dict
        return found

    def extract_data_from_required_pods(self):     
        for pod_item in self.pods_list:
            if type(pod_item) is list:
                for inner_pod_list in pod_item:
                    if inner_pod_list[0] == 'title':
                        if 'Metabolic properties' in inner_pod_list[1]:
                            metabolic_activities_table_dict = self.extract_data_out_of_pod_metabolic_activities(pod_item)
                            return metabolic_activities_table_dict


class extract_blood_alcohol_content_data:
    def __init__(self,pods_list):
        self.pods_list = pods_list
    
    def convert_to_camel_case(self,string):
        string_list = string.strip().split(' ')
        if len(string_list) > 1:
            for i in range(1,len(string_list)):
                string_list[i] = string_list[i].title()
            camel_case_string = ''
            for item in string_list:
                camel_case_string = camel_case_string+str(item)
            return camel_case_string
        else:
            return string.strip()


    def extract_data_out_of_pod_estimated_result(self,pod_item):
        found = False
        estimated_result_table_dict = {'legalDirivingLimitInIndia' : '.03%'}
        for inner_pod_list in pod_item:
            if type(inner_pod_list) is list and inner_pod_list[0] == 'subpod':
                for subpod_item in inner_pod_list:
                    if type(subpod_item) is list and subpod_item[0] == 'plaintext':
                        estimated_result_table_rows =  subpod_item[1].split('\n')
                        for row in estimated_result_table_rows:
                            columns = row.split('|')
                            if len(columns) >= 2 :
                                found = True
                                if (columns[0].encode('utf-8')).strip() == 'blood alcohol percentage' :
                                    estimated_result_table_dict.update({''+self.convert_to_camel_case(columns[0])+'':''+(columns[1]).strip()+''})
                                if 'total time to' in (columns[0]).strip():
                                    estimated_result_table_dict.update({''+self.convert_to_camel_case(columns[0]).replace('0.08%','LegalLimit')+'':''+(columns[1]).strip()+''})
        if found is True:
            return estimated_result_table_dict
        return found
    def extract_data_from_required_pods(self):
        for pod_item in self.pods_list:
            if type(pod_item) is list:
                for inner_pod_list in pod_item:
                    if inner_pod_list[0] == 'title':
                        if 'Estimated result' in inner_pod_list[1]:
                            estimated_result_table_dict = self.extract_data_out_of_pod_estimated_result(pod_item)
                            return estimated_result_table_dict

class extract_medical_test_data:
    def __init__(self,pods_list):
        self.pods_list = pods_list

    def convert_to_camel_case(self,string):
        string_list = string.strip().split(' ')
        if len(string_list) > 1:
            for index in range(1,len(string_list)):
                string_list[index] = string_list[index].title()
            camel_case_string = ''
            for item in string_list:
                camel_case_string = camel_case_string+str(item)
            return camel_case_string
        else:
            return string.strip()

    def extract_data_out_of_pod_reference_distribution(self,pod_item):
        reference_distribution_table_dict = {}
        for inner_pod_list in pod_item:
            if type(inner_pod_list) is list and inner_pod_list[0] == 'subpod':
                for subpod_item in inner_pod_list:
                    if type(subpod_item) is list and subpod_item[0] == 'plaintext':
                        reference_distribution_table_rows = subpod_item[1].split('\n')
                        for row_index in range(len(reference_distribution_table_rows)):

                            columns = reference_distribution_table_rows[row_index].split('|')
                            if len(columns) >=2:
                                reference_distribution_table_dict.update({''+self.convert_to_camel_case(columns[0])+'':''+(columns[1]).strip()+''})
        return reference_distribution_table_dict

    def extract_data_from_required_pods(self):
        medical_information_obtained = False
        for pod_item in self.pods_list:
            if type(pod_item) is list:
                for inner_pod_list in pod_item:
                    if inner_pod_list[0] == 'title':
                        if 'Reference distribution' in inner_pod_list[1]:
                            medical_information_obtained = True
                            print('required pods working')
                            reference_distribution_table_dict = self.extract_data_out_of_pod_reference_distribution(pod_item)
                            print(reference_distribution_table_dict)
                            return reference_distribution_table_dict

        return medical_information_obtained


class supervise_extraction_of_data():
    def __init__(self,json_result,medical_test_wolram_query_flag,type_of_calculator):
        self.json_result = json_result
        self.medical_test_wolram_query_flag = medical_test_wolram_query_flag
        self.type_of_calculator = int(type_of_calculator)
            
    def retrieving_all_pods_from_data(self):
        pods_list = []
        for result in self.json_result:
            if type(result) is list:
                if result[0] == 'pod':
                    pods_list.append(result)
        if self.medical_test_wolram_query_flag is False:
            if self.type_of_calculator == 1:
                extracting_weight_loss_data = extract_weight_loss_data(pods_list)
                result_dict = extracting_weight_loss_data.extract_data_from_required_pods()

            if self.type_of_calculator == 2:
                extracting_heart_risk_data = extract_heart_risk_data(pods_list)
                result_dict = extracting_heart_risk_data.extract_data_from_required_pods()
            if self.type_of_calculator == 3:
                extracting_physical_excercises_data = extract_physical_excercises_data(pods_list)
                result_dict = extracting_physical_excercises_data.extract_data_from_required_pods()
            if self.type_of_calculator == 4:
                extracting_physical_excercises_data = extract_bmi_data(pods_list)
                result_dict= extracting_physical_excercises_data.extract_data_from_required_pods()
            if self.type_of_calculator == 5:
                extracting_physical_excercises_data = extract_blood_alcohol_content_data(pods_list)
                result_dict= extracting_physical_excercises_data.extract_data_from_required_pods()
            return result_dict

        if self.medical_test_wolram_query_flag is True:
            extracting_medical_test_data = extract_medical_test_data(pods_list)
            print('supervise working')
            reference_distribution_table_dict = extracting_medical_test_data.extract_data_from_required_pods()
            return reference_distribution_table_dict