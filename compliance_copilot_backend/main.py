
from fastapi import FastAPI, UploadFile
from services.pipeline import run_analysis

app = FastAPI(title="AI Compliance Copilot Backend")

@app.get("/")
def root():
    return {"message": "Compliance Copilot API running"}

@app.post("/analyze")
async def analyze(regulation: UploadFile, policy: UploadFile):
    result = await run_analysis(regulation, policy)
    return result
