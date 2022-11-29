#!/usr/bin/env bash
#./build_debug.sh > /dev/null 2> /dev/null
#./build_debug.sh

python3 populate_template.py "${1}"
mdb "${1}.render" > "${1}.out" 2> /dev/null
#mdb "${1}.render" > "${1}.out"


if [[ ! -z "${2}" ]]; then
  python3 "${2}" "${1}.out" "${3}"
fi

rm -f "${1}.out" "${1}.render"
