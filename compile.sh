#! /usr/bin/env bash

set -e # Exit on error 
set -u # Exit on unbound variables

if [ -z "$1" ]; then
	echo "Missing argument: please provide build directory"
	exit 1
fi

echo ":: Compiling TEE in $1"

if [ ! -f "$1/resize_dataports.py" ]; then
	ln -s "$(pwd)/resize_dataports.py" "$1/resize_dataports.py"
fi

if [ ! -f "$1/remap_dataports.py" ]; then
	ln -s "$(pwd)/remap_dataports.py" "$1/remap_dataports.py"
fi

echo ":: Installed symbolic links in build directory"

echo ":: Running first build"

cd "$1"

ninja

echo ":: Resizing dataports"

python3 resize_dataports.py --spec "$(pwd)/tee.cdl" --header "$(pwd)/../projects/camkes/apps/tee/components/include/buffer.h"

echo ":: Running build (to generate new spec with correct number of dataport frames)"

ninja

echo ":: Mapping TA code pages into the Attestation component's VSpace"

python3 remap_dataports.py  --spec "$(pwd)/capdl_spec.c"

echo ":: Running final build"

ninja

echo ":: Done"
