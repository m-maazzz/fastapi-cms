from fastapi import FastAPI
from app.core.database import Base, engine
from app.api import routers
import os
from fastapi.staticfiles import StaticFiles


# Create tables (temporary for dev; use Alembic for production)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Portfolio API", version="1.0")

UPLOAD_DIR = os.path.join(os.getcwd(), "uploads")
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

@app.get("/")
def read_root():
    return {"message": "API is running 🚀"}

# Include all routers
for router in routers:
    print(f"Including router with prefix: {router.prefix}")  # Debug print
    app.include_router(router)