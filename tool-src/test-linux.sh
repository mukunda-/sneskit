#!/bin/bash
make

# Test build template project.
export SNESKIT=/app

make -C templates/snes-project
make -C example/snesmod
