from complex_test_generator import *
import pickle

if __name__ == '__main__':
    generator = ComplexTestGenerator()
    generator.let_200ms_pass()

    generator.press_confirm()

    for i in range(9):
        generator.let_200ms_pass()
        generator.press_up()

    for i in range(3):
        generator.let_200ms_pass()
        generator.press_down()

    generator.let_200ms_pass()
    generator.press_toggle()

    for i in range(7):
        generator.let_200ms_pass()
        generator.press_up()

    generator.let_200ms_pass()
    generator.press_toggle()

    for i in range(2):
        generator.let_200ms_pass()
        generator.press_down()

    generator.let_200ms_pass()
    generator.press_toggle()

    for i in range(7):
        generator.let_200ms_pass()
        generator.press_down()

    for i in range(2):
        generator.let_200ms_pass()
        generator.press_up()

    generator.let_200ms_pass()
    generator.press_confirm()

    generator.let_200ms_pass()
    generator.press_confirm()

    generator.let_200ms_pass()

    generator.press_confirm()

    generator.let_200ms_pass()
    if not generator.ledblink:
        generator.let_200ms_pass()
    generator.check_port_values()

    generator.press_down()
    generator.let_200ms_pass()
    generator.press_up()
    generator.let_200ms_pass()
    generator.press_toggle()
    generator.let_200ms_pass()
    generator.press_down()

    generator.debug_quit()

    with open("drawing_line_test.dbg", "w") as f:
        f.write(generator.debug_test)

    with open("drawing_line_test_port_values.pkl", "wb") as f:
        print(generator.correct_outputs)
        pickle.dump(generator.correct_outputs, f)
