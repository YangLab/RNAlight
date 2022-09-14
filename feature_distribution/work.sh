cp ../../lncRNA/06_SHAP_kmer/02_SHAP_kmer_Zscore_Output/Nuc_related_kmer_20_lncRNA.txt ./ 
cp ../../lncRNA/06_SHAP_kmer/02_SHAP_kmer_Zscore_Output/Cyto_related_kmer_43_lncRNA.txt ./

awk '{print $1"\t"$1}' Nuc_related_kmer_20_lncRNA.txt  | seqkit tab2fx > Nuc_related_kmer_20_lncRNA.fa
awk '{print $1"\t"$1}' Cyto_related_kmer_43_lncRNA.txt | seqkit tab2fx > Cyto_related_kmer_43_lncRNA.fa

seqkit locate -f Nuc_related_kmer_20_lncRNA.fa -P -i NEAT1.fa | sed 1d | cut -f2 | sort | uniq -c | awk '{print $2"\t"$1}' > NEAT1_nuc_lnc_20_kmer_enrichment.txt
