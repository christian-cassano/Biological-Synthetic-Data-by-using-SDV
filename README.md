# Biological Synthetic Data by using SDV
-------

In this project we use The Synthetic Data Vault (SDV) which is an ecosystem of libraries for creating synthetic data that enables users to quickly learn about single-table, datasets in order to create new Biological synthetic data that is identical to the original dataset in terms of format and statistical characteristics.

When training machine learning models, synthetic data can then be used to complement, enhance, and in some circumstances replace real data. It also makes it possible to test software systems that depend on data, like machine learning, without running the risk of disclosing sensitive information.

It is powered by a number of deep learning-based and probabilistic graphical modelling algorithms. We make use of novel hierarchical generative modelling and recursive sampling approaches to enable a range of data storage architectures.

       
# Getting Started
---------------

to install the application clone the repository use pip:

    git clone https://github.com/christian-cassano/Biological-Synthetic-Data-by-using-SDV
    cd Biological-Synthetic-Data-by-using-SDV
    pip install -r requirements.txt

In order to run script the user need to set the configuration file #config.yaml as follow:

    1 - Choose and Activate the desired model. 
        active : "type of the model we want to run"
    2 - Specify dataset path
    3 - Pass the Primary key of the Dataset
    4 - Specify the regex for the primary key elements 
    5 - Change parameters, such as epochs, batch size, number of rows for the model we wish to run.
    6 - (Optional) - Specify Anonymization for the desired features - Activate by setting "True" 


# FOLDERS:
---------------
find the outcome of the script in the following folders:

   ## SyntheticData 
     in which there are the new data generated. 
     
   ## Histo
     in which there are the histogram of the probability distribution regarding each columns of the real dataset. 
     this process is crucial in order understand  and improve the synthetic generation outcome.
     
   ## Image 
     in which there are the graph that compare the hemoglobine for the genuine dataset with the synthetic one and the graph for the SDMetrics evaluation. 
     this could be done for each model

# IMPORTANT REMINDER:  
-----------
        Always double check the result outcome with SDmetrics chart to asses the purity of the new data generated 


# OVERVIEW OF THE PROJECT TO BETTER UNDERSTAND WHAT THE MODELS INVOLVED DO

## SINGLE TABLE DATA MODELS USED:
------------

## 1 - GaussianCopulaModel 
---------------
is a tool to model multivariative distributions by using Copula function, 
Copula function is a multivariate cumulative distribution function, where each variable's marginal probability distribution has a uniform shape on the range [0, 1]. is useful in order to explain or represent the interdependence (correlation) between random variables.
this mathematical function enables us to analyse the dependencies between the marginal distributions of multiple random variables in order to characterise the joint distribution of those random variables.

The GaussianCopula carried out the following tasks each time we fitted it:

    - learn the data types and format for the passed information.
    - Reversible Data Transforms are used to convert non-numerical and null data into a fully numerical 
      representation from which we can learn the probability distribution
    - Comprehend the probability distribution for each column in the table.
    - Convert the values in each numerical column to their marginal distribution CDF values before applying 
      an inverse CDF transformation of a standard normal to them.
    - Discover the correlations between the freshly generated random variables.
    
After those steps, when we used the sample method to generate new data for our table, the model did the following:

    - Sample from a Multivariate Standard Normal distribution with the learned correlations.
    - Revert the sampled values by computing their standard normal CDF and then applying 
      the inverse CDF of their marginal distributions.
    - Revert the RDT transformations to go back to the original data format.
    
the GaussianCopula had to learn and reproduce the individual distributions of each column in our table, the Marginal Probability Distributions play a critical role. with this model Using the get distributions method, we can investigate the distributions used by the GaussianCopula to design each column.

then we can assing a certain distribution to a specific column, the conditional sampling allows us to generate only values that satisfy certain conditions by sampling from a conditional distribution using the GaussianCopula model. As a list of sdv.sampling, these conditional values can be passed to the sample conditions method. Condition objects or a dataframe can be passed to the sample remaining columns method.
after a sdv.sampling is specified. We can pass in the desired conditions as a dictionary and specify the number of rows for that condition using the Condition object.

in this way we can improve the quality of our new Synthetic data.


## 2 - CopulaGANModel 
---------------
is a CTGAN model variation that makes the work of learning the data for the underlying CTGAN model easier by utilising the CDF-based modification that the GaussianCopulas apply.


The CopulaGAN carried out the following tasks each time we fitted it:

      - learn the data types and format for the passed information.
      - Reversible Data Transforms are used to convert non-numerical and null data into a fully numerical representation 
        from which we can learn the probability distribution
      - Comprehend the probability distribution for each column in the table.
      - Convert the values in each numerical column to their marginal distribution CDF values before applying an inverse 
        CDF transformation of a standard normal to them.
      - Fit a CTGAN model to the transformed data to learn how each column is related to the others.
      
      
After those steps, when we used the sample method to generate new data for our table, the model did the following:

    - Sample rows from the CTGAN model.
    - Revert the sampled values by computing their standard normal CDF and then applying the inverse
      CDF of their marginal distributions.
    - Revert the RDT transformations to go back to the original data format.
    
Then we can assing a certain distribution to a specific column, the conditional sampling allows us to generate only values that satisfy certain conditions by sampling from a conditional distribution using the GaussianCopula model. As a list of sdv.sampling, these conditional values can be passed to the sample conditions method. Condition objects or a dataframe can be passed to the sample remaining columns method.
after a sdv.sampling is specified. We can pass in the desired conditions as a dictionary and specify the number of rows for that condition using the Condition object.

In the CopulaGAN There are a number of extra hyperparameters that regulate its learning behaviour and have an impact on the model's performance in terms of the quality of the generated data and computation time:

      epochs and batch_size:
    
      These arguments specify how many iterations the model will run to optimise its parameters, as well as 
      how many samples will be used in each step. The default values are 300 and 500, respectively, 
      and batch size must always be a multiple of 10.  
   
      These hyperparameters have a direct effect not only on the length of the training process but also
      on the performance of the data, so for new datasets, you might prefer to start by defining a low value 
      on both of them to see how long the training process takes on your data and then increase the number 
      to acceptable values to improve performance.


## 3 - TVAEmodel
---------------
is based on the VAE-based Deep Learning data synthesiser that was demonstrated in the paper Modeling Tabular Data Using Conditional GAN at NeurIPS 2020.

The TVAE model carried out the following tasks:
 
    - it Create a TVAE instance. 
    - Then Incorporate the instance into the data. 
    - Makes artificial replicas of existing data. 
    - If required anonymize PII information. 
    - If needed set hyperparameters to enhance the quality of the output.  
   
## Evaluation Synthetic Data Method 
----

    Synthetic Data Metrics (SDMetrics) is an open source Python library for assessing tabular synthetic data. 
    Utilizing a range of measures, compare fake data to real data, create visual reports.
    
    we can use the SDMetrics library with synthetic data produced by any model at any time because it is model-agnostic.
    
    with SDmetric Producing reports for project is simple. Reports concentrate on a certain feature of synthetic data, 
    like data quality. Drill down using them until you have the answers.
    


# For more details Please visit the [SDV gitHub](https://github.com/sdv-dev)