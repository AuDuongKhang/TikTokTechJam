import warnings

import scipy
from transformers import AutoProcessor, MusicgenForConditionalGeneration

warnings.filterwarnings("ignore")

processor = AutoProcessor.from_pretrained("facebook/musicgen-small")
model = MusicgenForConditionalGeneration.from_pretrained("facebook/musicgen-small")

def changeConfig(guidance_scale=4.0, max_new_tokens=256, temperature=1.5):
    model.generation_config.guidance_scale = guidance_scale
    model.generation_config.max_new_tokens = max_new_tokens
    model.generation_config.temperature = temperature
    print(model.generation_config)

def getPrompt(prompt: str):
    return prompt.splitlines()

def gen(out_name, prompt, max_token=256):
    changeConfig()
    inputs = processor(
        text=getPrompt(prompt),
        padding=True,
        return_tensors="pt",
    )

    audio_values = model.generate(**inputs, max_new_tokens=max_token)
    sampling_rate = model.config.audio_encoder.sampling_rate
    scipy.io.wavfile.write(out_name, rate=sampling_rate, data=audio_values[0, 0].numpy())
