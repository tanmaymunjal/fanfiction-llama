import torch
import librosa
from transformers import pipeline


asr_pipeline = pipeline(
    "automatic-speech-recognition",
    model="openai/whisper-medium",
    torch_dtype=torch.float16,
    chunk_length_s=30,
    return_timestamps=False,
    use_safetensors = True
)

text_pipeline = pipeline(
    "question-answering",
    model="sarvamai/OpenHathi-7B-Hi-v0.1-Base",
    torch_dtype=torch.float16,
    use_safetensors = True
)
