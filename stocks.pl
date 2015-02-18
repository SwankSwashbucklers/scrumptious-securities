#!/usr/bin/perl
use strict;
use warnings;
use JSON qw( decode_json );
use LWP::UserAgent;
use Term::ANSIScreen qw( cls );
#use Chart::Graph::Gnuplot qw(gnuplot);

system("cls");

sub build_endpoint {
	$_[1] =~ s/[\%]/%25/g; #this must be done first

	$_[1] =~ s/[\ ]/%20/g;
	$_[1] =~ s/[\!]/%21/g;
	$_[1] =~ s/[\"]/%22/g;
	$_[1] =~ s/[\#]/%23/g;
	$_[1] =~ s/[\$]/%24/g;
	$_[1] =~ s/[\&]/%26/g;
	$_[1] =~ s/[\']/%27/g;
	$_[1] =~ s/[\(]/%28/g;
	$_[1] =~ s/[\)]/%29/g;
	$_[1] =~ s/[\*]/%2A/g;
	$_[1] =~ s/[\+]/%2B/g;
	$_[1] =~ s/[\,]/%2C/g;
	$_[1] =~ s/[\-]/%2D/g;
	$_[1] =~ s/[\.]/%2E/g;
	$_[1] =~ s/[\/]/%2F/g;
	$_[1] =~ s/[\:]/%3A/g;
	$_[1] =~ s/[\;]/%3B/g;
	$_[1] =~ s/[\<]/%3C/g;
	$_[1] =~ s/[\=]/%3D/g;
	$_[1] =~ s/[\>]/%3E/g;
	$_[1] =~ s/[\?]/%3F/g;
	$_[1] =~ s/[\@]/%40/g;

	return sprintf("%s?q=%s&format=%s&diagnostics=%s&env=%s&callback=%s", @_); 
}

sub make_request {
	# set custom HTTP request header fields
	my $req = HTTP::Request->new(GET => $_[0]);
	$req->header('content-type' => 'application/json');
	$req->header('x-auth-token' => 'kfksj48sdfj4jd9d');

	my $resp = $_[1]->request($req);
	if ($resp->is_success) {
	    my $response = decode_json($resp->decoded_content);
	    my $quote = $response->{'query'}{'results'}{'quote'};
	    my %return = ('Name' => $quote->{'Name'},
	    			  'Bid'  => $quote->{'Bid'}, 
	    			  'Ask'  => $quote->{'Ask'}, 
	    			  'Time' => $response->{'query'}{'created'});
	    return %return;
	} 
	else {
	    print "HTTP GET error code: ", $resp->code, "\n";
	    print "HTTP GET error message: ", $resp->message, "\n";
	    exit 1; 
	}
}

my $ua       = LWP::UserAgent->new;
my $query    = "SELECT Name, Bid, Ask, LastTradePriceOnly FROM yahoo.finance.quotes WHERE symbol=\"TSLA\"";
my $env      = "store%3A%2F%2Fdatatables.org%2Falltableswithkeys";
my $endpoint = build_endpoint( "https://query.yahooapis.com/v1/public/yql", 
							   $query,   #YQL query
							   "json",   #format of response
							   "false",  #boolean to include diagnostic info
							   $env,     #
							   "" );     #callback


=begin comment
my @x_column;
my @y_column;

for ( $i=0; $i<1; $i++ ) {
	%response = make_request($endpoint);
	$x_column[$i] = $response{'Time'};
	$y_column[$i] = $response{'Bid'};

	gnuplot({'title' => 'foo'},
          [@x_column, @y_column ]);
}
=cut

$| = 1;
my %response = make_request($endpoint, $ua);
print $response{'Name'}."\n";
print "Bid : ".$response{'Bid'}."\n";
print "Ask : ".$response{'Ask'};

for ( ; ; ) {
	sleep 10;
	system("cls"); #cls();

	%response = make_request($endpoint, $ua);
	print $response{'Name'}."\n";
	print "Bid : ".$response{'Bid'}."\n";
	print "Ask : ".$response{'Ask'};
}

exit 0;
