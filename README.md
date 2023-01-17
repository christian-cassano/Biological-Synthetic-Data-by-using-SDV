# Generating-Synthetic-Data-by-using-SDV
Biological Synthetic Data by using SDV

OVERVIEW:

Variational AutoEncoders is a deep learning approach for building synthetic data.

In this project we use The Synthetic Data Vault (SDV) which is an ecosystem of libraries for creating synthetic data that enables users to quickly learn about single-table, datasets in order to create new Biological synthetic data that is identical to the original dataset in terms of format and statistical characteristics.

When training machine learning models, synthetic data can then be used to complement, enhance, and in some circumstances replace real data. It also makes it possible to test software systems that depend on data, like machine learning, without running the risk of disclosing sensitive information.

It's powered by a number of deep learning-based and probabilistic graphical modelling algorithms. We make use of novel hierarchical generative modelling and recursive sampling approaches to enable a range of data storage architectures.

SINGLE TABLE DATA MODELS IN SDV ECOSYSTEM USED:

1 - GaussianCopulaModel 
is a tool to model multivariative distributions by using Copula function, 

Copula function is a multivariate cumulative distribution function, where each variable's marginal probability distribution has a uniform shape on the range [0, 1]. is useful in order to explain or represent the interdependence (correlation) between random variables.
this mathematical function enables us to analyse the dependencies between the marginal distributions of multiple random variables in order to characterise the joint distribution of those random variables.


2 - CopulaGANModel 
is a CTGAN model variation that makes the work of learning the data for the underlying CTGAN model easier by utilising the CDF-based modification that the GaussianCopulas apply.


3 - TVAEmodel
is based on the VAE-based Deep Learning data synthesiser that was demonstrated in the paper Modeling Tabular Data Using Conditional GAN at NeurIPS 2020.
