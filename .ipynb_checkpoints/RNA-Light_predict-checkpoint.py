# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.9.1
#   kernelspec:
#     display_name: pytorch
#     language: python
#     name: pytorch
# ---

# Args
import argparse

# Get args
def get_args():
    parser = argparse.ArgumentParser(description = "Predict diverse RNA subcellular localization with RNA sequence (cDNA format: ACGT)", usage = "RNA-Light -q query.fasta [-m mRNA] [-p Prefix] [-O Output_Dir] [-h] [-v]", epilog="Happy Light!")
    parser.add_argument("-q","--query", dest = "query", type = str, metavar=("Query"),required = True, help = "query file to be predicted (fasta format)")
    parser.add_argument("-p","--prefix",dest = "prefix", type = str, default = "query", metavar=("Prefix"), help = "prefix of outputfiles (default: query)")
    parser.add_argument("-O","--outputdir",dest = "outputdir",type = str, default = "RNA-Light_output", metavar=("Output_Dir"), help = "output directions of outputfiles (default:RNA-Light_output)")
    parser.add_argument("-m","--mRNA",dest = "mRNA", action = "store_true", help = "query sequence is mRNA")
    parser.add_argument("--RNA",dest = "RNA",action = "store_false", help = "query sequence is RNA format(ACGU)")
    parser.add_argument("-v","--version",action="version",version='RNA-Light v1.0',help = "version for RNA-Light")
    args = parser.parse_args()
    return args


args = get_args()
query_file = args.query
mRNA = args.mRNA
prefix = args.prefix
outputdir = args.outputdir


args = get_args()
query_file = args.query
mRNA = args.mRNA
prefix = args.prefix
outputdir = args.outputdir
from sklearn.externals import joblib

if args.mRNA:
    print("mRNA")
else:
    print("lncRNA")
