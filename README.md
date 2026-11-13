# AI Career Companion

AI Career Companion helps students understand their career profile and prepare for internship applications.

## Milestone 1 status

Implemented:
- Create and retrieve student profiles using MongoDB.
- Upload PDF or DOCX resumes to a profile.
- Extract selectable resume text with PyMuPDF or python-docx.
- Parse extracted text into structured fields with Gemini and validate the result with Pydantic.

Designed for later milestones:
- React + Vite student interface.
- Six specialist agents orchestrated with LangGraph.
- Career-resource retrieval with ChromaDB.

The frontend and agent/RAG workflows are not implemented in this milestone.

## Technology

- Backend API: FastAPI, Uvicorn, Pydantic
- Database: MongoDB
- Resume text extraction: PyMuPDF and python-docx
- Resume parsing: Gemini API with structured output
- Planned frontend: React + Vite
- Planned orchestration and retrieval: LangGraph, LangChain, and ChromaDB

## Run locally on Windows

Requirements: Python 3.12+, MongoDB running locally, and a Gemini API key.

1. Start the MongoDB service.
2. Open PowerShell in the project folder and set up the backend:

   ```powershell
   cd backend
   py -3.12 -m venv .venv
   .\.venv\Scripts\Activate.ps1
   pip install -r requirements.txt