from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os

def upload_to_gdrive(uploaded_file, label):
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)

    folder_id = 'YOUR_FOLDER_ID'  # Ganti dengan folder ID kamu

    file_drive = drive.CreateFile({
        'title': f"{label}_{uploaded_file.name}",
        'parents': [{"id": folder_id}]
    })
    file_drive.SetContentFile(uploaded_file.name)
    file_drive.Upload()