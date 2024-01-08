#! /usr/bin/env python3

# modules
import argparse
import sys
import os


# ------- #
# Parsers #
# ------- #

# main parser
parser = argparse.ArgumentParser(
    description = ('TOPOS: Tissue-of-Origin Predictor of Onco-Samples.\n' +  
                   'A robust SVC of the tissue of origin of' + 
                   'primary, circulating tumor cell, metastasis, ' +
                   'cell line, organoid, and ' +
                   'patient-derived xenograft samples.')
)



# add arguments

# test matrix (TPM)
parser.add_argument(
    '-i', '--input_test_matrix',
    required = True
)

# gene list (optional) 
parser.add_argument(
    '-g', '--gene_list_path')


# directory where predictions are stored
parser.add_argument(
    '-p', '--prediction_directory',
    required = True
)


# return some data from the options specified
args = parser.parse_args()
# print(args)



# --------- #
# Run TOPOS #
# --------- #

# add path-with-module to python path at runtime
sys.path.append('./functions')


print('You are running TOPOS in\n')
print(' ++++++++++++++++++++++\n', 
      '+ TOO detection mode +\n', 
      '++++++++++++++++++++++')
print('\n')


## import functions
from training import train
from normalization import normalize
from prediction import predict

## import packages
import pandas as pd
import numpy as np


## import data

print('... Importing required data ...\n\n')

# TOO prediction train matrix
train_too = pd.read_pickle('./required_data/train_exp.pkl')

# TOO prediction train labels
train_labels_too = pd.read_pickle('./required_data/train_label.pkl')

# test matrix features
test_features = pd.read_table(
    args.input_test_matrix, 
    index_col = 0).columns.to_numpy()


print('... Training starts ...\n')

# encoder and classifier for tumor detection
encdr, clf = train(
    train_exp = train_too,
    train_labels = train_labels_too, 
    test_features = test_features,
    gene_list_path = args.gene_list_path
)

print('... Training ends ...\n\n')

print('... Normalization of test dataset starts ...\n')

# normalize test dataset on too train matrix
test_sw_fw = normalize(
    train_exp = train_too, 
    test_exp_path = args.input_test_matrix, 
    gene_list_path = args.gene_list_path
)

print('... Normalization of test dataset ends ...\n\n')

print('... TOO prediction starts ...\n')

# prediction file
prediction_file = os.path.join(
    args.prediction_directory, 
    ('P_test_model-trained-with-') + str(test_sw_fw.shape[1]) + '-genes.tsv'
)

# predict TOO
predict(
    test_nrmlz = test_sw_fw,
    clf = clf,
    encdr = encdr, 
    prediction_file = prediction_file
)

print('... TOO prediction ends ...\n\n')
