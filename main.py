import utilities 
from pyaml_env import parse_config
import pandas as pd

def main(config):
	#
	model_name = config["models"]["active"]
	data = pd.read_excel(config["models"][model_name]["data_path"])
	# Check if the Anonymization flag is active or not 
	if not config["models"][model_name]['Anonymization']['active']:
		#  if the Anonymization flag is not active, the anonymize_fields is None
		anonymize_fields=None
	else:
		#  if the Anonymization flag is  active, we use the anonymize_fields method to create the anonymize_fields
		anonymize_fields=utilities.anonymize_fields(config["models"][model_name]['Anonymization']['name_of_the_fields'],
					 								config["models"][model_name]['Anonymization']['category_of_the_fields'])
	#Check which model we want to run and import the correct library 
	#Based on the configuration settings it initializes the choosing model 
	if model_name == "TVAE":
		from sdv.tabular import TVAE
		model = TVAE(primary_key=config["models"][model_name]["primary_key"], 
					 epochs=config["models"][model_name]["epochs"], 
					 batch_size=config["models"][model_name]["batch_size"],
					 anonymize_fields=anonymize_fields)
	elif(model_name == "CopulaGAN"):
		from sdv.tabular import CopulaGAN
		model = CopulaGAN(primary_key=config["models"][model_name]["primary_key"], 
						  epochs=config["models"][model_name]["epochs"], 
						  batch_size=config["models"][model_name]["batch_size"],
					 	  anonymize_fields=anonymize_fields,
					 	  field_distributions =  config["models"][model_name]['field_distributions'])
	else:
		from sdv.tabular import GaussianCopula
		model = GaussianCopula(primary_key=config["models"][model_name]["primary_key"], 
						 	   anonymize_fields=anonymize_fields,
					 	       field_distributions =  config["models"][model_name]['field_distributions'])
	# Fit of the data 
	model.fit(data)
	# Saving of the model for future use
	model.save('SyntheticData/'+model_name+'.pkl')
	#model.load('my_model_'+model_name+'.pkl')
	#Creation of the DataFrame with the synthetic data  
	new_data = model.sample(num_rows =config["models"][model_name]['num_rows'])
	
	utilities.report(data,new_data,config["models"][model_name]["primary_key"])
	utilities.plotting_column(model_name,data,new_data,config["models"][model_name]["primary_key"])
	utilities.plotting_column_pair(model_name,data,new_data,config["models"][model_name]["primary_key"])
	utilities.plotting_data_synthetic(model_name,data,new_data)

if __name__ == "__main__":
	#parsing to retrieve the configuration settings
	config = parse_config("./config.yaml")
	main(config)

