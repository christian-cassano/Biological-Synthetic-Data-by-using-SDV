import pandas as pd
from sdv.tabular import TVAE
from sdv.evaluation import evaluate
from sdv.sampling import Condition
import openpyxl
import numpy as np

data = pd.read_excel('Synthetic_Dataset_run_06_12_2021_163219.xlsx')


model = TVAE(primary_key='ID', epochs=1, batch_size=500)
model.fit(data)

model.save('my_model_TVAE.pkl')
# model.load('my_model_TVAE.pkl')


print('finished')
new_data = model.sample(num_rows=200)



# print(data['Hemoglobin'].mean())
# print(data['Hemoglobin'].std())

x_min = 2
x_max = 20

n_bins = 50

bins_hemo = [k*(x_max - x_min)/n_bins for k in range(n_bins)]

hist, bin_edges = np.histogram(data['Hemoglobin'], bins=bins_hemo, density=True)
hist_new, bin_edges = np.histogram(new_data['Hemoglobin'], bins=bins_hemo, density=True)

print(hist)
print(bin_edges)

from matplotlib import pyplot as plt

figsize = (14,8)
fsize = 18
dpi = 300
plot_params = {
	'linewidth': 0.9,
	'markersize': 1.5,
	'markeredgewidth': 2.0
}

plt.figure(figsize=figsize)

plt.plot(bin_edges[:-1], hist, color='red', label='Original')
plt.plot(bin_edges[:-1], hist_new, color='blue', label='TVAE')

plt.legend(loc='upper left')
plt.savefig('lol.png', dpi=dpi)
plt.close()

