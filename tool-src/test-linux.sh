#!/bin/bash
chmod u+x ./setup.py
./setup.py

# Test build template project.
export SNESKIT=/app/
cd templates/snes-project
make
