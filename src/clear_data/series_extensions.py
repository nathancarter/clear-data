
import pandas as pd

def series_has_duplicates ( self ):
	"""
	Does this Series have any duplicate entries?
	Returns a boolean result.

	This is equivalent to asking whether any entry in the series' duplicated()
	array is true.
	"""
	return any( self.duplicated() )

pd.Series.has_duplicates = series_has_duplicates

def series_has_no_duplicates ( self ):
	"""
	Does this Series have all unique entries?
	Returns a boolean result, which is guaranteed to be the opposie of the
	result of the function has_duplicates().
	"""
	return not self.has_duplicates()

pd.Series.has_no_duplicates = series_has_no_duplicates

def is_a_finite_function ( inputs, outputs ):
	as_a_dict = dict( zip( inputs, outputs ) )
	return all( inputs.map( as_a_dict ) == outputs )

def series_is_a_function_to ( self, other_series ):
	"""
	If we view this Series as a list of inputs, and the other_series as a
	corresponding list of outputs, do those pairs form a function?  In other
	words, does every input in this Series line up with exactly one output in
	the other_series, so that we could reliably do a lookup operation?
	The result is a boolean.

	For example, if this series were [1,2,3] and the other ['a','b','a'], the
	result would be true, because no matter which input we look up (1, 2, or 3)
	we get a predictable, single output.  But if this series were [1,2,3,1] and
	the other ['a','b','a','c'], the result would be false, because for the
	input 1, it is unclear whether the output should be 'a' or 'c'.
	"""
	return is_a_finite_function( self, other_series )

pd.Series.is_a_function_to = series_is_a_function_to

def series_is_a_function ( self ):
	"""
	If we view this Series' index as a list of inputs, and its entries as a
	corresponding list of outputs, do those pairs form a function?  See the
	documentation for Series.is_a_function_to(other) for more details; this
	function asks about mapping the Series' inputs to its own entries, rather
	than a separate Series' entries.
	"""
	return is_a_finite_function( self.index.to_series(), self )

pd.Series.is_a_function = series_is_a_function
