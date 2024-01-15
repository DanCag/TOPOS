TOPOS: Tissue-of-Origin Predictor of Onco-Samples
=================================================

A versatile support vector machine (SVM) to predict the tissue of origin (TOO) of primary, circulating tumor cell (CTC), metastasis, cell line, organoid and patient-derived xenograft (PDX) samples.

Get TOPOS ready
---------------

You need to have Conda installed as a prerequisite (we have used version 23.7.3).

1. Download TOPOS repository: `git clone https://github.com/DanCag/TOPOS.git` (you should see a new directory called `TOPOS`)
2. Download necessary files (`required_data.tar.gz`, `test_set_instance.tar.gz`) from [zenodo](https://zenodo.org/records/10498070)
3. Move files into `TOPOS` directory
4. Go to `TOPOS` directory
5. Extract the compressed archives `required_data.tar.gz` and the `test_set_instance.tar.gz`. You should see new directories called `required_data` and `test_set_instance`.

6. Create the conda environment: `conda env create -f ./TOPOS.yml`  

7. Activate the environment `conda activate TOPOS`

Data
----
* `required_data` contains the train matrix and the train labels files necessary to run TOPOS 
* `test_set_instance` contains an instance of test set and a file with the list of top 275 genes identified in the study

Usage
-----

The model trains a SVM to distinguish between 15 different TOOs and make a prediction on an gene expression dataset.

### Example
> Train and test TOPOS with all genes in common between train and test set
```
./topos.py -i ./test_set_instance/ccle_test_exp.tsv -p ./predictions
```

Runtime ~ 2 minutes
<br>

> Train and test TOPOS with genes in common between train, test set and a list of genes of interest
```
./topos.py -i ./test_set_instance/ccle_test_exp.tsv -g ./test_set_instance/top-250-genes.txt -p ./predictions
```
Runtime ~ 0.1 minute
<br>

**Required parameters**

- `-i`, `--input_test_matrix`<br>
User's test expression matrix pathway. The file must be tab-separated with rows as samples and columns as genes (named with Entrez gene ids). Columns and samples must be named, so there will be a column and a row index.<br> Below you see how the expression file must look like:


| | | | |  |
| :----:   | :----: | :----: | :----: | :----: |
|          | gene_1 | gene_2 | ...    | gene_n | 
| sample_1 |
| sample_2 |
| ...     | 
| sample_n |



- `-p`, `--prediction_directory`<br>
Prediction directory where to store prediction file


**Optional parameter**

- `-g`, `--gene_list`<br>
path of gene list file. The file contains genes (entrez gene ids) to use for train and test.<br>
If not provided, TOPOS will use the overlap between train and test genes.



### Runtime tests

Runtimes are estimated on the following machine:

| | |
| :----: | :----: |
| **OS**     | Ubuntu 20.04.4 LTS |
| **Memory** | 5.5 Gib     |
| **Processor** | Intel® Core™ i5-8500T CPU @ 2.10GHz × 6 |
