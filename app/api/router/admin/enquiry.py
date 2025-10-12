import csv
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from io import StringIO

from app.core.security import AuthService
from app.core.database import get_db
from app.crud.enquiry import ContactCRUD
from app.schemas.enquiry import ContactResponse,ContactCreate, ContactOut

auth_service = AuthService()
router = APIRouter(prefix="/contacts", tags=["enquiry admin"])


@router.get("/list", response_model=ContactResponse, summary="List All Enquiries")
def list_contacts(db: Session = Depends(get_db),current_user=Depends(auth_service.get_current_user)):
    contacts = ContactCRUD(db).get_all()
    return{
        "data": [ContactOut.model_validate(contact) for contact in contacts],
        "message": "Contacts fetched successfully"
    }
@router.get("/export",summary="Export Enquiries as CSV")
def export_contacts(db: Session = Depends(get_db), current_user=Depends(auth_service.get_current_user)):
    contacts = ContactCRUD(db).get_all()

    def generate():
        output = StringIO()
        writer = csv.writer(output)
        writer.writerow(["ID", "Name", "Email", "Phone", "Message", "Created At"])
        yield output.getvalue()  # Yield the header
        output.seek(0)
        output.truncate(0)

        for c in contacts:
            writer.writerow([c.id, c.name, c.email, c.phone, c.message, c.created_at.isoformat()])
            yield output.getvalue()
            output.seek(0)
            output.truncate(0)

    return StreamingResponse(
        generate(),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=contacts.csv"},
    )
