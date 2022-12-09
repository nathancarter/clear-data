
import sys, os
this_dir = os.path.dirname( os.path.realpath( __file__ ) )
sys.path.append( os.path.join( this_dir, '..', 'src' ) )
import clear_data

import unittest
import warnings # for testing emission of warnings in some tests
import pandas as pd

class TestSubsetting( unittest.TestCase ):

    def test_subset_using_bool_series ( self ):
        df = pd.DataFrame( {
            'divisor'  : [ 1, 1, 2, 1, 3, 1, 2, 4, 1, 5 ],
            'dividend' : [ 1, 2, 2, 3, 3, 4, 4, 4, 5, 5 ]
        } )
        # select just the even dividends
        subset = df.rows_satisfying( df.dividend % 2 == 0 )
        self.assertTrue( subset.divisor.to_list() == [ 1, 2, 1, 2, 4 ] )
        self.assertTrue( subset.dividend.to_list() == [ 2, 2, 4, 4, 4 ] )
        # ensure what was selected is a copy, not the original
        with warnings.catch_warnings( record=True ) as ws:
            subset.dividend = 7
            self.assertEqual( subset.dividend.to_list(), [ 7, 7, 7, 7, 7 ] )
            self.assertEqual( len( ws ), 0 )
        # rather than test each synonym, let's just ensure they're all the
        # same function!
        self.assertEqual( df.rows_satisfying, df.rows_such_that )
        self.assertEqual( df.rows_satisfying, df.rows_in_which )
        self.assertEqual( df.rows_satisfying, df.rows_where )
        self.assertEqual( df.rows_satisfying, df.select_rows )
        self.assertEqual( df.rows_satisfying, df.rows_select )
        self.assertEqual( df.rows_satisfying, df.rows_subset )
    
    def test_subset_using_predicate ( self ):
        df = pd.DataFrame( {
            'divisor'  : [ 1, 1, 2, 1, 3, 1, 2, 4, 1, 5 ],
            'dividend' : [ 1, 2, 2, 3, 3, 4, 4, 4, 5, 5 ]
        } )
        # select just the even dividends
        subset = df.rows_satisfying( lambda row: row.dividend % 2 == 0 )
        self.assertTrue( subset.divisor.to_list() == [ 1, 2, 1, 2, 4 ] )
        self.assertTrue( subset.dividend.to_list() == [ 2, 2, 4, 4, 4 ] )
        # ensure what was selected is a copy, not the original
        with warnings.catch_warnings( record=True ) as ws:
            subset.dividend = 7
            self.assertEqual( subset.dividend.to_list(), [ 7, 7, 7, 7, 7 ] )
            self.assertEqual( len( ws ), 0 )
	
    def test_efficient_subset_using_bool_series ( self ):
        df = pd.DataFrame( {
            'divisor'  : [ 1, 1, 2, 1, 3, 1, 2, 4, 1, 5 ],
            'dividend' : [ 1, 2, 2, 3, 3, 4, 4, 4, 5, 5 ]
        } )
        # select just the even dividends
        subset = df.rows_satisfying( df.dividend % 2 == 0, efficient=True )
        self.assertTrue( subset.divisor.to_list() == [ 1, 2, 1, 2, 4 ] )
        self.assertTrue( subset.dividend.to_list() == [ 2, 2, 4, 4, 4 ] )
        # ensure what was selected is a slice, not a copy
        with warnings.catch_warnings( record=True ) as ws:
            subset.dividend = 7
            self.assertEqual( subset.dividend.to_list(), [ 7, 7, 7, 7, 7 ] )
            self.assertEqual( len( ws ), 1 )
            self.assertTrue( 'slice' in str( ws[-1].message ) )
    
    def test_efficient_subset_using_predicate ( self ):
        df = pd.DataFrame( {
            'divisor'  : [ 1, 1, 2, 1, 3, 1, 2, 4, 1, 5 ],
            'dividend' : [ 1, 2, 2, 3, 3, 4, 4, 4, 5, 5 ]
        } )
        # select just the even dividends
        subset = df.rows_satisfying(
            lambda row: row.dividend % 2 == 0, efficient=True )
        self.assertTrue( subset.divisor.to_list() == [ 1, 2, 1, 2, 4 ] )
        self.assertTrue( subset.dividend.to_list() == [ 2, 2, 4, 4, 4 ] )
        # ensure what was selected is a slice, not a copy
        with warnings.catch_warnings( record=True ) as ws:
            subset.dividend = 7
            self.assertEqual( subset.dividend.to_list(), [ 7, 7, 7, 7, 7 ] )
            self.assertEqual( len( ws ), 1 )
            self.assertTrue( 'slice' in str( ws[-1].message ) )
	
    def test_subset_of_index_using_bool_series ( self ):
        # Same as first test, but now on just indices
        df = pd.DataFrame( {
            'divisor'  : [ 1, 1, 2, 1, 3, 1, 2, 4, 1, 5 ],
            'dividend' : [ 1, 2, 2, 3, 3, 4, 4, 4, 5, 5 ]
        } )
        # select just the even dividends
        indices = df.indices_satisfying( df.dividend % 2 == 0 )
        self.assertTrue( indices.to_list() == [ 1, 2, 5, 6, 7 ] )
        # rather than test each synonym, let's just ensure they're all the
        # same function!
        self.assertEqual( df.indices_satisfying, df.indices_such_that )
        self.assertEqual( df.indices_satisfying, df.indices_in_which )
        self.assertEqual( df.indices_satisfying, df.indices_where )
    
    def test_subset_of_index_using_predicate ( self ):
        # Same as second test, but now on just indices
        df = pd.DataFrame( {
            'divisor'  : [ 1, 1, 2, 1, 3, 1, 2, 4, 1, 5 ],
            'dividend' : [ 1, 2, 2, 3, 3, 4, 4, 4, 5, 5 ]
        } )
        # select just the even dividends
        indices = df.indices_satisfying( lambda row: row.dividend % 2 == 0 )
        self.assertTrue( indices.to_list() == [ 1, 2, 5, 6, 7 ] )
	
if __name__ == '__main__':
    unittest.main()
