
import pandas as pd
import importlib

def load_any_file ( filename, *args, **kwargs ):
    # Assumes first column is index unless it has duplicates
    extension = filename.split( '.' )[-1].lower()
    match extension:
        case 'csv':
            df = pd.read_csv( filename, *args, **kwargs )
            if not any( df.index.duplicated() ):
                df.set_index( df.columns[0], inplace=True )
            return df
        case 'tsv':
            df = pd.read_csv( filename, sep='\t', *args, **kwargs )
            if not any( df.index.duplicated() ):
                df.set_index( df.columns[0], inplace=True )
            return df
        case 'xls' | 'xlsx':
            if extension == 'xls' and importlib.util.find_spec( 'xlwt' ) is None:
                raise ImportError( 'Cannot write in the XLS format without the '
                    + '(deprecated) xlwt module; install it to use this feature' )
            df = pd.read_excel( filename, *args, **kwargs )
            if not any( df.index.duplicated() ):
                df.set_index( df.columns[0], inplace=True )
            return df
        case _:
            raise ValueError( f'Unsupported file extension: {extension}' )

pd.load = load_any_file

def save_any_dataframe ( self, filename, *args, **kwargs ):
    extension = filename.split( '.' )[-1].lower()
    match extension:
        case 'csv':
            self.to_csv( filename, *args, **kwargs )
        case 'tsv':
            self.to_csv( filename, sep='\t', *args, **kwargs )
        case 'xls' | 'xlsx':
            if extension == 'xls' and importlib.util.find_spec( 'xlwt' ) is None:
                raise ImportError( 'Cannot write in the XLS format without the '
                    + '(deprecated) xlwt module; install it to use this feature' )
            self.to_excel( filename, *args, **kwargs )
        case _:
            raise ValueError( f'Unsupported file extension: {extension}' )

pd.DataFrame.save = save_any_dataframe
