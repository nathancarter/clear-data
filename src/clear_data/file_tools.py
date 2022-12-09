
import pandas as pd
import importlib
import json
import requests
import tempfile
import os

def load_any_file ( filename, *args, **kwargs ):
    '''
    Load a DataFrame from a file with any of the following extensions, inferring
    the format from the extension: CSV, TSV, XLSX, parquet, PKL or pickle, HDF
    or h5, DTA, ORC, JSON, HTML.  URLs can also be used instead of filenames.
    The XLS extension is not supported due to the deprecation of the xlwt module
    that pandas would use to read such files.

    The only required argument is the filename (with extension), but if you pass
    additional positional or keyword arguments, they will be passed on to the
    appropriate pandas loading function (e.g., `pd.read_csv()`,
    `pd.read_html()`, etc.).

    Certain formats come with certain convenience behaviors built in, to help
    alleviate some of the annoyances that come with pandas.

      1. If the filename is a URL, but the format does not support loading from a
         URL (such as HDF) the content will be downloaded to a temporary folder
         and read from there.
      2. If the extension is TSV, the separator argument is automatically set to
         the tab character in the call to `pd.read_csv()`.
      3. If no key is specified when reading from an HDF file, the key "default"
         is used.  This works well with the `df.save()` function in Clear Data,
         which uses that same default, so that if you want to use HDF files for
         archiving one DataFrame per file, you can omit the key.
      4. If the format is JSON, then the "orient" argument to `pd.read_json()`
         will be inferred from the structure of the data itself.  In the rare case
         where the automatic inference guesses incorrectly between "index" and
         "columns," you can pass the "orient" keyword argument manually.
      5. If the format is HTML, the Beautiful Soup 4 library is used for parsing,
         which alleviates some silent failures of the default lxml parsing library
         (though you can still restore the original behavior with `flavor="lxml"`
         if you prefer, since it is much more efficient for large files).
      6. If the format is HTML, by default, the first table in the page is
         returned.  If you want a different one, pass `index=1` or `index=2` or
         some other values (zero-based).  That is, the surprise that
         `pd.read_html()` returns a list of DataFrames is explicitly removed here;
         you receive exactly one DataFrame, as with all other `pd.read_*()`
         routines.  You decide which one with the "index" argument.

    This function is added to the `pandas` module, so you can call it as
    `pd.load(filename)`.
    '''
    extension = filename.split( '.' )[-1].lower()
    # Throw an error if they are trying to read the old XLS format without the
    # necessary module for doing so (which is deprecated anyway).
    if extension == 'xls' and importlib.util.find_spec( 'xlwt' ) is None:
        raise ImportError( 'Cannot read the XLS format without the '
            + '(deprecated) xlwt module; install it to use this feature' )
    # utility function
    def is_url ():
        return any(
            filename.startswith( f'{protocol}://' )
            for protocol in ['http','https','ftp']
        )
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
        case 'hdf' | 'h5':
            if 'key' not in kwargs:
                kwargs['key'] = 'default'
            if is_url():
                with tempfile.TemporaryDirectory() as dir:
                    temp_filename = os.path.join( dir, 'data.h5' )
                    with open( temp_filename, 'wb' ) as f:
                        f.write( requests.get( filename ).content )
                    df = pd.read_hdf( temp_filename, *args, **kwargs )
            else:
                df = pd.read_hdf( filename, *args, **kwargs )
        case 'dta':
            df = pd.read_stata( filename, *args, **kwargs )
        case 'orc':
            df = pd.read_orc( filename, *args, **kwargs )
        case 'json':
            if 'orient' not in kwargs:
                # detect orientation from JSON structure when possible
                if is_url():
                    json_obj = json.loads( requests.get( filename ).text )
                else:
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
        case 'html':
            if 'flavor' not in kwargs:
                kwargs['flavor'] = 'bs4'
            if 'index' in kwargs:
                index = kwargs['index']
                del kwargs['index']
            else:
                index = 0
            if is_url():
                dfs = pd.read_html( filename, *args, **kwargs )
            else:
                with open( filename, 'r' ) as f:
                    dfs = pd.read_html( f, *args, **kwargs )
            df = dfs[index]
        case _:
            raise ValueError( f'Unsupported file extension: {extension}' )
    # In many cases, the index may have been pushed into the first column of
    # the storage format.  A heuristic to reverse that is to check to see if the
    # first column could function as an index, and if so, use it as one:
    if extension in [ 'csv', 'tsv', 'xls', 'xlsx', 'dta', 'html' ] and \
            not any( df.index.duplicated() ):
        df.set_index( df.columns[0], inplace=True )
        if df.index.name.startswith( 'Unnamed: ' ):
            df.index.name = None
    # Done, so return the result:
    return df

pd.load = load_any_file

def save_any_dataframe ( self, filename, *args, **kwargs ):
    '''
    Save a DataFrame to a file with any of the following extensions, inferring
    the format from the extension: CSV, TSV, XLSX, parquet, PKL or pickle, HDF
    or h5, DTA, ORC, JSON, HTML.  The XLS extension is not supported due to the
    deprecation of the xlwt module that pandas would use to read such files.

    The only required argument is the filename (with extension), but if you pass
    additional positional or keyword arguments, they will be passed on to the
    appropriate pandas saving function (e.g., `df.to_csv()`, `df.to_html()`,
    etc.).

    Certain formats come with certain convenience behaviors built in, to help
    alleviate some of the annoyances that come with pandas.

      1. If the extension is TSV, the separator argument is automatically set to
         the tab character in the call to `df.to_csv()`.
      2. If no key is specified when reading from an HDF file, the key "default"
         is used.  This works well with the `pd.load()` function in Clear Data,
         which uses that same default, so that if you want to use HDF files for
         archiving one DataFrame per file, you can omit the key.
      3. If the format is JSON, then the "orient" argument to `df.to_json()` is
         set to "split" (instead of the default "columns") because this helps
         ensure accuracy when reloading.

    This function is added to the `DataFrame` class, so you can call it as
    `df.save(filename)`.
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
        case 'hdf' | 'h5':
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
        case 'html':
            with open( filename, 'w' ) as f:
                self.to_html( f, *args, **kwargs )
        case _:
            raise ValueError( f'Unsupported file extension: {extension}' )

pd.DataFrame.save = save_any_dataframe
