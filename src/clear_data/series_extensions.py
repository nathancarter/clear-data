
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
