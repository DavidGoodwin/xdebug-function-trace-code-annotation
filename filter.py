import sys

CHR0 = ord('0')
CHR9 = ord('9')

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

RECORD_TYPE_ENTER = '0'
RECORD_TYPE_EXIT = '1'


class Stack(object):

    def __init__(self):
        self.array = [0] * 100
        self.pointer = -1

    def push(self, value):
        self.pointer += 1
        self.array[self.pointer] = value

    def peek(self):
        return self.array[self.pointer]

    def pop(self):
        value = self.array[self.pointer]
        self.pointer -= 1
        return value


try:
    trace_file = open(sys.argv[2], "r")
except IndexError:
    print "No trace file supplied!"
    sys.exit(1)


try:
    path = sys.argv[1]
except IndexError:
    print "No search supplied!"
    sys.exit(1)


func_queue = Stack()

for line in trace_file:

    # lines we care about start with the call stack depth, so the first char will be a number
    if ord(line[0]) < CHR0 or ord(line[0]) > CHR9:
        continue

    line_bits = line.split("\t")
    function_id = line_bits[FUNCTION_ID]

    if line_bits[RECORD_TYPE] == RECORD_TYPE_ENTER:     # if enter function line

        if path not in line_bits[FILENAME]:             # check its a file we care about
            continue

        func_queue.push(function_id)                    # add the function_id to the stack

        print line,

    else:                                               # it's an exit line

        if func_queue.peek() != function_id:
            continue                                    # skip if we don't care about the function call

        func_queue.pop()                                # else, remove from the stack

        print line,

