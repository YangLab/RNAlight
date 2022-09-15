my $bracket=shift;
open(BR,$bracket);
my $cn=0;
my $name="";
my %dict;
while (my $line=<BR>){
    chomp($line);
    if ($cn%3==0){
       $name=$line;
    }
    
    if ($cn%3==2){
	my @data=split(/\s+/,$line);
	my @dd=split(/\(/,@data[1]);
	my @dd1=split(/\)/,@dd[1]);
	$dict{$name}=@dd1[0];
    }
    $cn=$cn+1;
}
close(BR);
open(BR,$bracket);
$cn=0;
while (my $line=<BR>){
    chomp($line);
    if ($cn%3==0){
	my $energy=$dict{$line};
	my @dd=split(/\>/,$line);
	my $out=">"."ENERGY = ".$energy."  ".@dd[1];
	print $out,"\n";
    }
    if ($cn%3==1){print $line,"\n";}
    if ($cn%3==2){
	my @dd=split(/\s+/,$line);
	print @dd[0],"\n";
     }
    $cn=$cn+1;
}
