import os
import random
import numpy as np
import pandas as pd
import gensim
from gensim.models import Word2Vec


# padding sequence to 9000nt
def padding_truncate_seq(seq):
    length = len(seq)  
    if length > 9000: 
        seq = seq[:9000]   # trancate seq to 9000nt
    else:
        seq = seq + (9000 -length)*'N'  #padding N after seq to 9000nt
    return seq


SEED = 100
random.seed(SEED)
np.random.seed(SEED)

output_dir = "./Pretrained_CNN_word2vec_model"
if not (os.path.exists(output_dir)):
    os.makedirs(output_dir)

kmer_lens = [3,4]
mRNA_Training_Set = pd.read_csv("/data/rnomics8/yuanguohua/RNA-Light_Original/mRNA/03_Model_Construction/mRNA_sublocation_TrainingSet.tsv", sep = '\t')
mRNA_Training_Set["padding_truncate_seq"] = mRNA_Training_Set.apply(lambda x: padding_truncate_seq(x["cdna"]),axis = 1)

for kmer_len in kmer_lens:
	mRNA_Training_Set["kmer"] = mRNA_Training_Set.apply(lambda x: [ x["padding_truncate_seq"][i:i+kmer_len] for i in range(0,len(x["padding_truncate_seq"])-kmer_len)],axis = 1)
	mRNA_kmer_list = mRNA_Training_Set["kmer"].tolist()
	word2vec_model = Word2Vec(mRNA_kmer_list, size=100, window=5, min_count=1, workers=16, sg=0, negative=5)
	word2vec_model.save(os.path.join(output_dir,"00_pretrained_CNN_word2vec_"+str(kmer_len)+"_mer_len.model"))
    

kmer_lens = [5]
mRNA_Test_Set = pd.read_csv("/data/rnomics8/yuanguohua/RNA-Light_Original/mRNA/03_Model_Construction/mRNA_sublocation_TestSet.tsv", sep = '\t')
mRNA_Whole_Set = pd.concat([mRNA_Training_Set,mRNA_Test_Set])

mRNA_Whole_Set["padding_truncate_seq"] = mRNA_Whole_Set.apply(lambda x: padding_truncate_seq(x["cdna"]),axis = 1)

for kmer_len in kmer_lens:
	mRNA_Whole_Set["kmer"] = mRNA_Whole_Set.apply(lambda x: [ x["padding_truncate_seq"][i:i+kmer_len] for i in range(0,len(x["padding_truncate_seq"])-kmer_len)],axis = 1)
	mRNA_kmer_list = mRNA_Whole_Set["kmer"].tolist()
	word2vec_model = Word2Vec(mRNA_kmer_list, size=100, window=5, min_count=1, workers=16, sg=0, negative=5)
	word2vec_model.save(os.path.join(output_dir,"00_pretrained_CNN_word2vec_"+str(kmer_len)+"_mer_len.model"))
