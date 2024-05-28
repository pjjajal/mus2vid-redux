# mus2vid-redux
a soirée into music-to-video/image generation.

(note: clone this repo with --recurse-submodules)
## setup

### environment setup
```sh
conda create -n mus2vid python=3.12
conda activate mus2vid
pip install -r requirements.txt
```

### data and checkpoints
```sh
$ ./download_checkpoints.sh # this requires a huggingface-cli token.
$ ./download_datasets.sh # this downloads the aist dataset to the data directory.
```

## running the app
### mullum + stable diffusion
```sh
python app.py --generator mullm # this runs the image generation with the mullm model
```

### debugging
```sh
python app.py --generator random --debug --item-registry --style-editor --resizable
```