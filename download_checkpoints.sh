#!/bin/sh


cd ./thirdparty/mullama/mullama || exit

mkdir ckpts

cd ckpts || exit

huggingface-cli login
huggingface-cli download mu-llama/MU-LLaMA --local-dir .