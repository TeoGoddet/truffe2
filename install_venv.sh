#!/bin/bash

current_dir=$(dirname $(readlink -f "$0"))
cd $current_dir

rm -rf venv

python2 -m virtualenv venv

. venv/bin/activate
pip install -U pip
pip install -r truffe2/data/pip-reqs.txt
