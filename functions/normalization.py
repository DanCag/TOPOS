# Modules
import pandas as pd
import numpy as np
from sklearn.preprocessing import scale


# normalize test dataset function
def normalize(
    train_exp,
    test_exp_path,
    gene_list_path = ''):
    
    """Normalize test dataset
    
    Keyword arguments
    train_exp_path -- train expression matrix
    test_exp_path -- path of test expression matrix samples x entrez gene id (tab-separated file)
    gene_list_path -- path of gene list file (tab-separated file)
    """
    
    
    ## Import data
        
    # test #
    
    # test matrix
    test = pd.read_table(
        test_exp_path,
        index_col = 0)
    
    
    ## Data wrangling
    
    # if path is not empty
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
            test.columns.to_numpy() # numpy array of genes in test matrix
        )

        # intersection of genes in gene_list and train and test matrixes
        common_genes = np.intersect1d(
            gene_list['gene'].to_numpy(),# numpy array of genes in gene list
            train_test_genes
        )
        
        # subset train
        train_common = train_exp.loc[:, common_genes]
        
        # subset test
        test_common = test.loc[:, common_genes]
    
    else:
        
        # intersection of genes in gene_list, train and test matrixes
        common_genes = np.intersect1d(
            train_exp.columns.to_numpy(), # numpy array of genes in train matrix
            test.columns.to_numpy() # numpy array of genes in test matrix
        )

        # subset train
        train_common = train_exp.loc[:, common_genes]
        
        # subset test
        test_common = test.loc[:, common_genes]
        
        
    ## Normalization
    
    # Scale datasets sample-wise
    
    # train
    x_train_sw = pd.DataFrame(
        scale(
            X = train_common, 
            axis = 1), 
        index = train_common.index, 
        columns = train_common.columns)
    
    # test
    x_test_sw = pd.DataFrame(
        scale(
            X = test_common, 
            axis = 1), 
        index = test_common.index, 
        columns = test_common.columns)
    
    # Mean - stardard deviation table of train matrix
    
    # mean - sd table
    mean_sd = pd.concat(
        [x_train_sw.mean(), 
         x_train_sw.std()], 
        axis = 1)
    
    # table columns names
    mean_sd.columns = ['mean', 'sd']
    
    
    # Scale test dataset feature wise
    x_test_sw_fw = pd.DataFrame(
        (x_test_sw - mean_sd.loc[x_test_sw.columns,'mean'])/(mean_sd.loc[x_test_sw.columns,'sd']),
        index = test_common.index, 
        columns = test_common.columns)
    
    return x_test_sw_fw
