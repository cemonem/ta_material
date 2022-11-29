import os
import sys
import the1_utils

with open(sys.argv[1]) as f:
    output_str = f.read()

results = []
for i in range(5):
    result = the1_utils.read_stopwatch_result_ms(output_str, f"msec_result_{i}")
    if result and abs(result-200) < 50:
        results.append(result)
    else:
        print(f"{sys.argv[1]} measured {result} ms at measurement {i}, FAIL!")
        exit()

print(f"{sys.argv[1]} measured {sum(results)/5:.4f} ms average, SUCCESS!")
