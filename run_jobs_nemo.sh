#!/bin/bash
for filename in NEMO/*.moab; do
  echo "$filename"
  msub -V "$filename"
done
