from sdv import Metadata
from sdmetrics.reports.single_table import QualityReport
from sdmetrics.reports.utils import get_column_plot
from sdmetrics.reports.utils import get_column_pair_plot
from matplotlib import pyplot as plt
import numpy as np
import warnings
warnings.filterwarnings("ignore")



''' Creation of the final report. It takes 3 parameters as arguments:
    data: an array representing the real data
    new_data: an array representing the synthetic data
    primary_key: string, representing the primary_key
'''
def report(data,new_data,primary_key = "ID"):
    metadata_map = creation_metadata(data,primary_key)

    report = QualityReport()
    report.generate(data, new_data, metadata_map)
    report.get_details(property_name='Column Shapes')
    report.get_visualization(property_name='Column Shapes')
    report.get_visualization(property_name='Column Pair Trends')



''' Creation of the matadeta for the SDmetrics. It takes 2 parameters as arguments:
    data: an array representing the real data
    primary_key: string, representing the primary_key
'''
def creation_metadata(data,primary_key):
    dict_column = dict((key,value) for key,value in data.dtypes.items())
    column_information = {}
    for el in dict_column:
        column_information[el] = {}
        if dict_column[el] == "int64":
            column_information[el]["type"] = "numerical"
            column_information[el]["subtype"] = "integer"
        elif dict_column[el] == "float64":
            column_information[el]["type"] = "numerical"
            column_information[el]["subtype"] = "float"
        else:
            column_information[el]["type"]= "id"
            column_information[el]["subtype"]=  "string"
            column_information[el]["regex"]=  "[0-9]"
    metadata_map = {"primary_key" : "ID", "fields": column_information}
    return metadata_map



''' Anonymization of the data. It takes 2 parameters as arguments:
    name_of_the_fields: The name of the field that we want to anonymize
    category_of_the_fields: The category of the field that we want to use when we generate fake values for it
    (if we want to use it just add the paramiter anonymize_fields into the model file)
'''
def anonymize_fields(name_of_the_fields,category_of_the_fields):
    return dict((name_of_the_fields[i],category_of_the_fields[i])  for i in range(len(name_of_the_fields)))



''' Plot Real vs. Synthetic Data for column_names ('chosen'). It takes 4 parameters as arguments:
    model: the type of model used
    new_data: an array representing the synthetic data
    primary_key: string, representing the primary_key
    column_names: the colums we want to plot 
'''
def plotting_column(model,data,new_data,primary_key,column_names=['AOD','Neutrophils','Hemoglobin','Platelets','BMB','BMRS']):
    metadata_map = creation_metadata(data,primary_key)
    for column_name in column_names:
        fig = get_column_plot(
        real_data=data,
        synthetic_data=new_data,
        metadata=metadata_map,
        column_name=column_name
        )
        fig.write_image('Image/'+model+'/SDV_Metrics_'+model+'_'+column_name+'.png')
        #fig.show()



''' Plot Real vs. Synthetic Data for columns_names 'Chosen_colum' and 'Gender'. It takes 4 parameters as arguments:
    model: the type of model used
    data: an array representing the real data
    new_data: an array representing the synthetic data
    primary_key: string, representing the primary_key
    column_names: the colums we want to plot 
'''
def plotting_column_pair(model,data,new_data,primary_key,column_names=['AOD','Neutrophils','Hemoglobin','Platelets','BMB','BMRS']):
    metadata_map = creation_metadata(data,primary_key)
    for column_name in column_names:
        fig = get_column_pair_plot(data,new_data,[column_name,"Gender"],metadata_map)
        fig.write_image('Image/'+model+'/SDV_Metrics_'+model+'_pairing_'+'Gender'+column_name+'.png')
        #fig.show()



''' Plot the synthetic data in comparison with the real data. It takes 4 parameters as arguments:
    model: the type of model used
    data: an array representing the real data
    new_data: an array representing the synthetic data
    primary_key: string, representing the primary_key
    column_names: the colums we want to plot 
'''
def plotting_data_synthetic(model,data,new_data,column_names=['AOD','Neutrophils','Hemoglobin','Platelets','BMB','BMRS']):
    for column_name in column_names:
        x_min = min(data[column_name].min(),new_data[column_name].min())
        x_max = max(data[column_name].max(),new_data[column_name].max())
        n_bins = 50

        bins_hemo = [x_min + k*(x_max - x_min)/n_bins for k in range(n_bins)]

        hist, bin_edges = np.histogram(data[column_name], bins=bins_hemo, density=True)
        hist_new, bin_edges = np.histogram(new_data[column_name], bins=bins_hemo, density=True)
    
        #print(hist)
        #print(bin_edges)
    
        figsize = (14,8)
        fsize = 18
        dpi = 300
        plot_params = {
            'linewidth': 0.9,
            'markersize': 1.5,
            'markeredgewidth': 2.0
        }
        plt.xlabel(column_name)
        plt.ylabel("Frequency")
        plt.figure(figsize=figsize)
        
        plt.plot(bin_edges[:-1], hist, color='red', label='Original')
        plt.plot(bin_edges[:-1], hist_new, color='blue', label=model)
        
        plt.legend(loc='upper left')
        plt.savefig('Image/'+model+'/comparison_'+model+'_'+column_name+'.png', dpi=dpi)
        plt.close()



''' Creation of the Hinstogram plot for each colums of the Real data. It takes 2 parameters as arguments:
    model: the type of model used
    data: an array representing the real data    
'''
def get_histo(model,data):
    distributions = model.get_distributions()
    
    for i in data.columns:
        print( i)
        print(data[i].value_counts())
        data[i].hist()
        plt.savefig('Histo/'+i+'.png')
        plt.close()

