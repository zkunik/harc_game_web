#!/bin/bash
set -exuo pipefail

# Ubuntu 20.04 (bento Vagrant)

# Fix `bash: python: command not found`
sudo ln -s /usr/bin/python3 /usr/bin/python

# Install distutils as prerequisite to installing pip
sudo apt update
sudo apt install --yes python3-distutils

# Install pip
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python get-pip.py --user

# Install virtualenv
pip install virtualenv
