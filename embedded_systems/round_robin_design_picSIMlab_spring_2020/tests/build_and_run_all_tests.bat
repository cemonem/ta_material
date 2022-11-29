echo "cd into .. and build in debug mode"
cd ..
make TYPE_IMAGE=DEBUG_RUN
cd tests

call run_test.bat sec_passed_test.dbg sec_passed_parse_output.py
call run_test.bat msec200_passed_test.dbg msec200_passed_parse_output.py
call run_test.bat msec200_passed_test_rb0_hold.dbg msec200_passed_parse_output.py
call run_test.bat msec200_passed_test_rb1_hold.dbg msec200_passed_parse_output.py
call run_test.bat msec200_passed_test_rb2_hold.dbg msec200_passed_parse_output.py
call run_test.bat msec200_passed_test_rb3_hold.dbg msec200_passed_parse_output.py
call run_test.bat debounce_test_rb0.dbg debounce_parse_output.py rb0
call run_test.bat debounce_test_rb1.dbg debounce_parse_output.py rb1
call run_test.bat debounce_test_rb2.dbg debounce_parse_output.py rb2
call run_test.bat debounce_test_rb3.dbg debounce_parse_output.py rb3
call run_test.bat selecting_line_test.dbg complex_test_parse_output.py selecting_line_test_values.pkl
call run_test.bat drawing_line_test.dbg complex_test_parse_output.py drawing_line_test_values.pkl
