import pandas as pd

def window_data(data, lag=5,num_windows=3, step=1, predict_year=2010, target=None):
    """
    Split up input feature dataframe into windowed data.

    Efficiency improvement: If needed when the datasets get bigger the 3 for loops belowcan be made faster.
    It is copying overlapping windows from one dataframe to another so unless there is a major overhaul..
    we probably need to hold on to one of the for loops but the other 2 could go:

    1. (Straightforward) The inner-most for loop can be replaced by copying a block of 'lag' rows in one go. [Done]
    2. (a bit trickier) The outer-most loop (countries) could be replaced by placing it inside of the..
        split loop and copying one split each for all the countries in one go.

    Bug: Lags are wrong way around. For example if window width of 5 is specified (lag=5) then the lag=1 column..
        gives the 5th value while lag=5 gives the 1st value in the time window.

    Args:
        data: multiIndex dataframe of feature data with index of (country, year) and columns of the feature names.
        lag: size of window
        num_windows: number of windows to gererate
        step: the delta between the windows. 1 will mean that there is maximum overlap between windows.
        predict_year: the year that we are targetting
        target: feature to be used as target
    
    Returns:
        training_data_regressors
        training_data_targets
        test_data_regressors
        test_data_targets
    """
    
    assert(target in list(data.columns.values)), "Target should be in the input dataframe"
    
    countries_in_data = list(data.index.levels[0]) 
    
    #Create an empty test and training dataframes
    regressors_index = pd.MultiIndex.from_product([countries_in_data,
                                  list(range(1,num_windows+1)), list(range(1,lag+1))],
                                 names=[u'country', u'window', u'lag'])
    target_index = pd.MultiIndex(levels=[[],[]],
                           codes=[[],[]],
                           names=[u'country', u'window'])
    test_regressors_index =  pd.MultiIndex.from_product([countries_in_data,list(range(1,lag+1))],
                           names=[u'country', u'lag'])
    test_target_index = countries_in_data   
    training_data_regressors = pd.DataFrame(index=regressors_index, columns=data.columns)
    training_data_targets = pd.DataFrame(index=target_index, columns=[target])
    test_data_regressors = pd.DataFrame(index=test_regressors_index, columns=data.columns)
    test_data_targets = pd.DataFrame(index=test_target_index, columns=[target])
    
    #fill out the training dataframes : training_data_regressors and training_data_targets
    #..and the testing dataframes     : test_data_regressors and test_data_targets
    for country in countries_in_data:
        test_data_targets.loc[country, target] =  data.loc[(country,str(predict_year)), target]

        test_data_regressors.loc[(country,1):(country,lag+1),:] = \
            data.loc[(country,str(predict_year-lag)):(country,str(predict_year-1)), :].values       
            
        for window in range(1,num_windows+1):
            year= predict_year - window       
            #Add the target value for the spilt to the test_data 
            training_data_targets.loc[(country, window),:] = data.loc[(country,str(year)), target]
    
            training_data_regressors.loc[(country,window,1):(country,window,lag+1),:] = \
                data.loc[(country,str(year-lag)):(country,str(year-1)), :].values
    
    #According to pandas docs on multiIndex usage: For objects to be indexed and sliced effectively, they need to be sorted.
    training_data_regressors = training_data_regressors.sort_index()
    training_data_targets = training_data_targets.sort_index()
    test_data_targets = test_data_targets.sort_index()
    
    #unstacking the input features. Each row will now represent a set of features.
    training_data_regressors  = training_data_regressors.unstack(level=2)
    test_data_regressors  = test_data_regressors.unstack(level=1)
    
    
    return training_data_regressors, training_data_targets, test_data_regressors, test_data_targets