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

#--------------------------------------------------------------------------------------------------------------------------------
total_tests_of_labtests_online = [u'5-HIAA', u'17-Hydroxyprogesterone', u'A/G Ratio', u'HbA1c', u'Absolute neutrophils', u'ACE', u'Acetaminophen', u'Acetylcholinesterase', u'AChR Antibody', u'ACR', u'ACT', u'ACTH', u'Adenosine Deaminase', u'ADH', u'AFB Testing', u'AFP Maternal', u'AFP Tumor Markers', u'Albumin', u'Aldolase', u'Aldosterone', u'ALK Mutation (Gene Rearrangement)', u'Allergy Blood Testing', u'ALP', u'Alpha-1 Antitrypsin', u'ALT', u'AMA', u'Amikacin',
u'Aminoglycoside Antibiotics', u'Ammonia', u'Amniocentesis', u'Amylase', u'ANA', u'ANCA', u'Androstenedione', u'Anion Gap', u'Anti-CCP', u'Anti-DNase B', u'Anti-dsDNA', u'Anti-LKM-1', u'Anti-Mullerian Hormone', u'Antibody ID, RBC', u'Anticentromere Antibody', 
u'Antiphospholipids', u'Antithrombin', u'APC Resistance', u'Apo A-I', u'Apo B', u'APOE Genotyping, Alzheimer Disease',
u'APOE Genotyping, CVD', u'aPTT', u'Arbovirus Testing', u'Arterial Blood Gases', u'ASCA', u'ASO', u'AST', u'Autoantibodies', u'B Vitamins', u'B-cell Ig Gene Rearrangement', u'BCR-ABL1', u'Beta-2 Glycoprotein 1 Antibodies', u'Beta-2 Microglobulin Kidney Disease', u'Beta-2 Microglobulin Tumor Marker', u'Bicarbonate', u'Bilirubin', u'Blood Culture', u'Blood Donation', u'Blood Gases', u'Blood Ketones', u'Blood Smear',
u'Blood Transfusion', u'Blood Typing', u'BMP', u'BNP', u'Body Fluid Analysis', u'Bone Markers', u'Bone Marrow', u'BRCA', u'Breast Cancer, Gene Expression', u'BUN', u'c-ANCA', u'C-peptide', u'C-telopeptide', u'C. difficile', u'CA 15-3', u'CA 19-9', u'CA 27.29', u'CA-125', u'Caffeine', u'Calcitonin', u'Calcium', u'Calprotectin', u'CALR Mutation', u'Carbamazepine', u'Cardiac Biomarkers',
u'Cardiac Risk', u'Cardiolipin Antibodies', u'Catecholamines', u'CBC', u'CCP Antibody', u'CD4 Count', u'CEA', u'Celiac Disease Tests', u'Cell-Free Fetal DNA', u'Ceruloplasmin', u'CF Gene Mutations', u'Chem 7', u'Chemistry Panels', u'Chickenpox', u'Chlamydia', u'Chloride', u'Cholesterol', u'Cholinesterase', u'Chromogranin A', u'Chromosome Analysis', u'Chymotrypsin', u'CK', u'CK-MB', u'Clopidogrel',
u'Clostridium difficile', u'CMP', u'CMV Tests', u'CO2, Total',
u'Coagulation Cascade', u'Coagulation Factors', u'Cold Agglutinins', u'Complement', u'Coombs, Direct', u'Coombs, Indirect', u'Copper', u'Cortisol', u'Creatinine', u'Creatinine Clearance', u'CRP', u'CRP, high-sensitivity', u'Cryoglobulins', u'CSF Analysis', u'Cyclosporine', u'Cystatin C', u'D-dimer', u'DCP', u'Dengue Fever', u'DHEAS', u'Diabetes Autoantibodies', u'Differential', u'Digoxin', u'Dilute Russell Viper Venom Test',
u'Direct Antiglobulin Test', u'Direct LDL-C', u'Drug Abuse Testing', u'E. coli (Shiga toxin-producing)', u'EBV Antibodies', u'eGFR', u'EGFR [Her-1]', u'Elastase', u'Electrolytes', u'Electrophoresis', u'Emergency/Overdose Drug Testing', u'ENA Panel', u'Erythropoietin',
u'ESR', u'Estradiol', u'Estrogen/Progesterone Receptors', u'Estrogens', u'Ethanol', u'Factor V Leiden', u'Fecal Fat', u'Fecal Occult Blood Test', u'Ferritin', u'fFN', u'Fibrinogen', u'FIP1L1-PDGFRA', u'First Trimester Screening', u'Flu Tests', u'Folate', u'Free Light Chains', u'Free T3', u'Free T4', u'Fructosamine', u'FSH', u'Fungal Tests', u'G6PD', u'Gastrin', u'Genetic Tests for Targeted Cancer Therapy', u'Gentamicin', u'GFR', u'GGT', u'GI Pathogens Panel', u'Glucose',
u'Gonorrhea', u'Gram Stain', u'Group B Strep Screen', u'Growth Hormone', u'H. pylori', u'Haptoglobin', u'hCG Pregnancy', u'hCG Tumor Marker', u'HDL', u'HE4', u'Heavy Metals', u'Hematocrit', u'Hemoglobin', u'Hemoglobin A1c', u'Hemoglobinopathy Eval', u'Heparin Anti-Xa', u'Hepatitis A', u'Hepatitis B', u'Hepatitis C', u'Hepatitis Panel', u'HER2/neu', u'Herpes', u'Histamine', u'Histone Antibody', 
u'HIT Antibody', u'HIV Antiretroviral Drug Resistance', u'HIV Screening', u'HIV Viral Load', u'HLA Testing', u'HLA-B27', u'Homocysteine', u'HPV', u'hs-CRP', u'HTLV', u'IgE, Total', u'IGF-1', u'IMA', u'Immunoelectrophoresis', u'Immunoglobulins', u'Immunophenotyping', u'Influenza Tests', 
u'Inhibin A', u'INR', u'Insulin', u'Interleukin-6', u'Intrinsic Factor Antibody', u'Ionized Calcium', u'Iron Tests', u'Iron, serum', u'IRT', u'JAK2 Mutation', u'Kappa/Lambda Ratio', u'Karyotyping', u'Ketones, blood', u'Kidney Stone Analysis', u'Kidney Stone Risk Panel', u'KRAS Mutation', u'Lactate', u'Lactoferrin', u'Lactose Tolerance Tests', u'LD', u'LDL', u'LDL-P', u'Lead', u'Legionella', u'Leptin', u'Levetiracetam', u'LH', u'Lipase', u'Lipid Profile', u'Lithium', u'Liver Panel', u'Lp(a)', u'Lp-PLA2',
u'Lupus Anticoagulant Testing', u'Lyme Disease', u'Magnesium', u'MCH', u'MCHC', u'MCV', u'Measles', u'Mercury', u'Metanephrines', u'Methotrexate', u'Microalbumin', u'MMA', u'Mononucleosis Test', u'MPA', u'MRSA Screening', u'MTHFR Mutation', u'Mumps', u'Mycoplasma', u'Myoglobin', u'Nicotine / Cotinine', u'NIPT', u'Non-HDL Cholesterol', u'NT-proBNP', u'Osmolality', u'Ova and Parasite Exam', u'p-ANCA', u'P1NP', u'Pap Test', u'PAPP-A', u'Parietal Cell Antibody', u'Parvovirus B19', u'Pericardial Fluid Analysis', u'Peritoneal Fluid Analysis',
u'Pertussis', u'Pharmacogenetic Tests', u'Phenobarbital', u'Phenytoin', u'Phosphorus', u'Plasma Metanephrines', u'Platelet Count', u'Platelet Function Tests', u'Pleural Fluid Analysis', u'PML-RARA', u'Porphyrins', u'Potassium', u'Prealbumin', u'Pregnancy Test', u'Pregnenolone', u'Procalcitonin', u'Progesterone', u'Progesterone Receptors', u'Prolactin',
u'Protein C', u'Protein Electrophoresis', u'Protein S', u'Prothrombin Time', u'PSA', u'PSEN1', u'Pseudocholinesterase', u'PT 20210', u'PTH', u'PTT', u'Quad Screen', u'RBC', u'RBC Antibody ID', u'RBC Antibody Screen', u'RDW', u'Renal Panel', u'Renin', u'Reticulocytes', u'Rheumatoid Factor', u'RSV', u'Rubella', u'Salicylates', u'Second Trimester Screening', u'Semen Analysis', u'Sensitivity Testing', u'Serotonin', u'Serum Iron', u'SHBG', u'Shingles', u'Sickle Cell Tests', u'Sirolimus', u'Smooth Muscle Antibody', u'SMRP', u'Sodium',
u'Soluble Transferrin Receptor', u'Sputum Culture', u'Stool Culture', u'Strep Throat Test', u'Susceptibility Testing', u'Sweat Chloride', u'Synovial Fluid Analysis', u'Syphilis', u'T-Cell Receptor Gene Rearrangement', u'T3', u'T4', u'Tacrolimus', u'Tau/A\xdf42', u'TB Screening Tests', u'Testosterone', u'Theophylline', u'Therapeutic Drug Monitoring', u'Throat Culture', 
u'Thrombin Time', u'Thyroglobulin', u'Thyroid Antibodies', u'Thyroid Panel', u'TIBC', u'Tobramycin', u'TORCH', u'Total Protein', u'Toxoplasmosis', u'TPMT', u'Trace Minerals', u'Transferrin', u'Trichomonas', u'Triglycerides', u'Triple Screen', u'Troponin', u'Tryptase', u'TSH', u'tTG Antibody', u'Tumor Markers', u'UIBC', u'UP/CR', u'Uric Acid', u'Urinalysis', u'Urine Albumin', u'Urine Culture', u'Urine Metanephrines', u'Urine Protein', u'Valproic Acid', u'Vancomycin', u'Vitamin A', u'Vitamin B12', u'Vitamin D', u'Vitamin K', u'VLDL',
u'VMA', u'von Willebrand Factor', u'Warfarin Sensitivity Testing', u'WBC', u'WBC Differential', u'West Nile Virus', u'Whooping Cough', u'Widal Test', u'Wound Culture', u'Xylose Absorption', u'Zika Virus Testing', u'ZPP']

#-----------------------------------------------------------------------------------------------------------------------------------------------

total_tests_available = ['AMYLASE ', 'CHLORIDE', 'HOMOCYSTEINE', 'IRON TOTAL IRON BINDING CAPACITY (TIBC) ', 
'% TRANSFERRIN SATURATION BLOOD UREA NITROGEN (BUN)', 'CREATININE - SERUM', 'URIC ACID', 'CALCIUM', 
'BUN / SR.CREATININE RATIO', 'SODIUM', 'LIPASE', 'FOLLICLE STIMULATING HORMONE (FSH)', 'LUTEINISING HORMONE (LH)', 
'PROLACTIN (PRL)', 'TOTAL CHOLESTEROL', 'HDL CHOLESTEROL - DIRECT', 'TRIGLYCERIDES', 'LDL CHOLESTEROL - DIRECT', 
'TC/ HDL CHOLESTEROL RATIO', 'LDL / HDL RATIO', 'VLDL CHOLESTEROL', 'NON-HDL CHOLESTEROL', 'ALKALINE PHOSPHATASE', 
'BILIRUBIN -DIRECT', 'BILIRUBIN - TOTAL', 'BILIRUBIN (INDIRECT)', 'GAMMA GLUTAMYL TRANSFERASE (GGT)', 
'ASPARTATE AMINOTRANSFERASE (SGOT )', 'ALANINE TRANSAMINASE (SGPT)', 'PROTEIN - TOTAL', 'ALBUMIN - SERUM', 'SERUM GLOBULIN', 
'SERUM ALBUMIN/GLOBULIN RATIO', 'TESTOSTERONE', 'TOTAL TRIIODOTHYRONINE (T3)', 'TOTAL THYROXINE (T4) ', 'THYROID STIMULATING HORMONE (TSH)', '25-OH VITAMIN D (TOTAL)', 'VITAMIN B-12', 
'AVERAGE BLOOD GLUCOSE (ABG)', 'HbA1c', 'TOTAL LEUCOCYTES COUNT', 'NEUTROPHILS', 'LYMPHOCYTE PERCENTAGE', 'MONOCYTES', 'EOSINOPHILS', 'BASOPHILS', 'IMMATURE GRANULOCYTE PERCENTAGE(IG%)', 
'NEUTROPHILS - ABSOLUTE COUNT', 'LYMPHOCYTES - ABSOLUTE COUNT', 'MONOCYTES - ABSOLUTE COUNT', 'BASOPHILS - ABSOLUTE COUNT', 'EOSINOPHILS - ABSOLUTE COUNT', 'IMMATURE GRANULOCYTES(IG)', 'TOTAL RBC', 
'NUCLEATED RED BLOOD CELLS', 'NUCLEATED RED BLOOD CELLS %', 'HEMOGLOBIN', 'HEMATOCRIT(PCV)', 'MEAN CORPUSCULAR VOLUME(MCV)', 'MEAN CORPUSCULAR HEMOGLOBIN(MCH)', 'MEAN CORP.HEMO.CONC(MCHC)', 'RED CELL DISTRIBUTION WIDTH - SD(RDW-SD)', 
'RED CELL DISTRIBUTION WIDTH (RDW-CV)', 'PLATELET DISTRIBUTION WIDTH(PDW)', 'MEAN PLATELET VOLUME(MPV)', 'PLATELET COUNT', 'PLATELET TO LARGE CELL RATIO(PLCR)', 'PLATELETCRIT(PCT)']


#---------------------------------------------------------------------------------------------------------------------------------------



class calculate_percentile_using_database:
    def __init__(self,name_to_use_for_calculation, input_value, age, gender):
        self.name_to_use_for_calculation = name_to_use_for_calculation
        self.input_value = input_value
        self.age = age
        self.gender = gender

    def calculate_percentile(self,frame):
        length = len(frame)
        if length >= 0:
            count = 0
            for value in frame['value'].values:
                try:
                    if type(value) is float or type(value) is str or type(value) is int:
                        if float(value) < float(self.input_value):
                            count = count + 1
                    else:
                        length = length - 1
                        continue
                except ValueError:
                    length = length - 1
                    continue

        percentage_below_you = float(count)/float(length) *100
        percentage_above_you = 100 - percentage_below_you

        data_dictionary ={'percentage of people below your value':percentage_below_you,'percentage of people above your value':percentage_above_you}
        return data_dictionary

    def percentile_on_basis_of_age(self,all_values_of_given_test):
        all_values_of_given_test_dropna = all_values_of_given_test.dropna()
        all_values_of_given_test_dropna = all_values_of_given_test_dropna[all_values_of_given_test_dropna.age != '']
        all_values_of_given_test_dropna['age'] = all_values_of_given_test_dropna['age'].apply(lambda x: int(x))
        age_band_list = ['20-29','30-39','40-49','50-59','60-69','70-79','80-89','90-99']
        for age_band in age_band_list:
            if self.age[0] == age_band[0]:
                age_band_frame = all_values_of_given_test_dropna[np.logical_and(all_values_of_given_test_dropna.age >= int(age_band.split('-')[0]),all_values_of_given_test_dropna.age <= int(age_band.split('-')[1]))]
                break
        data_dictionary = self.calculate_percentile(age_band_frame)
        return data_dictionary


    def percentile_on_basis_of_gender(self,all_values_of_given_test):
        if self.gender == 'M':
            values_for_male_gender = all_values_of_given_test[all_values_of_given_test.gender == 'M']
            data_dictionary = self.calculate_percentile(values_for_male_gender)
        if self.gender == 'F':
            values_for_female_gender = all_values_of_given_test[all_values_of_given_test.gender == 'F']
            data_dictionary = self.calculate_percentile(values_for_female_gender)
        return data_dictionary
    
    def normal_percentile(self,all_values_of_given_test):
        data_dictionary = self.calculate_percentile(all_values_of_given_test)
        return data_dictionary

    def connect_to_database_to_form_result_dictionary (self):
        data_dictionary = {}
        db = MySQLdb.connect(host = 'localhost',
            user = 'root',
            password = 'jubi',
            db = 'parsed')

        query = 'select report.age,report.gender,test.value,test.name from report join profile on report.report_id=profile.report_report_id join test on profile.profile_id=test.profile_profile_id where test.name like '+ '\"%'+self.name_to_use_for_calculation+'%\"'+''
        
        all_values_of_given_test = pd.read_sql(query, db)
        data_dictionary.update({'overall':self.normal_percentile(all_values_of_given_test)})
        data_dictionary.update({'within your gender':self.percentile_on_basis_of_gender(all_values_of_given_test)})
        data_dictionary.update({'within you age group':self.percentile_on_basis_of_age(all_values_of_given_test)})
        return data_dictionary








class get_percentile_from_wolfram:
    def __init__(self,input_test_name,count_of_re_querying,server,appid,input_string):
        self.input_test_name = input_test_name
        self.count_of_re_querying = count_of_re_querying
        self.server = server
        self.appid = appid
        self.input_string = input_string

    def think_its_name(self,server,appid,input_string,type_of_calculator, medical_test_wolram_query_flag):
        get_assumptions = assumption_extraction.get_assumptions_and_formula_variables_from_basic_query(server,appid,input_string,type_of_calculator)
        assumption_list = get_assumptions.perform_basic_query_and_extract_assumptions()
        prepare_and_perform_query = prepare_and_perform_wolfram_query.prepare_and_perform_query_with_assumptions(input_string,assumption_list,appid,server,medical_test_wolram_query_flag,type_of_calculator)
        json_result = prepare_and_perform_query.perform_query()
        return json_result
    
    def check_validity_of_test_name_for_wolfram_query_try(self):
        highest_similarity = 0
        for test_name in total_tests_of_labtests_online:
            similarity = difflib.SequenceMatcher(None,str(test_name.encode('utf-8')).lower(),self.input_test_name.lower()).ratio()
            if similarity > highest_similarity:
                highest_similarity = similarity
                name_to_use_for_calculation = test_name
        re_query_flag = True
        if highest_similarity > .7:
            validate_test_name = raw_input("Is "+name_to_use_for_calculation+" the test you are looking for?Enter Yes or No: ")
            
            if validate_test_name.lower() == 'yes':
                re_query_flag = True
                return re_query_flag
            else:
                return re_query_flag
        else:
            return re_query_flag


    def wolfram_query_for_medical_test(self,count_of_re_querying): 
        count_of_re_querying = count_of_re_querying + 1   
        ype_of_calculator = 0
        medical_test_wolram_query_flag = True
        type_of_calculator = 0
        json_result = self.think_its_name(self.server,self.appid,self.input_string,type_of_calculator, medical_test_wolram_query_flag)

        supervise_data_extraction= supervise_wolfram_extraction.supervise_extraction_of_data(json_result,medical_test_wolram_query_flag,type_of_calculator)
        reference_distribution_table_dict = supervise_data_extraction.retrieving_all_pods_from_data()
        
        re_query_flag = True
        if type(reference_distribution_table_dict) is bool and count_of_re_querying < 5:
            if count_of_re_querying == 1:
                re_query_flag = self.check_validity_of_test_name_for_wolfram_query_try()

            if re_query_flag is False:
                print('Sorry, Name Not Found')
            else: 
                self.wolfram_query_for_medical_test()








def get_user_input_for_test_name():
    input_test_name = raw_input('Enter test name: ')
    highest_similarity = 0
    for test_name in total_tests_available:
        similarity = difflib.SequenceMatcher(None,test_name.lower(),input_test_name.lower()).ratio()
        if similarity > highest_similarity:
            highest_similarity = similarity
            name_to_use_for_calculation = test_name
    return name_to_use_for_calculation,input_test_name        


def get_other_details_of_user():
    value_flag = False
    gender_flag = False
    age_flag = False
    input_value = raw_input('Enter your value: ')
    if re.match(r'(\d+\.?\d*)',input_value):
        input_value = re.findall(r'(\d+\.?\d*)',input_value)[0]
        print(input_value)
        value_flag = True
    elif re.match(r'(\.\d+)',input_value):
        input_value = re.findall(r'(\.\d+)',input_value)[0]
        print(input_value)
        value_flag = True
    gender_identifier = raw_input('Enter 1 if male 2 if female: ')
    age = raw_input('Enter your age: ')
    if re.match(r'\d{1,2}',age):
        age = re.findall(r'(\d{1,2})',age)[0]
        print(age)
        age_flag = True
    if str(gender_identifier) == 1:
        gender_flag = True
        gender = 'M'
    else:
        gender_flag = True
        gender = 'F'
    if value_flag is True and gender_flag is True and age_flag is True:
        return input_value, age, gender
    else:
        print('Something went wrong.Please check your details and try again')
        get_other_details_of_user()




def validate_test_name(count_of_spelling_mistake_try):
    count_of_spelling_mistake_try = count_of_spelling_mistake_try + 1
    name_to_use_for_calculation,input_test_name = get_user_input_for_test_name()
    validate_test_name = raw_input("Is "+name_to_use_for_calculation+" the test you are looking for?Enter Yes or No: ")
    if 'yes' in validate_test_name.lower():     
        input_value, age, gender = get_other_details_of_user()
        return name_to_use_for_calculation,input_test_name, input_value, age, gender

    elif 'no' in validate_test_name.lower():
        if count_of_spelling_mistake_try < 3:
            print('please check spelling and try again')
            validate_test_name()
        else:
            return 
    else:
        if count_of_spelling_mistake_try < 3:
            print("sorry didn't get that.Please try again")
            validate_test_name()
        else:
            return




def for_medical_test_operations():
    percentile_information = {}
    count_of_spelling_mistake_try = 0
    name_to_use_for_calculation,input_test_name,input_value, age, gender = validate_test_name(count_of_spelling_mistake_try)
    calculate_percentile_for_test = calculate_percentile_using_database(name_to_use_for_calculation, input_value, age, gender)

    percentile_information = calculate_percentile_for_test.connect_to_database_to_form_result_dictionary()
    

    server = 'http://api.wolframalpha.com/v2/query.jsp'
    appid = 'EEKVX9-HGPX4GPUWY'
    input_string = ""+str(input_test_name)+" "+str(input_value)
    if len(percentile_information) != 0 and percentile_information is not None:
        print(percentile_information)
    else: 
        count_of_re_querying = 0
        print('looking up')
        get_wolfram_percentile = get_percentile_from_wolfram(input_test_name,count_of_re_querying,server,appid,input_string)
        get_wolfram_percentile.wolfram_query_for_medical_test(count_of_re_querying)

for_medical_test_operations()
