import os
from openai import OpenAI
from config import Config
from helpers.prompt_builder import build_system_prompt

# Pastikan API key terbaca
os.environ["OPENAI_API_KEY"] = Config.OPENROUTER_API_KEY

# Bangun system prompt dari data wisata
system_prompt = build_system_prompt()

def chat(user_prompt, model, max_tokens=200, temp=0.7):
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1"
    )

    completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=temp,
        max_tokens=max_tokens
    )

    # LANGSUNG BALIKIN TEKS (TIDAK STREAM)
    return completion.choices[0].message.content
