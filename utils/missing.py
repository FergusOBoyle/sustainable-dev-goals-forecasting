import pandas as pd


def perform_ffill_bfill(data, predict_year, target):
    """
    Perform forward fill of the data (on a column by column basis) followed by a backfill. For the target feature..
    ignore from the predict_year and onwards.

    Args:
        data: input data frame (countries/year as 2-level index and economic indicators as columns) 
        predict_year: the year that we are targetting
        target: feature to be used as target
          
    Returns:
        data with imputation as specified
    """
    countries_in_orig_data = list(data.index.levels[0]) 
    for country in countries_in_orig_data:
        data.loc[country, 'SI.POV.GINI':] = data.loc[country, 'SI.POV.GINI':].fillna(method='ffill')
        data.loc[country, 'SI.POV.GINI':] = data.loc[country, 'SI.POV.GINI':].fillna(method='bfill')
    
    #Above we did not fill data for the target variable
    #But it is  worth doing so up to but not including the year that we are predicting
    for country in countries_in_orig_data:
        data.loc[(country):(country, str(predict_year-1)), target] = data.loc[(country):(country, str(predict_year-1)), target].fillna(method='ffill')
        data.loc[(country):(country, str(predict_year-1)), target] = data.loc[(country):(country, str(predict_year-1)), target].fillna(method='bfill')
   
    return data

