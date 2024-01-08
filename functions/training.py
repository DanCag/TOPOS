# Modules
import pandas as pd
import numpy as np
from sklearn.svm import SVC
from sklearn.preprocessing import scale, LabelEncoder


# train tumor dector model
def train(
    train_exp,
    train_labels,
    test_features, 
    gene_list_path = ''):
    
    """Train TOO model
    
    Keyword arguments:
    train_exp -- train expression matrix
    train_labels -- train labels
    gene_list_path -- path of gene list file (tab-separated file)
    """
    
    
    ## Data wrangling
    
    # if gen list path is not empty
    if gene_list_path:
        
        # import gene list
        gene_list = pd.read_table(
            gene_list_path, 
            header = None, 
            names = ['gene'], 
            dtype = 'str')
        
        # intersection of genes in train and test matrixes
        train_test_genes = np.intersect1d(
            train_exp.columns.to_numpy(), # numpy array of genes in train matrix
            test_features # numpy array of genes in test matrix
        )

        # intersection of genes in list and train and test matrixes
        common_genes = np.intersect1d(
            gene_list['gene'].to_numpy(),# numpy array of genes in gene list
            train_test_genes
        )
        
        # subset train
        train_common = train_exp.loc[:, common_genes]
    
    else:
        
        # intersection of genes in list, train and test matrixes
        common_genes = np.intersect1d(
            train_exp.columns.to_numpy(), # numpy array of genes in train matrix
            test_features # numpy array of genes in test matrix
        )

        # subset train
        train_common = train_exp.loc[:, common_genes]
       
        
    ## Normalization
    
    # Scale datasets sample-wise
    
    # train
    x_train_sw = pd.DataFrame(
        scale(
            X = train_common, 
            axis = 1), 
        index = train_common.index, 
        columns = train_common.columns)
    
    # Mean - stardard deviation table of train matrix
    
    # mean - sd table
    mean_sd = pd.concat(
        [x_train_sw.mean(), 
         x_train_sw.std()], 
        axis = 1)
    
    # table columns names
    mean_sd.columns = ['mean', 'sd']
    
    
    # Scale datasets feature wise
    x_train_sw_fw = pd.DataFrame(
        (x_train_sw - mean_sd.loc[x_train_sw.columns,'mean'])/(mean_sd.loc[x_train_sw.columns,'sd']),
        index = train_common.index,
        columns = train_common.columns)

    
    ## Build encoder
    encoder = LabelEncoder().fit(train_labels)

    # transform labels
    y_train = encoder.transform(train_labels)
    
    
    ## Train the model
    
    # train classifier
    clf = SVC(kernel = 'linear').fit(x_train_sw_fw, y_train)
    
    return encoder, clf
