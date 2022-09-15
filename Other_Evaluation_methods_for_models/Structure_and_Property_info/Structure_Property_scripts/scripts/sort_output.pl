my $fa=shift;
my $struct=shift;
my $ratio=shift;
open(FA,$fa);
open(ST,$struct);
open(RA,$ratio);
my %dict_s;
my %dict_r;
print "id\tstructure\t";
while (my $line=<ST>){
    chomp($line);
    my @data=split(/\t/,$line);
    $dict_s{@data[0]}=@data[1];
}
my $cn=0;
while (my $line=<RA>){
    chomp($line);
    $cn=$cn+1;
    my @data=split(/\t/,$line);
    if ($cn==1){
	print join("\t",@data[1..14]),"\n";
    }
    else{
	$dict_r{@data[0]}=join("\t",@data[1..14]);
    }
}
while (my $line=<FA>){
    chomp($line);
    if ($line=~/\>/){
	my $name=substr($line,1);
	print $name,"\t",$dict_s{$name},"\t",$dict_r{$name},"\n";
    }
}
