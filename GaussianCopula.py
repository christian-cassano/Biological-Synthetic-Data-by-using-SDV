import pandas as pd
from sdv.tabular import GaussianCopula
import openpyxl
print(openpyxl.__version__)
#python -m pip install --user sdv
data = pd.read_excel('Synthetic_Dataset_run_06_12_2021_163219.xlsx')



print(data.head())


model = GaussianCopula()
model.fit(data)
new_data = model.sample(num_rows=200)

print(new_data.head())

model.save('SyntheticData/GaussianCopula.pkl')

loaded = GaussianCopula.load('SyntheticData/GaussianCopula.pkl')
new_data = loaded.sample(num_rows=200)

print(data.ID.value_counts().max())