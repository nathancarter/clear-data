
import sys, os
this_dir = os.path.dirname( os.path.realpath( __file__ ) )
sys.path.append( os.path.join( this_dir, '..', 'src' ) )
import clear_data

import unittest
import pandas as pd

class TestRelations( unittest.TestCase ):

    def test_binary_relation_using_series ( self ):
        # build series of all "a divides b" pairs for a,b from 1 to 9
        L = [ ]
        R = [ ]
        for b in range(1,10):
            for a in range(1,b+1):
                if b % a == 0:
                    L.append( a )
                    R.append( b )
        L = pd.Series( L )
        R = pd.Series( R )
        self.assertEqual( len(L), len(R) )
        # test to see if to_relation() builds the correct binary relation
        divides = L.to_relation( R )
        self.assertTrue( divides( 3, 6 ) )
        self.assertFalse( divides( 3, 5 ) )
        self.assertFalse( divides( 30, 60 ) ) # true in math, but too big here
        self.assertTrue( divides( 1, 5 ) )
        self.assertFalse( divides( 5, 1 ) )
        self.assertFalse( divides( '1', '5' ) )
        # repeat test with synonym for to_relation()
        divides = L.to_predicate( R )
        self.assertTrue( divides( 3, 6 ) )
        self.assertFalse( divides( 3, 5 ) )
        self.assertFalse( divides( 30, 60 ) ) # true in math, but too big here
        self.assertTrue( divides( 1, 5 ) )
        self.assertFalse( divides( 5, 1 ) )
        self.assertFalse( divides( '1', '5' ) )
        # repeat test with synonym for to_relation()
        divides = L.to_relation_with( R )
        self.assertTrue( divides( 3, 6 ) )
        self.assertFalse( divides( 3, 5 ) )
        self.assertFalse( divides( 30, 60 ) ) # true in math, but too big here
        self.assertTrue( divides( 1, 5 ) )
        self.assertFalse( divides( 5, 1 ) )
        self.assertFalse( divides( '1', '5' ) )
        # repeat test with synonym for to_relation()
        divides = L.to_predicate_with( R )
        self.assertTrue( divides( 3, 6 ) )
        self.assertFalse( divides( 3, 5 ) )
        self.assertFalse( divides( 30, 60 ) ) # true in math, but too big here
        self.assertTrue( divides( 1, 5 ) )
        self.assertFalse( divides( 5, 1 ) )
        self.assertFalse( divides( '1', '5' ) )
        # repeat test with synonym for to_relation()
        divides = L.get_relation( R )
        self.assertTrue( divides( 3, 6 ) )
        self.assertFalse( divides( 3, 5 ) )
        self.assertFalse( divides( 30, 60 ) ) # true in math, but too big here
        self.assertTrue( divides( 1, 5 ) )
        self.assertFalse( divides( 5, 1 ) )
        self.assertFalse( divides( '1', '5' ) )
        # repeat test with synonym for to_relation()
        divides = L.get_predicate( R )
        self.assertTrue( divides( 3, 6 ) )
        self.assertFalse( divides( 3, 5 ) )
        self.assertFalse( divides( 30, 60 ) ) # true in math, but too big here
        self.assertTrue( divides( 1, 5 ) )
        self.assertFalse( divides( 5, 1 ) )
        self.assertFalse( divides( '1', '5' ) )
        # repeat test with synonym for to_relation()
        divides = L.get_relation_with( R )
        self.assertTrue( divides( 3, 6 ) )
        self.assertFalse( divides( 3, 5 ) )
        self.assertFalse( divides( 30, 60 ) ) # true in math, but too big here
        self.assertTrue( divides( 1, 5 ) )
        self.assertFalse( divides( 5, 1 ) )
        self.assertFalse( divides( '1', '5' ) )
        # repeat test with synonym for to_relation()
        divides = L.get_predicate_with( R )
        self.assertTrue( divides( 3, 6 ) )
        self.assertFalse( divides( 3, 5 ) )
        self.assertFalse( divides( 30, 60 ) ) # true in math, but too big here
        self.assertTrue( divides( 1, 5 ) )
        self.assertFalse( divides( 5, 1 ) )
        self.assertFalse( divides( '1', '5' ) )
    
    def test_unary_predicate_using_series ( self ):
        # create a simple set for membership testing
        S = pd.Series( [ 'one', 'two', 'three', 'four', 'five',
                         'six', 'seven', 'eight', 'nine', 'ten' ] )
        # ensure that to_predicate() creates a function for membership testing
        is_a_number_word = S.to_predicate()
        self.assertTrue( is_a_number_word( 'one' ) )
        self.assertTrue( is_a_number_word( 'four' ) )
        self.assertTrue( is_a_number_word( 'eight' ) )
        self.assertFalse( is_a_number_word( 'won' ) )
        self.assertFalse( is_a_number_word( 'for' ) )
        self.assertFalse( is_a_number_word( 'ate' ) )
	
    def test_ternary_predicate_using_series ( self ):
        # create a ternary relation on [1,10]x[1,10] that means x*y=z
        tuples = [ (x,y,x*y) for x in range(1,11) for y in range(1,11) ]
        X = pd.Series( [ t[0] for t in tuples ] )
        Y = pd.Series( [ t[1] for t in tuples ] )
        Z = pd.Series( [ t[2] for t in tuples ] )
        equation = X.to_relation_with( Y, Z )
        # test it on some simple math facts
        self.assertTrue( equation( 3, 4, 12 ) )
        self.assertTrue( equation( 4, 3, 12 ) )
        self.assertTrue( equation( 9, 9, 81 ) )
        self.assertTrue( equation( 1, 1, 1 ) )
        self.assertFalse( equation( 1, 1, 11 ) )
        self.assertFalse( equation( 3, 7, 37 ) )
        self.assertFalse( equation( 6, 6, 6 ) )
        self.assertFalse( equation( -1, -1, 1 ) ) # true but outside domain

    def test_binary_relation_using_dataframes ( self ):
        # build series of all "a divides b" pairs for a,b from 1 to 9
        L = [ ]
        R = [ ]
        for b in range(1,10):
            for a in range(1,b+1):
                if b % a == 0:
                    L.append( a )
                    R.append( b )
        df = pd.DataFrame( { "L" : L, "R" : R } )
        # test to see if to_relation() builds the correct binary relation
        divides = df.to_relation( "L", "R" )
        self.assertTrue( divides( 3, 6 ) )
        self.assertFalse( divides( 3, 5 ) )
        self.assertFalse( divides( 30, 60 ) ) # true in math, but too big here
        self.assertTrue( divides( 1, 5 ) )
        self.assertFalse( divides( 5, 1 ) )
        self.assertFalse( divides( '1', '5' ) )
        # repeat test with synonym for to_relation()
        divides = df.to_predicate( "L", "R" )
        self.assertTrue( divides( 3, 6 ) )
        self.assertFalse( divides( 3, 5 ) )
        self.assertFalse( divides( 30, 60 ) ) # true in math, but too big here
        self.assertTrue( divides( 1, 5 ) )
        self.assertFalse( divides( 5, 1 ) )
        self.assertFalse( divides( '1', '5' ) )
        # repeat test with synonym for to_relation()
        divides = df.get_relation( "L", "R" )
        self.assertTrue( divides( 3, 6 ) )
        self.assertFalse( divides( 3, 5 ) )
        self.assertFalse( divides( 30, 60 ) ) # true in math, but too big here
        self.assertTrue( divides( 1, 5 ) )
        self.assertFalse( divides( 5, 1 ) )
        self.assertFalse( divides( '1', '5' ) )
        # repeat test with synonym for to_relation()
        divides = df.get_predicate( "L", "R" )
        self.assertTrue( divides( 3, 6 ) )
        self.assertFalse( divides( 3, 5 ) )
        self.assertFalse( divides( 30, 60 ) ) # true in math, but too big here
        self.assertTrue( divides( 1, 5 ) )
        self.assertFalse( divides( 5, 1 ) )
        self.assertFalse( divides( '1', '5' ) )
    
    def test_unary_predicate_using_dataframes ( self ):
        # create a simple dataframe for membership testing
        df = pd.DataFrame( {
            "small" : [ 'one', 'two', 'three', 'four', 'five' ],
            "large" : [ 'six', 'seven', 'eight', 'nine', 'ten' ]
        } )
        # ensure that to_predicate() creates a function for membership testing
        # first using the first column of the dataframe
        is_a_small_number_word = df.to_predicate( "small" )
        self.assertTrue( is_a_small_number_word( 'one' ) )
        self.assertTrue( is_a_small_number_word( 'four' ) )
        self.assertFalse( is_a_small_number_word( 'eight' ) )
        self.assertFalse( is_a_small_number_word( 'won' ) )
        self.assertFalse( is_a_small_number_word( 'for' ) )
        self.assertFalse( is_a_small_number_word( 'ate' ) )
        # ...then using the second column of the dataframe
        is_a_large_number_word = df.to_predicate( "large" )
        self.assertFalse( is_a_large_number_word( 'one' ) )
        self.assertFalse( is_a_large_number_word( 'four' ) )
        self.assertTrue( is_a_large_number_word( 'eight' ) )
        self.assertFalse( is_a_large_number_word( 'won' ) )
        self.assertFalse( is_a_large_number_word( 'for' ) )
        self.assertFalse( is_a_large_number_word( 'ate' ) )
	
    def test_ternary_predicate_using_dataframes ( self ):
        # create a ternary relation on [1,10]x[1,10] that means x*y=z
        tuples = [ (x,y,x*y) for x in range(1,11) for y in range(1,11) ]
        df = pd.DataFrame( tuples, columns=["x","y","z"] )
        equation = df.to_relation()
        # test it on some simple math facts
        self.assertTrue( equation( 3, 4, 12 ) )
        self.assertTrue( equation( 4, 3, 12 ) )
        self.assertTrue( equation( 9, 9, 81 ) )
        self.assertTrue( equation( 1, 1, 1 ) )
        self.assertFalse( equation( 1, 1, 11 ) )
        self.assertFalse( equation( 3, 7, 37 ) )
        self.assertFalse( equation( 6, 6, 6 ) )
        self.assertFalse( equation( -1, -1, 1 ) ) # true but outside domain
	
if __name__ == '__main__':
    unittest.main()
