from pathlib import Path
from uuid import uuid4

from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    UploadFile,
    status,
)
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.resume import (
    ResumeCreate,
    ResumeResponse,
    ResumeUpdate,
)
from app.services.resume_service import (
    create_resume,
    delete_resume,
    get_resume_by_id,
    get_resumes_by_user_id,
    update_resume,
)

router = APIRouter(
    prefix="/resumes",
    tags=["Resumes"],
)

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

ALLOWED_EXTENSIONS = {".pdf", ".docx"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

@router.post(
    "/upload",
    response_model=ResumeResponse,
    status_code=status.HTTP_201_CREATED,
)
async def upload_resume(
    user_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    """
    Upload a resume file and create its database record.
    """

    extension = Path(file.filename).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF and DOCX files are allowed.",
        )

    contents = await file.read()

    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File exceeds the maximum allowed size (10 MB).",
        )

    unique_filename = f"resume_{uuid4().hex}{extension}"

    file_path = UPLOAD_DIR / unique_filename

    try:
        with open(file_path, "wb") as buffer:
            buffer.write(contents)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to save uploaded file.",
        )

    resume_data = ResumeCreate(
        user_id=user_id,
        filename=file.filename,
        file_path=str(file_path),
        parsed_text=None,
    )

    return create_resume(db, resume_data)

@router.post(
    "/",
    response_model=ResumeResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_new_resume(
    resume: ResumeCreate,
    db: Session = Depends(get_db),
):
    return create_resume(db, resume)


@router.get(
    "/{resume_id}",
    response_model=ResumeResponse,
)
def read_resume(
    resume_id: int,
    db: Session = Depends(get_db),
):
    resume = get_resume_by_id(db, resume_id)

    if resume is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found",
        )

    return resume


@router.get(
    "/user/{user_id}",
    response_model=list[ResumeResponse],
)
def read_user_resumes(
    user_id: int,
    db: Session = Depends(get_db),
):
    return get_resumes_by_user_id(db, user_id)


@router.put(
    "/{resume_id}",
    response_model=ResumeResponse,
)
def edit_resume(
    resume_id: int,
    resume_data: ResumeUpdate,
    db: Session = Depends(get_db),
):
    resume = update_resume(
        db,
        resume_id,
        resume_data,
    )

    if resume is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found",
        )

    return resume


@router.delete(
    "/{resume_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def remove_resume(
    resume_id: int,
    db: Session = Depends(get_db),
):
    deleted = delete_resume(
        db,
        resume_id,
    )

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found",
        )