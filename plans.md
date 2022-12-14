
# Visualization

 * `Series.plot_distribution()` will make an intelligent guess about the
   type of plot based on the series's size and content, but you can
   override with `using="hist"` or box, swarm, strip, violin, ECDF, etc.
    * If the data type is integer:
       * Let's say the max number of bars that look good in a bar plot is $n$
         (though this should be an optional parameter).
       * If the range is $\leq n$, just do a bar plot, one bar per integer.
       * If the range is $>n$, group `ceiling(m/n)` integers per bin.
    * If the data type is float or timedelta64 or datetime64:
       * Maybe just do ordinary `plt.hist()` for this, and add the KDE if the
         number of points is above a certain threshold?
    * If the data type is bool, treat it as categorical with 2 categories.
    * If the data type is categorical, treat it as integers, one per category,
      no gaps between them, so the range is the same size as the number of
      categories.
    * If the user commands any of the other types (except ECDF) just call the
      existing matplotlib function for it.
    * If the user commands ECDF, graph it with the default of showing the normal
      curve on top, but make that a parameter the user can replace with whatever
      NumPy random variable they like.  See code
      [here](https://nathancarter.github.io/MA346-course-notes/_build/html/chapter-10-visualization.html#can-t-i-test-a-single-column-for-normality)
      for how to create such a plot.
    * If the user commands QQ plot, graph it with the default of showing the
      $y=x$ line on top, but make that a parameter the user can replace with
      whatever NumPy random variable they like.  Recall that a QQ plot contains
      points $(x_i,y_i)$ for $i$ in `range(101)` and $x_i$ the $i$th percentile
      for the chosen theoretical distribution and $y_i$ the $i$th percentile in
      the actual data.
 * `DataFrame.plot_function(x[,y,z])`
    * By default, do not first verify that the thing actually is a function;
      just believe the user.  But make this a parameter they can change.
    * If any one column is categorical with a small enough number of categories,
      just sort the categories, use them as the axis labels, and convert the
      data to numbers that line up correctly.  If the data is strings, just
      treat them as categories in this sense.  Same for bool.  If the data is
      any other non-numeric thing, raise an exception.
    * For $(x,y)$ pairs (no $z$ yet):
       * If the $x$ data type is integer or dates or has been converted to such
         from categorical, use dots as the marker, but the user can override
         this with an optional parameter if they choose.
       * If the $x$ data type is float or timedelta64, use lines as the marker,
         also overridable.
    * For $(x,y,z)$ triples:
       * If $x$ and $y$ both discrete, use dots as the marker (overridable).
       * If $x$ and $y$ both continuous, plot a surface.
       * If $x$ discrete and $y$ continuous, plot separate lines parallel to the
         $yz$ plane.
       * If $x$ continuous and $y$ discrete, plot separate lines parallel to the
         $xz$ plane.
 * `DataFrame.plot_relation(x[,y])` (or `plot_binary_relation`)
    * Always does a scatterplot.
    * If the number of points is above a certain threshold, defaults to using an
      alpha value to make the cloud more informative.
    * Adds the KDE plot for an axis by default if the count of unique values for
      that axis is above a certain threshold, but this can be overridden.
    * If no $y$ is specified, multiple relations are shown on the same graph,
      with different colors and a legend, but the same $x$ variable for each.
 * `DataFrame.plot_relations()` (or `plot_binary_relations`) does a
   pair plot
 * `DataFrame.plot_distribution(x,*args,**kwargs)` functions just like
   `df[x].plot_distribution(*args,**kwargs)`.
 * `DataFrame.plot_distributions(cols...)` can also accept `using="..."`,
   and will be smart about multiple columns, e.g., side-by-side bars in a
   histogram.  I haven't yet written out all the plans for this one.
 * `DataFrame.plot_linear_model(x[,y,z])` - not yet planned in detail.
 * `DataFrame.plot_correlations([colnames...])` does a heat map not yet planned
   in detail.
 * `DataFrame.plot_on_map(lat,lng[,labels])` does a geographic plot, not yet
   planned in detail.

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
