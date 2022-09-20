
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

    def test_to_function ( self ):
        # recreate same I/O sets from the previous test function
        df = pd.DataFrame( {
            "unique_inputs"   : [ 1, 2, 3, 4 ],
            "repeat_inputs"   : [ 1, 2, 1, 3 ],
            "unique_outputs"  : [ 'a', 'b', 'c', 'd' ],
            "repeat_outputs1" : [ 'x', 'x', 'y', 'y' ],
            "repeat_outputs2" : [ 'x', 'y', 'x', 'y' ]
        } )
        # create all the functions that are valid to create (see previous test)
        f1 = df.to_function( 'unique_inputs', 'unique_outputs' )
        f2 = df.to_function( 'unique_inputs', 'repeat_outputs1' )
        f3 = df.to_function( 'unique_inputs', 'repeat_outputs2' )
        f4 = df.to_function( 'repeat_inputs', 'repeat_outputs2' )
        f5 = df.to_function( df.index, 'unique_outputs' )
        f6 = df.to_function( df.index, 'repeat_outputs1' )
        f7 = df.to_function( df.index, 'repeat_outputs2' )
        # test three inputs and outputs for each
        self.assertEqual( f1( 1 ), 'a' )
        self.assertEqual( f1( 3 ), 'c' )
        self.assertEqual( f1( '1' ), None )
        self.assertEqual( f2( 2 ), 'x' )
        self.assertEqual( f2( 4 ), 'y' )
        self.assertEqual( f2( 0 ), None )
        self.assertEqual( f3( 1 ), 'x' )
        self.assertEqual( f3( 2 ), 'y' )
        self.assertEqual( f3( -1 ), None )
        self.assertEqual( f4( 1 ), 'x' )
        self.assertEqual( f4( 3 ), 'y' )
        self.assertEqual( f4( 4 ), None )
        self.assertEqual( f5( 1 ), 'b' )
        self.assertEqual( f5( 'a' ), None )
        self.assertEqual( f5( 'd' ), None )
        self.assertEqual( f6( -1 ), None )
        self.assertEqual( f6( 1 ), 'x' )
        self.assertEqual( f6( 'z' ), None )
        self.assertEqual( f7( 0 ), 'x' )
        self.assertEqual( f7( 3 ), 'y' )
        self.assertEqual( f7( 4 ), None )

if __name__ == '__main__':
    unittest.main()
