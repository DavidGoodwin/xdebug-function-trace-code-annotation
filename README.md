xdebug-function-trace-code-annotation
=====================================

Munges an xdebug trace output with the source file, to make for easier analysis. Perhaps of use with large trace files (>20Gb etc).


Usage
=====


 * Run an xdebug function trace ( see http://xdebug.org/docs/execution_trace ) on some code that needs optimising.
   * Ensure the PHP ini setting for xdebug.trace_format is set to 1

 * Grab the output file (e.g. MyTraceFile.xt) and filter it with :

```Shell
python filter.py Module/File.php MyTraceFile.xt > filtered.xt
```

 * Then, merge the filtered.xt into the source code producing a report -

```Shell
python report.py filtered.xt ./path/to/Source/Code/Module/File.php > report.html
```

You'll see report.html looking a little like :

```PHP
99  ....
100 foreach ($x as $y) {
101 $qty = $allocationRepo->getSomethingByXAndY($y, $location);	
      {'....->getSomethingByXAndY': {'avg_time': 0.018434527744934828, 'count': 774700, 'total_time': 14281.22864400101} }

102 if( ! $qty ) { continue ; }
103 ....
```

You could obviously repeat the above for all files within your application, however it's probably the case that you can pre-select the code that's more likely to be the bottleneck beforehand through simple visual analysis.
