"""
AI Regulatory Compliance Copilot - FastAPI Backend
Integrated with enhanced pipeline services
"""

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import numpy as np
import io
import uuid
import datetime

# Import new integrated services
from services.pipeline import run_analysis as pipeline_run_analysis
from services.pdf_parser import extract_text_from_buffer
from services.chunking import split_into_clauses as split_clauses
from services.embeddings import generate_embeddings
from services.similarity_engine import compute_similarity_matrix
from services.classifier import classify_compliance, calculate_risk

app = FastAPI(title="ComplianceAI API", version="2.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for history
history_storage = []


class AnalysisRequest(BaseModel):
    threshold: float = 0.75
    use_ai: bool = False
    gemini_key: Optional[str] = None


class ClauseResult(BaseModel):
    clause: str
    regulatory_text: str
    policy_match: str
    similarity: float
    status: str
    risk: str
    full_reg: str
    full_policy: str
    explanation: str = ""


class AnalysisResponse(BaseModel):
    total_clauses: int
    compliant: int
    partial: int
    missing: int
    risk_score: int
    results: List[ClauseResult]


class HistoryItem(BaseModel):
    id: str
    timestamp: str
    reg_file_name: str
    policy_file_name: str
    threshold: float
    results: AnalysisResponse


class HistorySummary(BaseModel):
    id: str
    timestamp: str
    reg_file_name: str
    policy_file_name: str
    threshold: float
    total_clauses: int
    compliant: int
    partial: int
    missing: int
    risk_score: int


@app.get("/")
async def root():
    return {"message": "ComplianceAI API is running", "version": "2.0.0"}


@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "2.0.0"}


@app.get("/info")
async def api_info():
    """Get API information and available features"""
    from services.rag_explainer import check_api_configuration
    
    api_config = check_api_configuration()
    
    return {
        "name": "AI Regulatory Compliance Copilot",
        "version": "2.0.0",
        "ai_configured": api_config,
        "features": [
            "PDF text extraction",
            "Clause-level chunking",
            "Semantic similarity using SentenceTransformers",
            "Compliance classification (Fully Compliant, Partially Compliant, Not Addressed)",
            "AI-powered explanations via OpenAI/Gemini",
            "Analysis history tracking"
        ],
        "endpoints": {
            "/": "API root",
            "/health": "Health check",
            "/info": "API information",
            "/config": "AI configuration status",
            "/analyze": "Analyze documents (POST)",
            "/analyze/v2": "Enhanced analysis with AI explanations (POST)",
            "/history": "Get analysis history",
            "/history/{item_id}": "Get specific history item",
            "/history/{item_id}": "Delete specific history item",
            "/history": "Clear all history (DELETE)"
        }
    }


@app.get("/config")
async def get_config():
    """Get AI API configuration status"""
    from services.rag_explainer import check_api_configuration
    return check_api_configuration()


# History endpoints
@app.get("/history", response_model=List[HistorySummary])
async def get_history():
    """Get all history items (summary only)"""
    return [
        HistorySummary(
            id=item["id"],
            timestamp=item["timestamp"],
            reg_file_name=item["reg_file_name"],
            policy_file_name=item["policy_file_name"],
            threshold=item["threshold"],
            total_clauses=item["results"]["total_clauses"],
            compliant=item["results"]["compliant"],
            partial=item["results"]["partial"],
            missing=item["results"]["missing"],
            risk_score=item["results"]["risk_score"]
        )
        for item in history_storage
    ]


@app.get("/history/{item_id}", response_model=HistoryItem)
async def get_history_item(item_id: str):
    """Get a specific history item with full results"""
    for item in history_storage:
        if item["id"] == item_id:
            return HistoryItem(
                id=item["id"],
                timestamp=item["timestamp"],
                reg_file_name=item["reg_file_name"],
                policy_file_name=item["policy_file_name"],
                threshold=item["threshold"],
                results=item["results"]
            )
    raise HTTPException(status_code=404, detail="History item not found")


@app.delete("/history/{item_id}")
async def delete_history_item(item_id: str):
    """Delete a history item"""
    global history_storage
    history_storage = [item for item in history_storage if item["id"] != item_id]
    return {"status": "deleted", "id": item_id}


@app.delete("/history")
async def clear_history():
    """Clear all history"""
    global history_storage
    history_storage = []
    return {"status": "cleared"}


@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_documents(
    reg_file: UploadFile = File(...),
    policy_file: UploadFile = File(...),
    threshold: float = 0.75,
    use_ai: bool = False,
    gemini_key: Optional[str] = None
):
    """
    Analyze regulatory and policy documents for compliance
    (Original implementation for backward compatibility)
    """
    try:
        # Read PDF content as bytes
        reg_content = await reg_file.read()
        policy_content = await policy_file.read()
        
        # Create BytesIO objects for preprocessing
        reg_buffer = io.BytesIO(reg_content)
        policy_buffer = io.BytesIO(policy_content)
        
        # Extract text from PDFs
        reg_text = extract_text_from_buffer(reg_buffer)
        policy_text = extract_text_from_buffer(policy_buffer)
        
        # Split into clauses
        reg_clauses = split_clauses(reg_text)
        policy_clauses = split_clauses(policy_text)
        
        # If no clauses found with primary method, try alternative
        if not reg_clauses:
            from services.chunking import split_into_clauses as alt_split
            reg_clauses = alt_split(reg_text)
        if not policy_clauses:
            from services.chunking import split_into_clauses as alt_split
            policy_clauses = alt_split(policy_text)
        
        # Generate embeddings
        reg_embeddings = generate_embeddings(reg_clauses)
        policy_embeddings = generate_embeddings(policy_clauses)
        
        # Compute similarity
        similarities = compute_similarity_matrix(reg_embeddings, policy_embeddings)
        
        # Process results
        results = []
        compliant_count = 0
        partial_count = 0
        missing_count = 0
        
        for i, reg_clause in enumerate(reg_clauses):
            # Get similarity scores for this regulatory clause
            row = similarities[i]
            best_idx = row.argmax()
            similarity_score = float(row[best_idx])
            policy_clause = policy_clauses[best_idx]
            
            # Classify compliance
            if similarity_score > threshold:
                status = "Compliant"
            elif similarity_score > (threshold - 0.2):
                status = "Partial"
            else:
                status = "Missing"
            
            # Calculate risk
            if status == "Missing":
                risk = "High"
            elif status == "Partial":
                risk = "Medium"
            else:
                risk = "Low"
            
            # Count statuses
            if status == "Compliant":
                compliant_count += 1
            elif status == "Partial":
                partial_count += 1
            else:
                missing_count += 1
            
            # AI explanation (placeholder - would need Gemini API integration)
            explanation = ""
            if use_ai and gemini_key and status != "Compliant":
                explanation = "AI explanation requires Gemini API configuration"
            
            results.append(ClauseResult(
                clause=f"Clause {i+1}",
                regulatory_text=reg_clause[:200] + "..." if len(reg_clause) > 200 else reg_clause,
                policy_match=policy_clause[:200] + "..." if len(policy_clause) > 200 else policy_clause,
                similarity=round(similarity_score, 2),
                status=status,
                risk=risk,
                full_reg=reg_clause,
                full_policy=policy_clause,
                explanation=explanation
            ))
        
        # Calculate total risk score
        risk_score = missing_count * 2 + partial_count * 1
        
        analysis_response = AnalysisResponse(
            total_clauses=len(results),
            compliant=compliant_count,
            partial=partial_count,
            missing=missing_count,
            risk_score=risk_score,
            results=results
        )
        
        # Save to history
        history_item = {
            "id": str(uuid.uuid4()),
            "timestamp": datetime.datetime.now().isoformat(),
            "reg_file_name": reg_file.filename,
            "policy_file_name": policy_file.filename,
            "threshold": threshold,
            "results": analysis_response.dict()
        }
        history_storage.insert(0, history_item)
        
        return analysis_response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/analyze/v2")
async def analyze_documents_v2(
    reg_file: UploadFile = File(...),
    policy_file: UploadFile = File(...),
    use_ai: bool = False,
    gemini_key: Optional[str] = None
):
    """
    Enhanced analyze endpoint with AI-powered explanations
    Uses the new integrated pipeline services
    """
    try:
        # Run the enhanced analysis pipeline
        result = await pipeline_run_analysis(
            regulation_file=reg_file,
            policy_file=policy_file,
            use_ai=use_ai,
            gemini_key=gemini_key
        )
        
        # Convert to response format
        results = []
        for r in result["results"]:
            results.append(ClauseResult(
                clause=f"Clause {r.get('id', '')[:8]}",
                regulatory_text=r.get("regulatory_clause", ""),
                policy_match=r.get("matched_policy_clause", ""),
                similarity=r.get("similarity_score", 0),
                status=r.get("status", ""),
                risk=r.get("risk", ""),
                full_reg=r.get("full_regulatory_clause", ""),
                full_policy=r.get("full_policy_clause", ""),
                explanation=r.get("explanation", "")
            ))
        
        analysis_response = AnalysisResponse(
            total_clauses=result["total_clauses"],
            compliant=result["compliant"],
            partial=result["partial"],
            missing=result["missing"],
            risk_score=result["risk_score"],
            results=results
        )
        
        # Save to history
        history_item = {
            "id": result["id"],
            "timestamp": result["timestamp"],
            "reg_file_name": reg_file.filename,
            "policy_file_name": policy_file.filename,
            "threshold": 0.75,
            "results": analysis_response.dict()
        }
        history_storage.insert(0, history_item)
        
        return {
            "id": result["id"],
            "timestamp": result["timestamp"],
            "total_clauses": result["total_clauses"],
            "compliant": result["compliant"],
            "partial": result["partial"],
            "missing": result["missing"],
            "risk_score": result["risk_score"],
            "summary": result.get("summary", ""),
            "results": results
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
