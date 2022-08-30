cat ../../lncRNA/06_SHAP_kmer/03_Nuc_Cyto_kmer_assembly_Output/cyto_favour_motif_consensus.txt ../../mRNA/06_SHAP_kmer/03_Nuc_Cyto_kmer_assembly_Output/cyto_favour_motif_consensus.txt | awk -v OFS='\t' '{print $1"_"$2,$2}' | seqkit tab2fx -w 0 > lncRNA_mRNA_cyto_favour_motif_consensus.fa

cat ../../lncRNA/06_SHAP_kmer/03_Nuc_Cyto_kmer_assembly_Output/nuc_favour_motif_consensus.txt ../../mRNA/06_SHAP_kmer/03_Nuc_Cyto_kmer_assembly_Output/nuc_favour_motif_consensus.txt | awk -v OFS='\t' '{print $1"_"$2,$2}' | seqkit tab2fx -w 0 > lncRNA_mRNA_nuc_favour_motif_consensus.fa


seqkit locate -f  lncRNA_mRNA_nuc_favour_motif_consensus.fa -P -i /data/rnomics8/yuanguohua/RNA-Light_Original/mRNA/01_Resources/References/gencode.v30.intron.fa > lncRNA_mRNA_nuc_favour_motif_consensus_intron.txt &

seqkit locate -f  lncRNA_mRNA_nuc_favour_motif_consensus.fa -P -i /data/rnomics8/yuanguohua/RNA-Light_Original/mRNA/01_Resources/References/gencode.v30.exon.fa  > lncRNA_mRNA_nuc_favour_motif_consensus_exon.txt &


seqkit locate -f  lncRNA_mRNA_cyto_favour_motif_consensus.fa -P -i /data/rnomics8/yuanguohua/RNA-Light_Original/mRNA/01_Resources/References/gencode.v30.intron.fa > lncRNA_mRNA_cyto_favour_motif_consensus_intron.txt &


seqkit locate -f  lncRNA_mRNA_cyto_favour_motif_consensus.fa -P -i /data/rnomics8/yuanguohua/RNA-Light_Original/mRNA/01_Resources/References/gencode.v30.exon.fa > lncRNA_mRNA_cyto_favour_motif_consensus_exon.txt &
