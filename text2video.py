import torch
from diffusers import DiffusionPipeline, DPMSolverMultistepScheduler
from diffusers.utils import export_to_video
import imageio
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Initialize the video generation pipeline
pipe = DiffusionPipeline.from_pretrained("damo-vilab/text-to-video-ms-1.7b", torch_dtype=torch.float16, variant="fp16")
pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
pipe.enable_model_cpu_offload()
pipe.enable_vae_slicing()

def generate_video(prompt, negative_prompt, video_duration_seconds):
    num_frames = video_duration_seconds * 15
    video_frames = pipe(prompt, negative_prompt=negative_prompt, num_inference_steps=25, num_frames=num_frames).frames
    video_path = export_to_video(video_frames[0])
    return video_path

def display_video(video_path):
    video = imageio.mimread(video_path)
    fig = plt.figure(figsize=(4.2, 4.2))
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
    mov = []
    for i in range(len(video)):
        img = plt.imshow(video[i], animated=True)
        plt.axis('off')
        mov.append([img])
    anime = animation.ArtistAnimation(fig, mov, interval=100, repeat_delay=1000)
    plt.close()
    return anime
