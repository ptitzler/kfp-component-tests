#!/usr/bin/env python3
import argparse
from pathlib import Path


# Defining and parsing the command-line arguments
parser = argparse.ArgumentParser(description='My program description')
# Paths must be passed in, not hardcoded
parser.add_argument('--input1-path',
                    type=str,
                    help='Path of the local file containing the Input 1 data.')
parser.add_argument('--output1-path',
                    type=str,
                    help='Path of the local file where the Output 1 data should be written.')
args = parser.parse_args()

print('Input arguments:')
print(args)

# Creating the directory where the output file is created (the directory
# may or may not exist).
Path(args.output1_path).parent.mkdir(parents=True, exist_ok=True)

count = 0
with open(args.input1_path, 'r') as input1_file:
    for line in input1_file:
        count += 1
print(f'Input file contains {count} lines')
with open(args.output1_path, 'w') as output1_file:
    output1_file.write(str(count))
