from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from dotenv import load_dotenv
from bson import ObjectId
from fastapi import FastAPI, File, HTTPException, UploadFile
from pymongo.errors import DuplicateKeyError

from app.database import profiles_collection
from app.resume_service import extract_resume_text, parse_resume_text
from app.schemas import ProfileCreate, ProfileResponse


load_dotenv()

app = FastAPI(title="AI Career Companion API")

MAX_UPLOAD_BYTES = 10 * 1024 * 1024
ALLOWED_EXTENSIONS = {".pdf", ".docx"}
UPLOAD_DIR = Path(__file__).resolve().parents[1] / "uploads"


def profile_response(document):
    return {
        "id": str(document["_id"]),
        "full_name": document["full_name"],
        "email": document["email"],
        "education": document.get("education"),
        "target_role": document.get("target_role"),
        "created_at": document["created_at"],
        "resume_filename": document.get("resume_filename"),
        "parsed_resume": document.get("parsed_resume"),
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/api/profiles", response_model=ProfileResponse, status_code=201)
def create_profile(profile: ProfileCreate):
    profile_data = profile.model_dump(mode="json")
    profile_data["email"] = profile_data["email"].lower()
    profile_data["created_at"] = datetime.now(timezone.utc)

    try:
        result = profiles_collection.insert_one(profile_data)
    except DuplicateKeyError:
        raise HTTPException(
            status_code=409,
            detail="A profile with this email already exists",
        )

    saved_profile = profiles_collection.find_one({"_id": result.inserted_id})
    return profile_response(saved_profile)


@app.get("/api/profiles/{profile_id}", response_model=ProfileResponse)
def get_profile(profile_id: str):
    if not ObjectId.is_valid(profile_id):
        raise HTTPException(status_code=400, detail="Invalid profile ID")

    profile = profiles_collection.find_one({"_id": ObjectId(profile_id)})
    if profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")

    return profile_response(profile)


@app.post(
    "/api/profiles/{profile_id}/resume",
    response_model=ProfileResponse,
)
def upload_resume(profile_id: str, file: UploadFile = File(...)):
    if not ObjectId.is_valid(profile_id):
        raise HTTPException(status_code=400, detail="Invalid profile ID")

    profile = profiles_collection.find_one({"_id": ObjectId(profile_id)})
    if profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")

    original_filename = (file.filename or "").replace("\\", "/").split("/")[-1]
    extension = Path(original_filename).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=415, detail="Upload a PDF or DOCX file")

    file_bytes = file.file.read(MAX_UPLOAD_BYTES + 1)

    if not file_bytes:
        raise HTTPException(status_code=400, detail="The uploaded file is empty")

    if len(file_bytes) > MAX_UPLOAD_BYTES:
        raise HTTPException(status_code=413, detail="File exceeds the 10 MiB limit")

    if extension == ".pdf" and not file_bytes.startswith(b"%PDF-"):
        raise HTTPException(status_code=415, detail="File content is not a PDF")

    if extension == ".docx" and not file_bytes.startswith(b"PK"):
        raise HTTPException(status_code=415, detail="File content is not a DOCX")

    try:
        resume_text = extract_resume_text(file_bytes, extension)
    except Exception:
        raise HTTPException(status_code=422, detail="Could not read this resume")

    if not resume_text.strip():
        raise HTTPException(
            status_code=422,
            detail="No selectable text found; scanned resumes need OCR",
        )

    try:
        parsed_resume = parse_resume_text(resume_text)
    except RuntimeError as error:
        raise HTTPException(status_code=503, detail=str(error))
    except Exception as error:
        print(f"Gemini parse failure: {type(error).__name__}: {error}")
        raise HTTPException(
            status_code=502,
            detail="Gemini could not parse this resume",
        )

    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    stored_filename = f"{profile_id}_{uuid4().hex}{extension}"
    stored_path = UPLOAD_DIR / stored_filename

    try:
        stored_path.write_bytes(file_bytes)
        profiles_collection.update_one(
            {"_id": ObjectId(profile_id)},
            {
                "$set": {
                    "resume_filename": original_filename[:255],
                    "resume_storage_name": stored_filename,
                    "parsed_resume": parsed_resume.model_dump(mode="json"),
                }
            },
        )
    except Exception:
        stored_path.unlink(missing_ok=True)
        raise HTTPException(
            status_code=500,
            detail="Could not save the resume",
        )

    updated_profile = profiles_collection.find_one(
        {"_id": ObjectId(profile_id)}
    )
    return profile_response(updated_profile)