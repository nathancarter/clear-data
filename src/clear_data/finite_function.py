
import pandas as pd

class FiniteFunction:
    """
    A `FiniteFunction` is made up of a finite list of ordered pairs in which
    each input (left hand element in a pair) is paired with exactly one
    corresponding output (right hand element in the pair).  We construct
    `FiniteFunction` instances by passing the domain (sequence of inputs) and
    the range (sequence of outputs) to the constructor, and it pairs them up in
    the obvious way, throwing an error if the above condition is not met.  One
    can then do lookup into these input-and-output arrays by calling the
    function, or invert it if possible with `inverse()`.
    """

    def __init__ ( self, inputs, outputs ):
        """
        To create a new `FiniteFunction`, pass a list, array, or Series as each
        argument.  For example, the squaring function on the first 5 integers
        can be built by `f = FiniteFunction([1,2,3,4,5],[1,4,9,16,25])`.  Throws
        an error if your inputs don't define a function, as in
        `FiniteFunction([1,2,1],[1,2,3])`.  (What does 1 map to?)

        You can use instances with ordinary function appication notation, as in
        the following example.  If you had `f` as defined above, you could
        evaluate it on the input 2 with the code `f( 2 )` (which returns 4).
        """
        if not isinstance( inputs, pd.Series ):
            inputs = pd.Series( inputs ) # defaults to range index -- good
        if not isinstance( outputs, pd.Series ):
            outputs = pd.Series( outputs ) # default to range index -- good
        if not inputs.is_a_function_to( outputs ):
            raise ValueError( 'Inputs and outpus do not form a function' )
        self._inputs = inputs
        self._outputs = outputs
        self._inputs_as_list = inputs.tolist()
        self._outputs_as_list = outputs.tolist()
    
    def __call__ ( self, input ):
        """
        Apply the function by looking the input up in the original set of
        inputs and returning the corresponding output.  Returns `None` if the
        input is not in the function's domain.
        """
        try:
            return self._outputs_as_list[self._inputs_as_list.index( input )]
        except:
            return None
    
    def domain ( self ):
        """
        The inputs provided at construction time.
        """
        return self._inputs
    
    def inputs ( self ):
        """
        Same as `domain()`.
        """
        return self._inputs
    
    def range ( self ):
        """
        The outputs provided at construction time.
        """
        return self._outputs
    
    def outputs ( self ):
        """
        Same as `range()`.
        """
        return self._outputs
    
    def is_injective ( self ):
        """
        Same as `is_invertible()`.
        """
        return self._outputs.is_a_function_to( self._inputs )
    
    def is_invertible ( self ):
        """
        Whether this function's outputs are also a function to its inputs,
        meaning that the function has an inverse.  If this function returns
        `True`, you can create the inverse with `inverse()`.
        """
        return self.is_injective()
    
    def inverse ( self ):
        """
        The `FiniteFunction` mapping this function's outputs to their
        corresponding inputs.  Trying to create this will throw an error unless
        `is_invertible()` holds.
        """
        return FiniteFunction( self._outputs, self._inputs )
