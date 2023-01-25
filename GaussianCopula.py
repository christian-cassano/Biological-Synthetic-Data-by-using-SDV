''' Model GaussianCopula
	
	it recalls 4 function from utilities.py
'''


import pandas as pd
from sdv.tabular import GaussianCopula
import openpyxl
from matplotlib import pyplot as plt
import numpy as np
import utilities



data = pd.read_excel('Synthetic_Dataset_run_06_12_2021_163219.xlsx')
primary_key = 'ID'


model = GaussianCopula(primary_key='ID')
model.fit(data)
model.save('SyntheticData/GaussianCopula.pkl')

new_data = model.sample(num_rows=200)

print(new_data.head())


#loaded = GaussianCopula.load('SyntheticData/GaussianCopula.pkl')
#new_data = loaded.sample(num_rows=200)


utilities.report(data,new_data,primary_key)

utilities.plotting_column('GaussianCopula',data,new_data,primary_key)
utilities.plotting_column_pair('GaussianCopula',data,new_data,primary_key,column_names=['Hemoglobin', 'BMB'])
utilities.plotting_data_synthetic('GaussianCopula',data,new_data)
