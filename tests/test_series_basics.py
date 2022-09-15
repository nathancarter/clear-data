
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
	
	def test_is_a_function ( self ):
		unique_inputs = pd.Series( [ 1, 2, 3, 4 ] )
		repeat_inputs = pd.Series( [ 1, 2, 1, 3 ] )
		unique_outputs = pd.Series( [ 'a', 'b', 'c', 'd' ] )
		repeat_outputs1 = pd.Series( [ 'x', 'x', 'y', 'y' ] )
		repeat_outputs2 = pd.Series( [ 'x', 'y', 'x', 'y' ] )
		# with unique inputs it's always a function
		self.assertTrue( unique_inputs.is_a_function_to( unique_outputs ) )
		self.assertTrue( unique_inputs.is_a_function_to( repeat_outputs1 ) )
		self.assertTrue( unique_inputs.is_a_function_to( repeat_outputs2 ) )
		# with repeat inputs it may or may not be, depending on the outputs
		self.assertFalse( repeat_inputs.is_a_function_to( unique_outputs ) )
		self.assertFalse( repeat_inputs.is_a_function_to( repeat_outputs1 ) )
		self.assertTrue( repeat_inputs.is_a_function_to( repeat_outputs2 ) )
		# all outputs are functions from the default range-style index
		self.assertTrue( unique_outputs.is_a_function() )
		self.assertTrue( repeat_outputs1.is_a_function() )
		self.assertTrue( repeat_outputs2.is_a_function() )
		# but I can change the indices to make them no longer functions
		unique_outputs.index = [ 0, 0, 1, 2 ]
		self.assertFalse( unique_outputs.is_a_function() )

if __name__ == '__main__':
	unittest.main()
