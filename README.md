<!--
     Copyright 2021 Aalto University & University of Waterloo

     SPDX-License-Identifier: CC-BY-SA-4.0
-->

# seL4 CAmkES TEE mapping scripts

This repository contains the mapping scripts for the trusted execution environment (TEE)
proof-of-concept implementation for the project researching integrity protection of
remote attestation procedures in the case of confidentiality compromise of the TEE.

See the `sel4-tee` repo that contains the TEE implementation ([GitHub](https://github.com/ssg-research/sel4-tee)) to get started.

By setting up the project using `repo`, this repository should be pulled in and
initialized automatically.

The files in this repository have the following functions:

- `resize_dataports.py` determines the executable size of a TA and resizes the
  dataport in the Attestation component.
- `remap_dataports.py` manipulates an intermediate capDL representation of the
  capability distribution in the TEE to achieve a correct mapping.
- `compile.sh` interleaves the execution of these scripts into several rounds of
  compilation to solve the circular dependency described in the thesis.