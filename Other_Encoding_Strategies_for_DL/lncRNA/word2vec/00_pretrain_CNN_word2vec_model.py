import os
import random
import numpy as np
import pandas as pd
import gensim
from gensim.models import Word2Vec


# padding sequence to 4000nt
def padding_truncate_seq(seq):
    length = len(seq)  
    if length > 4000: 
        seq = seq[:4000]   # trancate seq to 4000nt
    else:
        seq = seq + (4000 -length)*'N'  #padding N after seq to 4000nt
    return seq


SEED = 100
random.seed(SEED)
np.random.seed(SEED)

output_dir = "./Pretrained_CNN_word2vec_model"
if not (os.path.exists(output_dir)):
    os.makedirs(output_dir)

kmer_lens = [3,4,5]
lncRNA_Training_Set = pd.read_csv("/data/rnomics8/yuanguohua/RNA-Light_Original/lncRNA/03_Model_Construction/lncRNA_sublocation_TrainingSet.tsv", sep = '\t')
lncRNA_Training_Set["padding_truncate_seq"] = lncRNA_Training_Set.apply(lambda x: padding_truncate_seq(x["cdna"]),axis = 1)

for kmer_len in kmer_lens:
	lncRNA_Training_Set["kmer"] = lncRNA_Training_Set.apply(lambda x: [ x["padding_truncate_seq"][i:i+kmer_len] for i in range(0,len(x["padding_truncate_seq"])-kmer_len)],axis = 1)
	lncRNA_kmer_list = lncRNA_Training_Set["kmer"].tolist()
	word2vec_model = Word2Vec(lncRNA_kmer_list, size=100, window=5, min_count=1, workers=16, sg=0, negative=5)
	word2vec_model.save(os.path.join(output_dir,"00_pretrained_CNN_word2vec_"+str(kmer_len)+"_mer_len.model"))
