#!/usr/bin/env python3
"""
Minimal FastAPI PRMSU Chatbot for Railway deployment
"""

import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import cohere
import re

# Environment variables
COHERE_API_KEY = os.getenv("COHERE_API_KEY", "m7uIZhmn9itLRlZmEvHVwIJ6nvJ0FU2zZ5vd40e9")
PORT = int(os.getenv("PORT", 8000))

# Initialize FastAPI app
app = FastAPI(
    title="PRMSU Student Handbook Chatbot",
    description="AI-powered chatbot for PRMSU student handbook questions",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Cohere client
cohere_client = cohere.Client(COHERE_API_KEY)

# PRMSU Knowledge Base (embedded directly)
PRMSU_KNOWLEDGE = {
    "prmsu_stands_for": "PRMSU stands for President Ramon Magsaysay State University. The main campus is located in Iba, Zambales, Philippines.",
    "establishment": "PRMSU was officially established through Republic Act No. 11015 on April 20, 2018.",
    "campuses": "PRMSU has seven (7) campuses throughout Zambales province.",
    "vision": "To be a premier state university in the ASEAN region committed to total human development for a progressive society.",
    "mission": "PRMSU is committed to provide quality and relevant education through instruction, research, extension, and production services.",
    "admission_requirements": "Admission requirements include: completed application form, high school diploma or equivalent, transcript of records, certificate of good moral character, medical certificate, and entrance examination results.",
    "grading_system": "PRMSU uses a 5.0 grading system where 1.0 is the highest grade and 5.0 is failing. The passing grade is 3.0.",
    "scholarship_private": "Private scholarship applicants at PRMSU must maintain a minimum General Weighted Average (GWA) of 1.75. Additional conditions include: being officially enrolled, demonstrating good moral character, and having no failing or incomplete grades.",
    "graduation_honors": "Three honors are awarded: Summa Cum Laude (1.0-1.25 GWA, no grade below 1.5), Magna Cum Laude (1.26-1.5 GWA, no grade below 1.75), and Cum Laude (1.51-1.75 GWA, no grade below 2.0).",
    "uniform_policy": "Students must wear prescribed uniforms. Male students: white polo shirt, black pants, black shoes. Female students: white blouse, black skirt/pants, black shoes.",
    "liquor_first_offense": "First offense for liquor violations: 15 days suspension, 12 hours transformative experience, mandatory guidance intervention.",
    "liquor_second_offense": "Second offense for liquor violations: 30 days suspension, 24 hours transformative experience, continued guidance intervention.",
    "liquor_third_offense": "Third offense for liquor violations: One-year suspension from the university.",
    "student_assistant_hours": "Student assistants work a maximum of 100 hours per month. In a typical 4-month semester, this equals approximately 400 hours per semester.",
    "deficiency_clearance": "All deficiencies must be cleared three (3) working days before the University-wide Academic Council meeting.",
    "cross_enrollment_types": "PRMSU recognizes four types of cross-enrollment: inbound regular, inbound irregular, outbound regular, and outbound irregular.",
    "transferee_honors": "For transferees to graduate with honors, they must: complete all academic units at PRMSU, carry regular academic load, finish within prescribed time, and have no failing/incomplete grades or disciplinary violations."
}

# Request/Response models
class ChatRequest(BaseModel):
    question: str
    max_results: Optional[int] = 5

class ChatResponse(BaseModel):
    question: str
    answer: str
    sources_used: int
    response_time: float

def validate_prmsu_relevance(question: str) -> bool:
    """Validate if question is PRMSU-related."""
    question_lower = question.lower()
    
    # Check for non-PRMSU patterns first
    non_prmsu_patterns = [
        r'\d+\s*[\+\-\*\/]\s*\d+',  # Math operations
        r'what\s+is\s+\d+\s*[\+\-\*\/]',  # Math questions
        r'weather|temperature|climate',
        r'cooking|recipe|food',
        r'movie|music|celebrity',
        r'programming|code|software',
        r'health|medical|doctor'
    ]
    
    for pattern in non_prmsu_patterns:
        if re.search(pattern, question_lower):
            return False
    
    # Check for PRMSU-related keywords
    prmsu_keywords = [
        'prmsu', 'president ramon magsaysay', 'magsaysay', 'university',
        'student', 'academic', 'enrollment', 'admission', 'scholarship',
        'grade', 'gwa', 'graduation', 'uniform', 'campus', 'college'
    ]
    
    return any(keyword in question_lower for keyword in prmsu_keywords)

def search_knowledge_base(question: str):
    """Search the embedded knowledge base."""
    question_lower = question.lower()
    relevant_info = []
    
    # Simple keyword matching
    if any(word in question_lower for word in ['stands for', 'acronym', 'what does', 'what is prmsu']):
        relevant_info.append(PRMSU_KNOWLEDGE["prmsu_stands_for"])
    
    if 'establishment' in question_lower or 'established' in question_lower or 'founded' in question_lower:
        relevant_info.append(PRMSU_KNOWLEDGE["establishment"])
    
    if 'campus' in question_lower and 'how many' in question_lower:
        relevant_info.append(PRMSU_KNOWLEDGE["campuses"])
    
    if 'vision' in question_lower:
        relevant_info.append(PRMSU_KNOWLEDGE["vision"])
    
    if 'mission' in question_lower:
        relevant_info.append(PRMSU_KNOWLEDGE["mission"])
    
    if 'admission' in question_lower:
        relevant_info.append(PRMSU_KNOWLEDGE["admission_requirements"])
    
    if 'grading' in question_lower or 'grade system' in question_lower:
        relevant_info.append(PRMSU_KNOWLEDGE["grading_system"])
    
    if 'scholarship' in question_lower and 'private' in question_lower:
        relevant_info.append(PRMSU_KNOWLEDGE["scholarship_private"])
    
    if 'honors' in question_lower or 'cum laude' in question_lower:
        relevant_info.append(PRMSU_KNOWLEDGE["graduation_honors"])
    
    if 'uniform' in question_lower:
        relevant_info.append(PRMSU_KNOWLEDGE["uniform_policy"])
    
    if 'liquor' in question_lower:
        if 'first' in question_lower:
            relevant_info.append(PRMSU_KNOWLEDGE["liquor_first_offense"])
        elif 'second' in question_lower:
            relevant_info.append(PRMSU_KNOWLEDGE["liquor_second_offense"])
        elif 'third' in question_lower:
            relevant_info.append(PRMSU_KNOWLEDGE["liquor_third_offense"])
        else:
            relevant_info.extend([
                PRMSU_KNOWLEDGE["liquor_first_offense"],
                PRMSU_KNOWLEDGE["liquor_second_offense"],
                PRMSU_KNOWLEDGE["liquor_third_offense"]
            ])
    
    if 'student assistant' in question_lower and 'hours' in question_lower:
        relevant_info.append(PRMSU_KNOWLEDGE["student_assistant_hours"])
    
    if 'deficiencies' in question_lower and 'cleared' in question_lower:
        relevant_info.append(PRMSU_KNOWLEDGE["deficiency_clearance"])
    
    if 'cross' in question_lower and 'enrollment' in question_lower:
        relevant_info.append(PRMSU_KNOWLEDGE["cross_enrollment_types"])
    
    if 'transferee' in question_lower and 'honors' in question_lower:
        relevant_info.append(PRMSU_KNOWLEDGE["transferee_honors"])
    
    return relevant_info

def format_response(answer: str, question: str) -> str:
    """Format response with emojis and structure."""
    question_lower = question.lower()
    
    if any(word in question_lower for word in ['stands for', 'acronym', 'what does']):
        return f"🏫 **PRMSU Information:**\n{answer}"
    elif 'scholarship' in question_lower:
        return f"💰 **Scholarship Information:**\n{answer}"
    elif 'uniform' in question_lower:
        return f"👔 **Uniform Policy:**\n{answer}"
    elif 'liquor' in question_lower or 'penalty' in question_lower:
        return f"⚖️ **Disciplinary Policy:**\n{answer}"
    elif 'admission' in question_lower:
        return f"📝 **Admission Information:**\n{answer}"
    elif 'grade' in question_lower or 'gwa' in question_lower:
        return f"📊 **Academic Information:**\n{answer}"
    elif 'graduation' in question_lower or 'honors' in question_lower:
        return f"🎓 **Graduation Information:**\n{answer}"
    else:
        return f"📚 **PRMSU Student Handbook:**\n{answer}"

@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "PRMSU Student Handbook Chatbot API",
        "version": "1.0.0",
        "endpoints": {
            "chat": "POST /chat - Ask questions about PRMSU",
            "health": "GET /health - Health check",
            "docs": "GET /docs - API documentation"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "PRMSU Chatbot",
        "knowledge_base": "embedded",
        "total_topics": len(PRMSU_KNOWLEDGE)
    }

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Main chat endpoint."""
    import time
    start_time = time.time()
    
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    
    # Validate PRMSU relevance
    if not validate_prmsu_relevance(request.question):
        answer = """🚫 **Sorry, I can only answer questions related to PRMSU (President Ramon Magsaysay State University) student handbook.**

I cannot help with:
• Math calculations or general knowledge
• Weather, news, or entertainment topics
• Other universities or non-academic subjects
• Personal advice or general information

Please ask about:
• PRMSU policies and regulations
• Academic requirements and procedures
• Student services and programs
• University information and guidelines

**Example questions:**
• 'What does PRMSU stand for?'
• 'What are the admission requirements?'
• 'What is the grading system?'"""
        
        return ChatResponse(
            question=request.question,
            answer=answer,
            sources_used=0,
            response_time=time.time() - start_time
        )
    
    # Search knowledge base
    relevant_info = search_knowledge_base(request.question)
    
    if not relevant_info:
        answer = "I don't have specific information about that topic in my PRMSU student handbook database. Please try asking about admission requirements, grading system, scholarships, uniforms, or other university policies."
    else:
        # Use the most relevant information
        answer = relevant_info[0]
    
    # Format response
    formatted_answer = format_response(answer, request.question)
    
    return ChatResponse(
        question=request.question,
        answer=formatted_answer,
        sources_used=len(relevant_info),
        response_time=time.time() - start_time
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT)
