my $annotation=shift;
open(ANNO,$annotation);
my $name="";
while (my $line=<ANNO>){
    chomp($line);
    if ($line=~/\>/){
	$cn=0;
	my @data=split(/\s+/,$line);
	$name=@data[3];
    }
    $cn=$cn+1;
    if ($cn==7){
	print $name,"\t",$line,"\n";
    }

}
