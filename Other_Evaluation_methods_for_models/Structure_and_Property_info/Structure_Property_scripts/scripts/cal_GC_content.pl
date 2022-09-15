my $bracket=shift;
open(BR,$bracket);
my $cn=0;
my $name;
my $energy;
print "id","\t","length","\t","MFE","\t","Z-curve_x","\t","Z-curve_y","\t","Z-curve_z","\t","GC","\t","AUGC","\t","GCskew","\n";
while (my $line=<BR>){
    chomp($line);
    if ($cn%3==0){
	my @data=split(/\s+/,$line);
	$name=@data[3];
	$energy=@data[2];
    }
    if ($cn%3==1){
	my @data=split(//,$line);
	my $nn_A=0;my $nn_C=0;my $nn_G=0;my $nn_U=0;
	my $len=0;
	foreach my $id (@data){
	    if ($id eq "A"){$nn_A=$nn_A+1;}
	    if ($id eq "C"){$nn_C=$nn_C+1;}
	    if ($id eq "U"){$nn_U=$nn_U+1;}
	    if ($id eq "G"){$nn_G=$nn_G+1;}
	    $len=$len+1;
	}
	my $ratio_A=$nn_A/$len;my $ratio_C=$nn_C/$len;my $ratio_G=$nn_G/$len;my $ratio_U=$nn_U/$len;
	my $x=($ratio_A+$ratio_G)-($ratio_C+$ratio_U);
	my $y=($ratio_A+$ratio_C)-($ratio_G+$ratio_U);
	my $z=($ratio_A+$ratio_U)-($ratio_G+$ratio_C);
	my $GC=$ratio_G+$ratio_C;
	my $AUGC=($ratio_A+$ratio_U)/($ratio_G+$ratio_C);
	my $GCskew=($ratio_G-$ratio_C)/($ratio_G+$ratio_C);
	print $name,"\t",$len,"\t",$energy,"\t",$x,"\t",$y,"\t",$z,"\t",$GC,"\t",$AUGC,"\t",$GCskew,"\n";
    }

    $cn=$cn+1;
}
