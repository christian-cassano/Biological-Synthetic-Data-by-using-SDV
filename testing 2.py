import unittest 
import pandas as pd
import utilities 

class TestCreationMetadata(unittest.TestCase):

	def test_creation_metadata(self):
		'''
		Test for the creation_metadata method
		'''

		#Setting a primary key
		primary_key_test = 'col3'
		# Creation of a sample Dataframe 
		data_test = pd.DataFrame(data={'col1': [1, 2],
									   'col2': [3.4, 4.6],
									   'col3' : ['1','2'],
									   	'col4' : ['tier1','tier2']})
		data_test_result = {'col1': {'type' : 'numerical',
									'subtype' : 'integer'},
							'col2': {'type' : 'numerical',
									 'subtype' : 'float'},
							'col3': {'type' : 'id',
									 'subtype' : 'string',
									 'regex' : '[0-9]'},
							'col4': {'type' : 'categorical'}}

		# Creation of the expected metadata dictionary returns from creation_metadata method
		metadata_map_test_result  = {"primary_key" : primary_key_test, "fields": data_test_result}		
		# Assert if the returns of the 	creation_metadata method is what we expect 
		self.assertEqual( utilities.creation_metadata(data_test,primary_key_test), metadata_map_test_result)
		self.assertTrue(utilities.creation_metadata(data_test,primary_key_test)== metadata_map_test_result)
		#Change the expected metadata dictionary to assert the contrary 
		data_test_result['col1']['subtype'] = 'float'	
		self.assertFalse(utilities.creation_metadata(data_test,primary_key_test)== metadata_map_test_result)	


class TestAnonymizeFields(unittest.TestCase):
	def test_anonymize_fields(self):

		'''
			Test for the anonymize_fields method
		'''
		# Creation of the input parameters for the anonymize_fields method
		name_of_the_fields_test = ['col1','col2','col3']
		category_of_the_fields_test = ['address','job','phone_number']
		# Creation of the expected  dictionary returns from anonymize_fields method
		result_map = {'col1' : 'address',
					  'col2' : 'job',
					  'col3' : 'phone_number'}
		#Test if the expect and the return value are equal 				  
		self.assertEqual( utilities.anonymize_fields(name_of_the_fields_test,category_of_the_fields_test), result_map)
		self.assertTrue(utilities.anonymize_fields(name_of_the_fields_test,category_of_the_fields_test)== result_map)
		#Change the expected metadata dictionary to assert the contrary 
		result_map['col1'] = 'person'	
		self.assertFalse(utilities.anonymize_fields(name_of_the_fields_test,category_of_the_fields_test)== result_map)			  





if __name__ == "__main__":
	unittest.main()	
