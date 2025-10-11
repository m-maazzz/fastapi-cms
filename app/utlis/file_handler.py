import os
import uuid
from fastapi import UploadFile

UPLOAD_DIR = os.path.join(os.getcwd(), "uploads")

# Ensure uploads directory exists
os.makedirs(UPLOAD_DIR, exist_ok=True)

def save_upload_file(file: UploadFile, subfolder: str = "") -> str:
    """
    Saves an uploaded file and returns its relative URL (e.g., /uploads/blogs/filename.jpg)
    """
    # Create subfolder path (for better organization)
    folder_path = os.path.join(UPLOAD_DIR, subfolder)
    os.makedirs(folder_path, exist_ok=True)

    # Generate a unique file name
    file_ext = file.filename.split(".")[-1]
    file_name = f"{uuid.uuid4()}.{file_ext}"
    file_path = os.path.join(folder_path, file_name)

    # Save the file
    with open(file_path, "wb") as f:
        f.write(file.file.read())

    # Return relative URL for database or API response
    if subfolder:
        return f"/uploads/{subfolder}/{file_name}"
    return f"/uploads/{file_name}"
