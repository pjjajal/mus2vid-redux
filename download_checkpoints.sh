#!/bin/sh


cd ./thirdparty/mullama/mullama || exit

mkdir ckpts

huggingface-cli login
huggingface-cli download mu-llama/MU-LLaMA --local-dir .