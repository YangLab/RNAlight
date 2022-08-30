# RNA-Light

RNA-Light: a machine learning model to identify determinant features for RNA subcellular localization.


## 1. Installation
### 1.1 Download RNA-Light git repo
    git clone git@github.com:YangLabPublic/RNA-Light_Private.git
    
### 1.2 Set PATH enviromental virable of RNA-Light
    RNA-Light="/Your_Path/RNA-Light"
    export PATH=${RNA-Light}:$PATH
    
    echo "export ${RNA-Light}:\$PATH" >> ~/.bashrc

### 1.3 RNA-Light Conda setup
* Create a new conda environment and activate

        conda create -n RNA-Light python=3.6.10
        conda activate RNA-Light

* Install dependencies

        conda install scikit-learn=0.20.3 numpy=1.17.0 pandas=0.21.0 lightgbm=3.1.1
        conda install seqkit=0.14.0

## 2. Usage
    usage: RNA-Light -q query.fasta [-m mRNA] [-p Prefix] [-O Output_Dir] [-h] [-v]

    Predict diverse RNA subcellular localization with RNA sequence (cDNA format:
    ACGT)

    optional arguments:
      -h, --help            show this help message and exit
      -q Query, --query Query
                            query file to be predicted (fasta format)
      -p Prefix, --prefix Prefix
                            prefix of outputfiles (default: query)
      -O Output_Dir, --outputdir Output_Dir
                            output directions of outputfiles (default:RNA-
                            Light_output)
      -m, --mRNA            query sequence is mRNA
      --RNA                 query sequence is RNA format(ACGU)
      -v, --version         version for RNA-Light
      
## 3. Example
* Your query file need to be a fasta format which recorded the cDNA sequence of RNA (U was replaced as T, ACGT).
        
        RNA-Light -q $RNA-Light/example/query.fasta -p Test -O RNA-Light_Test
        
* Please add the argument -m or --mRNA if your query sequences are mRNAs.

        RNA-Light -q Your_query_mRNA.fasta -m -p mRNA -O RNA-Light_mRNA
        
* Please add the argument --RNA if your query file is a fasta format of RNA sequence (ACGU).  

        RNA-Light -q Your_query_RNA_format.fasta --RNA -p RNA_format -O RNA-Light_RNA_foramt
        
   
## 4. Output

    RNA-Light_Test/
    ├── Test_df_kmer345_freq.tsv        # kmer frequency file (k = 3,4,5)
    ├── Test_df_kmer345_rawcount.tsv    # kmer rawcount file (k = 3,4,5)
    ├── Test_RNA-Light_predict_df       # Predict result 
    └── Test.tmp
        └── Test.txt                    # tabular format of querey sequences
        
- Test_RNA-Light_predict_df

    | **Field**      | **Discription**      | 
    | ---------- | :-----------:  |
    | seq_id     | ID of sequence      |
    | RNALight_pred_label | Predict label of sequence (0:Cytoplasm; 1: Nucleus) |
    | RNALight_pred_prob| Probility of necleus loclaization from RNA-Light |
    | Light_score | Scaled RNALight_pred_prob (range from -1 to 1) |
    
    
## 5. Repeat this work
If you want to repeat this from scratch, please see [Repeat_Work](./Repeat_Work.md) to find requirements you need. If only use RNA-Light to predict RNA subcellular localization, please ignore this part.

    
## 6. Citation



## 7. License
Copyright ©2021 Shanghai Institute of Nutrition and Health. All Rights Reserved.

Licensed GPLv3 for open source use or contact YangLab (yanglab@picb.ac.cn) for commercial use.

Permission to use, copy, modify, and distribute this software and its documentation for educational, research, and not-for-profit purposes, without fee and without a signed licensing agreement, is hereby granted, provided that the above copyright notice in all copies, modifications, and distributions.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
