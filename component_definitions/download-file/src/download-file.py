#!/usr/bin/env python3
import argparse
from pathlib import Path
import requests


# Defining and parsing the command-line arguments
parser = argparse.ArgumentParser(description='Download file from public HTTP/S URL')
# Paths must be passed in, not hardcoded
parser.add_argument('--file-url',
                    type=str,
                    help='Public URL of file to download')
parser.add_argument('--output1-path',
                    type=str,
                    help='Path of the local file where the Output 1 data should be written.')
args = parser.parse_args()

print(f'Program arguments: {args}')

# Creating the directory where the output file is created (the directory
# may or may not exist).
Path(args.output1_path).parent.mkdir(parents=True, exist_ok=True)

response = requests.get(url=args.file_url)
if response.status_code == 200:
    with open(args.output1_path, 'wb') as output1_file:
        output1_file.write(response.content)
else:
    raise RuntimeError(f'Download of {args.file_url} returned HTTP status code {response.status_code}')
