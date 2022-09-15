
import sys, os
this_dir = os.path.dirname( os.path.realpath( __file__ ) )
sys.path.append( os.path.join( this_dir, '..', 'src' ) )
import clear_data

import unittest
import pandas as pd

class TestSeriesBasics( unittest.TestCase ):

	def test_has_duplicates ( self ):
		no_dups = pd.Series( [ 1, 2, 3, 4 ] )
		self.assertTrue( no_dups.has_no_duplicates() )
		self.assertFalse( no_dups.has_duplicates() )
		one_dup = pd.Series( [ 1, 2, 1, 4 ] )
		self.assertTrue( one_dup.has_duplicates() )
		self.assertFalse( one_dup.has_no_duplicates() )

if __name__ == '__main__':
	unittest.main()
