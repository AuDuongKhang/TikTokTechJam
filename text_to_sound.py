import scipy
from transformers import AutoProcessor, MusicgenForConditionalGeneration

processor = AutoProcessor.from_pretrained("facebook/musicgen-small")
model = MusicgenForConditionalGeneration.from_pretrained("facebook/musicgen-small")

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
    
    
prompt = "80s pop track with bassy drums and synth\n90s rock song with loud guitars and heavy drums"
gen("gen", prompt)