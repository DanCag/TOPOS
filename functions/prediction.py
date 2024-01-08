import pandas as pd
import numpy as np


# tumor detector predictions
def predict( 
    test_nrmlz,
    clf,
    encdr,
    prediction_file):
    
    """Predict TOO
    
    Keyword arguments
    test_nrmlz -- sample-wise + feature-wise normalized test matrix
    clf -- trained classifier object
    encdr -- encoder object
    prediction_file -- path of prediction file (tab-separated file)
    """
    
    
    ## Import data
    
        
    ## Predict
    
    # predictions dataframe
    preds = pd.Series(
        encdr.inverse_transform(
            clf.predict(test_nrmlz)), 
        index = test_nrmlz.index, 
        name = "best_prediction")
    
    # write prediction to tsv file
    preds.to_csv(
        prediction_file,
        sep = '\t', 
        index_label = 'sample')
