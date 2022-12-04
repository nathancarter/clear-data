
import pandas as pd
import importlib
import json

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
            if 'sep' not in kwargs:
                kwargs['sep'] = '\t'
            df = pd.read_csv( filename, *args, **kwargs )
        case 'xls' | 'xlsx':
            df = pd.read_excel( filename, *args, **kwargs )
        case 'parquet':
            df = pd.read_parquet( filename, *args, **kwargs )
        case 'pickle' | 'pkl':
            df = pd.read_pickle( filename, *args, **kwargs )
        case 'hdf':
            if 'key' not in kwargs:
                kwargs['key'] = 'default'
            df = pd.read_hdf( filename, *args, **kwargs )
        case 'dta':
            df = pd.read_stata( filename, *args, **kwargs )
        case 'orc':
            df = pd.read_orc( filename, *args, **kwargs )
        case 'json':
            if 'orient' not in kwargs:
                # detect orientation from JSON structure when possible
                with open( filename ) as f:
                    json_obj = json.load( f )
                if type( json_obj ) == list:
                    if all( type( inner ) == list for inner in json_obj ):
                        orient = 'values'
                    elif all( type( inner ) == dict for inner in json_obj ):
                        orient = 'records'
                    else:
                        raise ValueError( 'JSON does not have a table structure' )
                elif type( json_obj ) == dict:
                    if (
                        'columns' in json_obj and
                        'index' in json_obj and
                        'data' in json_obj and
                        type( json_obj['columns'] ) == list and
                        type( json_obj['index'] ) == list and
                        type( json_obj['data'] ) == list
                    ):
                        orient = 'split'
                    elif (
                        'schema' in json_obj and
                        'data' in json_obj and
                        type( json_obj['schema'] ) == dict and
                        type( json_obj['data'] ) == list
                    ):
                        orient = 'table'
                    else:
                        keys = list( json_obj.keys() )
                        if all( type( json_obj[key] ) == dict for key in keys ):
                            num_keys = len( keys )
                            num_inner_keys = len( json_obj[keys[0]].keys() )
                            if num_keys > num_inner_keys:
                                # heuristic: guess outer keys are the rows
                                orient = 'index'
                            else:
                                # other way around, inner keys are the rows
                                orient = 'columns'
                        else:
                            raise ValueError( 'JSON does not have a table structure' )
                else:
                    raise ValueError( 'JSON does not have a table structure' )
            if orient == 'records':
                df = pd.json_normalize( json_obj ) # must ignore args and kwargs
            else:
                df = pd.read_json( filename, orient=orient, *args, **kwargs )
        case _:
            raise ValueError( f'Unsupported file extension: {extension}' )
    # In many cases, the index may have been pushed into the first column of
    # the storage format.  A heuristic to reverse that is to check to see if the
    # first column could function as an index, and if so, use it as one:
    if extension in [ 'csv', 'tsv', 'xls', 'xlsx', 'dta' ] and \
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
            if 'sep' not in kwargs:
                kwargs['sep'] = '\t'
            self.to_csv( filename, *args, **kwargs )
        case 'xls' | 'xlsx':
            self.to_excel( filename, *args, **kwargs )
        case 'parquet':
            self.to_parquet( filename, *args, **kwargs )
        case 'pickle' | 'pkl':
            self.to_pickle( filename, *args, **kwargs )
        case 'hdf':
            if 'key' not in kwargs:
                kwargs['key'] = 'default'
            self.to_hdf( filename, *args, **kwargs )
        case 'dta':
            self.to_stata( filename, *args, **kwargs )
        case 'orc':
            self.to_orc( filename, *args, **kwargs )
        case 'json':
            if 'orient' not in kwargs:
                kwargs['orient'] = 'split'
            self.to_json( filename, *args, **kwargs )
        case _:
            raise ValueError( f'Unsupported file extension: {extension}' )

pd.DataFrame.save = save_any_dataframe
