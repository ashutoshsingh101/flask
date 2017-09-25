from flask import Flask,jsonify,request
import os
import wolfram_calculator
import mongo_for_wolfram
app = Flask(__name__)

@app.route('/',methods=['GET'])
def home():
    return "Working"


@app.route('/',methods=['POST'])
def post():
    database = mongo_for_wolfram.mongo_db_database()
    input_json = request.get_json()
    type_of_calculator = input_json['typeOfCalculator']
    input_variable_dict = input_json['variables']
    medical_calculation = wolfram_calculator.wolfram_calculators(type_of_calculator,input_variable_dict)
    result_dict = medical_calculation.for_calculator_operations()
    database_document = {**input_variable_dict, **result_dict}
    keys_of_result_dict = result_dict.keys()
    if 'sorry' in keys_of_result_dict:
        return jsonify(result_dict)

    database.connect_to_database(type_of_calculator,database_document)
    return jsonify(result_dict)
    



if __name__ == '__main__':
	port = int(os.environ.get("PORT", 8080))
	app.run(host='0.0.0.0', port=port)
	#app.run(host ='0.0.0.0:80')
