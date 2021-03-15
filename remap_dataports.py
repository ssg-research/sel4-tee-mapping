#!/bin/python3
import os
import argparse

parser = argparse.ArgumentParser(description='Script to map TA code pages into Attestation component\'s VSpace')
parser.add_argument('-s', '--spec', help='File path for C representation of CapDL specification', required=True)
args = parser.parse_args()

file_path = args.spec
ta_name = 'ta'
connection_name = 'ta_binary'

def findall(p, s):
    i = s.find(p)
    while i != -1:
        yield i
        i = s.find(p, i+1)

# Read in current spec
with open(file_path, 'r') as f:
    spec = f.read()

# 1. Find all code frames of the TA

# a. First retrieve all frames of the TA, later prune out irrelevant frames
#    Note that we can not just findall, because these frames will be mentioned
#    at other spots too.
nr_ta_frames = spec.count('.name = "frame_{}'.format(ta_name))
offset = 0
frame_indices = []
for _ in range(nr_ta_frames):
    i = spec.find('.name = "frame_{}'.format(ta_name), offset)
    frame_indices.append(i)
    offset = i + 1

# b. Loop over frame_indices and save indices of the ones with FileData
filedata_frame_indices = []
for i in frame_indices:
    post = spec[i:i+200]
    if post.find('CDL_FrameFill_FileData') != -1:
        filedata_frame_indices.append(i)

# c. Get object IDs of the code frames
code_obj_ids = []
for i in filedata_frame_indices:
    pre = spec[i-40:i]
    obj_id = pre[pre.find('[')+1:pre.find(']')]
    code_obj_ids.append(obj_id)

# 2. Find dataport Frame Objects
#dataport_frames = [i for i in findall('.name = "{}_data'.format(connection_name), spec)]
count_dataport_frames = spec.count('.name = "{}_data'.format(connection_name))
dataport_obj_ids = []
for i in range(count_dataport_frames):
    offset = spec.find('.name = "{}_data_{}_obj'.format(connection_name, i))
    pre = spec[offset-40:offset]
    obj_id = pre[pre.find('[')+1:pre.find(']')]
    dataport_obj_ids.append(obj_id)

assert len(code_obj_ids) >= len(dataport_obj_ids)

# 3. Find cap for dataport in the Attestation component

# a. First find index of start of Attestation capability group
index_attest_caps = spec.find('.name = "pt_attestation_group_bin')

# b. Find Attestation's FrameCaps for dataports
framecaps = [index_attest_caps + i for i in findall('/* {}_data'.format(connection_name), spec[index_attest_caps:])]
# Select only those that are part of Attestation capabilities
framecaps = framecaps[0:count_dataport_frames]

# 4. Insert obj_id for code frame into dataport caps
for i in range(len(dataport_obj_ids)):
    area = spec[framecaps[i]-16:framecaps[i]]
    area = area.replace(dataport_obj_ids[i], code_obj_ids[i])
    spec = spec[:framecaps[i]-16] + area + spec[framecaps[i]:]

# 5. Move capdl_spec.c to capdl_spec.c.old
os.rename(file_path, file_path + '.old')

# Write amended spec to capdl_spec.c
with open(file_path, 'w') as f:
    f.write(spec)
