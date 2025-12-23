"""
Pydantic Models for API
Data validation models for request/response
"""

from pydantic import BaseModel, Field
from typing import List, Optional


class ReviewRequest(BaseModel):
    """Request model for single review analysis"""
    review_text: str = Field(..., min_length=1, max_length=5000, description="Review text to analyze")


class ReviewResponse(BaseModel):
    """Response model for review analysis"""
    review_text: str
    sentiment_label: str = Field(..., description="Sentiment label: POSITIVE, NEGATIVE, or NEUTRAL")
    sentiment_score: float = Field(..., ge=0, le=1, description="Sentiment confidence score")
    theme: str = Field(..., description="Identified theme category")


class BatchReviewRequest(BaseModel):
    """Request model for batch review analysis"""
    reviews: List[str] = Field(..., min_items=1, max_items=100, description="List of review texts")


class BatchReviewResponse(BaseModel):
    """Response model for batch review analysis"""
    results: List[ReviewResponse]
    count: int


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    version: Optional[str] = "1.0.0"

