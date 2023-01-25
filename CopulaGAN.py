import pandas as pd
from sdv.tabular import CopulaGAN
import openpyxl
import numpy as np
from matplotlib import pyplot as plt
import utilities

data = pd.read_excel('Synthetic_Dataset_run_06_12_2021_163219.xlsx')
primary_key = "ID"
model = CopulaGAN(primary_key=primary_key, epochs=1, batch_size=500)

model.fit(data)
model.save('SyntheticData/CopulaGAN.pkl')

new_data = model.sample(num_rows=200)

print(new_data.head())


utilities.report(data,new_data,primary_key)

utilities.plotting_column('CopulaGAN',data,new_data,primary_key)
utilities.plotting_column_pair('CopulaGAN',data,new_data,primary_key,column_names=['Hemoglobin', 'BMB'])
utilities.plotting_data_synthetic('CopulaGAN',data,new_data)