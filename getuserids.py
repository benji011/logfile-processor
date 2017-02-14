# get x amount of user ids from user.txt
# TODO: replace copied_user.txt after the 2nd execution because:
#       1. user ids are no longer valid
#       2. count will be thrown off balance

import progressbar
from time import sleep

import timeit
import sys
import os

specified_limit      = int(sys.argv[2])
input_file           = sys.argv[1]
reversed_input_file  = input_file

copied_user_txt          = 'copied_user.txt'
reversed_copied_user_txt = 'reversed_copied_user.txt'

max_file = 'results.txt'

def load_progressbar():
    bar = progressbar.ProgressBar(maxval=80, \
    widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
    bar.start()
    for i in range(80):
        bar.update(i+1)
        sleep(0.1)
    bar.finish()

# ----------------------------------------------------------------------------
# Get total line number from user_max.txt
# ----------------------------------------------------------------------------
def get_max_lines(input_file):
    with open(max_file, 'r') as f:
        return len(f.readlines())
    f.close()

# ----------------------------------------------------------------------------
# Get xxx amount of ids from user_max.txt
# ----------------------------------------------------------------------------
def get_ids(input_file, specified_limit):
    count = 0
    max_lines = get_max_lines(input_file)
    init_lines = max_lines

    user_txt_copy = open(copied_user_txt, 'w')      # input
    user_txt_file = open(input_file).readlines()    # output

    for i, line in enumerate(user_txt_file[:]):
        # print line.rstrip('\n')
        copy_data_to_new_text_file(line, user_txt_copy)
        count += 1
        del user_txt_file[i]
        if count == specified_limit:
            print "\n", count, "lines processed\n"
            break

    processed_max_lines = get_max_lines(open(input_file, 'w').writelines(user_txt_file))
    print "Initial total [", init_lines, "] lines"
    print "Total         [", processed_max_lines, "] lines left\n"

# ----------------------------------------------------------------------------
# Get xxx amount of ids from user_max.txt in reverse order
# sort this out later
# ----------------------------------------------------------------------------
def get_ids_reversed(input_file, specified_limit):
    count = 0
    max_lines = get_max_lines(input_file)
    init_lines = max_lines

    reversed_user_txt_copy = open(reversed_copied_user_txt, 'w')      # input
    reversed_user_txt_file = open(input_file).readlines()             # output

    for line in reversed(reversed_user_txt_file):
        copy_data_to_new_text_file(line, reversed_user_txt_copy)
        reversed_user_txt_file.remove(line)
        count += 1
        if count == specified_limit:
            break

    processed_max_lines = get_max_lines(open(input_file, 'w').writelines(reversed_user_txt_file))
    print "Initial total [", init_lines, "] lines"
    print "Total         [", processed_max_lines, "] lines left\n"


# ----------------------------------------------------------------------------
# Write each line data to a usable user text file (copied)
# ----------------------------------------------------------------------------
def copy_data_to_new_text_file(line, copied_user_txt):
    copied_user_txt.write(line)

# Main point of execution
t = timeit.Timer()
load_progressbar()
get_ids(input_file, specified_limit)
print ("execution time -- ", t.timeit() / 1000000)

load_progressbar()
get_ids_reversed(input_file, specified_limit)
print ("execution time -- ", t.timeit() / 1000000)
