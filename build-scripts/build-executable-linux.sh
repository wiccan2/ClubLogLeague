#! /bin/env bash

# Copyright © 2020 Antony Jordan <antony.r.jordan@gmail.com>
# This work is free. You can redistribute it and/or modify it under the
# terms of the Do What The Fuck You Want To Public License, Version 2,
# as published by Sam Hocevar. See the COPYING file for more details.

# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

# NOTE: This script must be run from the project root directory (one directory up from where this file is found).

SCRIPT_NAME=ClubLogLeague
OUTPUT_DIR=executables
VENV_DIR=venv_win

mkdir -p ${OUTPUT_DIR:?}
rm -rf dist build "${OUTPUT_DIR:?}/${SCRIPT_NAME}"

python -m venv ${VENV_DIR}
source "./${VENV_DIR}/bin/activate"

pip install pyinstaller

pyinstaller --onefile ${SCRIPT_NAME}.py

cp ./dist/${SCRIPT_NAME} ${OUTPUT_DIR}
