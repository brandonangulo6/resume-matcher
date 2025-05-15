from transformers import AutoModel, AutoTokenizer
from peft import PeftModel
import torch
import torch.nn.functional as F

# Load once on startup
base_model = AutoModel.from_pretrained("BAAI/bge-large-en-v1.5")
model = PeftModel.from_pretrained(base_model, "shashu2325/resume-job-matcher-lora")
tokenizer = AutoTokenizer.from_pretrained("BAAI/bge-large-en-v1.5")

def get_embedding(text):
    inputs = tokenizer(text, return_tensors="pt", max_length=512, padding="max_length", truncation=True)
    with torch.no_grad():
        outputs = model(**inputs)
        emb = outputs.last_hidden_state.mean(dim=1)
        emb = F.normalize(emb, p=2, dim=1)
    return emb

def get_match_score(resume_text, job_text):
    resume_emb = get_embedding(resume_text)
    job_emb = get_embedding(job_text)
    similarity = torch.sum(resume_emb * job_emb, dim=1)
    match_score = torch.sigmoid(similarity).item()
    return match_score