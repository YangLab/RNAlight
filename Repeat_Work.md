# Requirments for repeat this work from scratch

## 1. Basic dependencies
* python

      python==3.6.10
      scikit-learn==0.20.3
      numpy==1.17.0 
      pandas==0.21.0 
      lightgbm==3.1.1
      shap==0.34.0
      scipy>=1.5.3
      statsmodels>=0.10.2
      matplotlib>=3.2.2
      jupyterlab>=3.0.3
      gensim==3.7.3
* R

      r-base>=3.6.3
      ggplot2
      reshape2
      
* others

      seqkit==0.14.0
      meme==5.3.0
      clustalo==1.2.4
      CLEAR/CIRCexplorer3==1.0
      
## 2. Deep learning model
* GPU: NVIDIA Tesla V100 PCIe 32GB, Driver Version: 440.31, CUDA Version: 10.2
* Tensorflow2: we recommend to create a new environment with conda to install tensorflow2 and perform deep learning model training.

      tensorflow-gpu==2.0.0
      tensorflow-determinism==0.3.0
      cudnn==7.6.5=cuda10.0_0
      cudatoolkit==10.0.130
      numpy==1.17.0
      pandas==0.20.3
      h5py==3.1.0
      scikit-learn==0.20.3
      matplotlib>=3.3.3

Trained deep learning models were not provided because of the file size limitation. Please contact us to get their specific parameters if you need.

## 3. Gene annotation files
Gene annotation files were not provided because of the file size limitation. Please download them additionally into the corresponding directions according to the codes expected to be run.

* gencode.v30.lncRNA_transcripts.fa

        wget http://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_human/release_30/gencode.v30.lncRNA_transcripts.fa.gz
        
* gencode.v30.pc_transcripts.fa

        wget http://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_human/release_30/gencode.v30.pc_transcripts.fa.gz
        
* gencode.v30.annotation.gtf

        wget http://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_human/release_30/gencode.v30.annotation.gtf.gz
        
* gencode.v30.transcripts.fa

        wget http://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_human/release_30/gencode.v30.transcripts.fa.gz

