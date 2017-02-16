#!/usr/bin/env python
# -*- coding: utf-8 -*-

from progressbar import AnimatedMarker, Bar, BouncingBar, Counter, ETA, \
    FileTransferSpeed, FormatLabel, Percentage, \
    ProgressBar, ReverseBar, RotatingMarker, \
    SimpleProgress, Timer
import time
import timeit
import sys
import os

specified_limit      = int(sys.argv[2])
input_file           = sys.argv[1]
reversed_input_file  = input_file

copied_user_txt          = 'copied_user.txt'
reversed_copied_user_txt = 'reversed_copied_user.txt'

max_file = 'user_max.txt'

# ----------------------------------------------------------------------------
# Initialization. If a file exists from the previous run, delete it just in case
# since count will be off set
# ----------------------------------------------------------------------------
def init():
    if os.path.isfile(copied_user_txt):
        user_txt_line_count = get_max_lines(copied_user_txt)
        os.remove(copied_user_txt)
        print "deleted [", copied_user_txt,"]. Original line count [", user_txt_line_count, "]"

    if os.path.isfile(reversed_copied_user_txt):
        reversed_txt_line_count = get_max_lines(reversed_copied_user_txt)
        os.remove(reversed_copied_user_txt)
        print "deleted [", reversed_copied_user_txt,"]. Original line count [", reversed_txt_line_count, "]\n"

# ----------------------------------------------------------------------------
# Get total line number from user_max.txt
# ----------------------------------------------------------------------------
def get_max_lines(input_file):
    if input_file == None:
        input_file = max_file
    with open(input_file, 'r') as f:
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

    widgets = ['Status: ', Percentage(), ' ', Bar('=', '[', ']'), ' ', ETA(), ' ', FileTransferSpeed()]
    pbar = ProgressBar(widgets=widgets, maxval=specified_limit).start()
    for i, line in enumerate(user_txt_file[:]):
        copy_data_to_new_text_file(line, user_txt_copy)
        count += 1
        pbar.update(i+1)
        del user_txt_file[i]
        if count == specified_limit:
            pbar.finish()
            print "\n", count, "lines processed\n"
            break
    processed_max_lines = get_max_lines(open(input_file, 'w').writelines(user_txt_file))
    print "Initial total [", init_lines, "] lines"
    print "Total         [", processed_max_lines, "] lines left\n"


# ----------------------------------------------------------------------------
# Get xxx amount of ids from user_max.txt in reverse order
# ----------------------------------------------------------------------------
def get_ids_reversed(input_file, specified_limit):
    count = 0
    max_lines = get_max_lines(input_file)
    init_lines = max_lines
    reversed_user_txt_copy = open(reversed_copied_user_txt, 'w')      # input
    reversed_user_txt_file = open(input_file).readlines()             # output

    widgets = ['Status: ', Percentage(), ' ', Bar('=', '[', ']'), ' ', ETA(), ' ', FileTransferSpeed()]
    pbar = ProgressBar(widgets=widgets, maxval=specified_limit).start()
    for line in reversed(reversed_user_txt_file):
        copy_data_to_new_text_file(line, reversed_user_txt_copy)
        reversed_user_txt_file.remove(line)
        pbar.update(count+1)
        count += 1
        if count == specified_limit:
            pbar.finish()
            break
    processed_max_lines = get_max_lines(open(input_file, 'w').writelines(reversed_user_txt_file))
    print "Initial total [", init_lines, "] lines"
    print "Total         [", processed_max_lines, "] lines left\n"


# ----------------------------------------------------------------------------
# Write each line data to a usable user text file (copied)
# ----------------------------------------------------------------------------
def copy_data_to_new_text_file(line, copied_user_txt):
    copied_user_txt.write(line)

init()
# Main point of execution
t = timeit.Timer()
get_ids(input_file, specified_limit)
print ("execution time -- ", (t.timeit() / 1000000))

get_ids_reversed(input_file, specified_limit)
print ("execution time -- ", (t.timeit() / 1000000))
