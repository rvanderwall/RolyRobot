#!/bin/bash

# NOTE:  Currently, these run on a system that does NOT have the 
#        Raspberry GPIO package installed
cd ..

python -m unittest Tests.all_tests
