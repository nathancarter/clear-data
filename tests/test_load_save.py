
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
