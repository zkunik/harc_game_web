#!/usr/bin/env python3
#-*- coding: utf-8 -*-

"""
convert_tasks tasks.csv

Converts tasks csv file in following format:
- tab separated file
- columns:
    KATEGORIA
    NAZWA
    OPIS
    JAK CZĘSTO
    NAGRODA
    NAGRODA SPECJALNA

"""

import json, csv
import os, sys, argparse # params parser

# define expected input data columns
input_columns = ['KATEGORIA', 'NAZWA', 'OPIS', 'JAK CZĘSTO', 'NAGRODA', 'NAGRODA SPECJALNA']

data_template = """{
    "model": "tasks.task",
    "pk": 0,
    "fields": {
      "name": "",
      "description": "",
      "allowed_completition_frequency": "",
      "prize": 0,
      "extra_prize": ""
    }
}"""

def replace_last(source_string, replace_what, replace_with):
    head, _sep, tail = source_string.rpartition(replace_what)
    return head + replace_with + tail


# Input parameters
parser = argparse.ArgumentParser(description="Convert tasks csv file to json.")
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
            data['fields']['name'] = row[input_columns.index('NAZWA')]
            data['fields']['description'] = row[input_columns.index('OPIS')]
            data['fields']['allowed_completition_frequency'] = row[input_columns.index('JAK CZĘSTO')]
            data['fields']['prize'] = row[input_columns.index('NAGRODA')]
            try:
                data['fields']['extra_prize'] = row[input_columns.index('NAGRODA SPECJALNA')]
            except IndexError:
                # There is no extra prize
                data['fields']['extra_prize'] = None
            if pk != 1:
                f.write(',\n')
            f.write(json.dumps(data, indent=4))
            pk += 1
        f.write('\n]')




