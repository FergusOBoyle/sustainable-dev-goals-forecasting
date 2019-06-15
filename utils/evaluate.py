import pandas as pd
import numpy as np

def mse_countries(true_data, predictions_data, ignore_countries = None):  
    """
    Calculates MSE of country and returns meta data on missing true values and predictions 

    Args:
        true_data: dataframe of  true_data
        predictions_data: dataframe of prediction data for comparing with true_data. Needs to be the..
                          dimension as true_data.
        ignore_countries: Countries to have their predictions ignored. Their predictions are set to NaN
    
    Returns:
        mse: Mean Squared Eror value
        countries_no_true_value: list of countries with no true value
        countries_no_prediction: list of coutries that have a true value bit no prediction
    """
    predictions_data_local = predictions_data.copy()
    
    assert(true_data.shape == predictions_data_local.shape), "Input dataframes need to have same dimensions"
    
    if ignore_countries is not None:
        predictions_data_local.loc[ignore_countries] = np.NaN
    
    mse = np.mean((predictions_data_local - true_data)**2)
    countries_no_true_value = list(true_data[true_data.isna().values].index)
    countries_with_true_value = list(true_data[~true_data.isna().values].index)
    total_countries_with_no_prediction = list(predictions_data_local[predictions_data_local.isna().values].index)
    #What we are interested in is countries that have real values but no predictions.
    countries_no_prediction =  set(countries_with_true_value) & set(total_countries_with_no_prediction)
    countries_predicted = set(countries_with_true_value)
    return mse, countries_no_true_value, countries_no_prediction
