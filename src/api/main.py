"""
FastAPI Application
API endpoints for sentiment and theme prediction
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.predict import predict_sentiment, predict_theme

app = FastAPI(
    title="Ethiopian Bank Reviews Analysis API",
    description="API for sentiment and thematic analysis of bank reviews",
    version="1.0.0"
)


class ReviewRequest(BaseModel):
    """Request model for single review"""
    review_text: str


class ReviewResponse(BaseModel):
    """Response model for review analysis"""
    review_text: str
    sentiment_label: str
    sentiment_score: float
    theme: str


class BatchReviewRequest(BaseModel):
    """Request model for batch reviews"""
    reviews: List[str]


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Ethiopian Bank Reviews Analysis API",
        "version": "1.0.0",
        "endpoints": {
            "/predict": "POST - Predict sentiment and theme for a single review",
            "/predict/batch": "POST - Predict sentiment and theme for multiple reviews",
            "/health": "GET - Health check"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


@app.post("/predict", response_model=ReviewResponse)
async def predict_single(request: ReviewRequest):
    """
    Predict sentiment and theme for a single review.
    
    Args:
        request: ReviewRequest with review_text
        
    Returns:
        ReviewResponse with predictions
    """
    try:
        sentiment_label, sentiment_score = predict_sentiment(request.review_text)
        theme = predict_theme(request.review_text)
        
        return ReviewResponse(
            review_text=request.review_text,
            sentiment_label=sentiment_label,
            sentiment_score=sentiment_score,
            theme=theme
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/predict/batch")
async def predict_batch_endpoint(request: BatchReviewRequest):
    """
    Predict sentiment and theme for multiple reviews.
    
    Args:
        request: BatchReviewRequest with list of reviews
        
    Returns:
        List of ReviewResponse objects
    """
    try:
        results = []
        for review_text in request.reviews:
            sentiment_label, sentiment_score = predict_sentiment(review_text)
            theme = predict_theme(review_text)
            results.append({
                "review_text": review_text,
                "sentiment_label": sentiment_label,
                "sentiment_score": sentiment_score,
                "theme": theme
            })
        return {"results": results, "count": len(results)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

