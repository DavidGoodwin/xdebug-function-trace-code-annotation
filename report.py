import cgi
import sys

# Original author: William Redman @ Pale Purple Ltd.

# see: http://xdebug.org/docs/all_settings#trace_format
LEVEL = 0
FUNCTION_ID = 1
RECORD_TYPE = 2
TIME = 3
MEM = 4
FUNC_NAME = 5
USER_DEF = 6
INC_FILE = 7
FILENAME = 8
LINE_NUMBER = 9

TYPE_ENTER = '0'
TYPE_EXIT = '1'

try:
    trace_file = open(sys.argv[1], "r")
except IndexError:
    print "No trace file supplied!"
    sys.exit(1)


try:
    source_file = open(sys.argv[2], "r")
except IndexError:
    print "No source code file supplied!"
    sys.exit(1)

# lines[source_code_line_number] => [function_id, another_function_id, ...]
lines = {}

# functions[function_id] => {
#   name => string
#   enter => {
#      time => float
#   }
#   exit => {
#      time => float
#   }
#   time => float
# }
functions = {}

counter = 0

for line in trace_file:

    line_bits = line.split("\t")
    function_id = int(line_bits[FUNCTION_ID])
    function_time = float(line_bits[TIME])

    try:
        function_dict = functions[function_id]
    except KeyError:
        function_dict = {}

    if line_bits[RECORD_TYPE] == TYPE_ENTER:

        function_name = line_bits[FUNC_NAME]

        function_dict['enter'] = {'time': function_time}
        function_dict['name'] = function_name

        line_number = int(line_bits[LINE_NUMBER].rstrip())
        try:
            line_list = lines[line_number]
        except KeyError:
            line_list = []
        line_list.append(function_id)
        lines[line_number] = line_list

    else:
        function_dict['exit'] = {'time': function_time}
        function_dict['time'] = function_time - function_dict['enter']['time']

    functions[function_id] = function_dict


print """
<html>
    <head>
        <title></title>
        <style>
            td.l {
                color: gray;
            }
            tr.c {
                color: blue;
            }
            tr.a > td {
                padding-bottom: 20px;
            }
        </style>
    </head>
    <body>
        <table>
"""

import pprint
pp = pprint.PrettyPrinter(depth=6)


line_number = 0
for line in source_file:
    line_number += 1

    print '<tr class="c">'
    print '  <td class="l"><a name="%i">' % line_number, line_number, '</a></td>'
    print '  <td><code>', cgi.escape(line).replace(" ", "&nbsp;").replace("\t", "&nbsp;&nbsp;&nbsp;&nbsp;"), '</code></td>'
    print '</tr>'

    try:
        line_functions = lines[line_number]
    except KeyError:
        continue

    print '<tr class="a"><td colspan="2">',

    function_names = {}

    for function_id in line_functions:

        function_dict = functions[function_id]
        try:
            func = function_names[function_dict['name']]
        except KeyError:
            func = {'count': 0, 'total_time': 0.0}

        func['count'] += 1
        func['total_time'] += function_dict['time']
        func['avg_time'] = func['total_time'] / func['count']

        function_names[function_dict['name']] = func

    print '<pre>%s</pre>' % pp.pformat(function_names)
    print '</td></tr>'

print """
        </table>

    </body>
</html>
"""
