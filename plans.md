
# File load/save

Both of the following functions can take extra parameters for specific
actions/details, such as a sheet name in Excel.  Should support many
formats, including XLS[X], CSV, TSV, JSON, HTML, DB?, GRAPHML?

 * `pd.load("file or URL")` that is smart enough to handle a wide variety
   of file types and gives nice reports/explanations if something went
   wrong, in general being like `pd.read_X` for various `X`, but inspecting
   the file to figure out what `X` should be, together with appropriate
   parameters specific to the file type, or explaining troubles to the user
   in a clear way if the right path forward can't be easily determined.
 * `DataFrame.save("filename")` uses the extension and does something
   smart, with output about what it did.

# Filtering

In all of these, there is an optional `kwarg` that is `efficient=False`,
meaning to make a copy of the DataFrame, not a slice, to avoid the most
annoying error in all of data science.  You can override it with
`efficient=True` to get a slice.  It would also be good to enable a change
to the global default.

 * `DataFrame.rows_satisfying(bool_series)` with synonyms:
    * `rows_such_that`, `rows_where`, `rows_in_which`, `select`,
      `select_rows`, `filter`, `filter_rows`, `subset`

# Visualization

 * `Series.plot_distribution()` will make an intelligent guess about the
   type of plot based on the series's size and content, but you can
   override with `using="hist"` or box, swarm, strip, violin, ECDF, etc.
 * `DataFrame.plot_function(x[,y,z])`
 * `DataFrame.plot_relation(x[,y])` (or `plot_binary_relation`)
 * `DataFrame.plot_relations(x[,y])` (or `plot_binary_relations`) does a
   pair plot
 * `DataFrame.plot_distribution(x[,y])` can accept `using="..."` as above
 * `DataFrame.plot_distributions(cols...)` can also accept `using="..."`,
   and will be smart about multiple columns, e.g., side-by-side bars in a
   histogram
 * `DataFrame.plot_linear_model(x[,y,z])`
 * `DataFrame.plot_correlations([colnames...])` does a heat map
 * `DataFrame.plot_on_map(lat,lng[,labels])` does a geographic plot

# Statistics

 * `Series.is_normally_distributed()` and similar questions for other
   commonly used distribution tests
 * `Series.has_mean(m)` does a hypothesis test with `alpha=0.05`, but you
   can override and give a different `alpha`; similarly:
    * `has_mean_above(m)`, `has_mean_below(m)`
    * `mean_confidence_interval()`
 * `DataFrame.get_linear_model(domaincols...,rangecol)` uses statsmodels
   or sklearn classes but adds a reference from the model to the training
   data
 * `DataFrame.get_logistic_model(domaincols...,rangecol)` like previous
 * `Model.show()` should give nice LaTeX output
 * `Series.get_RSSE(yhats)` and other scoring tools such as `RMSE`,
   `F1_score`, precision, recall, and so on
    * Plus `Model.get_RSSE()` etc. that use the training data or
      `Model.get_RSSE(test_data)` that use the test data
 * `DataFrame.add_polynomial_term(colname,degree)`
 * `DataFrame.add_interaction_term(col1,col2)`
 * `Model.add_polynomial_term(colname,degree)` returns a new model trained
   on the same data plus that new term, and similarly for
   `add_interaction_term`

What other test?  Chi-square, ANOVA, etc.?

Some easy way to add dummy columns and one-hot encoding columns, unless
something like `df.add_columns(df[x].get_dummies())` already does it.

# Pivoting and melting

 * `DataFrame.pivot_possibilities()`
 * `DataFrame.melt_possibilities()`

Check your notes on pivoting for the appropriate English phrasing of most
common aggregation descriptions, and try to make an aggregation parameter
name setup that lets us express such pivot tables in natural ways.
```
DataFrame.aggregate(   # or summarize?
    "average",         # or any aggregation function
    "temperature",     # column name
    by="...",          # groupby, for_each
    # etc
)
```

# Concatenation and merging

 * `Series.next_to(other_series)`
 * `DataFrame.add_rows(other_dfs...)` does a `pd.concat`
 * `DataFrame.add_columns(other_df[,merge_params...])` defaults to merging
   on the index, complains if it's not a perect 1-1 match/lineup, and
   suggests code for a manual merge instead
 * `DataFrame.can_merge(merge_params...)` gives a report on if/how a merge
   would work

# Looping

These could each take optional parameters for progress bars, and should
even introduce progress bars by default when the size is large enough.

 * `Series.for_each(f)`
 * `DataFrame.for_each_row(f)` which should call `f(col=val,...)` and
   should also support letting `f` be one of the model classes from famous
   packages like statsmodels or sklearn
 * `DataFrame.for_each_column(f)` calls `f(df[col])`

# Conversion

 * `Series.can_convert_to(type)`
 * `Series.can_view_as(type)`
 * `Series.view_as(type)`
 * Support other types like currency, dollars, numbers, dates, etc.

# Networks

 * `DataFrame.to_edge_list([includeweights])`
 * `DataFrame.to_adjacency_matrix([weightcol])`
 * `DataFrame.to_graph()` or `to_directed_graph`?
 * `DataFrame.plot_network([nx_draw_prameters])`
 * `DataFrame.normalize_rows()`
