
import pandas as pd
import clear_data.series_extensions

def dataframe_is_a_function ( self, input, output ):
    """
    Does the given DataFrame represent a function from the given input column
    to the given output column?  The answer is computed by treating the two
    columns in question as Series, and simply calling
    `series_is_a_function(other)`; see its documentation for details.

    For the `input` and `output` parameters, you can pass column names, which
    will be used to choose the relevant columns.  Or you can pass the columns
    themselves, or any other series of the same length.  Or you can pass the
    DataFrame's index, which will be converted to a Series for you.

	This function is added to the `DataFrame` class, so you can call it as
	`df.is_a_function(input_col,output_col)` or as
    `df.can_lookup(input_col,output_col)`.
    """
    # ensure input is a Series
    if type( input ) is str:
        input = self[input]
    elif isinstance( input, pd.Index ):
        input = input.to_series()
    # ensure output is a Series
    if type( output ) is str:
        output = self[output]
    elif isinstance( output, pd.Index ):
        output = output.to_series()
    # do the work
    return input.is_a_function( output )

pd.DataFrame.is_a_function = dataframe_is_a_function
pd.DataFrame.can_lookup = dataframe_is_a_function

def dataframe_to_function ( self, input, output ):
    """
    If the given DataFrame represents a function from the given input column
    to the given output column, which you can test using
    `dataframe_is_a_function`, then this function will construct for you a
    Python function embodying that relationship, that you can subsequently
    call.

    For the `input` and `output` parameters, you can pass column names, which
    will be used to choose the relevant columns.  Or you can pass the columns
    themselves, or any other series of the same length.  Or you can pass the
    DataFrame's index, which will be converted to a Series for you.

	This function is added to the `DataFrame` class, so you can call it as
	`df.get_function(input_col,output_col)`.
    """
    # ensure input is a Series
    if type( input ) is str:
        input = self[input]
    elif isinstance( input, pd.Index ):
        input = input.to_series()
    # ensure output is a Series
    if type( output ) is str:
        output = self[output]
    elif isinstance( output, pd.Index ):
        output = output.to_series()
    # do the work
    return input.get_function( output )

pd.DataFrame.to_function = dataframe_to_function
