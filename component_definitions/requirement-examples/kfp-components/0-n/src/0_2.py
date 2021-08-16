#!/usr/bin/env python3
import argparse
from pathlib import Path


# Defining and parsing the command-line arguments
parser = argparse.ArgumentParser(description='My program description')
# Paths must be passed in, not hardcoded
parser.add_argument('--output1-path',
                    type=str,
                    help='output 1 data')
parser.add_argument('--output2-path',
                    type=str,
                    help='output 2 data')
args = parser.parse_args()

print('Input arguments:')
print(args)

# Creating the directory where the output file is created (the directory
# may or may not exist).
Path(args.output1_path).parent.mkdir(parents=True, exist_ok=True)

print(f'Writing output 1 data to {args.output1_path}')
with open(args.output1_path, 'w') as output1_file:
    output1_file.write('line1')
    output1_file.write('line2')
    output1_file.write('line3')
    output1_file.write('line4')
    output1_file.write('line5')

print(f'Writing output 2 data to {args.output2_path}')
with open(args.output2_path, 'w') as output2_file:
    output2_file.write('lineA')
    output2_file.write('lineB')
    output2_file.write('lineC')
    output2_file.write('lineD')
    output2_file.write('lineE')
