from thirdparty.mullama.mullama.data.utils import load_and_transform_audio_data
from thirdparty.mullama.mullama.util.misc import *
import thirdparty.mullama.mullama.llama as llama


if __name__ == "__main__":
    model = llama.load(
        "thirdparty/mullama/mullama/ckpts/checkpoint.pth",
        llama_dir="thirdparty/mullama/mullama/ckpts/LLaMA",
        knn=False,
        knn_dir="thirdparty/mullama/mullama/ckpts",
    )
