from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.schemas.enquiry import ContactCreate, ContactOut, TestimonialCreate,TestimonialOut,TestimonialResponse
from app.core.database import get_db
from app.crud.enquiry import ContactCRUD
from fastapi import BackgroundTasks
from app.services.email_service import send_thank_you_email
from app.models.enquiry import Testimonial

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

@router.post("/testimonial", response_model=TestimonialResponse ,summary="Testimonial Submission")
def create_testimonial(
    testimonial: TestimonialCreate,
    db: Session = Depends(get_db)
):
    created= Testimonial(**testimonial.model_dump())
    db.add(created)
    db.commit()
    db.refresh(created)
    return TestimonialResponse(
        data=[TestimonialOut.model_validate(created)],
        message="Testimonial submitted successfully"
    )
    

@router.get("/testimonials", response_model=TestimonialResponse ,summary="List Approved Testimonials")
def list_testimonials(
    db: Session = Depends(get_db)
):
    testimonials = db.query(Testimonial).filter(Testimonial.is_approved == True).all()
    return TestimonialResponse(
        data=[TestimonialOut.model_validate(t) for t in testimonials],
        message="Testimonials fetched successfully"
    )