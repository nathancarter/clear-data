
import pandas as pd
from clear_data.finite_function import FiniteFunction

def series_has_duplicates ( self ):
	"""
	Does this Series have any duplicate entries?
	Returns a boolean result.

	This is equivalent to asking whether any entry in the series' `duplicated()`
	array is true.

	This function is added to the `Series` class, so you can call it as
	`mySeries.has_duplicates()`.
	"""
	return any( self.duplicated() )

pd.Series.has_duplicates = series_has_duplicates

def series_has_no_duplicates ( self ):
	"""
	Does this Series have all unique entries?
	Returns a boolean result, which is guaranteed to be the opposie of the
	result of the function `series_has_duplicates()`.

	This function is added to the `Series` class, so you can call it as
	`mySeries.has_no_duplicates()`.
	"""
	return not self.has_duplicates()

pd.Series.has_no_duplicates = series_has_no_duplicates

# Not a public function; do not make docs for this.
def _is_a_finite_function ( inputs, outputs ):
	as_a_dict = dict( zip( inputs, outputs ) )
	return all( inputs.map( as_a_dict ) == outputs )

def series_is_a_function_to ( self, other_series ):
	"""
	If we view this Series as a list of inputs, and the other_series as a
	corresponding list of outputs, do those pairs form a function?  In other
	words, does every input in this Series line up with exactly one output in
	the other_series, so that we could reliably do a lookup operation?
	The result is a boolean.

	For example, if this series were `[1,2,3]` and the other `['a','b','a']`,
	the result would be true, because no matter which input we look up (1, 2, or
	3) we get a predictable, single output.  But if this series were `[1,2,3,1]`
	and the other `['a','b','a','c']`, the result would be false, because for
	the input 1, it is unclear whether the output should be `'a'` or `'c'`.

	This function is added to the `Series` class, so you can call it as
	`mySeries.is_a_function_to(yourSeries)`.
	"""
	return _is_a_finite_function( self, other_series )

pd.Series.is_a_function_to = series_is_a_function_to

def series_is_a_function ( self ):
	"""
	If we view this Series' index as a list of inputs, and its entries as a
	corresponding list of outputs, do those pairs form a function?  See the
	documentation for `series_is_a_function_to(other)` for more details; this
	function asks about mapping the Series' inputs to its own entries, rather
	than a separate Series' entries.

	This function is added to the `Series` class, so you can call it as
	`mySeries.is_a_function()`.
	"""
	return _is_a_finite_function( self.index.to_series(), self )

pd.Series.is_a_function = series_is_a_function

def series_to_function ( self ):
	"""
	See the documentation for `series_is_a_function()` to understand how to view
	a Series as a function.  If that test returns True, this function will
	create a `FiniteFunction` instance that embodies the function in question,
	making it easy to apply the function to do lookups.

	This function is added to the `Series` class, so you can call it as
	`mySeries.to_function()`.
	"""
	return FiniteFunction( self.index.to_series(), self )

pd.Series.to_function = series_to_function

def series_to_function_to ( self, other_series ):
	"""
	See the documentation for `series_is_a_function_to(other)` to understand how
	to view one Series as a function to another Series.  If that test returns
	`True`, this function will create a FiniteFunction instance that embodies
	the function in question, making it easy to apply the function to do
	lookups.

	This function is added to the `Series` class, so you can call it as
	`mySeries.to_function_to(yourSeries)`.
	"""
	return FiniteFunction( self, other_series )

pd.Series.to_function_to = series_to_function_to

def series_to_dictionary ( self ):
	"""
	See the documentation for `series_is_a_function()` to understand how to view
	a Series as a function.  If that test returns True, this function will
	create a Python dict that embodies the function in question, making it easy
	to perform lookup operations.

	This function is added to the `Series` class, so you can call it as
	`mySeries.to_dictionary()` or just as `mySeries.to_dict()`.
	"""
	return dict( zip( self.index.to_series(), self ) )

pd.Series.to_dict = series_to_dictionary
pd.Series.to_dictionary = series_to_dictionary

def series_to_dictionary_to ( self, other_series ):
	"""
	See the documentation for `series_is_a_function_to(other)` to understand how
	to view one Series as a function to another Series.  If that test returns
	`True`, this function will create a Python dict that embodies the function
	in question, making it easy to perform lookup operations.

	This function is added to the `Series` class, so you can call it as
	`mySeries.to_dictionary_to(yourSeries)` or just as
	`mySeries.to_dict_to(yourSeries)`.
	"""
	return dict( zip( self, other_series ) )

pd.Series.to_dict_to = series_to_dictionary_to
pd.Series.to_dictionary_to = series_to_dictionary_to
