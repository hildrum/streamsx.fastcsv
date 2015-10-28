package BatchFileSourceCommon;

use strict;
 use File::Basename;
 my $addDebug = 0;
my $indent="      ";
our $i2 = ${indent}.$indent;
my $i3 = ${indent}.$i2;
my $i4 = $i2.$i2;



sub isLineNumberAttribute($) {
	my ($name) = @_;
	return ($name eq "lineNumber" || $name eq "linenumber" || $name eq "lineno");
	
}

sub isErrorCodeAttribute($) {
my ($name) = @_;
	return ($name eq "code" || $name eq "errorCode" || $name eq "errorcode");
}

# used to determine whether the attribute can be populated with the filename.
sub isFileAttribute($) {
	my ($name) = @_;
	return ($name eq "file" || $name eq "filename" || $name eq "fileName");
}


# Get info related to output ports.  Used to set variables in
# .h and .cpp.

sub getOutputPortInfo($) {
  my ($model) = @_;
  my $numOutputs = $model->getNumberOfOutputPorts();
  my $useRecordType = 0;
  my $errorPort = ($numOutputs == 2);
  my $numRec = 0;
  if ($numOutputs > 2) {
    SPL::CodeGen::exitln("Only 2 output ports are allowed, found $numOutputs");
  }
  
  return ($numOutputs,$useRecordType, $errorPort);
}

1;
