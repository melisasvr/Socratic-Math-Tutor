import base64
import json
import re


def encode_image(uploaded_file):
    bytes_data = uploaded_file.read()
    b64 = base64.b64encode(bytes_data).decode("utf-8")
    ext = uploaded_file.name.split(".")[-1].lower()
    media_type = {
        "jpg": "image/jpeg",
        "jpeg": "image/jpeg",
        "png": "image/png",
        "webp": "image/webp",
    }.get(ext, "image/png")
    return b64, media_type


def extract_bold_question(text: str):
    match = re.search(r"\*\*(.+?\?)\*\*", text)
    return match.group(1) if match else None


def is_solution_likely_correct(review_text: str) -> bool:
    text = (review_text or "").strip()
    if not text:
        return False

    try:
        payload = json.loads(text)
        solved = payload.get("solved") if isinstance(payload, dict) else None
        if isinstance(solved, bool):
            return solved
    except json.JSONDecodeError:
        pass

    match = re.search(r"\{[\s\S]*?\}", text)
    if not match:
        return False

    try:
        payload = json.loads(match.group(0))
    except json.JSONDecodeError:
        return False

    solved = payload.get("solved") if isinstance(payload, dict) else None
    return solved if isinstance(solved, bool) else False
