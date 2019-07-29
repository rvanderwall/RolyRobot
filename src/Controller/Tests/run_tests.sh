#!/bin/bash

# NOTE:  Currently, these run on a system that does NOT have the 
#        Raspberry GPIO package installed
here=`pwd`

cd ..
export PYTHON_PATH=`pwd`

python -m unittest Tests.all_tests
