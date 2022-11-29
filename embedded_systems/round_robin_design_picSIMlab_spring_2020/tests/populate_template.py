import os
import sys
import string
import the1_utils

template_identifiers = the1_utils.get_symbol_dict_from_map_file()

the1_compiled_dir = os.path.join("..", "dist", "default", "debug")
the1_cof_loc = os.path.join(the1_compiled_dir, "the1.debug.cof")

template_identifiers["cof_file_loc"] = the1_cof_loc

#for idd in template_identifiers:
#    print(idd, template_identifiers[idd])

# open template debug file and replace stuff
with open(sys.argv[1], "r") as template_file:
    render = string.Template(template_file.read()).substitute(**template_identifiers)


with open(sys.argv[1]+".render", "w") as render_file:
    render_file.write(render)
