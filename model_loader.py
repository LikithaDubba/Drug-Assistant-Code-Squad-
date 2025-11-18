# backend/app/model_loader.py
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import os

class GraniteModel:
    def __init__(self, model_name="ibm-granite/granite-3.3-2b-instruct", device=None):
        self.model_name = model_name
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        # load tokenizer and model
        print(f"Loading model {model_name} to {self.device} (this can take minutes)...")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name)
        # move model to device
        self.model.to(self.device)
    def ask(self, prompt_or_messages, max_new_tokens=128):
        # support messages list or plain prompt
        if isinstance(prompt_or_messages, list):
            messages = prompt_or_messages
            # convert to chat template if tokenizer supports apply_chat_template
            inputs = self.tokenizer.apply_chat_template(
                messages,
                add_generation_prompt=True,
                tokenize=True,
                return_dict=True,
                return_tensors="pt",
            )
        else:
            messages = [{"role":"user","content": str(prompt_or_messages)}]
            inputs = self.tokenizer.apply_chat_template(
                messages,
                add_generation_prompt=True,
                tokenize=True,
                return_dict=True,
                return_tensors="pt",
            )
        inputs = {k: v.to(self.device) for k, v in inputs.items()}
        outputs = self.model.generate(**inputs, max_new_tokens=max_new_tokens)
        gen = self.tokenizer.decode(outputs[0][inputs["input_ids"].shape[-1]:])
        return gen
