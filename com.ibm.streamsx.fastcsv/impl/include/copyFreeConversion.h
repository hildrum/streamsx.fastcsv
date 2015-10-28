/*
 * conversions.h
 *
 *  Created on: Jul 9, 2014
 *      Author: fnparr
 */

#ifndef COPYFREECONVERSIONS_H_
#define COPYFREECONVERSIONS_H_


#endif /* CONVERSIONS_H_ */
/* these libraries will allow us to use  C standard atoi  */

// long token_to_uint64 ( char * bufferp, size_t startp, size_t endp, bool & valid );
// float     token_to_float32 (char * bufferp, size_t startp, size_t endp, bool &valid );
// int  token_to_string (char * bufferp, size_t startp, size_t endp,
//		    char * outbufferp,  size_t outstartp, bool* valid );
/* *************************************************************************************** */
/* each of the Above routines takes as input  (buffer, start and end offset within that    */
/* of token string to convert, address of a boolean to report whether the conversion is    */
/*  If the conversion is invalid - a standard value appropriate to the target type is      */
/* returned as the value                                                                   */
/* for the token_to_string we copy to a designated location and return the number of bytes */
/* this will then help the generated code manage position in the output buffer             */
/* *************************************************************************************** */





// ==========

void next_field (const char * bufferp, size_t * startPtr, const char delim, bool & valid) {

	// if there has been an error previously then do not bother to do anything
	if (!valid) return;

	size_t i = * startPtr;

	while ((bufferp[i] != delim) &&(bufferp[i] != '\n') ) {
		i++;
	}
	if (bufferp[i] == delim)
		i++;
	*startPtr = i;

}

unsigned long str_to_uint64_allowempty(const char * bufferp, size_t * startPtr, const size_t limit, const char delim, bool & valid) {

	// if there has been an error previously then do not bother to anything
	if (!valid) return  (unsigned long)  0;

	unsigned long int n=0;
	size_t i;
	i = * startPtr;
	 const char * s = bufferp;


	// if separator found
	if ((s[i] == delim) || (s[i] == '\n')) {
			if (s[i] == delim)
			i++;
		*startPtr = i ;
		return (unsigned long int) 0;
	}

	while (isspace(  s[i]  )) i++ ;         // read through blank space

	switch (s[i])
	{ case '-':
		while ((s[i]  != delim ) && (i <= limit) && (s[i] != '\n') ) i++ ;
		valid = false;
		if ( s[i] != delim ) i++;                             // return index 1 beyond the delimiter
		* startPtr = i;
		return 0;
	case '+': i++;
	}

	bool haveDigit = false;
	while ( isdigit(s[i]) ) {
		n = 10*n +(s[i] - '0') ;
		i++;
		haveDigit = true;
	}


	while (isspace(  s[i]  )) i++ ;         // read through blank space

	// if next char is delimiter or new line char
	if ( ( s[i] != delim ) && ( s[i] != '\n' ) ) {
		n = 0 ;
		valid =false;
		// move to the next delimiter char
		while (( s[i] != delim ) && (i <= limit) && ( s[i]!= '\n' ) ) i++ ;
	}

	if ( s[i] == delim )
		i++;                             // return index 1 beyond the delimiter
	*startPtr = i ;
	return n;
}

unsigned long str_to_uint64(const char * bufferp, size_t * startPtr, const size_t limit, const char delim, bool & valid,  unsigned char * nullVector, const char nullMask, const unsigned long default_value) {

	// if there has been an error previously then do not bother to anything
	if (!valid) return  default_value;

	unsigned long int n=0;
	size_t i;
	i = * startPtr;
	const char * s = bufferp;


	// if separator found
	if ((s[i] == delim) || (s[i] == '\n')) {
			if (s[i] == delim)
			i++;
		*startPtr = i ;
		// we didn't see any numbers before the separator.
		*nullVector = *nullVector | nullMask;
		return (unsigned long int) default_value;
	}

	while (isspace(  s[i]  )) i++ ;         // read through blank space

	switch (s[i])
	{ case '-':
		while ((s[i]  != delim ) && (i <= limit) && (s[i] != '\n') ) i++ ;
		valid = false;
		if ( s[i] != delim ) i++;                             // return index 1 beyond the delimiter
		* startPtr = i;
		return default_value;
	case '+': i++;
	}

	bool haveDigit = false;
	while ( isdigit(s[i]) ) {
		n = 10*n +(s[i] - '0') ;
		i++;
		haveDigit = true;
	}

	if (!haveDigit) {
		*nullVector = *nullVector | nullMask;
		n = default_value;
	}

	while (s[i]==' '  || s[i] == '\t') i++ ;         // read through blank space

	// if next char is delimiter or new line char
	if ( ( s[i] != delim ) && ( s[i] != '\n' ) ) {
		n = default_value ;
		valid = false;
		// move to the next delimiter char
		while (( s[i] != delim ) && (i <= limit) && ( s[i]!= '\n' ) ) i++ ;
	}

	if ( s[i] == delim )
		i++;                             // return index 1 beyond the delimiter
	*startPtr = i ;
	return n;
}

// ==========

float str_to_float(const char * bufferp, size_t * startPtr, const size_t limit, const char delim, bool & valid, unsigned char * nullVector, const char nullMask, const float default_value) {

	if (!valid) return default_value;

	size_t i;
	i = *startPtr;

	int fint = 0;
	bool neg = false;
	float f = 0;
	int fdec = 0;
	int divisor = 1;
	const char * s = bufferp;


	// if separator found
	if ((s[i] == delim) || (s[i] == '\n')) {
		if (s[i] == delim)
			i++;
		*startPtr = i ;
		*nullVector = *nullVector | nullMask;
		return default_value;
	}

	while (isspace(s[i])) i++ ;         // read through blank space

	// lead + or - sign
	switch (s[i]) {
	case '-':
		neg = true;
		i++;
	case '+' :
		i++;
	}

	bool foundDigit = false;
	// leading digits before the decimal
	while  (isdigit(s[i])) {
		fint = 10*fint +(s[i++] - '0') ;
		foundDigit = true;
	}

	if  (s[i] == '.') {
		i++;
		// Let us deal with mantissa
		while ( isdigit(s[i]) ) {
			foundDigit = true;
			fdec =   fdec*10 + (s[i++] - '0') ;
			divisor = 10* divisor;
		}
	}

	// Calculate the float to return
	f = (double)fint + ((double)fdec / (double) divisor );

	// read through any trailing blank space
	while (isspace(s[i])) i++ ;

	// if it is not separator of end of line
	if ( ( s[i] != delim ) && (s[i] != '\n') ) {
		valid = false;
		f = default_value;
		// move to the next separator
		while (( s[i] != delim ) && (s[i] != '\n' ) && (i <= limit) ) i++ ;
	}

	// move the pointer to the next field if separator found
	if ( s[i] == delim )
		i++;       // return index 1 beyond the delimiter
	*startPtr = i;
	if (!foundDigit) {
		*nullVector = *nullVector | nullMask;
		f = default_value;
	}
	return (float)f;
}


size_t str_to_rstring (const char * bufferp,  size_t * startPtr,
		const size_t limit, const char delim, bool &valid ,  unsigned char * nullVector, const char nullMask
	) {

	if (!valid) return 0;

	size_t i = *startPtr;
	size_t t =0;
	bool foundChar = false;
	while ((bufferp[i] != delim) && (i <= limit) && (bufferp[i] != '\n') ) {
		// increment t & i
		t++;
		i++;
		foundChar = true;
	}
	// Check whether the string was too long--hitting a delimeter or a newline means we ended
	// right, but if we didn't hit one of those, there are still bits of string left in the file.
	if ( bufferp[i] != delim && bufferp[i] != '\n' ) {
		valid = false;
	}
	// TODO: determine whether we need to advance the buffer pointer in the case of an error.
	if (bufferp[i] == delim)
		i++;
	*startPtr = i;
	if (!foundChar) {
		*nullVector = *nullVector | nullMask;
	}
	// return the length of the string.
	return t;
}


