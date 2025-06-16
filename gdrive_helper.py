import pandas as pd
import datetime

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
