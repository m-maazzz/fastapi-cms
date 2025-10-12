from app.models.enquiry import ContactForm

class ContactCRUD:
    def __init__(self, db):
        self.db = db

    def create(self, data):
        contact = ContactForm(**data.model_dump())
        self.db.add(contact)
        self.db.commit()
        self.db.refresh(contact)
        return contact

    def get_all(self):
        return self.db.query(ContactForm).order_by(ContactForm.created_at.desc()).all()
