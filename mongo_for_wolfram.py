import pymongo

class mongo_db_database():
	def __init__(self):
		pass

	def connect_to_database(self,type_of_calculator,database_document):
		uri = 'mongodb://ashutosh:nodedb123@ds139124.mlab.com:39124/health_personnel_google_places' 
		client = pymongo.MongoClient(uri)
		db = client.get_default_database()
		if int(type_of_calculator) == 1:
			db['weightLoss'].insert_one(database_document)
		if int(type_of_calculator) == 2:
			db['heartRisk'].insert_one(database_document)
		if int(type_of_calculator) == 3:
			db['physicalExercise'].insert_one(database_document)
		if int(type_of_calculator) == 5:
			db['bloodAlcoholContent'].insert_one(database_document)
		client.close()
		







