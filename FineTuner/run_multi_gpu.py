import torch
from accelerate import PartialState
from huggingface_utils import asr_pipeline,model
from read_s3 import data

distributed_state = PartialState()
model.to(distributed_state.device)

with distributed_state.split_between_processes(data) as prompt:
    result = asr_pipeline(prompt[0])
    result.save(f"result_{prompt[1]}.txt")
