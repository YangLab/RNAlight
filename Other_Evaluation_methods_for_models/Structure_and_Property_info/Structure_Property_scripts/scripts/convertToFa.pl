my $fa=shift;
open(FA,$fa);
while (my $line=<FA>){
    chomp($line);
    my @data=split(/\t/,$line);
    print ">",@data[0],"\n";
    my @bb=split(//,@data[2]);
    for (my $id=0;$id<scalar(@bb);$id++){
	if (@bb[$id] eq "T"){
            @bb[$id]="U";
	}
    }
    my $bb=join("",@bb);
    print $bb,"\n";
}
