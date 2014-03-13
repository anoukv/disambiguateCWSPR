#!/usr/bin/perl -w

die "usage: score infile reference\n" unless ($#ARGV==1);
$infile = $ARGV[0];
$reffile = $ARGV[1];

open(FIN, $infile) or die "unable to open $infile\n";
@answers = <FIN>;
close(FIN);

open(FIN, $reffile) or die "unable to open $reffile\n";
@ref = <FIN>;
close(FIN);

die "mismatched number of reference scripts and answers\n" 
    unless ($#answers == $#ref);

$i=0;
foreach $a (@answers) {
    $a =~ s/[\r\n\s]//og;
    $r = $ref[$i++];
    $r =~ s/[\r\n]//og;
    ($type, $target) = split(/\s+/, $r);
    $correct{$type}++ if ($a eq $target);
    $questions{$type}++;
}

sub process {
    my $type = shift;
    $correct{$type} = 0 unless (defined($correct{$type}));
    return (0,0) unless (defined($questions{$type}));
    $pc = 100 * $correct{$type} / $questions{$type};
    print "$type $pc \n";
    return ( $correct{$type}, $questions{$type});
}

($c, $q ) = process("JJ_JJR");
$adj_corr += $c; $adj_tot += $q;
($c, $q ) = process("JJR_JJ");
$adj_corr += $c; $adj_tot += $q;
print "\n";
($c, $q ) = process("JJ_JJS");
$adj_corr += $c; $adj_tot += $q;
($c, $q ) = process("JJS_JJ");
$adj_corr += $c; $adj_tot += $q;
print "\n";
($c, $q ) = process("JJR_JJS");
$adj_corr += $c; $adj_tot += $q;
($c, $q ) = process("JJS_JJR");
$adj_corr += $c; $adj_tot += $q;
print "\n";
$ap = int(10000 * $adj_corr / $adj_tot)/100;
print "Adjectives $ap % correct\n\n";

($c, $q) = process("NNS_NN");
$noun_corr += $c; $noun_tot += $q;
($c, $q) = process("NN_NNS");
$noun_corr += $c; $noun_tot += $q;
print "\n";
($c, $q) = process("NN_NNPOS");
$noun_corr += $c; $noun_tot += $q;
($c, $q) = process("NNPOS_NN");
$noun_corr += $c; $noun_tot += $q;
print "\n";
$np = int(10000 * $noun_corr / $noun_tot)/100;
print "Nouns $np % correct\n\n";

($c, $q ) = process("VB_VBZ");
$vb_corr += $c; $vb_tot += $q;
($c, $q ) = process("VBZ_VB");
$vb_corr += $c; $vb_tot += $q;
print "\n";
($c, $q ) = process("VB_VBD");
$vb_corr += $c; $vb_tot += $q;
($c, $q ) = process("VBD_VB");
$vb_corr += $c; $vb_tot += $q;
print "\n";
($c, $q ) = process("VBD_VBZ");
$vb_corr += $c; $vb_tot += $q;
($c, $q ) = process("VBZ_VBD");
$vb_corr += $c; $vb_tot += $q;
print "\n";
$vp = int(10000 * $vb_corr / $vb_tot)/100;
print "Verbs $vp % correct\n\n";

$totcorrect = $adj_corr + $noun_corr + $vb_corr;
$tot = $adj_tot + $noun_tot + $vb_tot;

$pc = int(10000 * $totcorrect / $tot)/100;
print "Overall correct: $pc %\n";
