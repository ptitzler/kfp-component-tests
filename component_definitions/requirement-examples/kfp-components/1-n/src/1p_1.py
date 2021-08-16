#!/usr/bin/env python3
import argparse
from pathlib import Path


# Defining and parsing the command-line arguments
parser = argparse.ArgumentParser(description='My program description')
# Paths must be passed in, not hardcoded
parser.add_argument('--input1-path',
                    type=str,
                    help='input 1 data')
parser.add_argument('--output1-path',
                    type=str,
                    help='output 1 data')
args = parser.parse_args()

print('Input arguments:')
print(args)

# Creating the directory where the output file is created (the directory
# may or may not exist).
Path(args.output1_path).parent.mkdir(parents=True, exist_ok=True)

print(f'Reading input 1 data from {args.input1_path}')
with open(args.input1_path, 'r') as input1_file:
    for line in input1_file:
        print(line)

print(f'Writing output 1 data to {args.output1_path}')
with open(args.output1_path, 'w') as output1_file:
    output1_file.write('1p_1 output')
