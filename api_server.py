from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from ai_defender import AIDefender
from ai_defender.pro_license import EnterpriseLicenseManager

app = FastAPI(title="AI Defender Cloud Security API", version="1.0.0")
license_mgr = EnterpriseLicenseManager()

# تحميل النموذج والمسبار المدرب مرة واحدة عند تشغيل السيرفر
model_id = "Qwen/Qwen2.5-0.5B-Instruct"
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(model_id, dtype=torch.float32)
model.eval()

defender = AIDefender(
    model=model,
    tokenizer=tokenizer,
    target_layer_index=-2,
    probe_weights_path="ai_defender/weights/qwen_0.5b_probe.pt"
)

class ScanRequest(BaseModel):
    prompt: str
    client_email: str

@app.post("/v1/scan")
def scan_endpoint(req: ScanRequest, x_api_key: str = Header(...)):
    if not license_mgr.verify_key(req.client_email, x_api_key):
        raise HTTPException(status_code=403, detail="Invalid or expired Enterprise License Key.")
    
    result = defender.scan_prompt(req.prompt)
    return {"protected_by": "AI Defender Pro", "result": result}
