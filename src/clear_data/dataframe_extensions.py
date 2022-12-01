
import numpy as np
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

def dataframe_rows_satisfying ( self, test, efficient=False ):
    """
    There are two ways to use this function.
    
    First, you can call `dataframe_rows_satisfying(df,S)` where `S` is a
    pandas Series of boolean values, and it will give the same result as
    `df[S]` would.  Obviously that notation is more concise, while this one is
    more explicit.
    
    Because this function will be installed in the DataFrame class, you can
    call it as `df.rows_satisfying(S)` or any of the following synonyms:
    `df.rows_where(S)`, `df.rows_such_that(S)`, `df.rows_in_which(S)`,
    `df.select(S)`, `df.select_rows(S)`, or `df.subset(S)`.

    Second, you can call `dataframe_rows_satisfying(df,P)` where `P` is any
    Python function to be used as a predicate on rows.  `P` will be called
    once for each row, with the row passed as a pandas Series.  The result of
    the function will be another DataFrame containing only the rows for which
    `P` returns True.  The same calling synonyms as above apply in this case
    as well.

    One further difference between this function and `df[S]` is that `df[S]`
    creates a slice of `df`, leading to the potential of the dreaded "writing
    to a slice of a DataFrame" error.  This function, by default, creates a
    copy, because this is often perfectly acceptable, given that most use
    cases do not involve big data.  You can pass the optional keyword
    argument `efficient=True` to get a slice instead of a copy.
    """
    if callable( test ):
        test = pd.Series( test( row ) for _,row in self.iterrows() )
    slice = self[test]
    return slice if efficient else slice.copy()

pd.DataFrame.rows_satisfying = dataframe_rows_satisfying
pd.DataFrame.rows_such_that = dataframe_rows_satisfying
pd.DataFrame.rows_in_which = dataframe_rows_satisfying
pd.DataFrame.rows_where = dataframe_rows_satisfying
pd.DataFrame.rows_select_rows = dataframe_rows_satisfying
pd.DataFrame.rows_select = dataframe_rows_satisfying
pd.DataFrame.rows_subset = dataframe_rows_satisfying

# Top 50 last names from 2010 US Census data:
def random_last_name ():
    return np.random.choice( [ 'Smith', 'Johnson', 'Williams', 'Brown',
        'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez',
        'Hernandez', 'Lopez', 'Gonzalez', 'Wilson', 'Anderson', 'Thomas',
        'Taylor', 'Moore', 'Jackson', 'Martin', 'Lee', 'Perez', 'Thompson',
        'White', 'Harris', 'Sanchez', 'Clark', 'Ramirez', 'Lewis', 'Robinson',
        'Walker', 'Young', 'Allen', 'King', 'Wright', 'Scott', 'Torres',
        'Nguyen', 'Hill', 'Flores', 'Green', 'Adams', 'Nelson', 'Baker',
        'Hall', 'Rivera', 'Campbell', 'Mitchell', 'Carter', 'Roberts' ] )
# Top 50 first names from 2021 US Social Security data, 25 male, 25 female:
def random_first_name ():
    return np.random.choice( [ 'Liam', 'Olivia', 'Noah', 'Emma', 'Oliver',
        'Charlotte', 'Elijah', 'Amelia', 'James', 'Ava', 'William', 'Sophia',
        'Benjamin', 'Isabella', 'Lucas', 'Mia', 'Henry', 'Evelyn', 'Theodore',
        'Harper', 'Jack', 'Luna', 'Levi', 'Camila', 'Alexander', 'Gianna',
        'Jackson', 'Elizabeth', 'Mateo', 'Eleanor', 'Daniel', 'Ella', 'Michael',
        'Abigail', 'Mason', 'Sofia', 'Sebastian', 'Avery', 'Ethan', 'Scarlett',
        'Logan', 'Emily', 'Owen', 'Aria', 'Samuel', 'Penelope', 'Jacob',
        'Chloe', 'Asher', 'Layla' ] )
# Made up list of departments
def random_department ():
    return np.random.choice( [ 'Sales', 'Service', 'Management',
        'Administration', 'Finance', 'Accounting', 'Analytics', 'Research',
        'Human Resources', 'Facilities', 'Information Technology' ] )

def random_dataframe ( num_rows = 20, num_cols = 5, type = 'Employee' ):
    '''
    Generate a random DataFrame for use in examples or testing.

    Example uses of this function:
    
    `pandas.DataFrame.example(10,3,int)` gives a DataFrame of random integers,
    with 10 rows and 3 columns.
    
    `pandas.DataFrame.example(5,5,float)` gives a square (5-by-5) DataFrame of
    random floating point values.

    `pandas.DataFrame.example(100,10,'Employee')` gives a DataFrame of random
    employee records (using the top 50 most common first and last names from
    recent US Census and Social Security records, with random departments, IDs,
    salaries, etc.), with 100 rows and 10 columns.

    The default, produced by `pandas.DataFrame.example()`, uses 20 rows, 6
    columns, and Employee records.
    '''
    if type == int:
        return pd.DataFrame(
            np.random.randint( -10, 10, ( num_rows, num_cols ) ),
            columns=[ f'feature{i}' for i in range( 1, num_cols + 1 ) ] )
    if type == float:
        return pd.DataFrame(
            np.random.normal( 50, 25, ( num_rows, num_cols ) ),
            columns=[ f'feature{i}' for i in range( 1, num_cols + 1 ) ] )
    if type == 'Employee':
        num_cols = max( num_cols, 6 )
        result = pd.DataFrame( {
            'LastName' : [ random_last_name() for _ in range( num_rows ) ],
            'FirstName' : [ random_first_name() for _ in range( num_rows ) ],
            'ID' : [
                str(id) for id in np.random.randint( 100000, 999999, num_rows )
            ],
            'Department' : [ random_department() for _ in range( num_rows ) ],
            'Salary' : np.random.uniform( 50000, 150000, num_rows ).round( 2 ),
            'YearsAtCompany' : np.random.randint( 1, 20, num_rows )
        } )
        while len( result.columns ) < num_cols:
            result[f'feature{len( result.columns )-5}'] = \
                np.random.normal( 50, 25, num_rows )
        return result
    raise ValueError( f'Cannot generate example DataFrame of "{str(type)}"')

pd.DataFrame.example = random_dataframe
