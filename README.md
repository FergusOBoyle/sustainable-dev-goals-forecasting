# sustainable-dev-goals-forecasting
Time-series forecasting using machine learning methods.

## Packages

The code can be run from a set of Jupyter notebooks (in the notebooks directory) with support from some python ultily files (in the utils directory). Installing Anaconda and running jupyter from it is the easiest way to go (see below).

The required packages are specified in the environment.yml file. The environment and all required packages can be reconstructed in an anaconda environment by following the instructions in the Execution section. 

## Files

README.md: This file.  
notebooks/clean_input_streams.ipynb: Data Preparation before modelling
notebooks/linear_regression_predictor.ipynb: Linear Models
notebooks/naive_predictor.ipynb: Naive Prediction Model
notebooks/data_gathering/data_collection.ipynb: World Bank API interface
notebooks/data_gathering/world_bank_bulk_csv.ipynb: Reading from World Bank csv file
utils/evaluate.py : utilities for evaluating models
utils/missing.py: utilities related to missing values
utils/preprocess.py: utiltiies for preprocessing of data before modelling 
environment.yml: List of required packages for setting up of Anaconda environment. 
LICENSE: License file

## Installation and execution

### Checkout code from Github

1. Follow [these](https://help.github.com/en/articles/cloning-a-repository) instructions for cloning this repo to a location on your computer.

### Installing Anaconda

1. Download Anaconda from [here](https://www.anaconda.com/distribution/).
2. Install Anaconda using [these](https://docs.anaconda.com/anaconda/install/) instructions.
3. Create a new environment in the Anaconda Shell: >conda create -n my_new_env --file environment.yml.
4. Switch to the new environment: >conda activate my_new_env.

### Running Jupyter Notebook

1. The jupyter notebooks of this project can be accessed by launching Jupyter Notebook from the Anaconda Shell (>jupyter notebook). 
2. Then, within the Jupyter Notebook App, navigate to the location of the sustainable-dev-goals-forecasting folder and open the required notebooks.

### Reading data,preprocessing, and execution of the predictive models

1. Follow the instructions in the next section to download the World Development Indicator data.
2. Run world_bank_bulk_csv to read data 

## Access to data from the World Bank

1. World Bank [Data Catalog](https://datacatalog.worldbank.org/dataset/world-development-indicators)
2. Click on the "Data & Resources" tab.
3. Download data in CSV format.
4. Extract files from the donloaded folder.
5. Place WDIData.csv into a data/ subfolder of your local repo.

 
