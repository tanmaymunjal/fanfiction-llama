import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

model_id = "openai/whisper-medium"
model = AutoModelForSpeechSeq2Seq.from_pretrained(
    model_id, torch_dtype=torch_dtype, use_safetensors=True
)

processor = AutoProcessor.from_pretrained(model_id)