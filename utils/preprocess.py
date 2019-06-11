import pandas as pd

def window_data2(data, lag=5,num_windows=3, step=1, predict_year=2010, target=None):
    """
    Split up input feature dataframe into windowed data.

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
    
    assert(target in list(data.columns.values)), "Feck"
    
    countries_in_data = list(data.index.levels[0]) 
    
    #Create an empty test and training dataframes
    regressors_index = pd.MultiIndex(levels=[[],[],[]],
                            codes=[[],[],[]],
                            names=[u'country', u'window', u'lag'])
    target_index = pd.MultiIndex(levels=[[],[]],
                           codes=[[],[]],
                           names=[u'country', u'window'])
    test_regressors_index =  pd.MultiIndex(levels=[[],[]],
                           codes=[[],[]],
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

        for l in range(1,lag+1):
            year = predict_year - l
            test_data_regressors.loc[(country,l),:] = data.loc[(country,str(year)), :]  

        for window in range(1,num_windows+1):
            year= predict_year - window       
            #Add the target value for the spilt to the test_data 
            training_data_targets.loc[(country, window),:] = data.loc[(country,str(year)), target]
            for l in range(1,lag+1):
                year = year -1
                training_data_regressors.loc[(country,window,l),:] = data.loc[(country,str(year)), :]
    
    #According to pandas docs on multiIndex usage: For objects to be indexed and sliced effectively, they need to be sorted.
    training_data_regressors = training_data_regressors.sort_index()
    training_data_targets = training_data_targets.sort_index()
    test_data_targets = test_data_targets.sort_index()
    
    #unstacking the input features. Each row will now represent a set of features.
    training_data_regressors  = training_data_regressors.unstack(level=2)
    test_data_regressors  = test_data_regressors.unstack(level=1)
    
    
    return training_data_regressors, training_data_targets, test_data_regressors, test_data_targets