from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image, ExifTags
import io, hashlib, json, os

app = FastAPI(title="Device Image Analyzer API", version="0.1.0")

# Allow your Webflow domain later (e.g., https://yourdomain.com). For quick tests, "*" is fine.
origins_env = os.getenv("ALLOWED_ORIGINS", "*")
origins = [o.strip() for o in origins_env.split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if origins == ["*"] else origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_PATH = os.getenv("DATA_PATH", "data.json")

def load_local_data():
    try:
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/analyze")
async def analyze(file: UploadFile = File(...), label: str | None = Form(None)):
    content = await file.read()
    info = {}
    info["filename"] = file.filename
    info["content_type"] = file.content_type
    info["size_bytes"] = len(content)
    info["sha256"] = hashlib.sha256(content).hexdigest()

    # basic image info
    try:
        image = Image.open(io.BytesIO(content))
        info["width"], info["height"] = image.size
        exif_data = {}
        try:
            exif = image._getexif()
            if exif:
                for tag, value in exif.items():
                    decoded = ExifTags.TAGS.get(tag, tag)
                    exif_data[decoded] = str(value)
        except Exception:
            pass
        if exif_data:
            info["exif"] = exif_data
    except Exception:
        info["note"] = "Not an image or failed to parse as image."

    # local data lookup
    local_db = load_local_data()
    matched_label = label
    # Naive guess: try filename (without extension) as label if present in DB
    if not matched_label and file.filename:
        base = os.path.splitext(os.path.basename(file.filename))[0]
        if base in local_db:
            matched_label = base

    local_info = None
    if matched_label:
        local_info = local_db.get(matched_label)

    # Response
    return {
        "recognized_label": matched_label,  # TODO: replace with real model later
        "local_info": local_info,
        "meta": info,
        "message": "Stub recognition; plug your model or external API in analyze() to set recognized_label based on image content."
    }

@app.get("/local/{label}")
def get_local(label: str):
    db = load_local_data()
    return {"label": label, "data": db.get(label)}
