
# The purpose of this file is to create example data and store it in several
# formats in a subdirectory of this repository.  That way, when the repository
# is published on GitHub, that data will become predictably web-accessible, so
# that tests in this test suite can depend upon data existing at GitHub URLs.

# This script needs to run only if something important about the example data
# or the data saving routines changes.

import sys, os
this_dir = os.path.dirname( os.path.realpath( __file__ ) )
sys.path.append( os.path.join( this_dir, '..', 'src' ) )
import clear_data

import pandas as pd

extensions = [
    'csv', 'tsv',
    'xlsx', # 'xls', # commented out because of deprecated xlwt module
    'parquet',
    'pickle', 'pkl',
    'hdf',
    'dta',
    'orc',
    'json',
    'html'
]

df = pd.example()
for extension in extensions:
    filename = os.path.join( this_dir, 'data', f'example.{extension}' )
    df.save( filename )
