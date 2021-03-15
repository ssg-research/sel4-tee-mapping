#!/bin/python3
import argparse

parser = argparse.ArgumentParser(description='Script to resize the dataport shared between TA and Attestation based on true binary size of the TA')
parser.add_argument('-s', '--spec', help='File path for CapDL specification', required=True)
parser.add_argument('-d', '--header', help='File path for C header specifying size of the dataport', required=True)
args = parser.parse_args()

file_path_spec = args.spec
file_path_header = args.header
ta_name = 'ta'

keyword_frame = f'{ta_name}_group_bin'
keyword_code = f'CDL_FrameFill_FileData "{keyword_frame}"'

def findall(p, s):
    i = s.find(p)
    while i != -1:
        yield i
        i = s.find(p, i+1)

with open(file_path_spec, 'r') as f:
    spec = f.read()

ta_code_page_count = len([i for i in findall(keyword_code, spec)])

print(':: Found {} executable pages for TA "{}"'.format(ta_code_page_count, ta_name))

lines = open(file_path_header, 'r').readlines()
new_define = '#define {}_BUFSIZE {}'.format(ta_name.upper(), 4096*ta_code_page_count)
lines[-1] = new_define

open(file_path_header, 'w').writelines(lines)
