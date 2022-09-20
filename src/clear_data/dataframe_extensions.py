
import pandas as pd
import clear_data.series_extensions

def dataframe_is_a_function ( self, input, output ):
    """
    Does the given DataFrame represent a function from the given input column
    to the given output column?  The answer is computed by treating the two
    columns in question as Series, and simply calling
    `series_is_a_function_to(other)`; see its documentation for details.
    """
    return self[input].is_a_function( self[output] )

pd.DataFrame.is_a_function = dataframe_is_a_function
