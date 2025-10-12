from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.schemas.enquiry import ContactCreate, ContactOut
from app.core.database import get_db
from app.crud.enquiry import ContactCRUD
from fastapi import BackgroundTasks
from app.services.email_service import send_thank_you_email

router = APIRouter(prefix="/enquiry", tags=["enquiry"])


@router.post("/", response_model=ContactOut ,summary="Enquiry Form Submission")
def create_contact(
    contact: ContactCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    created = ContactCRUD(db).create(contact)

    # Send thank-you email in the background
    background_tasks.add_task(
        send_thank_you_email,
        name=contact.name,
        email=contact.email,
        message=contact.message
    )

    return created