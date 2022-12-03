
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
        df = pd.example()
        # Save it and ensure that it got saved
        filename = temp_filename( 'csv' )
        self.assertFalse( file_exists( filename ) )
        df.save( filename )
        self.assertTrue( file_exists( filename ) )
        # Reload it and ensure that it's similar
        # (though it won't be the same because CSV is limited)
        similar_df = pd.load( filename )
        self.assertEqual( df.index.tolist(), similar_df.index.tolist() )
        self.assertEqual( df.columns.tolist(), similar_df.columns.tolist() )
        self.assertEqual( df[df.columns[0]].tolist(),
                          similar_df[similar_df.columns[0]].tolist() )
        self.assertEqual( df[df.columns[1]].tolist(),
                          similar_df[similar_df.columns[1]].tolist() )
        # The above tests just compare the First/Last name columns, because they
        # are text and will import/export reliably as text.

    def test_read_write_tsv ( self ):
        df = pd.example()
        # Save it and ensure that it got saved
        filename = temp_filename( 'tsv' )
        self.assertFalse( file_exists( filename ) )
        df.save( filename )
        self.assertTrue( file_exists( filename ) )
        # Reload it and ensure that it's similar
        # (though it won't be the same because CSV is limited)
        similar_df = pd.load( filename )
        self.assertEqual( df.index.tolist(), similar_df.index.tolist() )
        self.assertEqual( df.columns.tolist(), similar_df.columns.tolist() )
        self.assertEqual( df[df.columns[0]].tolist(),
                          similar_df[similar_df.columns[0]].tolist() )
        self.assertEqual( df[df.columns[1]].tolist(),
                          similar_df[similar_df.columns[1]].tolist() )
        # The above tests just compare the First/Last name columns, because they
        # are text and will import/export reliably as text.

    def test_read_write_xls ( self ):
        df = pd.example()
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
        df = pd.example()
        # Save it and ensure that it got saved
        filename = temp_filename( 'xlsx' )
        self.assertFalse( file_exists( filename ) )
        df.save( filename )
        self.assertTrue( file_exists( filename ) )
        # Reload it and ensure that it's similar
        # (though it won't be the same because CSV is limited)
        similar_df = pd.load( filename )
        self.assertEqual( df.index.tolist(), similar_df.index.tolist() )
        self.assertEqual( df.columns.tolist(), similar_df.columns.tolist() )
        self.assertEqual( df[df.columns[0]].tolist(),
                          similar_df[similar_df.columns[0]].tolist() )
        self.assertEqual( df[df.columns[1]].tolist(),
                          similar_df[similar_df.columns[1]].tolist() )
        # The above tests just compare the First/Last name columns, because they
        # are text and will import/export reliably as text.

    def test_read_write_parquet ( self ):
        df = pd.example()
        # Save it and ensure that it got saved
        filename = temp_filename( 'parquet' )
        self.assertFalse( file_exists( filename ) )
        df.save( filename )
        self.assertTrue( file_exists( filename ) )
        # Reload it and ensure that it's the same (because parquet is robust)
        reloaded_df = pd.load( filename )
        self.assertEqual( df.index.tolist(), reloaded_df.index.tolist() )
        self.assertEqual( df.columns.tolist(), reloaded_df.columns.tolist() )
        for column_name in df.columns:
            self.assertEqual( df.dtypes[column_name],
                              reloaded_df.dtypes[column_name] )
            self.assertEqual( df[column_name].tolist(),
                              reloaded_df[column_name].tolist() )

    def test_read_write_pickle ( self ):
        df = pd.example()
        # Save it and ensure that it got saved
        filename = temp_filename( 'pickle' )
        self.assertFalse( file_exists( filename ) )
        df.save( filename )
        self.assertTrue( file_exists( filename ) )
        # Reload it and ensure that it's the same (because pickle is robust)
        reloaded_df = pd.load( filename )
        self.assertEqual( df.index.tolist(), reloaded_df.index.tolist() )
        self.assertEqual( df.columns.tolist(), reloaded_df.columns.tolist() )
        for column_name in df.columns:
            self.assertEqual( df.dtypes[column_name],
                              reloaded_df.dtypes[column_name] )
            self.assertEqual( df[column_name].tolist(),
                              reloaded_df[column_name].tolist() )
        # Repeat above test with alternate file extension
        filename = temp_filename( 'pkl' )
        self.assertFalse( file_exists( filename ) )
        df.save( filename )
        self.assertTrue( file_exists( filename ) )
        reloaded_df = pd.load( filename )
        self.assertEqual( df.index.tolist(), reloaded_df.index.tolist() )
        self.assertEqual( df.columns.tolist(), reloaded_df.columns.tolist() )
        for column_name in df.columns:
            self.assertEqual( df.dtypes[column_name],
                              reloaded_df.dtypes[column_name] )
            self.assertEqual( df[column_name].tolist(),
                              reloaded_df[column_name].tolist() )

    def test_read_write_hdf ( self ):
        df = pd.example()
        # Save it and ensure that it got saved
        filename = temp_filename( 'hdf' )
        self.assertFalse( file_exists( filename ) )
        df.save( filename )
        self.assertTrue( file_exists( filename ) )
        # Reload it and ensure that it's the same (because HDF is robust)
        reloaded_df = pd.load( filename )
        self.assertEqual( df.index.tolist(), reloaded_df.index.tolist() )
        self.assertEqual( df.columns.tolist(), reloaded_df.columns.tolist() )
        for column_name in df.columns:
            self.assertEqual( df.dtypes[column_name],
                              reloaded_df.dtypes[column_name] )
            self.assertEqual( df[column_name].tolist(),
                              reloaded_df[column_name].tolist() )

    def test_read_write_hdf_multiple ( self ):
        df = pd.example()
        int_df = pd.example( 10, 10, int )
        # Repeat above test, this time using a specific file key...
        # ...two, in fact, to be sure we can put more than 1 thing in the file.
        filename = temp_filename( 'hdf' )
        self.assertFalse( file_exists( filename ) )
        df.save( filename, key='employees' )
        int_df.save( filename, key='integers' )
        self.assertTrue( file_exists( filename ) )
        reloaded_df = pd.load( filename, key='employees' )
        self.assertEqual( df.index.tolist(), reloaded_df.index.tolist() )
        self.assertEqual( df.columns.tolist(), reloaded_df.columns.tolist() )
        for column_name in df.columns:
            self.assertEqual( df.dtypes[column_name],
                              reloaded_df.dtypes[column_name] )
            self.assertEqual( df[column_name].tolist(),
                              reloaded_df[column_name].tolist() )
        reloaded_int_df = pd.load( filename, key='integers' )
        self.assertEqual( int_df.index.tolist(), reloaded_int_df.index.tolist() )
        self.assertEqual( int_df.columns.tolist(), reloaded_int_df.columns.tolist() )
        for column_name in int_df.columns:
            self.assertEqual( int_df.dtypes[column_name],
                              reloaded_int_df.dtypes[column_name] )
            self.assertEqual( int_df[column_name].tolist(),
                              reloaded_int_df[column_name].tolist() )

    def test_read_write_dta ( self ):
        df = pd.example()
        # Save it and ensure that it got saved
        filename = temp_filename( 'dta' )
        self.assertFalse( file_exists( filename ) )
        df.save( filename )
        self.assertTrue( file_exists( filename ) )
        # Reload it and ensure that it's the same (because STATA dta is decent)
        similar_df = pd.load( filename )
        self.assertEqual( df.index.tolist(), similar_df.index.tolist() )
        self.assertEqual( df.columns.tolist(), similar_df.columns.tolist() )
        for column_name in df.columns:
            similar_int_types = [ np.int32, np.int64 ]
            self.assertTrue(
                df.dtypes[column_name] == similar_df.dtypes[column_name] or
                (
                    df.dtypes[column_name] in similar_int_types and
                    similar_df.dtypes[column_name] in similar_int_types
                )
            )
            self.assertEqual( df[column_name].tolist(),
                              similar_df[column_name].tolist() )

    def test_read_write_orc ( self ):
        df = pd.example()
        # Save it and ensure that it got saved
        filename = temp_filename( 'orc' )
        self.assertFalse( file_exists( filename ) )
        df.save( filename )
        self.assertTrue( file_exists( filename ) )
        # Reload it and ensure that it's the same (because ORC is robust)
        reloaded_df = pd.load( filename )
        self.assertEqual( df.index.tolist(), reloaded_df.index.tolist() )
        self.assertEqual( df.columns.tolist(), reloaded_df.columns.tolist() )
        for column_name in df.columns:
            self.assertEqual( df.dtypes[column_name],
                              reloaded_df.dtypes[column_name] )
            self.assertEqual( df[column_name].tolist(),
                              reloaded_df[column_name].tolist() )

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
