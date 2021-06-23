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
parser.add_argument('--output2-path',
                    type=str,
                    help='Path of the local file where the Output 2 data should be written.')

args = parser.parse_args()

print(f'Prograsm arguments: {args}')

# Creating the directory where the output file is created (the directory
# may or may not exist).
Path(args.output1_path).parent.mkdir(parents=True, exist_ok=True)
Path(args.output2_path).parent.mkdir(parents=True, exist_ok=True)

with open(args.input1_path, 'r') as input1_file:
    with open(args.output1_path, 'w') as output1_file:
        with open(args.output2_path, 'w') as output2_file:
            odd = True
            for line in input1_file:
                if odd:
                    output1_file.write(line)
                else:
                    output2_file.write(line)
                odd = not odd
