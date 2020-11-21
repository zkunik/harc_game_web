#!/usr/bin/env python3
#-*- coding: utf-8 -*-

"""
convert_passwords passwords.csv

Converts passwords csv file in following format:
- tab separated file
- columns:
    DZIEŃ
    HASŁO DNIA
    TREŚĆ
    PODPOWIEDŹ

"""

import json, csv
import os, sys, argparse # params parser

# define expected input data columns
input_columns = ['DZIEŃ', 'HASŁO DNIA', 'TREŚĆ', 'PODPOWIEDŹ']

data_template = """{
    "model": "wotd.wordoftheday",
    "pk": 0,
    "fields": {
      "question": "",
      "hint": "",
      "answer": "",
      "date": ""
    }
  }"""

def replace_last(source_string, replace_what, replace_with):
    head, _sep, tail = source_string.rpartition(replace_what)
    return head + replace_with + tail


# Input parameters
parser = argparse.ArgumentParser(description="Convert passwords csv file to json.")
parser.add_argument('input_file', help="name of the input file (csv)")
parser.add_argument('--output_file', help="name of the out file (json)")
args = parser.parse_args()
if not args.output_file:
    if args.input_file.endswith('.csv'):
        args.output_file = replace_last(args.input_file, '.csv', '.json')
    else:
        args.output_file = args.input_file + '.json'
print(f"\nProcessing input file {args.input_file} to output file {args.output_file}")

# read input csv
with open(args.input_file, 'r') as input_file:
    input_data = list(csv.reader(input_file, delimiter='\t'))

    # verify input data columns
    if input_data[0] != input_columns:
        raise SystemExit(f"\nInput file has wrong format, expected columns: {input_columns}")

    # output json to file
    with open(args.output_file,'w') as f:

        f.write('[\n')
        pk = 1
        for row in input_data[1:]:
            data = json.loads(data_template)
            data['pk'] = pk
            data['fields']['question'] = row[input_columns.index('TREŚĆ')]
            data['fields']['hint'] = row[input_columns.index('PODPOWIEDŹ')]
            data['fields']['answer'] = row[input_columns.index('HASŁO DNIA')]
            data['fields']['date'] = row[input_columns.index('DZIEŃ')]
            if pk != 1:
                f.write(',\n')
            f.write(json.dumps(data, indent=4))
            pk += 1
        f.write('\n]')




