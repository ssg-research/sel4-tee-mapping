#!/bin/python3
import argparse

# IMPORTANT: register lowercase name of all Trusted Applications here
ta_names = ['ta', 'ta2']

parser = argparse.ArgumentParser(description='Script to resize the dataport shared between TA and Attestation based on true binary size of the TA')
parser.add_argument('-s', '--spec', help='File path for CapDL specification', required=True)
parser.add_argument('-d', '--header', help='File path for C header specifying size of the dataport', required=True)
args = parser.parse_args()

def findall(p, s):
    i = s.find(p)
    while i != -1:
        yield i
        i = s.find(p, i+1)

spec = open(args.spec, 'r').read()
lines = open(args.header, 'r').readlines()

for ta_name in ta_names:
    keyword_frame = f'{ta_name}_group_bin'
    keyword_code = f'CDL_FrameFill_FileData "{keyword_frame}"'

    ta_code_page_count = len([i for i in findall(keyword_code, spec)])

    print(':: Found {} executable pages for TA "{}"'.format(ta_code_page_count, ta_name))

    try:
        index = [i for i, s in enumerate(lines) if '{}_BUFSIZE'.format(ta_name.upper()) in s][0]
    except:
        lines.append('')
        index = -1

    new_define = '#define {}_BUFSIZE {}\n'.format(ta_name.upper(), 4096*ta_code_page_count)
    lines[index] = new_define

open(args.header, 'w').writelines(lines)
