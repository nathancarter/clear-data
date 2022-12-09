
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

def series_is_a_function ( self, other_series=None ):
    """
    If we view this Series as a list of inputs, and the `other_series` as a
    corresponding list of outputs, do those pairs form a function?  In other
    words, does every input in this Series line up with exactly one output in
    the `other_series`, so that we could reliably do a lookup operation?
    The result is a boolean.

    For example, if this series were `[1,2,3]` and the other `['a','b','a']`,
    the result would be true, because no matter which input we look up (1, 2, or
    3) we get a predictable, single output.  But if this series were `[1,2,3,1]`
    and the other `['a','b','a','c']`, the result would be false, because for
    the input 1, it is unclear whether the output should be `'a'` or `'c'`.

    If we omit the parameter `other_series`, then we can view this Series'
    index as a list of inputs, and its entries as a corresponding list of
    outputs, and ask whether those pairs form a function.  That is, we ask
    about mapping the Series' index to its own entries, rather than a separate
    Series' entries.

    This function is added to the `Series` class, so you can call it as
    `mySeries.is_a_function(yourSeries)`.
    """
    if other_series is not None:
        return _is_a_finite_function( self, other_series )
    else:
        return _is_a_finite_function( self.index.to_series(), self )

pd.Series.is_a_function = series_is_a_function

def series_to_function ( self, other_series=None ):
    """
    See the documentation for `series_is_a_function()` to understand how to view
    a Series as a function.  If that test returns True, this function will
    create a `FiniteFunction` instance that embodies the function in question,
    making it easy to apply the function to do lookups.  You can pass a
    parameter or not, and the behavior is the same as it is for
    `series_is_a_function()`.

    This function is added to the `Series` class, so you can call it as
    `mySeries.to_function()` or `mySeries.get_function()`.
    """
    if other_series is not None:
        return FiniteFunction( self, other_series )
    else:
        return FiniteFunction( self.index.to_series(), self )

pd.Series.to_function = series_to_function
pd.Series.get_function = series_to_function

def series_to_dictionary ( self, other_series=None ):
    """
    See the documentation for `series_is_a_function()` to understand how to view
    a Series as a function.  If that test returns True, this function will
    create a Python dict that embodies the function in question, making it easy
    to perform lookup operations.  You can pass a parameter or not, and the
    behavior is the same as it is for `series_is_a_function()`.

    This function is added to the `Series` class, so you can call it as
    `mySeries.to_dictionary()` or just as `mySeries.to_dict()`.  You can also
    write `mySeries.get_dictionary()` or `mySeries.get_dict()`.
    """
    if other_series is not None:
        return dict( zip( self, other_series ) )
    else:
        return dict( zip( self.index.to_series(), self ) )

pd.Series.to_dict = series_to_dictionary
pd.Series.to_dictionary = series_to_dictionary
pd.Series.get_dict = series_to_dictionary
pd.Series.get_dictionary = series_to_dictionary

def series_to_relation ( self, *other_series ):
    """
    Given one or more series of the same length, convert them into a relation,
    also called a predicate.  For instance, given a table of data about
    restaurants in Philadelphia, we might use just the "address" and "type"
    columns, producing a relation that might be described in English as "There
    is a restaurant of type Y at address X in Philadelphia."  The relation or
    predicate produced is simply a membership test into the list of tuples
    given by the series provided.

    If `X = pd.Series([1,2,3])` and `Y = pd.Series([4,5,6])` and
    `Z = series_to_relation(X,Y)`, then we would have `Z(1,4) == True` but
    `Z(1,2) == False`, becauase `Z` represents the collection of tuples
    (1,4), (2,5), and (3,6).

    This function is added to the `Series` class, so you can call it using any
    of the following means: `my_series.to_relation(other)`,
    `my_series.to_relation_with(other)`, `my_series.to_predicate(other)`
    `my_series.to_predicate_with(other)`, `my_series.get_relation(other)`,
    `my_series.get_relation_with(other)`, `my_series.get_predicate(other)`, and
    `my_series.get_predicate_with(other)`.
    """
    def result ( *args ):
        return args in zip( *[ self, *other_series ] )
    return result

pd.Series.to_relation = series_to_relation
pd.Series.to_relation_with = series_to_relation
pd.Series.to_predicate = series_to_relation
pd.Series.to_predicate_with = series_to_relation
pd.Series.get_relation = series_to_relation
pd.Series.get_relation_with = series_to_relation
pd.Series.get_predicate = series_to_relation
pd.Series.get_predicate_with = series_to_relation
