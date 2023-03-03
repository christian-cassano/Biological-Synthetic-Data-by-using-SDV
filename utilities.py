from sdv import Metadata
from sdmetrics.reports.single_table import QualityReport
from sdmetrics.reports.utils import get_column_plot
from sdmetrics.reports.utils import get_column_pair_plot
from matplotlib import pyplot as plt
import numpy as np
import warnings
import re
from pyaml_env import parse_config
warnings.filterwarnings("ignore")

def report(data,new_data,primary_key = "ID"):
    '''
    Creation of the final report. 
    
    Parameters:
    
        data: an array representing the real data
        new_data: an array representing the synthetic data
        primary_key: string, representing the primary_key
    '''
    metadata_map = creation_metadata(data,primary_key)
    report = QualityReport()
    report.generate(data, new_data, metadata_map)
    report.get_details(property_name='Column Shapes')
    report.get_visualization(property_name='Column Shapes')
    report.get_visualization(property_name='Column Pair Trends')


def creation_metadata(data,primary_key):
    '''
    Creation of the metadata for the SDmetrics. 
    
    Parameters:
    
        data: a DataFrame made out of the real data
        primary_key: string, representing the primary_key of the dataset

    Returns:
       dictionary metadata
    '''
    #Check if the data is empty or None
    if  data.empty:
        raise Exception("Empty Data Set")
    if not (primary_key in data.columns):
        raise Exception("Primary Key is not present as Feature")
              

    #Check if primary_key is of e.g. SYNTETHIC12
    config = parse_config("./config.yaml")
    model_name = config["models"]["active"]
    #Retrieve the Regex of  primary key
    regex    = config["models"][model_name]["regex_primary_key"]
    
    for el in list(data[primary_key]):
        if re.search(regex,el)==None and instance(el,string):
            raise Exception("Wrong Primary Key Formatting")
            break 

    # Creation dictionary with key the column name and value the column type
    dict_column = dict((key,value) for key,value in data.dtypes.items())
    column_information = {}
    # Loop to construct a column_information dict with key the column name and value a dictionary 
    # with keys: type,subtype or regex
    for el in dict_column:
        column_information[el] = {}
        if dict_column[el] == "int64":
            column_information[el]["type"] = "numerical"
            column_information[el]["subtype"] = "integer"
        elif dict_column[el] == "float64":
            column_information[el]["type"] = "numerical"
            column_information[el]["subtype"] = "float"
        elif el == primary_key:
            column_information[el]["type"]= "id"
            column_information[el]["subtype"]=  "string"
            column_information[el]["regex"]=  regex
        else:
            column_information[el]["type"]= "categorical"  
    # creation metadata map with 
    # key primary_key and value primary_key of the dataset 
    # key fields and value the map column_information
    metadata_map = {"primary_key" : primary_key, "fields": column_information}
    return metadata_map


def anonymize_fields(name_of_the_fields,category_of_the_fields):
    '''
    Anonymization of the data. 

    Parameters:
        name_of_the_fields: Array, the name of the field that we want to anonymize
        category_of_the_fields: Array, the category of the field that we want to use when we generate fake values for it
    
    Returns:
        dictionary with key name of the Anonymized fields and value the associated category
    (if we want to use it just add the parameter  anonymize_fields into the config file)
    
    '''
    #Check if the Arguments are not None, otherwise raise an exception.
    if name_of_the_fields == None or  category_of_the_fields == None:
            raise Exception("Passing None argument") 
    # Check if the Arguments are not Array type, otherwise raise an exception.
    if not isinstance(name_of_the_fields,(list,np.ndarray)) or not isinstance(category_of_the_fields,(list,np.ndarray)):
         raise Exception("No Type List/Array") 
    # Check if the Arguments have the same length, otherwise raise an exception.
    if len(name_of_the_fields) != len(category_of_the_fields):
            raise Exception("Length of name_of_the_fields different from Length of category_of_the_fields") 

    name_of_the_fields = np.array(name_of_the_fields,dtype='U')
    category_of_the_fields = np.array(category_of_the_fields,dtype='U')
    return dict((name_of_the_fields[i],category_of_the_fields[i])  for i in range(len(name_of_the_fields)))


def plotting_column(model,data,new_data,primary_key,column_names=['AOD','Neutrophils','Hemoglobin','Platelets','BMB','BMRS']):
    '''
    Plot Real vs. Synthetic Data for column_names 
        
        Parameters:
        
        model: string, the model name used
        data: DataFrame, representing the real data
        new_data: DataFrame representing the synthetic data
        primary_key: string, representing the primary_key
        column_names: array, the columns we want to plot 
    '''
    #Creation metadata by using the specific method
    metadata_map = creation_metadata(data,primary_key)
    #Creation of n plots, with n the size of column_names
    for column_name in column_names:
        fig = get_column_plot(real_data=data,
                              synthetic_data=new_data,
                              metadata=metadata_map,
                              column_name=column_name)
        #Save the Image 
        fig.write_image('Image/'+model+'/SDV_Metrics_'+model+'_'+column_name+'.png')
        fig.show()

def plotting_column_pair(model,data,new_data,primary_key,column_names=['AOD','Neutrophils','Hemoglobin','Platelets','BMB','BMRS']):
    '''
      Plot and Save Real vs. Synthetic Data for columns_names Chosen_colum and Gender
         Parameters:

            model: string, the model name used
            data: DataFrame, representing the real data
            new_data: DataFrame representing the synthetic data
            primary_key: string, representing the primary_key
            column_names: array, the columns we want to plot 
'''
    # Creation metadata by using the specific method
    metadata_map = creation_metadata(data,primary_key)
    #Creation of n plots, with n the size of column_names
    for column_name in column_names:
        fig = get_column_pair_plot(data,new_data,[column_name,"Gender"],metadata_map)
        #Save the Image
        fig.write_image('Image/'+model+'/SDV_Metrics_'+model+'_pairing_'+'Gender'+column_name+'.png')
        fig.show()



def plotting_data_synthetic(model,data,new_data,column_names=['AOD','Neutrophils','Hemoglobin','Platelets','BMB','BMRS']):
    '''
    Plot and Save the synthetic data in comparison with the real data. 
    
     Parameters:

            model: string, the model name used
            data: DataFrame, representing the real data
            new_data: DataFrame representing the synthetic data
            primary_key: string, representing the primary_key
            column_names: array, the columns we want to plot

'''
    # Creation of the Histogram with number of bins equals to 50
    for column_name in column_names:
        x_min = min(data[column_name].min(),new_data[column_name].min())
        x_max = max(data[column_name].max(),new_data[column_name].max())
        n_bins = 50

        bins_hemo = [x_min + k*(x_max - x_min)/n_bins for k in range(n_bins)]

        hist, bin_edges = np.histogram(data[column_name], bins=bins_hemo, density=True)
        hist_new, bin_edges = np.histogram(new_data[column_name], bins=bins_hemo, density=True)
    
        #print(hist)
        #print(bin_edges)
        plt.figure(figsize=(16,8))
        plt.title("Original vs Synthetic Data - "+column_name)
        plt.xlabel(column_name,fontsize=18)
        plt.ylabel("Frequency",fontsize=18)
        plt.plot(bin_edges[:-1], hist, color='red', label='Original')
        plt.plot(bin_edges[:-1], hist_new, color='blue', label=model)
        plt.legend(loc='upper left')
        # Save the Image
        plt.savefig('Image/'+model+'/comparison_'+model+'_'+column_name+'.png', dpi=300)
        plt.show()
        plt.close()



def get_histo(model,data):
    ''' 
    Creation of the Histogram plot for each columns of the Real data. 
    
      Parameters:
        model:  string, the model name used
        data: DataFrame, representing the real data    
'''
    distributions = model.get_distributions()
    # Creation of histogram for each columns in the dataset
    for i in data.columns:
        print(i)
        print(data[i].value_counts())
        data[i].hist()
        # Save the Histogram
        plt.savefig('Histo/'+i+'.png')
        plt.close()

