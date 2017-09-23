from flask import Flask,jsonify,request
import os
import wolfram_calculator
app = Flask(__name__)

@app.route('/',methods=['GET'])
def home():
    return "Working"


@app.route('/',methods=['POST'])
def post():
    input_json = request.get_json()
    type_of_calculator = input_json['type']
    input_variable_dict = input_json['variables']
    medical_calculation = wolfram_calculator.wolfram_calculators(type_of_calculator,input_variable_dict)
    result_dict = medical_calculation.for_calculator_operations()
    keys_of_result_dict = result_dict.keys()
    if 'sorry' not in keys_of_result_dict:
      input_variable_dict = input_variable_dict.update(result_dict)  
    return jsonify(result_dict)
    



if __name__ == '__main__':
	port = int(os.environ.get("PORT", 8080))
	app.run(host='0.0.0.0', port=port)
	#app.run(host ='0.0.0.0:80')
