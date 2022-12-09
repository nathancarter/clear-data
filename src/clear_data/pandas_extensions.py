
import numpy as np
import pandas as pd

# Top 50 last names from 2010 US Census data:
def _random_last_name ():
    return np.random.choice( [ 'Smith', 'Johnson', 'Williams', 'Brown',
        'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez',
        'Hernandez', 'Lopez', 'Gonzalez', 'Wilson', 'Anderson', 'Thomas',
        'Taylor', 'Moore', 'Jackson', 'Martin', 'Lee', 'Perez', 'Thompson',
        'White', 'Harris', 'Sanchez', 'Clark', 'Ramirez', 'Lewis', 'Robinson',
        'Walker', 'Young', 'Allen', 'King', 'Wright', 'Scott', 'Torres',
        'Nguyen', 'Hill', 'Flores', 'Green', 'Adams', 'Nelson', 'Baker',
        'Hall', 'Rivera', 'Campbell', 'Mitchell', 'Carter', 'Roberts' ] )
# Top 50 first names from 2021 US Social Security data, 25 male, 25 female:
def _random_first_name ():
    return np.random.choice( [ 'Liam', 'Olivia', 'Noah', 'Emma', 'Oliver',
        'Charlotte', 'Elijah', 'Amelia', 'James', 'Ava', 'William', 'Sophia',
        'Benjamin', 'Isabella', 'Lucas', 'Mia', 'Henry', 'Evelyn', 'Theodore',
        'Harper', 'Jack', 'Luna', 'Levi', 'Camila', 'Alexander', 'Gianna',
        'Jackson', 'Elizabeth', 'Mateo', 'Eleanor', 'Daniel', 'Ella', 'Michael',
        'Abigail', 'Mason', 'Sofia', 'Sebastian', 'Avery', 'Ethan', 'Scarlett',
        'Logan', 'Emily', 'Owen', 'Aria', 'Samuel', 'Penelope', 'Jacob',
        'Chloe', 'Asher', 'Layla' ] )
# Made up list of departments
def _random_department ():
    return np.random.choice( [ 'Sales', 'Service', 'Management',
        'Administration', 'Finance', 'Accounting', 'Analytics', 'Research',
        'Human Resources', 'Facilities', 'Information Technology' ] )

def random_dataframe ( num_rows = 20, num_cols = 5, type = 'Employee' ):
    '''
    Generate a random DataFrame for use in examples or testing.

    Example uses of this function:
    
    `pd.example(10,3,int)` gives a DataFrame of random integers, with 10 rows
    and 3 columns.
    
    `pd.example(5,5,float)` gives a square (5-by-5) DataFrame of random floating
    point values.

    `pd.example(100,10,'Employee')` gives a DataFrame of random employee records
    (using the top 50 most common first and last names from recent US Census and
    Social Security records, with random departments, IDs, salaries, etc.), with
    100 rows and 10 columns.

    The default, produced by `pd.example()`, uses 20 rows, 6 columns, and
    Employee records.

    This function is added to the `pandas` module, so you can call it as
    `pd.example(args).
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
            'LastName' : [ _random_last_name() for _ in range( num_rows ) ],
            'FirstName' : [ _random_first_name() for _ in range( num_rows ) ],
            'ID' : [
                str(id) for id in np.random.randint( 100000, 999999, num_rows )
            ],
            'Department' : [ _random_department() for _ in range( num_rows ) ],
            'Salary' : np.random.uniform( 50000, 150000, num_rows ).round( 2 ),
            'YearsAtCompany' : np.random.randint( 1, 20, num_rows )
        } )
        while len( result.columns ) < num_cols:
            result[f'feature{len( result.columns )-5}'] = \
                np.random.normal( 50, 25, num_rows )
        return result
    raise TypeError( f'Cannot generate example DataFrame of "{str(type)}"')

pd.example = random_dataframe
