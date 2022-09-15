my $annotation=shift;
open(ANNO,$annotation);
my $name="";
my %dict_len;my %dict_ratio;my $cn=0;
print "id","\t","len_S","\t","len_H","\t","len_M","\t","len_I","\t","len_B","\t","len_E","\t","len_X","\t","num_S","\t","num_H","\t","num_M","\t","num_I","\t","num_B","\t","num_E","\t","num_X","\n";
while (my $line=<ANNO>){
    chomp($line);
    if ($line=~/\>/){
	my $total=0;
	foreach my $id (keys %dict_ratio){
	    $total=$total+$dict_ratio{$id};
	}
	foreach my $id (keys %dict_ratio){
	    $dict_ratio{$id}=$dict_ratio{$id}/$total;
	}
	print $dict_ratio{"S"},"\t",$dict_ratio{"H"},"\t",$dict_ratio{"M"},"\t",$dict_ratio{"I"},"\t",$dict_ratio{"B"},"\t",$dict_ratio{"E"},"\t",$dict_ratio{"X"},"\n";
        %dict_len=("S"=>0,"H"=>0,"M"=>0,"I"=>0,"B"=>0,"E"=>0,"X"=>0);
	%dict_ratio=("S"=>0,"H"=>0,"M"=>0,"I"=>0,"B"=>0,"E"=>0,"X"=>0);
	$cn=0;
	my @data=split(/\s+/,$line);
	$name=@data[3];
    }
    $cn=$cn+1;
    if ($cn==7){
	my @data=split(//,$line);
	my $len=0;
	foreach my $id (@data){
	    $len=$len+1;
	    $dict_len{$id}=$dict_len{$id}+1;
	}
	foreach my $id (keys %dict_len){
	    $dict_len{$id}=$dict_len{$id}/$len;
	}
	print $name,"\t",$dict_len{"S"},"\t",$dict_len{"H"},"\t",$dict_len{"M"},"\t",$dict_len{"I"},"\t",$dict_len{"B"},"\t",$dict_len{"E"},"\t",$dict_len{"X"},"\t";
    }
    if ($cn>=9){
	if ($line=~/segment/){}
	else{
	    my @data=split(/\s+/,$line);
	    my @dd=split(/\./,@data[0]);
	    my $m=substr(@dd[0],0,1);
	    my $bb=substr(@dd[0],1);
	    $dict_ratio{$m}=$bb;
	}
    } 
    

}
my $total=0;
foreach my $id (keys %dict_ratio){
    $total=$total+$dict_ratio{$id};
}
foreach my $id (keys %dict_ratio){
    $dict_ratio{$id}=$dict_ratio{$id}/$total;
}
print $dict_ratio{"S"},"\t",$dict_ratio{"H"},"\t",$dict_ratio{"M"},"\t",$dict_ratio{"I"},"\t",$dict_ratio{"B"},"\t",$dict_ratio{"E"},"\t",$dict_ratio{"X"},"\n";
