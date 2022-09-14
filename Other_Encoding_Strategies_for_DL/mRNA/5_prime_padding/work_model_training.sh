 nohup python CNN_9000nt.py --training /data/rnomics8/yuanguohua/RNA-Light_Original/mRNA/03_Model_Construction/mRNA_sublocation_TrainingSet.tsv --test /data/rnomics8/yuanguohua/RNA-Light_Original/mRNA/03_Model_Construction/mRNA_sublocation_TestSet.tsv -o ./01_DL_Model_Output/CNN_9000nt_Model_Output 1> CNN_9000nt.log 2> CNN_9000nt.error & 
 
 nohup python CNN_RNN_9000nt.py --training /data/rnomics8/yuanguohua/RNA-Light_Original/mRNA/03_Model_Construction/mRNA_sublocation_TrainingSet.tsv --test /data/rnomics8/yuanguohua/RNA-Light_Original/mRNA/03_Model_Construction/mRNA_sublocation_TestSet.tsv -o ./01_DL_Model_Output/CNN_RNN_9000nt_Model_Output 1> CNN_RNN_9000nt.log 2> CNN_RNN_9000nt.error & 

