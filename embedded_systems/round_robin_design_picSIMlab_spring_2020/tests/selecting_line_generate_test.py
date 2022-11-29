from complex_test_generator import *
import pickle

if __name__ == '__main__':
    generator = ComplexTestGenerator()
    generator.let_200ms_pass()

    generator.check_port_values()
    generator.let_200ms_pass()
    generator.check_port_values()
    generator.let_200ms_pass()
    generator.check_port_values()

    for i in range(4):
        generator.press_down()
        generator.let_200ms_pass()
        generator.check_port_values()
        generator.let_200ms_pass()
        generator.check_port_values()

    for i in range(4):
        generator.press_up()
        generator.let_200ms_pass()
        generator.check_port_values()
        generator.let_200ms_pass()
        generator.check_port_values()

    generator.debug_quit()

    with open("selecting_line_test.dbg", "w") as f:
        f.write(generator.debug_test)

    with open("selecting_line_test_port_values.pkl", "wb") as f:
        print(generator.correct_outputs)
        pickle.dump(generator.correct_outputs, f)
