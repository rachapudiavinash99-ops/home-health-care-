from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
import os
import shutil
import uuid

from app.api import deps
from app.crud import crud_document, crud_patient
from app.schemas.document import DocumentResponse
from app.models.user import User

router = APIRouter()
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload", response_model=DocumentResponse)
async def upload_document(
    patient_id: int = Form(...),
    description: str = Form(None),
    file: UploadFile = File(...),
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.role_required(["DOCTOR", "ADMIN", "PATIENT"]))
) -> Any:
    # RBAC constraint
    if current_user.role.value == "PATIENT":
        patient = await crud_patient.get_patient_by_user_id(db, current_user.id)
        if not patient or patient.id != patient_id:
            raise HTTPException(status_code=403, detail="Not authorized")
            
    file_ext = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_ext}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    file_size = os.path.getsize(file_path)
    
    doc = await crud_document.create_document_record(
        db=db,
        patient_id=patient_id,
        uploaded_by=current_user.id,
        filename=file.filename,
        file_path=file_path,
        file_type=file.content_type,
        file_size=file_size,
        description=description
    )
    return doc

@router.get("/", response_model=List[DocumentResponse])
async def read_all_documents(
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.role_required(["DOCTOR", "ADMIN", "CAREGIVER", "NURSE"]))
) -> Any:
    docs = await crud_document.get_all_documents(db)
    return docs

@router.get("/patient/{patient_id}", response_model=List[DocumentResponse])
async def read_documents(
    patient_id: int,
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.role_required(["DOCTOR", "ADMIN", "CAREGIVER", "PATIENT"]))
) -> Any:
    if current_user.role.value == "PATIENT":
        patient = await crud_patient.get_patient_by_user_id(db, current_user.id)
        if not patient or patient.id != patient_id:
            raise HTTPException(status_code=403, detail="Not authorized")
            
    docs = await crud_document.get_patient_documents(db, patient_id=patient_id)
    return docs

@router.get("/download/{doc_id}")
async def download_document(
    doc_id: int,
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.role_required(["DOCTOR", "ADMIN", "CAREGIVER", "PATIENT"]))
):
    doc = await crud_document.get_document(db, doc_id=doc_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
        
    if current_user.role.value == "PATIENT":
        patient = await crud_patient.get_patient_by_user_id(db, current_user.id)
        if not patient or patient.id != doc.patient_id:
            raise HTTPException(status_code=403, detail="Not authorized")
            
    if not os.path.exists(doc.file_path):
        raise HTTPException(status_code=404, detail="File is missing on server")
        
    return FileResponse(path=doc.file_path, filename=doc.filename, media_type=doc.file_type)
