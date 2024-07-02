import warnings

import scipy
from transformers import AutoProcessor, MusicgenForConditionalGeneration

warnings.filterwarnings("ignore")

processor = AutoProcessor.from_pretrained("facebook/musicgen-small")
model = MusicgenForConditionalGeneration.from_pretrained("facebook/musicgen-small")

def changeConfig(guidance_scale, max_new_tokens, temperature):
    model.generation_config.guidance_scale = guidance_scale
    model.generation_config.max_new_tokens = max_new_tokens
    model.generation_config.temperature = temperature
    print(model.generation_config)

def getPrompt(prompt: str):
    return prompt.splitlines()

def gen(out_name, prompt, max_new_token=512):

    inputs = processor(
        text=getPrompt(prompt),
        padding=True,
        return_tensors="pt",
    )

    audio_values = model.generate(**inputs, max_new_tokens=max_new_token)
    sampling_rate = model.config.audio_encoder.sampling_rate
    scipy.io.wavfile.write(out_name + ".wav", rate=sampling_rate, data=audio_values[0, 0].numpy())

prompt = 'Title: "The Mysterious Disappearance of Flight 19: Uncovering the Truth Behind the Bermuda Triangle\'s Most Infamous Case"'
changeConfig(4.0, 256, 1.5)
gen("gen", prompt)
