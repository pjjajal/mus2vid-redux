from thirdparty.mullama.mullama.data.utils import load_and_transform_audio_data
from thirdparty.mullama.mullama.util.misc import *
import thirdparty.mullama.mullama.llama as llama
from dataclasses import dataclass
from diffusers import AutoPipelineForText2Image
import torch


# This was just pulled from the inference.py file in the mullama directory.
@dataclass
class DefaultGenConfig:
    audio_weight: float = 1.5
    # prompt: str = "Describe the song. Listen to this song and describe the painting that come to mind when you listen to it. The painting has as person in it. Describe the rest of the painting."
    prompt: str = "Describe in detail the emotions in this music."
    cache_size: int = 100
    cache_t: float = 20.0
    cache_weight: float = 0.0
    max_gen_len: int = 1024
    gen_t: float = 0.6
    top_p: float = 0.8


class ImageGenerator:
    def __init__(self, default_config: DefaultGenConfig):
        self.model = llama.load(
            "thirdparty/mullama/mullama/ckpts/checkpoint.pth",
            llama_dir="thirdparty/mullama/mullama/ckpts/LLaMA",
            knn=True,
            knn_dir="thirdparty/mullama/mullama/ckpts",
        )
        self.model.eval()

        self.default_config = default_config

        self.pipeline = AutoPipelineForText2Image.from_pretrained(
            "stabilityai/sdxl-turbo", torch_dtype=torch.float16, variant="fp16"
        )
        self.pipeline = self.pipeline.to("cuda")

    def generate_prompt(self, audio_path: str):
        inputs = {}
        audio = load_and_transform_audio_data([audio_path])

        inputs["Audio"] = [audio, self.default_config.audio_weight]
        text_output = None
        prompts = [llama.format_prompt(self.default_config.prompt)]
        prompts = [self.model.tokenizer.encode(x, bos=True, eos=False) for x in prompts]

        with torch.cuda.amp.autocast():
            results = self.model.generate(
                inputs,
                prompts,
                max_gen_len=self.default_config.max_gen_len,
                temperature=self.default_config.gen_t,
                top_p=self.default_config.top_p,
                cache_size=self.default_config.cache_size,
                cache_t=self.default_config.cache_t,
                cache_weight=self.default_config.cache_weight,
            )
        text_output = results[0].strip()
        return text_output

    def generate_image(self, prompt: str):
        image = self.pipeline(prompt=prompt, guidance_scale=0.0, num_inference_steps=1).images[0]
        return image

    def __call__(self, audio_path: str):
        print("Generating SD prompt with:", self.default_config.prompt, "And audio:", audio_path)
        prompt = self.generate_prompt(audio_path)
        print("Generated SD prompt:", prompt)
        image = self.generate_image(prompt)
        return image


if __name__ == "__main__":
    default_config = DefaultGenConfig()
    generator = ImageGenerator(default_config)
    audio_path = "data/aist/mLH3.wav"

    image = generator(audio_path)
    image.save("output.png")

    print(generator.default_config.prompt)
    default_config.prompt = "Hello Wolrd"
    print(generator.default_config.prompt)