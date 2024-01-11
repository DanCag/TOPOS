TOPOS: Tissue-of-Origin Predictor of Onco-Samples
=================================================

A versatile support vector machine (SVM) to predict the tissue of origin (TOO) of primary, circulating tumor cell (CTC), metastasis, cell line, organoid and patient-derived xenograft (PDX) samples.

Get TOPOS ready
---------------

You need to have Conda installed as a prerequisite (the conda version I have installed is the 23.7.3).

1. Download TOPOS repository: `git clone https://github.com/DanCag/TOPOS` (you should see a new directory called `TOPOS`)
2. Download necessary files (`required_data.tar.gz`, `test_set.tar.gz`) from [zenodo](https://zenodo.org/records/10469602)
3. Move files into `TOPOS` directory
4. Go inside TOPOS directory with `cd TOPOS`
5. Extract the compressed archive `required_data.tar.gz` and the `test_set.tar.gz`:

```
tar xvf <compressed archive>
```
(you should see new directories with same name of compressed archives after doing this)

6. Create the conda environment: `conda env create -f ./TOPOS.yml`  

7. Activate the environment `conda activate TOPOS`

Data
----
* `required_data` contains the necessary files for running TOPOS 
* `test_set` contains the test set used in the study 
and a the ccle test set that is used as example in this tutorial. The test set file is heavy (7.9 GB) 
and it needs strong computational resources to be imported and processed. To run TOPOS on this file I have used a workstation with a RAM of 188 GB and 48 cores and the computation took ~ 20 minutes.  

Usage
-----

The model trains a SVM to distinguish between 15 different TOOs and make a prediction on an gene expression dataset.

### Example
> Train and test TOPOS with all genes in common between train and test set
```
./topos.py -i ./test_set/ccle_test_exp.tsv -p ./predictions
```

Runtime: ~ 2 minutes
<br>

> Train and test TOPOS with genes in common between train, test set and a list of genes of interest
```
./topos.py -i ./test_set/ccle_test_exp.tsv -g ./required_data/top-250-genes.txt -p ./predictions
```
Runtime on a test set : ~ 0.1 minute
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
