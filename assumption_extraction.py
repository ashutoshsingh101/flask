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

class get_assumptions_and_formula_variables():
    def __init__(self,type_of_calculator):
        self.type_of_calculator = int(type_of_calculator)

 

    def extract_assumptions(self):
        if self.type_of_calculator == 1:
            assumption_list = [{'type': [u'Clash'], 'value': [u'*C.weight+loss-_*Formula-', u'*C.weight+loss-_*Symptom-', u'*C.weight+loss-_*RetailLocationClass-']}, {'type': [u'FormulaSolve'], 'value': [u'*FS-_**WeightLoss.t--', u'*FS-_**WeightLoss.CI--']}, {'type': [u'FormulaVariable'], 'value': [u'*FP.WeightLoss.S-_Gender%3AMale', u'*FP.WeightLoss.S-_Gender%3AFemale']}, {'type': [u'FormulaVariable'], 'value': [u'*F.WeightLoss.age-_40+yr']}, {'type': [u'FormulaVariable'], 'value': [u'*F.WeightLoss.H-_175+cm']}, {'type': [u'FormulaVariable'], 'value': [u'*F.WeightLoss.W1-_82+kg']}, {'type': [u'FormulaVariable'], 'value': [u'*F.WeightLoss.W2-_70+kg']}, {'type': [u'FormulaVariable'], 'value': [u'*F.WeightLoss.CI-_1144+Cal%2Fday']}, {'type': [u'FormulaVariable'], 'value': [u'*FP.WeightLoss.PAL-_PhysicalActivityLevel%3AExtremelyInactive', u'*FP.WeightLoss.PAL-_PhysicalActivityLevel%3ASedentary', u'*FP.WeightLoss.PAL-_PhysicalActivityLevel%3AModeratelyActive', u'*FP.WeightLoss.PAL-_PhysicalActivityLevel%3AVigorouslyActive', u'*FP.WeightLoss.PAL-_PhysicalActivityLevel%3AExtremelyActive']}, {'type': [u'FormulaVariableOption'], 'value': [u'*FVarOpt-_**WeightLoss.W2--', u'*FVarOpt-_**WeightLoss.dW--']}]

        if self.type_of_calculator == 2:
            assumption_list = [{'type': [u'FormulaVariable'], 'value': [u'*FP.HeartDisease.gender-_Gender%3AMale', u'*FP.HeartDisease.gender-_Gender%3AFemale']}, {'type': [u'FormulaVariable'], 'value': [u'*F.HeartDisease.age-_36+yr']}, {'type': [u'FormulaVariable'], 'value': [u'*F.HeartDisease.ldl-_111+mg%2FdL']}, {'type': [u'FormulaVariable'], 'value': [u'*F.HeartDisease.hdl-_54+mg%2FdL']}, {'type': [u'FormulaVariable'], 'value': [u'*F.HeartDisease.sbp-_120+mmHg']}, {'type': [u'FormulaVariable'], 'value': [u'*F.HeartDisease.dbp-_80+mmHg']}, {'type': [u'FormulaVariable'], 'value': [u'*FP.HeartDisease.smoking-_SmokingStatus%3AYes', u'*FP.HeartDisease.smoking-_SmokingStatus%3ANo']}, {'type': [u'FormulaVariable'], 'value': [u'*FP.HeartDisease.diabetes-_DiabetesStatus%3AYes', u'*FP.HeartDisease.diabetes-_DiabetesStatus%3ANo']}]
        if self.type_of_calculator == 3:
            assumption_list = [{'type': [u'Clash'], 'value': [u'*C.running-_*Formula-', u'*C.running-_*Word-']}, {'type': [u'FormulaSolve'], 'value': [u'*FS-_**Running.t--', u'*FS-_**Running.d--', u'*FS-_**Running.v--']}, {'type': [u'FormulaVariable'], 'value': [u'*F.Running.v-_6+mph']}, {'type': [u'FormulaVariable'], 'value': [u'*F.Running.d-_6+mi']}, {'type': [u'FormulaVariable'], 'value': [u'*F.Running.incline-_5+%25']}, {'type': [u'FormulaVariable'], 'value': [u'*FP.Running.S-_Gender%3AMale', u'*FP.Running.S-_Gender%3AFemale']}, {'type': [u'FormulaVariable'], 'value': [u'*F.Running.age-_35+yr']}, {'type': [u'FormulaVariable'], 'value': [u'*F.Running.H-_175+cm']}, {'type': [u'FormulaVariable'], 'value': [u'*F.Running.W-_72+kg']}, {'type': [u'FormulaVariable'], 'value': [u'*F.Running.HRResting-_68+bpm']}, {'type': [u'FormulaVariableOption'], 'value': [u'*FVarOpt-_**Running.v-.*Running.age-.*Running.H-.*Running.incline-.*Running.HRResting--', u'*FVarOpt-_**Running.p-.*Running.age-.*Running.H-.*Running.incline-.*Running.HRResting--']}]

        if self.type_of_calculator == 4:
            assumption_list = [{'type': [u'Clash'], 'value': [u'*C.BMI-_*Formula-', u'*C.BMI-_*MedicalTest-', u'*C.BMI-_*Financial-', u'*C.BMI-_*Airline-']}, {'type': [u'FormulaSolve'], 'value': [u'*FS-_**BodyMassIndex.BMI--', u'*FS-_**BodyMassIndex.H--', u'*FS-_**BodyMassIndex.W--']}, {'type': [u'FormulaVariable'], 'value': [u'*FP.BodyMassIndex.S-_Gender%3AMale', u'*FP.BodyMassIndex.S-_Gender%3AFemale']}, {'type': [u'FormulaVariable'], 'value': [u'*F.BodyMassIndex.W-_70+kg']}, {'type': [u'FormulaVariable'], 'value': [u'*F.BodyMassIndex.H-_170+cm']}]

        if self.type_of_calculator == 5:
            assumption_list = [{'type': [u'FormulaSolve'], 'value': [u'*FS-_**BloodAlcohol.BAC--', u'*FS-_**BloodAlcohol.T--', u'*FS-_**BloodAlcohol.drinks--']}, {'type': [u'FormulaVariable'], 'value': [u'*F.BloodAlcohol.drinks-_2']}, {'type': [u'FormulaVariable'], 'value': [u'*F.BloodAlcohol.T-_1+h']}, {'type': [u'FormulaVariable'], 'value': [u'*F.BloodAlcohol.W-_140+lb']}, {'type': [u'FormulaVariable'], 'value': [u'*FP.BloodAlcohol.S-_Gender%3AMale', u'*FP.BloodAlcohol.S-_Gender%3AFemale']}]

        return assumption_list
           

      