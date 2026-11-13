

```markdown
# M1.1 — Research and Technical Understanding

## Project problem

Students often need help turning their education, skills, projects, and experience into focused internship applications. The planned companion will help students understand their profiles, compare them with internship requirements, and prepare applications and interviews.

## Initial workflow

1. A student creates a profile.
2. The student uploads a PDF or DOCX resume.
3. The backend extracts selectable text.
4. Gemini returns resume details in a defined structure.
5. Pydantic validates the result before it is saved to MongoDB.
6. Future workflows can use the profile to match internships and prepare the student.

## Technology choices

- **FastAPI and Pydantic:** FastAPI exposes typed API routes, while Pydantic validates profile input and structured resume output. See the [FastAPI tutorial](https://fastapi.tiangolo.com/tutorial/).
- **MongoDB:** Stores student profiles and parsed resume fields as documents.
- **PyMuPDF and python-docx:** Extract text from PDFs and DOCX files. Scanned image-only PDFs need OCR, which is outside the current implementation.
- **Gemini structured output:** Requests resume information in the `ResumeData` shape. The application validates the response before saving it. Gemini supports structured output with Pydantic models, but the supported JSON Schema is a subset, so schemas must use compatible fields. See [Gemini structured outputs](https://ai.google.dev/gemini-api/docs/structured-output).
- **LangGraph and LangChain (planned):** LangGraph can coordinate stateful workflows made of nodes and transitions; LangChain can provide model and tool integrations. They are planned and are not currently wired into the backend. See the [LangGraph overview](https://langchain-ai.github.io/langgraph/).
- **ChromaDB (planned):** A future retrieval store for career resources and internship descriptions. It can store embeddings and metadata and retrieve relevant information. It is not part of the current running application. See [Chroma documentation](https://docs.trychroma.com/).

## Risks and safeguards

Resume data is personal. The local implementation limits accepted formats and file size, checks basic file signatures, generates storage filenames, and does not expose the upload folder as a public route. The Gemini key belongs in a local environment file and must not be committed.

Before production, add authentication and authorization, malware scanning, encryption and retention/deletion controls, and a user review step for extracted facts. Model output can be incomplete or incorrect, so students should be able to review parsed details. Scanned PDFs need OCR.