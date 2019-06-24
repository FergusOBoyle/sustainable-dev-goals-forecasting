import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer

def impute_data_interpolation(data, upto_year, method):
    """
    Interpolation of indicator time-series for each country seperately in indicator dataFrame 

    Args:
        data: multiIndex dataFrame of feature data with index of (country, year) and columns of the feature names.
        upto_year: Year up to and including to interpolate
        method: method of interpolation to be passed on to the pandas interpolation function

    Returns:
        interpolated dataFrame
    """

    #Protect data in caller 
    data_local = data.copy()
    
    #Interpolation. For loop could be removed if data restructured to have time-series on .. 
    # rows (i.e Country and indicator in Index and year as column) 
    for country in data.index.levels[0]:    
        data_local.loc[(country):(country,str(upto_year)),:] = \
            data_local.loc[(country):(country,str(upto_year)),:]. \
            interpolate( method=method, limit_direction='both').values  
    

    #Use mean of indicator for any remaining missing values   
    idx = pd.IndexSlice   
    imp_mean = SimpleImputer(missing_values=np.nan, strategy='mean')
    data_local.loc[idx[:,:str(upto_year)],:] = \
        imp_mean.fit_transform(data_local.loc[idx[:,:str(upto_year)],:])
    #data_local.loc[idx[:,:str(upto_year)],:] = imputed_subset
    
    #Set remaining missing values to 0. (This should be replaced by mean imputation ASAP)
    #idx = pd.IndexSlice
    #data_local.loc[idx[:, :str(upto_year)], :] = data_local.loc[idx[:, :str(upto_year)], :].fillna(0) 
    
    return data_local



def window_data(data, lag=5,num_windows=3, step=1, predict_year=2010, target=None, impute_type=None):
    """
    Split up input feature dataFrame into windowed data.

    Bug: Lags are wrong way around. For example if window width of 5 is specified (lag=5) then the lag=1 column..
        gives the 5th value while lag=5 gives the 1st value in the time window.

    Args:
        data: multiIndex dataframe of feature data with index of (country, year) and columns of the feature names.
        lag: size of window
        num_windows: number of windows to gererate
        step: the delta between the windows. 1 will mean that there is maximum overlap between windows.
        predict_year: the year that we are targetting
        target: feature to be used as target
        impute_type: must be one of ['interpolation'] or None

    Returns:
        data_regressors
        data_targets
    """
    assert(impute_type in ['interpolation', None]), "impute_type must be one of  ['interpolation'] or none"
    assert(target in list(data.columns.values)), "Target should be in the input dataframe"

    if impute_type == 'interpolation':
        impute_func = impute_data_interpolation
    else:
        impute_func = None

    countries_in_data = list(data.index.levels[0]) 
    idx = pd.IndexSlice

    #Create empty test and training dataframes
    regressors_index = pd.MultiIndex.from_product([countries_in_data,
                                                   list(range(1,num_windows+1)), 
                                                   list(range(1,lag+1))],
                                                  names=[u'country', u'window', u'lag'])

    target_index = pd.MultiIndex.from_product([countries_in_data,
                                               list(range(1,num_windows+1))],
                                              names=[u'country', u'window'])

    data_regressors = pd.DataFrame(index=regressors_index, columns=data.columns)
    data_targets = pd.DataFrame(index=target_index, columns=[target])


    #Each increment of window represents moving back a year in time
    for window in range(num_windows):
        year = predict_year - window

        #Redo Imputation every time we move back a year
        #This maintains the requirement not to use information from future years in our imputations 
        if impute_func is not None:
            data_imp = impute_func(data, upto_year=year-1, method='linear' )
        else:
            data_imp = data

        data_targets.loc[idx[:,window+1],:] = data_imp.loc[idx[:,str(year)], target].values

        data_regressors.loc[idx[:,window+1,1:lag+1],:] = \
                data_imp.loc[idx[:,str(year-lag):str(year-1)], :].values

    #According to pandas docs on multiIndex usage: For objects to be indexed and sliced effectively, they need to be sorted.
    data_regressors = data_regressors.sort_index()
    data_targets = data_targets.sort_index()

    #unstacking the input features. Each row will now represent a set of features.
    data_regressors  = data_regressors.unstack(level=2)

    return data_regressors, data_targets