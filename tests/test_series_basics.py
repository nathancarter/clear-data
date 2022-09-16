
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

	def test_to_function ( self ):
		# recreate same I/O sets from the previous test function
		unique_inputs = pd.Series( [ 1, 2, 3, 4 ] )
		repeat_inputs = pd.Series( [ 1, 2, 1, 3 ] )
		unique_outputs = pd.Series( [ 'a', 'b', 'c', 'd' ] )
		repeat_outputs1 = pd.Series( [ 'x', 'x', 'y', 'y' ] )
		repeat_outputs2 = pd.Series( [ 'x', 'y', 'x', 'y' ] )
		# create all the functions that are valid to create (see previous test)
		f1 = unique_inputs.to_function_to( unique_outputs )
		f2 = unique_inputs.to_function_to( repeat_outputs1 )
		f3 = unique_inputs.to_function_to( repeat_outputs2 )
		f4 = repeat_inputs.to_function_to( repeat_outputs2 )
		f5 = unique_outputs.to_function()
		f6 = repeat_outputs1.to_function()
		f7 = repeat_outputs2.to_function()
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

	def test_to_function ( self ):
		# recreate same I/O sets from the previous test function
		unique_inputs = pd.Series( [ 1, 2, 3, 4 ] )
		repeat_inputs = pd.Series( [ 1, 2, 1, 3 ] )
		unique_outputs = pd.Series( [ 'a', 'b', 'c', 'd' ] )
		repeat_outputs1 = pd.Series( [ 'x', 'x', 'y', 'y' ] )
		repeat_outputs2 = pd.Series( [ 'x', 'y', 'x', 'y' ] )
		# create all the dicts that are valid to create (see previous test)
		d1 = unique_inputs.to_dictionary_to( unique_outputs )
		d2 = unique_inputs.to_dictionary_to( repeat_outputs1 )
		d3 = unique_inputs.to_dictionary_to( repeat_outputs2 )
		d4 = repeat_inputs.to_dictionary_to( repeat_outputs2 )
		d5 = unique_outputs.to_dictionary()
		d6 = repeat_outputs1.to_dictionary()
		d7 = repeat_outputs2.to_dictionary()
		# ensure that both ways you can create dictionaries do the same thing
		self.assertEqual( d1, unique_inputs.to_dict_to( unique_outputs ) )
		self.assertEqual( d2, unique_inputs.to_dict_to( repeat_outputs1 ) )
		self.assertEqual( d3, unique_inputs.to_dict_to( repeat_outputs2 ) )
		self.assertEqual( d4, repeat_inputs.to_dict_to( repeat_outputs2 ) )
		self.assertEqual( d5, unique_outputs.to_dict() )
		self.assertEqual( d6, repeat_outputs1.to_dict() )
		self.assertEqual( d7, repeat_outputs2.to_dict() )
		# test three inputs and outputs for each
		self.assertEqual( d1[1], 'a' )
		self.assertEqual( d1[3], 'c' )
		self.assertFalse( '1' in d1 )
		self.assertEqual( d2[2], 'x' )
		self.assertEqual( d2[4], 'y' )
		self.assertFalse( 0 in d2 )
		self.assertEqual( d3[1], 'x' )
		self.assertEqual( d3[2], 'y' )
		self.assertFalse( -1 in d3 )
		self.assertEqual( d4[1], 'x' )
		self.assertEqual( d4[3], 'y' )
		self.assertFalse( 4 in d4 )
		self.assertEqual( d5[1], 'b' )
		self.assertFalse( 'a' in d5 )
		self.assertFalse( 'd' in d5 )
		self.assertFalse( -1 in d6 )
		self.assertEqual( d6[1], 'x' )
		self.assertFalse( 'z' in d6 )
		self.assertEqual( d7[0], 'x' )
		self.assertEqual( d7[3], 'y' )
		self.assertFalse( 4 in d7 )

if __name__ == '__main__':
	unittest.main()
