from transformers import AutoModel, AutoTokenizer
from peft import PeftModel
import torch
import torch.nn.functional as F

# Load once on startup
base_model = AutoModel.from_pretrained("BAAI/bge-large-en-v1.5")
model = PeftModel.from_pretrained(base_model, "shashu2325/resume-job-matcher-lora")
tokenizer = AutoTokenizer.from_pretrained("BAAI/bge-large-en-v1.5")

def get_match_score(resume_text, job_text):
    # Tokenize
    resume_inputs = tokenizer(resume_text, return_tensors="pt", max_length=512, padding="max_length", truncation=True)
    job_inputs = tokenizer(job_text, return_tensors="pt", max_length=512, padding="max_length", truncation=True)

    # Embed
    with torch.no_grad():
        resume_outputs = model(**resume_inputs)
        job_outputs = model(**job_inputs)

        resume_emb = resume_outputs.last_hidden_state.mean(dim=1)
        job_emb = job_outputs.last_hidden_state.mean(dim=1)

        resume_emb = F.normalize(resume_emb, p=2, dim=1)
        job_emb = F.normalize(job_emb, p=2, dim=1)

        similarity = torch.sum(resume_emb * job_emb, dim=1)
        match_score = torch.sigmoid(similarity).item()

    return match_score