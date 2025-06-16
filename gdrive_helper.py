import pandas as pd
import datetime
import json
import io
import streamlit as st
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from google.oauth2 import service_account

FOLDER_ID = "1tt57wZjDup4xaWhR9x3GrC_dV8IJ4t2Z"  # ID folder default di GDrive

def save_metadata_to_csv(food_name, region, taste, category, desc, gdrive_file_id):
    metadata = {
        "timestamp": datetime.datetime.now().isoformat(),
        "filename": f"{food_name.replace(' ', '_').lower()}_user.jpg",
        "label": food_name,
        "region": region,
        "taste": ", ".join(taste),
        "category": category,
        "description": desc,
        "gdrive_file_id": gdrive_file_id
    }

    df = pd.DataFrame([metadata])

    # Simpan ke temporary CSV
    tmp_path = "/tmp/metadata_upload.csv"
    df.to_csv(tmp_path, index=False)

    # Upload ke GDrive
    creds = service_account.Credentials.from_service_account_info(json.loads(st.secrets["service_account"]))
    service = build("drive", "v3", credentials=creds)

    media = MediaIoBaseUpload(open(tmp_path, "rb"), mimetype="text/csv")
    file_metadata = {
        "name": "upload_metadata.csv",
        "parents": [FOLDER_ID]
    }

    uploaded = service.files().create(
        body=file_metadata,
        media_body=media,
        fields="id"
    ).execute()

    return uploaded.get("id")

def upload_image_to_drive(file_bytes, filename: str, mimetype: str = "image/jpeg") -> str:
    creds = service_account.Credentials.from_service_account_info(json.loads(st.secrets["service_account"]))
    service = build("drive", "v3", credentials=creds)

    media = MediaIoBaseUpload(io.BytesIO(file_bytes), mimetype=mimetype)
    file_metadata = {
        "name": filename,
        "parents": [FOLDER_ID]
    }

    uploaded = service.files().create(
        body=file_metadata,
        media_body=media,
        fields="id"
    ).execute()

    return uploaded.get("id")
