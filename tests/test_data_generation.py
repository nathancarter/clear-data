
import sys, os
this_dir = os.path.dirname( os.path.realpath( __file__ ) )
sys.path.append( os.path.join( this_dir, '..', 'src' ) )
import clear_data

import unittest
import numpy as np
import pandas as pd

class TestDataGeneration( unittest.TestCase ):

    def test_int_case ( self ):
        # Example 1 - 4x6 ints
        df = pd.DataFrame.example( 4, 6, int )
        self.assertEqual( len( df ), 4 )
        self.assertEqual( len( df.columns ), 6 )
        self.assertTrue( all( dt == np.int64 for dt in df.dtypes ) )
        # Example 2 - 20x10 ints
        df = pd.DataFrame.example( 20, 10, int )
        self.assertEqual( len( df ), 20 )
        self.assertEqual( len( df.columns ), 10 )
        self.assertTrue( all( dt == np.int64 for dt in df.dtypes ) )
        # Example 3 - should work with default #rows/cols
        df = pd.DataFrame.example( type=int )
        self.assertGreater( len( df ), 0 )
        self.assertGreater( len( df.columns ), 0 )
        self.assertTrue( all( dt == np.int64 for dt in df.dtypes ) )

    def test_float_case ( self ):
        # Example 1 - 9x5 floats
        df = pd.DataFrame.example( 9, 5, float )
        self.assertEqual( len( df ), 9 )
        self.assertEqual( len( df.columns ), 5 )
        self.assertTrue( all( dt == np.float64 for dt in df.dtypes ) )
        # Example 2 - 30x12 floats
        df = pd.DataFrame.example( 30, 12, float )
        self.assertEqual( len( df ), 30 )
        self.assertEqual( len( df.columns ), 12 )
        self.assertTrue( all( dt == np.float64 for dt in df.dtypes ) )
        # Example 3 - should work with default #rows/cols
        df = pd.DataFrame.example( type=float )
        self.assertGreater( len( df ), 0 )
        self.assertGreater( len( df.columns ), 0 )
        self.assertTrue( all( dt == np.float64 for dt in df.dtypes ) )

    def test_employee_case ( self ):
        # Example 1 - default
        df = pd.DataFrame.example()
        self.assertGreater( len( df ), 0 )
        self.assertEqual( len( df.columns ), 6 )
        self.assertTrue( 'LastName' in df.columns )
        self.assertTrue( df.dtypes['LastName'] == np.object0 )
        self.assertTrue( 'FirstName' in df.columns )
        self.assertTrue( df.dtypes['FirstName'] == np.object0 )
        self.assertTrue( 'ID' in df.columns )
        self.assertTrue( df.dtypes['ID'] == np.object0 )
        self.assertTrue( 'Department' in df.columns )
        self.assertTrue( df.dtypes['Department'] == np.object0 )
        self.assertTrue( 'Salary' in df.columns )
        self.assertTrue( df.dtypes['Salary'] == np.float64 )
        self.assertTrue( 'YearsAtCompany' in df.columns )
        self.assertTrue( df.dtypes['YearsAtCompany'] == np.int64 )
        # Example 2 - default type, fewer rows
        df = pd.DataFrame.example( 3 )
        self.assertEqual( len( df ), 3 )
        self.assertEqual( len( df.columns ), 6 )
        self.assertTrue( 'LastName' in df.columns )
        self.assertTrue( df.dtypes['LastName'] == np.object0 )
        self.assertTrue( 'FirstName' in df.columns )
        self.assertTrue( df.dtypes['FirstName'] == np.object0 )
        self.assertTrue( 'ID' in df.columns )
        self.assertTrue( df.dtypes['ID'] == np.object0 )
        self.assertTrue( 'Department' in df.columns )
        self.assertTrue( df.dtypes['Department'] == np.object0 )
        self.assertTrue( 'Salary' in df.columns )
        self.assertTrue( df.dtypes['Salary'] == np.float64 )
        self.assertTrue( 'YearsAtCompany' in df.columns )
        self.assertTrue( df.dtypes['YearsAtCompany'] == np.int64 )
        # Example 3 - explicit #rows, #cols, and type
        df = pd.DataFrame.example( 10, 9, 'Employee' )
        self.assertEqual( len( df ), 10 )
        self.assertEqual( len( df.columns ), 9 )
        self.assertTrue( 'LastName' in df.columns )
        self.assertTrue( df.dtypes['LastName'] == np.object0 )
        self.assertTrue( 'FirstName' in df.columns )
        self.assertTrue( df.dtypes['FirstName'] == np.object0 )
        self.assertTrue( 'ID' in df.columns )
        self.assertTrue( df.dtypes['ID'] == np.object0 )
        self.assertTrue( 'Department' in df.columns )
        self.assertTrue( df.dtypes['Department'] == np.object0 )
        self.assertTrue( 'Salary' in df.columns )
        self.assertTrue( df.dtypes['Salary'] == np.float64 )
        self.assertTrue( 'YearsAtCompany' in df.columns )
        self.assertTrue( df.dtypes['YearsAtCompany'] == np.int64 )
        self.assertTrue( all( dt == np.float64
            for dt in df.dtypes[df.columns[6:]] ) )

if __name__ == '__main__':
    unittest.main()
