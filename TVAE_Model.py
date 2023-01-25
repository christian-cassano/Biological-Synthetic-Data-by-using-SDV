''' Model TVAE
	epochs=1, batch_size=500 (Default paramiter should be: epochs=300, batch_size=500)

	it recalls 5 functions from utilities.py 
	(the one for the nonymization only if required by setting the paramiter anonymize_fields)
'''
import pandas as pd
from sdv.tabular import TVAE
from sdv.evaluation import evaluate
from sdv.sampling import Condition
from matplotlib import pyplot as plt
import openpyxl
import numpy as np
import utilities 


data = pd.read_excel('Synthetic_Dataset_run_06_12_2021_163219.xlsx')
primary_key = "ID"

model = TVAE(primary_key=primary_key, epochs=1, batch_size=500)
model.fit(data)

model.save('SyntheticData/TVAE.pkl')
#model.load('my_model_TVAE.pkl')

new_data = model.sample(num_rows=200)

# print(data['Hemoglobin'].mean())
# print(data['Hemoglobin'].std())


utilities.report(data,new_data,primary_key)

utilities.plotting_column('TVAE',data,new_data,primary_key)
utilities.plotting_column_pair('TVAE',data,new_data,primary_key,column_names=['Hemoglobin', 'BMB'])
utilities.plotting_data_synthetic('TVAE',data,new_data)