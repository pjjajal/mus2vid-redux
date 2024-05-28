#!/bin/sh

mkdir data

mkdir data/aist

cd data/aist || exit

wget -i https://aistdancedb.ongaaccel.jp/v1.0.0/data/all_music_wav_url.csv

