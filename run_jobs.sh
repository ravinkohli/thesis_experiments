#!/bin/bash
for filename in SLURM/*.sh; do
  echo "$filename"
  sbatch "$filename" --bosch
done