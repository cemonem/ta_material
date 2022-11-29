import os
import sys
import the1_utils

with open(sys.argv[1]) as f:
    output_str = f.read()

symbols = the1_utils.get_symbol_dict_from_map_file()
address = hex(int(symbols[sys.argv[2]+"_released"],16))

breakpoint_hits = output_str.count("address:"+address)

if breakpoint_hits == 1:
    print(f"{sys.argv[1]} counted {breakpoint_hits} {sys.argv[2]}_released hit, SUCCESS!")
else:
    print(f"{sys.argv[1]} counted {breakpoint_hits} {sys.argv[2]}_released hits, FAIL!")
