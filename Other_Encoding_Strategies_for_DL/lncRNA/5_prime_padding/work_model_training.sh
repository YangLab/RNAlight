 nohup python CNN_4000nt.py --training /data/rnomics8/yuanguohua/RNA-Light_Original/lncRNA/03_Model_Construction/lncRNA_sublocation_TrainingSet.tsv --test /data/rnomics8/yuanguohua/RNA-Light_Original/lncRNA/03_Model_Construction/lncRNA_sublocation_TestSet.tsv -o ./01_DL_Model_Output/CNN_4000nt_Model_Output 1> CNN_4000nt.log 2> CNN_4000nt.error & 
 
 nohup python CNN_RNN_4000nt.py --training /data/rnomics8/yuanguohua/RNA-Light_Original/lncRNA/03_Model_Construction/lncRNA_sublocation_TrainingSet.tsv --test /data/rnomics8/yuanguohua/RNA-Light_Original/lncRNA/03_Model_Construction/lncRNA_sublocation_TestSet.tsv -o ./01_DL_Model_Output/CNN_RNN_4000nt_Model_Output 1> CNN_4000nt_RNN.log 2> CNN_RNN_4000nt.error & 

