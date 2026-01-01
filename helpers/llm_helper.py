from openai import OpenAI
import os
from helpers.prompt_builder import build_system_prompt

system_prompt = build_system_prompt()

def chat(user_prompt, model, max_tokens=200, temp=0.7):
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError("OPENAI_API_KEY tidak ditemukan di Environment Variable")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key
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

    return completion.choices[0].message.content
