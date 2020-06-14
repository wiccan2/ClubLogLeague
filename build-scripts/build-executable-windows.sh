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

mkdir -p ${OUTPUT_DIR:?}
rm -rf "${OUTPUT_DIR:?}/${SCRIPT_NAME}.exe"

vagrant up
vagrant winrm -c "copy C:\\vagrant C:\\vagrant-loc -r"
vagrant winrm -c "cd C:\\vagrant-loc ; .\\build-scripts\\build-executable-windows.ps1"
vagrant winrm -c "copy C:\\vagrant-loc\\${OUTPUT_DIR}\\${SCRIPT_NAME}.exe C:\\vagrant\\${OUTPUT_DIR}"
vagrant destroy -f
