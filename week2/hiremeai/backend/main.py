
import json
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from groq import Groq

from resume_parser import read_pdf, parse_resume

load_dotenv()

# PDF stored in the same folder as main.py
PDF_PATH = Path(__file__).parent / "FaizanKhan1 (2) (1)-1.pdf"

app = FastAPI(
    title="HireMeAI",
    description="AI-powered Resume Parser and Chat Assistant",
    version="1.0.0"
)


class ChatRequest(BaseModel):
    question: str


@app.get("/")
def home():
    return {
        "message": "HireMeAI is running!",
        "status": "online",
        "docs": "/docs",
        "endpoints": ["/chat", "/parse-resume"]
    }


# Chat with the candidate using resume text
@app.post("/chat")
def chat(request: ChatRequest):
    if not PDF_PATH.is_file():
        raise HTTPException(
            status_code=404,
            detail=f"Resume PDF not found: {PDF_PATH.name}"
        )

    try:
        resume_text = read_pdf(PDF_PATH)
        answer = ask_candidate(request.question, resume_text)

        return {"answer": answer}

    except HTTPException:
        raise
    except Exception as error:
        print(f"Chat error: {error}")
        raise HTTPException(
            status_code=500,
            detail="Failed to generate an answer. Check server logs."
        )


# Upload a PDF and convert its content into structured JSON
@app.post("/parse-resume")
async def upload_resume(file: UploadFile = File(...)):
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Please upload a PDF resume."
        )

    try:
        pdf_bytes = await file.read()

        if not pdf_bytes:
            raise HTTPException(
                status_code=400,
                detail="The uploaded file is empty."
            )

        resume_data = parse_resume(pdf_bytes)

        return JSONResponse(
            content={
                "message": "Resume parsed successfully!",
                "filename": file.filename,
                "resume": resume_data
            }
        )

    except HTTPException:
        raise
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error))
    except Exception as error:
        print(f"Resume parsing error: {error}")
        raise HTTPException(
            status_code=500,
            detail="Resume parsing failed. Check server logs."
        )


# Generate an answer based only on the candidate's resume
def ask_candidate(question: str, resume_text: str) -> str:
    client = Groq()

    system_prompt = f"""
You are HireMeAI, Faizan Khan's personal AI assistant.

IMPORTANT:
- You are an AI assistant, NOT Faizan.
- Never speak as if you are Faizan.
- Answer questions about Faizan using ONLY the resume below.
- Do not assume that a skill means practical experience.
- Do not invent projects, responsibilities, tools, or achievements.
- If a skill is listed but practical experience is not described,
  explicitly say that the resume lists the skill but does not
  provide details of hands-on experience.
- If the resume does not mention something, say:
  "I couldn't find that information in Faizan's resume."
- Be concise, factual, and professional.

RESUME:
{resume_text}

RULES:
1. Answer the interviewer's question using the resume.
2. Never invent skills, experience, achievements, or qualifications.
3. If the resume does not contain the answer, clearly say
   that the information is not mentioned in the resume.
4. Answer professionally and naturally in first person when appropriate.
5. Keep answers relevant and concise.
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question}
        ],
        temperature=0.2
    )

    answer = response.choices[0].message.content

    if not answer:
        raise ValueError("The AI returned an empty response.")

    return answer.strip()
