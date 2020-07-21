#!/usr/bin/env perl

# This file is derived from https://github.com/bricksdont/moses-scripts/blob/master/scripts/tokenizer/tokenizer.perl

use strict;
use warnings;

#binmode(STDIN, ":utf8");
#binmode(STDOUT, ":utf8");

while(<STDIN>)
{
print &tokenize($_);
}
        

sub tokenize
{
    my($text) = @_;

    chomp($text);
    $text = " $text ";

    #remove ASCII junk
    $text =~ s/\s+/ /g;
    $text =~ s/[\000-\037]//g;

    #word token method
    my @words = split(/\s/,$text);
    $text = "";
    for (my $i=0;$i<(scalar(@words));$i++)
    {
        my $word = $words[$i];
        
        $text .= $word." ";
    }

    # .' at end of sentence is missed
    $text =~ s/\.\' ?$/ . ' /;


    #ensure final line break
    $text .= "\n" unless $text =~ /\n$/;

    return $text;
}
