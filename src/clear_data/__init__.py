
"""
Working with data in pandas should not require arcane knowledge.

 * You should not have to know the secret of
   `dict( zip( df.date, df.temperature ) )`
 * Instead, you should be able to write
   `df.date.get_function( df.temperature )`

More examples will be put here.  There is no release yet; this is a brand new,
experimental project.
"""

import clear_data.series_extensions
import clear_data.dataframe_extensions
from clear_data.finite_function import FiniteFunction
