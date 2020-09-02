#! /bin/bash

#copied from https://github.com/bricksdont/sockeye-toy-models/blob/gpu/scripts/download_install_packages.sh

scripts=`dirname "$0"`
base=$scripts/..

tools=$base/tools
mkdir -p $tools

echo "Make sure this script is executed AFTER you have activated a virtualenv"

# install Sockeye

# CUDA version on instance
CUDA_VERSION=102

## Method A: install from PyPi
pip install mxnet-cu101mkl
wget https://raw.github.com/DianaLaura/sockeye/master/requirements/requirements.gpu-cu102.txt
pip install sockeye --no-deps -r requirements.gpu-cu102.txt
rm requirements.gpu-cu102.txt

# install BPE library

pip install subword-nmt

# install sacrebleu for evaluation

pip install sacrebleu

# install Moses scripts for preprocessing

git clone https://github.com/bricksdont/moses-scripts $tools/moses-scripts

# install python packages

pip install lxml

pip install bs4

pip install tqdm
