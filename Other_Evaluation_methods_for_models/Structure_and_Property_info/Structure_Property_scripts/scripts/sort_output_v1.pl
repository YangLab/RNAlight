my $fa=shift;
my $ratio=shift;
open(FA,$fa);
open(RA,$ratio);
my %dict_r;
my $cn=0;
while (my $line=<RA>){
    chomp($line);
    $cn=$cn+1;
    my @data=split(/\t/,$line);
    if ($cn==1){
	print $line,"\n";
    }
    else{
	$dict_r{@data[0]}=$line;
    }
}
while (my $line=<FA>){
    chomp($line);
    if ($line=~/\>/){
	my $name=substr($line,1);
	print $dict_r{$name},"\n";
    }
}
