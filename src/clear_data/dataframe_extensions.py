
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
	`df.to_function(input_col,output_col)` or
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
    return input.to_function( output )

pd.DataFrame.to_function = dataframe_to_function

def dataframe_to_dictionary ( self, input, output ):
    """
    If the given DataFrame represents a function from the given input column
    to the given output column, which you can test using
    `dataframe_is_a_function`, then this function will construct for you a
    Python dictionary embodying that relationship, that you can subsequently
    use for lookups.

    For the `input` and `output` parameters, you can pass column names, which
    will be used to choose the relevant columns.  Or you can pass the columns
    themselves, or any other series of the same length.  Or you can pass the
    DataFrame's index, which will be converted to a Series for you.

	This function is added to the `DataFrame` class, so you can call it as
	`df.to_dictionary(input_col,output_col)`,
	`df.get_dictionary(input_col,output_col)`,
	`df.to_dict(input_col,output_col)`, or
	`df.get_dict(input_col,output_col)`.
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
    return input.to_dictionary( output )

pd.DataFrame.to_dictionary = dataframe_to_dictionary
pd.DataFrame.get_dictionary = dataframe_to_dictionary
pd.DataFrame.to_dict = dataframe_to_dictionary
pd.DataFrame.get_dict = dataframe_to_dictionary

def dataframe_to_relation ( self, *column_names ):
    """
    Given one or more column names, convert them into a relation, also called
    a predicate.  For instance, if the DataFrame is about restaurants in
    Philadelphia, we might use just the "address" and "type" columns,
    producing a relation that might be described in English as "There is a
    restaurant of type Y at address X in Philadelphia."  The relation or
    predicate produced is simply a membership test into the list of tuples
    given by the columns provided.

    If `df = pd.DataFrame({"A":[1,2,3],"B":[4,5,6]})` and
    `R = dataframe_to_relation(df,"A","B")`, then we would have
    `R(1,4) == True` but `R(1,2) == False`, becauase `R` represents the
    collection of tuples (1,4), (2,5), and (3,6).

	This function is added to the `DataFrame` class, so you can call it using
    any of the following means: `my_df.to_relation(columns...)`,
    `my_df.to_predicate(columns...)` `my_df.get_relation(columns...)`, and
    `my_df.get_predicate(columns...)`.

    If you call this function on a DataFrame but do not specify the column
    names, it assumes that all columns in the DataFrame should be used.
    """
    if len( column_names ) == 0:
        column_names = self.columns
    columns = [ self[column_name] for column_name in column_names ]
    return columns[0].to_relation( *columns[1:] )

pd.DataFrame.to_relation = dataframe_to_relation
pd.DataFrame.to_predicate = dataframe_to_relation
pd.DataFrame.get_relation = dataframe_to_relation
pd.DataFrame.get_predicate = dataframe_to_relation
