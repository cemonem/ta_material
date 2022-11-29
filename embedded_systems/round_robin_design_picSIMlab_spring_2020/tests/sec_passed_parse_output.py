import os
import sys
import the1_utils

with open(sys.argv[1]) as f:
    output_str = f.read()

result = the1_utils.read_stopwatch_result_ms(output_str, "sec_result")
if result and abs(result-1000) < 50:
    print(f"{sys.argv[1]} measured {result:.4f} ms, SUCCESS!")
else:
    print(f"{sys.argv[1]} measured {result} ms, FAIL!")
