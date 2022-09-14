#Halo_p65
# protein coding / mRNA
awk '$3>=0.5 && $4<0.05'  TableS1.txt | grep protein_coding > 01_Halo_seq_mRNA_p65_enriched.txt
awk '$3<=-0.5 && $4<0.05' TableS1.txt | grep protein_coding > 01_Halo_seq_mRNA_p65_depleted.txt
# lncRNA
awk '$3>=0.5 && $4<0.05'  TableS1.txt | grep lncRNA > 01_Halo_seq_lncRNA_p65_enriched.txt
awk '$3<=-0.5 && $4<0.05' TableS1.txt | grep lncRNA > 01_Halo_seq_lncRNA_p65_depleted.txt

# Halo_H2B
# protein coding / mRNA
awk '$3>=0.5 && $4<0.05'  TableS2.txt | grep protein_coding > 01_Halo_seq_mRNA_H2B_enriched.txt
awk '$3<=-0.5 && $4<0.05' TableS2.txt | grep protein_coding > 01_Halo_seq_mRNA_H2B_depleted.txt
# lncRNA
awk '$3>=0.5 && $4<0.05'  TableS2.txt | grep lncRNA > 01_Halo_seq_lncRNA_H2B_enriched.txt
awk '$3<=-0.5 && $4<0.05' TableS2.txt | grep lncRNA > 01_Halo_seq_lncRNA_H2B_depleted.txt

# Cytoplasmic RNAs
# combine H2B_deleted and p65_enriched mRNAs as cytoplasmic mRNAs
cat 01_Halo_seq_mRNA_H2B_depleted.txt  01_Halo_seq_mRNA_p65_enriched.txt | sort -k1,1 | awk '!a[$1]++' |  awk '{print $0"\t0"}' >  02_Halo_seq_mRNA_cyto.txt
# combine H2B_deleted and p65_enriched lncRNAs as cytoplasmic lncRNAs
cat 01_Halo_seq_lncRNA_H2B_depleted.txt  01_Halo_seq_lncRNA_p65_enriched.txt | sort -k1,1 | awk '!a[$1]++' |  awk '{print $0"\t0"}' >  02_Halo_seq_lncRNA_cyto.txt

# Nuclear RNAs
# combine H2B_enriched and p65_deleted mRNAs as nuclear mRNAs
cat 01_Halo_seq_mRNA_H2B_enriched.txt  01_Halo_seq_mRNA_p65_depleted.txt | sort -k1,1 | awk '!a[$1]++' | awk '{print $0"\t1"}'  >  02_Halo_seq_mRNA_nuc.txt
# combine H2B_enriched and p65_deleted lncRNAs as nuclear lncRNAs
cat 01_Halo_seq_lncRNA_H2B_enriched.txt  01_Halo_seq_lncRNA_p65_depleted.txt | sort -k1,1 | awk '!a[$1]++' | awk '{print $0"\t1"}'  >  02_Halo_seq_lncRNA_nuc.txt

# Combine cytoplasmic and nuclear RNAs
cat 02_Halo_seq_mRNA_cyto.txt 02_Halo_seq_mRNA_nuc.txt > 03_Halo_seq_mRNA_cyto_nuc.txt
cat 02_Halo_seq_lncRNA_cyto.txt  02_Halo_seq_lncRNA_nuc.txt > 03_Halo_seq_lncRNA_cyto_nuc.txt
# RNA with inconsistent localizations
cat 02_Halo_seq_mRNA_cyto.txt 02_Halo_seq_mRNA_nuc.txt | cut -f1 | sort | uniq -d > 03_Halo_seq_mRNA_inconsistent_loc.cid
cat 02_Halo_seq_lncRNA_cyto.txt  02_Halo_seq_lncRNA_nuc.txt | cut -f1 | sort | uniq -d > 03_Halo_seq_lncRNA_inconsistent_loc.cid
# Remove inconsistent RNAs
cat 03_Halo_seq_mRNA_inconsistent_loc.cid| grep -v -f - 03_Halo_seq_mRNA_cyto_nuc.txt > 04_Halo_seq_mRNA_cyto_nuc_rm_inconsistent.txt
cat 03_Halo_seq_lncRNA_inconsistent_loc.cid| grep -v -f - 03_Halo_seq_lncRNA_cyto_nuc.txt > 04_Halo_seq_lncRNA_cyto_nuc_rm_inconsistent.txt

# get RNA sequences
touch 05_Halo_seq_mRNA_independent.tmp
cut -f2,6 04_Halo_seq_mRNA_cyto_nuc_rm_inconsistent.txt | while read id 
do
	gene_name=`echo "$id" | cut -f1`
	loc_label=`echo "$id" | cut -f2`
	awk -v gene="$gene_name" '$2==gene' /data/rnomics8/yuanguohua/RNAlight_Private/mRNA/01_Resources/References/gencode.v30.pc_mRNA_transcripts_major_compact_trans_id.txt | awk -v loc="$loc_label" '{print $0"\t"loc}' >>  05_Halo_seq_mRNA_independent.tmp
done
awk 'BEGIN{print "ensembl_transcript_id\tname\tcdna\ttag"} {print $0}'  05_Halo_seq_mRNA_independent.tmp >  05_Halo_seq_mRNA_independent.txt 

touch 05_Halo_seq_lncRNA_independent.tmp
cut -f2,6 04_Halo_seq_lncRNA_cyto_nuc_rm_inconsistent.txt | while read id 
do
	gene_name=`echo "$id" | cut -f1`
	loc_label=`echo "$id" | cut -f2`
	awk -v gene="$gene_name" '$2==gene' /data/rnomics8/yuanguohua/RNAlight_Private/lncRNA/01_Resources/References/gencode.v30.lncRNA_transcripts_major_compact_trans_id.txt | awk -v loc="$loc_label" '{print $0"\t"loc}' >>  05_Halo_seq_lncRNA_independent.tmp
done
awk 'BEGIN{print "ensembl_transcript_id\tname\tcdna\ttag"} {print $0}'  05_Halo_seq_lncRNA_independent.tmp >  05_Halo_seq_lncRNA_independent.txt 


# convert to fasta
sed 1d 05_Halo_seq_mRNA_independent.txt  | awk -v OFS='\t' '{print $1"_"$4,$3}' | seqkit tab2fx -w 0 > 06_Halo_seq_mRNA_independent.fa
sed 1d 05_Halo_seq_lncRNA_independent.txt  | awk -v OFS='\t' '{print $1"_"$4,$3}' | seqkit tab2fx -w 0 > 06_Halo_seq_lncRNA_independent.fa
