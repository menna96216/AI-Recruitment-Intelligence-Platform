import torch
import streamlit as st

from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM
)

from sentence_transformers import SentenceTransformer


MODEL_NAME = "Qwen/Qwen2.5-3B-Instruct"


@st.cache_resource(show_spinner="Loading AI models...")
def load_models():

    embedding_model = SentenceTransformer(
        "BAAI/bge-small-en-v1.5"
    )

    tokenizer = AutoTokenizer.from_pretrained(
        MODEL_NAME,
        trust_remote_code=True
    )

    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
        device_map="auto",
        low_cpu_mem_usage=True,
        trust_remote_code=True
    )

    model.eval()

    return embedding_model, tokenizer, model


