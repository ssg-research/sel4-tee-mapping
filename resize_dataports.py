#!/bin/python3

file_path_spec = 'build-x86/tee.cdl'
file_path_header = 'projects/camkes/apps/tee/include/buffer.h'
ta_name = 'ta'

keyword_start_caps = f'}}\npt_{ta_name}_group_bin'

with open(file_path_spec, 'r') as f:
    spec = f.read()

start = spec.find(keyword_start_caps)
end = start + spec[start+1:].find('}')
ta_code_page_count = spec[start:end].count('(RX)')

print(':: Found {} executable pages for TA "{}"'.format(ta_code_page_count, ta_name))

lines = open(file_path_header, 'r').readlines()
new_define = '#define {}_BUFSIZE {}'.format(ta_name.upper(), 4096*ta_code_page_count)
lines[-1] = new_define

open(file_path_header, 'w').writelines(lines)
