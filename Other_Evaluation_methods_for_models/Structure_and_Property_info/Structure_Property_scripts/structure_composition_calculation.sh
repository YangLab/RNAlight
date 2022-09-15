#conda install RNAfold
RNAfold --noPS -i lncRNA_sublocation_TestSet.fa > lncRNA_Test_bracket.txt

perl scripts/modify_bracket.pl lncRNA_Test_bracket.txt > lncRNA_Test_bracket_modified.txt

###set the Graph.pm directory to PERLLIB###
# If you need to change the PERLLIB, please run the following command.
# export PERLLIB=$PERLLIB:/picb/rnomics4/wangying/tools/Chart-Graph-1
python scripts/bpRNA_wrapper_modified_v1.py --data_bracket lncRNA_Test_bracket_modified.txt --text_out lncRNA_Test_annotation.txt --pickle_out lncRNA_Test_annotation.pkl

###calculation of  per structure ratio### 
perl scripts/cal_ratio.pl lncRNA_Test_annotation.txt > lncRNA_Test_ratio.txt
sed -i '2d' lncRNA_Test_ratio.txt


perl scripts/print_structure.pl lncRNA_Test_annotation.txt > lncRNA_Test_structure.txt 

perl scripts/sort_output.pl lncRNA_sublocation_TestSet.fa lncRNA_Test_structure.txt lncRNA_Test_ratio.txt > lncRNA_sublocation_TestSet_structure.txt 

perl scripts/cal_GC_content.pl lncRNA_Test_bracket_modified.txt > lncRNA_Test_biochemical.txt

perl scripts/sort_output_v1.pl lncRNA_sublocation_TestSet.fa lncRNA_Test_biochemical.txt > lncRNA_sublocation_TestSet_biochemical.txt
