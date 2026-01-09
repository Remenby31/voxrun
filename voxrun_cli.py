#!/usr/bin/env python3
"""Interactive CLI for Voxrun Mini 3B model."""

import argparse
import sys
import torch
from transformers import VoxrunForConditionalGeneration, AutoProcessor, BitsAndBytesConfig

# Global model and processor
model = None
processor = None

def load_model():
    """Load the Voxrun model."""
    global model, processor

    print("Loading Voxrun Mini 3B...")
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

    print(f"Model loaded! Memory: {model.get_memory_footprint() / 1024**3:.2f} GB")


def transcribe(audio_path: str, prompt: str = "Transcribe this audio.") -> str:
    """Transcribe or analyze audio."""
    conversation = [
        {
            "role": "user",
            "content": [
                {"type": "audio", "path": audio_path},
                {"type": "text", "text": prompt},
            ],
        }
    ]

    inputs = processor.apply_chat_template(conversation)
    inputs = inputs.to("cuda")

    outputs = model.generate(**inputs, max_new_tokens=1000)
    decoded = processor.batch_decode(
        outputs[:, inputs.input_ids.shape[1]:],
        skip_special_tokens=True
    )

    return decoded[0]


def chat(text: str) -> str:
    """Text-only chat."""
    conversation = [
        {
            "role": "user",
            "content": [{"type": "text", "text": text}],
        }
    ]

    inputs = processor.apply_chat_template(conversation)
    inputs = inputs.to("cuda")

    outputs = model.generate(**inputs, max_new_tokens=1000)
    decoded = processor.batch_decode(
        outputs[:, inputs.input_ids.shape[1]:],
        skip_special_tokens=True
    )

    return decoded[0]


def interactive_mode():
    """Run interactive session."""
    print("\n=== Voxrun Interactive Mode ===")
    print("Commands:")
    print("  /audio <path> [prompt]  - Analyze audio file")
    print("  /quit                   - Exit")
    print("  <text>                  - Chat with the model")
    print("=" * 35)

    while True:
        try:
            user_input = input("\n> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not user_input:
            continue

        if user_input.lower() == "/quit":
            print("Goodbye!")
            break

        if user_input.startswith("/audio "):
            parts = user_input[7:].split(" ", 1)
            audio_path = parts[0]
            prompt = parts[1] if len(parts) > 1 else "Transcribe this audio."

            print(f"Processing: {audio_path}")
            try:
                result = transcribe(audio_path, prompt)
                print(f"\n{result}")
            except Exception as e:
                print(f"Error: {e}")
        else:
            try:
                result = chat(user_input)
                print(f"\n{result}")
            except Exception as e:
                print(f"Error: {e}")


def main():
    parser = argparse.ArgumentParser(description="Voxrun Mini 3B CLI")
    parser.add_argument("--audio", "-a", help="Audio file to transcribe/analyze")
    parser.add_argument("--prompt", "-p", default="Transcribe this audio.",
                        help="Prompt for audio analysis")
    parser.add_argument("--text", "-t", help="Text-only query")
    parser.add_argument("--interactive", "-i", action="store_true",
                        help="Interactive mode")

    args = parser.parse_args()

    load_model()

    if args.interactive:
        interactive_mode()
    elif args.audio:
        result = transcribe(args.audio, args.prompt)
        print(result)
    elif args.text:
        result = chat(args.text)
        print(result)
    else:
        interactive_mode()


if __name__ == "__main__":
    main()
