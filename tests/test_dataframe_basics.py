
import sys, os
this_dir = os.path.dirname( os.path.realpath( __file__ ) )
sys.path.append( os.path.join( this_dir, '..', 'src' ) )
import clear_data

import unittest
import pandas as pd

class TestDataFrameBasics( unittest.TestCase ):

    def test_is_a_function ( self ):
        df = pd.DataFrame( {
            "unique_inputs"   : [ 1, 2, 3, 4 ],
            "repeat_inputs"   : [ 1, 2, 1, 3 ],
            "unique_outputs"  : [ 'a', 'b', 'c', 'd' ],
            "repeat_outputs1" : [ 'x', 'x', 'y', 'y' ],
            "repeat_outputs2" : [ 'x', 'y', 'x', 'y' ]
        } )
        # with unique inputs it's always a function
        self.assertTrue(
            df.is_a_function( 'unique_inputs', 'unique_outputs' ) )
        self.assertTrue(
            df.is_a_function( 'unique_inputs', 'repeat_outputs1' ) )
        self.assertTrue(
            df.is_a_function( 'unique_inputs', 'repeat_outputs2' ) )
        # with repeat inputs it may or may not be, depending on the outputs
        self.assertFalse(
            df.is_a_function( 'repeat_inputs', 'unique_outputs' ) )
        self.assertFalse(
            df.is_a_function( 'repeat_inputs', 'repeat_outputs1' ) )
        self.assertTrue(
            df.is_a_function( 'repeat_inputs', 'repeat_outputs2' ) )
        # do same 6 tests but using columns in place of their names
        # ...sometimes
        self.assertTrue(
        	df.is_a_function( df.unique_inputs, 'unique_outputs' ) )
        self.assertTrue(
            df.is_a_function( df.unique_inputs, df.repeat_outputs1 ) )
        self.assertTrue(
            df.is_a_function( 'unique_inputs', df.repeat_outputs2 ) )
        self.assertFalse(
            df.is_a_function( df.repeat_inputs, 'unique_outputs' ) )
        self.assertFalse(
            df.is_a_function( df.repeat_inputs, df.repeat_outputs1 ) )
        self.assertTrue(
            df.is_a_function( 'repeat_inputs', df.repeat_outputs2 ) )
        # the index can also be used as a column
        self.assertTrue( df.is_a_function( df.index, 'unique_outputs' ) )
        self.assertFalse( df.is_a_function( df.repeat_inputs, df.index ) )

if __name__ == '__main__':
    unittest.main()
