import os

def read_stopwatch_result_ms(output_str, echo_label):
    #lines = output_str.split(os.linesep)
    lines = output_str.split("\n") #odd!
    for i,line in enumerate(lines):
        if line.startswith("/*"+echo_label+":"):
            return float(lines[i+2].split()[4])/10000.0
    return None

def read_check_port_result(output_str, echo_label):
    lines = output_str.split("\n")
    result = bytearray(3)
    for i,line in enumerate(lines):
        if line.startswith("/*"+echo_label+":"):
            #PORTA PORTC PORTD
            for k,j in enumerate([2,5,8]):
                result[k] = int(lines[i+j].strip().split("=")[1])
            return result
    return None

def get_symbol_dict_from_map_file():
    symbol_dict = {}

    the1_compiled_dir = os.path.join("..", "dist", "default", "debug")
    the1_map_loc = os.path.join(the1_compiled_dir, "the1.debug.map")

    # get symbol adresses from map file
    with open(the1_map_loc, "r") as the1_map:
        while the1_map.readline().strip() != "Symbols - Sorted by Address":
            pass
        the1_map.readline()
        the1_map.readline()
        while True:
            line = the1_map.readline().strip()
            if line == "":
                break
            words = line.split()
            symbol_dict[words[0]] = words[1]

    return symbol_dict
