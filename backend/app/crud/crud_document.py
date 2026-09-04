from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.document import Document

async def create_document_record(db: AsyncSession, patient_id: int, uploaded_by: int, filename: str, file_path: str, file_type: str, file_size: int, description: str = None):
    db_obj = Document(
        patient_id=patient_id,
        uploaded_by=uploaded_by,
        filename=filename,
        file_path=file_path,
        file_type=file_type,
        file_size=file_size,
        description=description
    )
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj

async def get_all_documents(db: AsyncSession):
    result = await db.execute(select(Document))
    return result.scalars().all()

async def get_patient_documents(db: AsyncSession, patient_id: int):
    result = await db.execute(select(Document).where(Document.patient_id == patient_id))
    return result.scalars().all()

async def get_document(db: AsyncSession, doc_id: int):
    result = await db.execute(select(Document).where(Document.id == doc_id))
    return result.scalars().first()
