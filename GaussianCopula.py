import pandas as pd
from sdv.tabular import GaussianCopula
import openpyxl
from matplotlib import pyplot as plt
import numpy as np



data = pd.read_excel('Synthetic_Dataset_run_06_12_2021_163219.xlsx')



model = GaussianCopula(primary_key='ID')
model.fit(data)
model.save('SyntheticData/GaussianCopula.pkl')

new_data = model.sample(num_rows=200)

print(new_data.head())


#loaded = GaussianCopula.load('SyntheticData/GaussianCopula.pkl')
#new_data = loaded.sample(num_rows=200)


# Setting paramaeters for the graph
x_min = 2
x_max = 20

n_bins = 50

bins_hemo = [x_min + k*(x_max - x_min)/n_bins for k in range(n_bins)]

hist, bin_edges = np.histogram(data['Hemoglobin'], bins=bins_hemo, density=True)
hist_new, bin_edges = np.histogram(new_data['Hemoglobin'], bins=bins_hemo, density=True)

print(hist)
print(bin_edges)


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
plt.plot(bin_edges[:-1], hist_new, color='blue', label='GaussianCopula')

plt.legend(loc='upper left')
plt.savefig('Image/comparison_GaussianCopula.png', dpi=dpi)
plt.close()

