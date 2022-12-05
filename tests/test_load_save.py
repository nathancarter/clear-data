
import sys, os
this_dir = os.path.dirname( os.path.realpath( __file__ ) )
sys.path.append( os.path.join( this_dir, '..', 'src' ) )
import clear_data

import unittest
import numpy as np
import pandas as pd
import tempfile


#
# Utility functions for the tests below:
#

# First, does a file exist?
def file_exists ( filename ):
    return os.path.isfile( filename )
# Second, delete an existing file
def delete_file ( filename ):
    os.remove( filename )
# Third, get me a location for a temp file
def temp_filename ( extension ):
    return os.path.join( this_dir, f'temp_save_file.{extension}' )
# Finally, what are all the existing temp files?
def existing_temp_files ():
    return [
        os.path.join( this_dir, filename )
        for filename in os.listdir( this_dir )
        if filename.startswith( 'temp_save_file.' )
    ]



#
# And now the actual unit tests:
#

class TestLoadSave( unittest.TestCase ):

    #
    # Test dataframe for loading/saving, and simple comparison utilities
    #
    test_df = pd.example() # employees, 20 rows, 6 cols

    def assert_same ( self, other_df, compare_to = None ):
        if compare_to is None:
            compare_to = TestLoadSave.test_df.copy()
        # is other_df exactly like test_df()?
        self.assertEqual( compare_to.index.tolist(), other_df.index.tolist() )
        self.assertEqual( compare_to.columns.tolist(), other_df.columns.tolist() )
        for column_name in compare_to.columns:
            self.assertEqual( compare_to.dtypes[column_name],
                              other_df.dtypes[column_name] )
            self.assertEqual( compare_to[column_name].tolist(),
                              other_df[column_name].tolist() )

    def assert_same_except_int_dtypes ( self, other_df, compare_to = None ):
        if compare_to is None:
            compare_to = TestLoadSave.test_df.copy()
        # is other_df the same as test_df() except maybe for int32 vs. int64?
        self.assertEqual( compare_to.index.tolist(), other_df.index.tolist() )
        self.assertEqual( compare_to.columns.tolist(), other_df.columns.tolist() )
        for column_name in compare_to.columns:
            similar_int_types = [ np.int32, np.int64 ]
            self.assertTrue(
                compare_to.dtypes[column_name] == other_df.dtypes[column_name] or
                (
                    compare_to.dtypes[column_name] in similar_int_types and
                    other_df.dtypes[column_name] in similar_int_types
                )
            )
            self.assertEqual( compare_to[column_name].tolist(),
                              other_df[column_name].tolist() )

    def assert_same_except_dtypes ( self, other_df, compare_to = None ):
        if compare_to is None:
            compare_to = TestLoadSave.test_df.copy()
        # is other_df the same as test_df() except maybe for column dtypes?
        # (e.g., a column of string IDs got converted to integers)
        self.assertEqual( compare_to.index.tolist(), other_df.index.tolist() )
        self.assertEqual( compare_to.columns.tolist(), other_df.columns.tolist() )
        for column_name in compare_to.columns:
            self.assertEqual(
                [ str(x) for x in compare_to[column_name] ],
                [ str(x) for x in other_df[column_name] ]
            )

    def setUp ( self ):
        # In case any test created any files in the past, we clear them out
        # before each new test, so that every test can assume it's running in
        # a fresh environment.
        for filename in existing_temp_files():
            delete_file( filename )
    
    def tearDown ( self ):
        # Also delete all temp files here, for when exiting the final test.
        self.setUp()

    def test_read_write_csv ( self ):
        df = TestLoadSave.test_df.copy()
        # Save it and ensure that it got saved
        filename = temp_filename( 'csv' )
        self.assertFalse( file_exists( filename ) )
        df.save( filename )
        self.assertTrue( file_exists( filename ) )
        # Reload it and ensure that it's similar
        # (though it won't be the same because CSV is limited)
        self.assert_same_except_dtypes( pd.load( filename ) )

    def test_read_write_tsv ( self ):
        df = TestLoadSave.test_df.copy()
        # Save it and ensure that it got saved
        filename = temp_filename( 'tsv' )
        self.assertFalse( file_exists( filename ) )
        df.save( filename )
        self.assertTrue( file_exists( filename ) )
        # Reload it and ensure that it's similar
        # (though it won't be the same because TSV is limited)
        self.assert_same_except_dtypes( pd.load( filename ) )

    def test_read_write_xls ( self ):
        df = TestLoadSave.test_df.copy()
        # Save it and ensure that it got saved
        filename = temp_filename( 'xls' )
        self.assertFalse( file_exists( filename ) )
        # Can't save these without a deprecated module that's not in this repo
        with self.assertRaises( ImportError ):
            df.save( filename )
        # Can't load for the same reason (regardless of whether the file exists)
        with self.assertRaises( ImportError ):
            pd.load( filename )

    def test_read_write_xlsx ( self ):
        df = TestLoadSave.test_df.copy()
        # Save it and ensure that it got saved
        filename = temp_filename( 'xlsx' )
        self.assertFalse( file_exists( filename ) )
        df.save( filename )
        self.assertTrue( file_exists( filename ) )
        # Reload it and ensure that it's similar
        # (though it won't be the same because XLSX is limited)
        self.assert_same_except_dtypes( pd.load( filename ) )

    def test_read_write_parquet ( self ):
        df = TestLoadSave.test_df.copy()
        # Save it and ensure that it got saved
        filename = temp_filename( 'parquet' )
        self.assertFalse( file_exists( filename ) )
        df.save( filename )
        self.assertTrue( file_exists( filename ) )
        # Reload it and ensure that it's the same (because parquet is robust)
        self.assert_same( pd.load( filename ) )

    def test_read_write_pickle ( self ):
        df = TestLoadSave.test_df.copy()
        # Save it and ensure that it got saved
        filename = temp_filename( 'pickle' )
        self.assertFalse( file_exists( filename ) )
        df.save( filename )
        self.assertTrue( file_exists( filename ) )
        # Reload it and ensure that it's the same (because pickle is robust)
        self.assert_same( pd.load( filename ) )
        # Repeat above test with alternate file extension
        filename = temp_filename( 'pkl' )
        self.assertFalse( file_exists( filename ) )
        df.save( filename )
        self.assertTrue( file_exists( filename ) )
        self.assert_same( pd.load( filename ) )

    def test_read_write_hdf ( self ):
        df = TestLoadSave.test_df.copy()
        # Save it and ensure that it got saved
        filename = temp_filename( 'hdf' )
        self.assertFalse( file_exists( filename ) )
        df.save( filename )
        self.assertTrue( file_exists( filename ) )
        # Reload it and ensure that it's the same (because HDF is robust)
        self.assert_same( pd.load( filename ) )

    def test_read_write_hdf_multiple ( self ):
        df = TestLoadSave.test_df.copy()
        int_df = pd.example( 10, 10, int )
        # Repeat above test, this time using a specific file key...
        # ...two, in fact, to be sure we can put more than 1 thing in the file.
        filename = temp_filename( 'hdf' )
        self.assertFalse( file_exists( filename ) )
        df.save( filename, key='employees' )
        int_df.save( filename, key='integers' )
        self.assertTrue( file_exists( filename ) )
        self.assert_same( pd.load( filename, key='employees' ) )
        self.assert_same( pd.load( filename, key='integers' ), int_df )

    def test_read_write_dta ( self ):
        df = TestLoadSave.test_df.copy()
        # Save it and ensure that it got saved
        filename = temp_filename( 'dta' )
        self.assertFalse( file_exists( filename ) )
        df.save( filename )
        self.assertTrue( file_exists( filename ) )
        # Reload it and ensure that it's the same (because STATA dta is decent)
        self.assert_same_except_int_dtypes( pd.load( filename ) )

    def test_read_write_orc ( self ):
        df = TestLoadSave.test_df.copy()
        # Save it and ensure that it got saved
        filename = temp_filename( 'orc' )
        self.assertFalse( file_exists( filename ) )
        df.save( filename )
        self.assertTrue( file_exists( filename ) )
        # Reload it and ensure that it's the same (because ORC is robust)
        self.assert_same( pd.load( filename ) )

    def test_read_write_json ( self ):
        df = TestLoadSave.test_df.copy()
        # Save it and ensure that it got saved
        filename = temp_filename( 'json' )
        self.assertFalse( file_exists( filename ) )
        df.save( filename )
        self.assertTrue( file_exists( filename ) )
        # Reload it and ensure that it's similar
        # (though it won't be the same because JSON reloading assumes some types)
        self.assert_same_except_dtypes( pd.load( filename ) )
        # Repeat above test with each different way to store as JSON
        for orient in ['columns','index','values','records','split','table']:
            delete_file( filename )
            self.assertFalse( file_exists( filename ) )
            df.save( filename, orient=orient )
            self.assertTrue( file_exists( filename ) )
            reloaded_df = pd.load( filename )
            # One exception: If we stored only the values (no column names)
            # then we can't expect those to be reloaded.
            if orient == 'values':
                reloaded_df.columns = df.columns
            self.assert_same_except_dtypes( reloaded_df )
    
    def test_read_write_html ( self ):
        df = TestLoadSave.test_df.copy()
        # Save it and ensure that it got saved
        filename = temp_filename( 'html' )
        self.assertFalse( file_exists( filename ) )
        df.save( filename )
        self.assertTrue( file_exists( filename ) )
        # Reload it and ensure that it's the same (because ORC is robust)
        self.assert_same_except_dtypes( pd.load( filename ) )

    def test_unsupported_extensions ( self ):
        # Loading
        with self.assertRaisesRegex( ValueError, 'Unsupported.*extension' ):
            pd.load( 'anything.foobar' )
        with self.assertRaisesRegex( ValueError, 'Unsupported.*extension' ):
            pd.load( 'anything.xml' )
        # Saving
        df = pd.example()
        with self.assertRaisesRegex( ValueError, 'Unsupported.*extension' ):
            df.save( 'anything.foobar' )
        with self.assertRaisesRegex( ValueError, 'Unsupported.*extension' ):
            df.save( 'anything.xml' )

if __name__ == '__main__':
    unittest.main()
