
import sys, os
this_dir = os.path.dirname( os.path.realpath( __file__ ) )
sys.path.append( os.path.join( this_dir, '..', 'src' ) )
from clear_data import FiniteFunction

import unittest
import pandas as pd
import numpy as np

class TestFiniteFunction( unittest.TestCase ):

    def test_construction_success ( self ):
        f = FiniteFunction( [ 1, 2, 3 ], [ 4, 5, 6 ] )
        self.assertTrue( isinstance( f, FiniteFunction ) )
        f = FiniteFunction( [ 1, 1, 2, 2 ], [ 'x', 'x', 'y', 'y' ] )
        self.assertTrue( isinstance( f, FiniteFunction ) )

    def test_construction_failure ( self ):
        with self.assertRaises( ValueError ):
            FiniteFunction( [ 1, 2, 1 ], [ 3, 4, 5 ] )
        with self.assertRaises( ValueError ):
            FiniteFunction( np.arange( 10 ) % 3, np.arange( 10 ) )

    def test_domain_and_range ( self ):
        f = FiniteFunction( [ 1, 2, 3 ], [ 4, 5, 6 ] )
        self.assertTrue( isinstance( f.domain(), pd.Series ) )
        self.assertEqual( f.domain().tolist(), [ 1, 2, 3 ] )
        self.assertTrue( f.inputs() is f.domain() )
        self.assertTrue( isinstance( f.range(), pd.Series ) )
        self.assertEqual( f.range().tolist(), [ 4, 5, 6 ] )
        self.assertTrue( f.outputs() is f.range() )

    def test_invertibility ( self ):
        f = FiniteFunction( [ 1, 2, 3 ], [ 4, 5, 6 ] )
        self.assertTrue( f.is_injective() )
        self.assertTrue( f.is_invertible() )
        finv = f.inverse()
        self.assertTrue( isinstance( finv, FiniteFunction ) )
        self.assertTrue( f.domain() is finv.range() )
        self.assertTrue( f.range() is finv.domain() )
        f = FiniteFunction( [ 1, 2, 3 ], [ 4, 5, 4 ] )
        self.assertFalse( f.is_injective() )
        self.assertFalse( f.is_invertible() )
        with self.assertRaises( ValueError ):
            f.inverse()
    
    def test_calling ( self ):
        f = FiniteFunction( [ 1, 2, 3 ], [ 4, 5, 6 ] )
        self.assertEqual( f( 1 ), 4 )
        self.assertEqual( f( 2 ), 5 )
        self.assertEqual( f( 3 ), 6 )
        self.assertEqual( f( 4 ), None )
        finv = f.inverse()
        self.assertEqual( finv( 3 ), None )
        self.assertEqual( finv( 4 ), 1 )
        self.assertEqual( finv( 5 ), 2 )
        self.assertEqual( finv( 6 ), 3 )
