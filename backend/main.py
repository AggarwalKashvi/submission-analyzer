from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import uuid
from processor import process_csv

app = FastAPI()

# 🔓 ENABLE CORS (THIS IS THE KEY FIX)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # React app
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload")
async def upload_csv(file: UploadFile = File(...)):
    try:
        file_id = str(uuid.uuid4())

        input_path = f"{UPLOAD_DIR}/{file_id}.csv"
        output_path = f"{UPLOAD_DIR}/{file_id}_result.xlsx"

        with open(input_path, "wb") as f:
            f.write(await file.read())

        process_csv(input_path, output_path)

        return FileResponse(
            output_path,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            filename="submission_analysis.xlsx"
        )

    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Invalid CSV format or processing error"
        )
