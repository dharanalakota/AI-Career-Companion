# M1.2 — System Architecture

## Component diagram

```mermaid
flowchart LR
    Student --> Web[React + Vite frontend — planned]
    Web -. planned API calls .-> API[FastAPI]
    Student --> API
    API --> Profiles[Profile routes]
    Profiles --> Mongo[(MongoDB profiles)]
    API --> Upload[Resume upload validation]
    Upload --> Storage[Private local uploads folder]
    Upload --> Extract[PyMuPDF / python-docx]
    Extract --> Gemini[Gemini structured parsing]
    Gemini --> Validate[Pydantic ResumeData validation]
    Validate --> Mongo
    Orchestrator[LangGraph orchestration — planned] -. future workflows .-> API
    Orchestrator -. planned retrieval .-> Chroma[ChromaDB career resources]