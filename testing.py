import unittest 
import pandas as pd
import utilities 
import numpy as np
from pyaml_env import parse_config

class TestCreationMetadata(unittest.TestCase):
	global regex	
	
	config = parse_config("./config.yaml")
	model_name = config["models"]["active"]
	regex = config["models"][model_name]["regex_primary_key"]
	
	
	def test_passing_no_rows(self):
		
		data_without_rows = pd.DataFrame(data={'ID': [],
									           'col1': [],
									           'col2' : [],
									   	       'col3' : []})
		primary_key_test = 'ID'
		with self.assertRaises(Exception):
			utilities.creation_metadata(data_without_rows,primary_key_test)

	def test_not_passing_data(self):
		
		data_test = None		
		primary_key_test = 'ID'
		with self.assertRaises(Exception):
			utilities.creation_metadata(data_without_rows,primary_key_test)		
	
	def test_not_passing_primary_key(self):
		data_test = pd.DataFrame(data={'ID': ['SYNTHETIC1'],'col1':[1]})
		primary_key_test = None
		with self.assertRaises(Exception):
			utilities.creation_metadata(data_test,primary_key_test)


	def test_wrong_format_primary_key(self):
		data_test = pd.DataFrame(data={'ID':['1']})
		primary_key_test = 'ID'
		with self.assertRaises(Exception):
			utilities.creation_metadata(data_test,primary_key_test)

	def test_primary_key_not_type_string(self):
		data_test = pd.DataFrame()
		primary_key_test = 1
		with self.assertRaises(Exception):
			utilities.creation_metadata(data_test,primary_key_test)		
		
	def test_primary_key_is_not_present_as_feature(self):
		data_test = pd.DataFrame(data={'col1': [1],
									           'col2' : [2],
									   	       'col3' : [3]})
		primary_key_test = 'ID'
		with self.assertRaises(Exception):
			utilities.creation_metadata(data_test,primary_key_test)
	
	def test_negative_integer(self):
		primary_key_test = 'ID'
		data_test = pd.DataFrame(data={'ID': ["SYNTHETIC1", "SYNTHETIC2"],
									   'col1' : [-1,-2]})
		fields = {'ID': {'type' : 'id',
						'subtype' : 'string',
						'regex' :regex},
				'col1': {'type' : 'numerical',
						'subtype' : 'integer'}}
		metadata_map_test_expected = {"primary_key" : primary_key_test, "fields": fields}		
		self.assertEqual( utilities.creation_metadata(data_test,primary_key_test), metadata_map_test_expected)							 



	def test_creation_metadata(self):
		'''
		Test for the creation_metadata method
		'''

		#Setting a primary key
		primary_key_test = 'ID'
		# Creation of a sample Dataframe 
		data_test = pd.DataFrame(data={'ID': ["SYNTHETIC1", "SYNTHETIC2"],
									   'col1': [3.4, 4.6],
									   'col2' : [1,2],
									   	'col3' : ['tier1','tier2']})
		fields = {'col1': {'type' : 'numerical',
									'subtype' : 'float'},
							'col2': {'type' : 'numerical',
									 'subtype' : 'integer'},
							'ID': {'type' : 'id',
									 'subtype' : 'string',
									 'regex' : regex},
							'col3': {'type' : 'categorical'}}

		# Creation of the expected metadata dictionary returns from creation_metadata method
		metadata_map_test_expected  = {"primary_key" : primary_key_test, "fields": fields}		
		# Assert if the returns of the 	creation_metadata method is what we expect 
		self.assertEqual( utilities.creation_metadata(data_test,primary_key_test), metadata_map_test_expected)
		

class TestAnonymizeFields(unittest.TestCase):
		'''
		Test for different size of Array:

		'''
	# From two differet size of Arrays, the test is going to check if the function will throw an exception when the arrays have different size
	def test_different_length_arrays(self):
		name_of_the_fields_test = ['col1','col2','col3']
		category_of_the_fields_test = ['address','job']
		with self.assertRaises(Exception):
			utilities.anonymize_fields(name_of_the_fields_test,category_of_the_fields_test)

	# From two null Arrays, the test is going to check if the function will throw an exception if the arrays will have the Null size
	def test_array_null_size(self):
		name_of_the_fields_test = []
		category_of_the_fields_test = []
		expected = {}
		self.assertEqual( utilities.anonymize_fields(name_of_the_fields_test,category_of_the_fields_test), expected)

	# From one Array and one None, the test is going to check if the function will throw an exception if one or both the input arguments are None
	def test_None_parameter(self):
		name_of_the_fields_test = None
		category_of_the_fields_test = []
		with self.assertRaises(Exception):
			utilities.anonymize_fields(name_of_the_fields_test,category_of_the_fields_test)

	# From type Int and type String, the test is going to check if the function will throw an exception if the arguments passed are not Array type
	def test_argument_not_type_list(self):
		name_of_the_fields_test = 1
		category_of_the_fields_test = 'string'
		with self.assertRaises(Exception):
			utilities.anonymize_fields(name_of_the_fields_test,category_of_the_fields_test)

	# From two Arrays of mixed Types, the test is going to check if the function will throw an exception if the ywo arrays are mixed types
	def test_mixed_type_argument(self):
		name_of_the_fields_test = [1,'1']
		category_of_the_fields_test = [2,'2']
		self.assertEqual( utilities.anonymize_fields(name_of_the_fields_test,category_of_the_fields_test), {"1":"2","1":"2"})
		
	def test_anonymize_fields(self):

		'''
			Test for the anonymize_fields method
		'''
		# From two Arrays, the test is going to check if the function will return a dictionary with key name of the field with value category of the field 
		#Creation of the input parameters for the anonymize_fields method 
		name_of_the_fields_test = ['col1','col2','col3']
		category_of_the_fields_test = ['address','job','phone_number']
		# Creation of the expected  dictionary returns from anonymize_fields method
		result_map = {'col1' : 'address',
					  'col2' : 'job',
					  'col3' : 'phone_number'}
		#Test if the expect and the return value are equal 				  
		self.assertEqual( utilities.anonymize_fields(name_of_the_fields_test,category_of_the_fields_test), result_map)
		

if __name__ == "__main__":
	print("This is Test!")
	unittest.main()	
