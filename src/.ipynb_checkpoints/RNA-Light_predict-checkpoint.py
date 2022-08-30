#!/usr/bin/env python
# coding=utf-8

# +
# Args
import argparse

# Get args
def get_args():
    parser = argparse.ArgumentParser(description = "Predict diverse RNA subcellular localization with RNA sequence (cDNA format: ACGT)", usage = "RNA-Light -q query.fasta [-m mRNA] [-p Prefix] [-O Output_Dir] [-h] [-v]", epilog="Happy Light!")
    parser.add_argument("-q","--query", dest = "query", type = str, metavar=("Query"),required = True, help = "query file to be predicted (fasta format)")
    parser.add_argument("-p","--prefix",dest = "prefix", type = str, default = "query", metavar=("Prefix"), help = "prefix of outputfiles (default: query)")
    parser.add_argument("-O","--outputdir",dest = "outputdir",type = str, default = "./RNA-Light_output", metavar=("Output_Dir"), help = "output directions of outputfiles (default:RNA-Light_output)")
    parser.add_argument("-m","--mRNA",dest = "mRNA", action = "store_true", help = "query sequence is mRNA")
    parser.add_argument("--RNA",dest = "RNA",action = "store_false", help = "query sequence is RNA format(ACGU)")
    parser.add_argument("-v","--version",action="version",version='RNA-Light v1.0',help = "version for RNA-Light")
    args = parser.parse_args()
    return args


args = get_args()
query_file = args.query
mRNA = args.mRNA
RNA = args.RNA
prefix = args.prefix
outputdir = args.outputdir
# -

# Python import
import os
import copy
import time
import itertools
import numpy as np
import pandas as pd
from sklearn.externals import joblib


# Count the frequency of k-mer in each RNA sequence
# k-mer was normalized by total k-mer count of each RNA sequence
def _count_kmer(Dataset,k): # k = 3,4,5
    
    # copy dataset
    dataset = copy.deepcopy(Dataset)
    # alphbet of nucleotide
    nucleotide = ['A','C','G','T']
    
    # generate k-mers
    #  k == 5:
    five = list(itertools.product(nucleotide,repeat=5))
    pentamer = []
    for n in five:
        pentamer.append("".join(n))
    
    #  k == 4:
    four = list(itertools.product(nucleotide,repeat=4))
    tetramer = []
    for n in four:
        tetramer.append("".join(n))

    # k == 3:
    three = list(itertools.product(nucleotide,repeat=3))
    threemer = []
    for n in three:
        threemer.append("".join(n))
    
    # input features can be combinations of diffrent k values
    if k == 34:
        table_kmer = dict.fromkeys(threemer,0)
        table_kmer.update(dict.fromkeys(tetramer,0))
    if k == 45:
        table_kmer = dict.fromkeys(tetramer,0)
        table_kmer.update(dict.fromkeys(pentamer,0))
    if k == 345:
        table_kmer = dict.fromkeys(threemer,0)
        table_kmer.update(dict.fromkeys(tetramer,0))
        table_kmer.update(dict.fromkeys(pentamer,0))

    # count k-mer for each sequence
    for mer in table_kmer.keys():
        table_kmer[mer] = dataset["cdna"].apply(lambda x : x.count(mer))
    
    # for k-mer raw count without normalization
    rawcount_kmer_df = pd.DataFrame(table_kmer)
    df1_rawcount = pd.concat([rawcount_kmer_df,dataset["seq_id"]],axis = 1)


    # for k-mer frequency with normalization
    freq_kmer_df = rawcount_kmer_df.apply(lambda x: x/x.sum(),axis=1)
    df1 = pd.concat([freq_kmer_df,dataset["seq_id"]],axis = 1)

    return df1,df1_rawcount

# +
# Output dir
if not (os.path.exists(outputdir)):
    os.mkdir(outputdir)

# tmp_dir
tmp_dir_name = prefix + ".tmp"
tmp_dir = os.path.join(outputdir,tmp_dir_name)
if not (os.path.exists(tmp_dir)):
    os.mkdir(tmp_dir)

# Convert fasta file to tab format
tab_tmp = prefix + ".txt"
if RNA:
    fa2tab = "seqkit seq --dna2rna " + query_file +" | seqkit fx2tab > " + os.path.join(tmp_dir,tab_tmp)
else:
    fa2tab = "seqkit fx2ta " + query_file + " > " + os.path.join(tmp_dir,tab_tmp)

os.system(fa2tab)

# +
# Load RNA-Light model
print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),"\tStart Loading RNA-Light......\n")


absolute_path = os.popen("dirname `which RNA-Light`").read().strip('\n')

if mRNA:
    RNA_Light = joblib.load(os.path.join(absolute_path,"src/RNA-Light_model/RNA-Light_mRNA_model.pkl"))
else:
    RNA_Light = joblib.load(os.path.join(absolute_path,"src/RNA-Light_model/RNA-Light_lncRNA_model.pkl"))


print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),"\tSuccessfully Loaded RNA-Light!\n")

# +
# Data Processing
print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),"\tStart Data Processing......\n")


query = pd.read_csv(os.path.join(tmp_dir,tab_tmp),sep='\t',index_col = False, names = ["seq_id","cdna"])
df_kmer_345,df_kmer_345_rawcount = _count_kmer(query,345)

kmer_file = prefix + "_df_kmer345_freq.tsv"
kmer_rowcount_file = prefix + "_df_kmer345_rawcount.tsv"
df_kmer_345.to_csv(os.path.join(outputdir,kmer_file),sep='\t')
df_kmer_345_rawcount.to_csv(os.path.join(outputdir,kmer_rowcount_file),sep='\t')


print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),"\tSuccessfully Finished Data Processing!\n")

# +
# Predict 
print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),"\tStart Predicting......\n")


del df_kmer_345['seq_id']
x_kmer = df_kmer_345.values

y_pred = RNA_Light.predict(x_kmer)
y_prob = RNA_Light.predict_proba(x_kmer)[:,1]

# Output
query["RNALight_pred_label"] =  y_pred
query["RNALight_pred_prob"] = y_prob
query["Light_score"] = 2*y_prob-1 

outputfile = prefix + "_RNA-Light_predict_df"
query.to_csv(os.path.join(outputdir,outputfile),sep = '\t',index=False)


print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),"\tSuccessfully Finished Predicting!\n")
