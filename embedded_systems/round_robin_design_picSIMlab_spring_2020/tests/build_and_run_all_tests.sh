#!/usr/bin/env bash

./build_debug.sh > /dev/null 2> /dev/null

./run_test.sh sec_passed_test.dbg sec_passed_parse_output.py
./run_test.sh msec200_passed_test.dbg msec200_passed_parse_output.py
./run_test.sh msec200_passed_test_rb0_hold.dbg msec200_passed_parse_output.py
./run_test.sh msec200_passed_test_rb1_hold.dbg msec200_passed_parse_output.py
./run_test.sh msec200_passed_test_rb2_hold.dbg msec200_passed_parse_output.py
./run_test.sh msec200_passed_test_rb3_hold.dbg msec200_passed_parse_output.py
./run_test.sh debounce_test_rb0.dbg debounce_parse_output.py rb0
./run_test.sh debounce_test_rb1.dbg debounce_parse_output.py rb1
./run_test.sh debounce_test_rb2.dbg debounce_parse_output.py rb2
./run_test.sh debounce_test_rb3.dbg debounce_parse_output.py rb3
./run_test.sh selecting_line_test.dbg complex_test_parse_output.py selecting_line_test_values.pkl
./run_test.sh drawing_line_test.dbg complex_test_parse_output.py drawing_line_test_values.pkl
