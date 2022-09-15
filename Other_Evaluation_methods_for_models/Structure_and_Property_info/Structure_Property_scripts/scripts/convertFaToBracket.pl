my $fa=shift;
my $out=shift;
open(FA,$fa);
open(OUT,">>$out");
while (my $line=<FA>){
    chomp($line);
    if ($line=~/\>/){
        open(FA1,">tmp.fa");
	print FA1 $line,"\n";
    }
    else{
	print FA1 $line,"\n";
	close(FA1);
	system("/picb/rnomics4/wangying/tools/RNAstructure/exe/MaxExpect tmp.fa tmp.ct --sequence");
	system("/picb/rnomics4/wangying/tools/RNAstructure/exe/ct2dot tmp.ct 1 tmp_bracket.txt");
  	open(ST,"tmp_bracket.txt");
	while (my $ll=<ST>){
	    print OUT $ll;
	}
	close(ST);

	
    }
}
