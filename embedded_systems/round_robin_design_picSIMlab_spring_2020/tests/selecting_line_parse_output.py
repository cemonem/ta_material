import pickle
import the1_utils
import sys

def the1_bytearray_binary(bytearr):
    return f"PORTA=0b{bytearr[0]:08b} PORTC=0b{bytearr[1]:08b} PORTD=0b{bytearr[2]:08b}"

if __name__ == '__main__':
    with open(sys.argv[2], "rb") as f:
        correct_outputs = pickle.load(f)

    with open(sys.argv[1],"r") as f:
        output_str = f.read()

    for label in correct_outputs:
        if label.startswith("check_port_label"):
            measured_values = the1_utils.read_check_port_result(output_str, label)
            #print(f"measured {the1_bytearray_binary(measured_values)}, ground truth {the1_bytearray_binary(correct_outputs[label])}")
            if measured_values != correct_outputs[label]:
                print(f"In {sys.argv[1]}, at debug label {label}, measured {the1_bytearray_binary(measured_values)} instead of {the1_bytearray_binary(correct_outputs[label])}, FAIL!")
                exit()

    print(f"In {sys.argv[1]}, all values correct, SUCCESS!")
