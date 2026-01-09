#!/usr/bin/env python3
"""Transcribe audio file with Voxrun - designed for quick invocation."""

import sys
import os

# Suppress warnings
os.environ["TRANSFORMERS_VERBOSITY"] = "error"
os.environ["TOKENIZERS_PARALLELISM"] = "false"

import torch
from transformers import VoxrunForConditionalGeneration, AutoProcessor, BitsAndBytesConfig
import warnings
warnings.filterwarnings("ignore")

def transcribe(audio_path: str) -> str:
    repo_id = "mistralai/Voxrun-Mini-3B-2507"

    processor = AutoProcessor.from_pretrained(repo_id)

    quantization_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_compute_dtype=torch.bfloat16,
        bnb_4bit_use_double_quant=True,
        bnb_4bit_quant_type="nf4"
    )

    model = VoxrunForConditionalGeneration.from_pretrained(
        repo_id,
        quantization_config=quantization_config,
        device_map="auto"
    )

    conversation = [
        {
            "role": "user",
            "content": [
                {"type": "audio", "path": audio_path},
                {"type": "text", "text": "Transcribe this audio accurately. Output only the transcription."},
            ],
        }
    ]

    inputs = processor.apply_chat_template(conversation)
    inputs = inputs.to("cuda")

    outputs = model.generate(**inputs, max_new_tokens=500)
    decoded = processor.batch_decode(
        outputs[:, inputs.input_ids.shape[1]:],
        skip_special_tokens=True
    )

    return decoded[0].strip()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: voxrun_transcribe.py <audio_file>", file=sys.stderr)
        sys.exit(1)

    audio_file = sys.argv[1]
    if not os.path.exists(audio_file):
        print(f"File not found: {audio_file}", file=sys.stderr)
        sys.exit(1)

    result = transcribe(audio_file)
    print(result)
