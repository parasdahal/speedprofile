#!/bin/bash
mkdir -p /output
python /speedprofile.py -p /output -b chrome -u "$@"
