import torch

from utils.model_loader import load_models


def generate_json(prompt):

    _, tokenizer, model = load_models()

    messages = [
        {
            "role": "system",
            "content": "You are an AI Recruitment Agent. Return ONLY valid JSON. No markdown. No explanations. No extra text."
        },
        {
            "role": "user",
            "content": prompt
        }
    ]

    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )

    inputs = tokenizer(
        text,
        return_tensors="pt"
    ).to(model.device)

    input_length = inputs.input_ids.shape[1]

    with torch.no_grad():

        outputs = model.generate(
            **inputs,
            max_new_tokens=3000,
            do_sample=False,
            temperature=0.0,
            repetition_penalty=1.1,
            pad_token_id=tokenizer.eos_token_id
        )

    tokens = outputs[0][input_length:]

    response = tokenizer.decode(
        tokens,
        skip_special_tokens=True
    ).strip()

    return response