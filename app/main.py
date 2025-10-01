from fastapi import FastAPI
from app.core.database import Base, engine

# Create tables (later we’ll use Alembic instead of auto create)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Portfolio API", version="1.0")

@app.get("/")
def read_root():
    return {"message": "API is running 🚀"}
