
import pandas as pd
import importlib

def load_any_file ( filename, *args, **kwargs ):
    '''
    Documentation forthcoming.
    '''
    extension = filename.split( '.' )[-1].lower()
    # Throw an error if they are trying to read the old XLS format without the
    # necessary module for doing so (which is deprecated anyway).
    if extension == 'xls' and importlib.util.find_spec( 'xlwt' ) is None:
        raise ImportError( 'Cannot read the XLS format without the '
            + '(deprecated) xlwt module; install it to use this feature' )
    # Load the file using the method appropriate to the filename's extension.
    match extension:
        case 'csv':
            df = pd.read_csv( filename, *args, **kwargs )
        case 'tsv':
            df = pd.read_csv( filename, sep='\t', *args, **kwargs )
        case 'xls' | 'xlsx':
            df = pd.read_excel( filename, *args, **kwargs )
        case _:
            raise ValueError( f'Unsupported file extension: {extension}' )
    # In many cases, the index may have been pushed into the first column of
    # the storage format.  A heuristic to reverse that is to check to see if the
    # first column could function as an index, and if so, use it as one:
    if extension in [ 'csv', 'tsv', 'xls', 'xlsx' ] and \
            not any( df.index.duplicated() ):
        df.set_index( df.columns[0], inplace=True )
    # Done, so return the result:
    return df

pd.load = load_any_file

def save_any_dataframe ( self, filename, *args, **kwargs ):
    '''
    Documentation forthcoming.
    '''
    extension = filename.split( '.' )[-1].lower()
    # Throw an error if they are trying to write in the old XLS format without
    # the necessary module for doing so (which is deprecated anyway).
    if extension == 'xls' and importlib.util.find_spec( 'xlwt' ) is None:
        raise ImportError( 'Cannot write in the XLS format without the '
            + '(deprecated) xlwt module; install it to use this feature' )
    # Save the data using the method appropriate to the filename's extension.
    match extension:
        case 'csv':
            self.to_csv( filename, *args, **kwargs )
        case 'tsv':
            self.to_csv( filename, sep='\t', *args, **kwargs )
        case 'xls' | 'xlsx':
            self.to_excel( filename, *args, **kwargs )
        case _:
            raise ValueError( f'Unsupported file extension: {extension}' )

pd.DataFrame.save = save_any_dataframe
