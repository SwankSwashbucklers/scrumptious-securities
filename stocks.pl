#!/usr/bin/perl
use strict;
use warnings;
use JSON qw( decode_json );
use LWP::UserAgent;
use Chart::Graph::Gnuplot qw(gnuplot);


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

	my $resp = $ua->request($req);
	if ($resp->is_success) {
	    $response = decode_json($resp->decoded_content);
	    $quote = $response->{'query'}{'results'}{'quote'};
	    $return{'Bid'} = $quote->{'Bid'};
	    $return{'Ask'} = $quote->{'Ask'};
	    $return{'Time'} = $response->{'query'}{'created'};
	    return %return;
	} 
	else {
	    print "HTTP GET error code: ", $resp->code, "\n";
	    print "HTTP GET error message: ", $resp->message, "\n";
	    exit 1; 
	}
}

my $ua       = LWP::UserAgent->new;
my $query    = "SELECT Bid, Ask, LastTradePriceOnly FROM yahoo.finance.quotes WHERE symbol=\"TSLA\"";
my $env      = "store%3A%2F%2Fdatatables.org%2Falltableswithkeys";
my $endpoint = build_endpoint( "https://query.yahooapis.com/v1/public/yql", 
							   $query,   #YQL query
							   "json",   #format of response
							   "false",  #boolean to include diagnostic info
							   $env,     #
							   "" );     #callback

my @x_column;
my @y_column;

for ( $i=0; $i<1; $i++ ) {
	%response = make_request($endpoint);
	$x_column[$i] = $response{'Time'};
	$y_column[$i] = $response{'Bid'};

	gnuplot({'title' => 'foo'},
          [@x_column, @y_column ]);
}

exit 0;
