my $all=shift;
my $already=shift;
open(ALL,$all);
open(RD,$already);
my %dict;
while (my $line=<RD>){
    chomp($line);
    if ($line=~/\>/){
	$dict{$line}=1;
    }
}
my $judge=0;
while (my $line=<ALL>){
    chomp($line);
    if ($line=~/\>/){
	if (exists $dict{$line}){
	    $judge=1;
	}
	else{
	    $judge=0;
	    print $line,"\n";
	}
    }
    else{
	if ($judge==0){print $line,"\n";}
    }
}
