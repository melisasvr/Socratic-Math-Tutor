import base64
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
    lowered = (review_text or "").lower()
    negative_signals = [
        "mistake",
        "incorrect",
        "error",
        "fix",
        "try again",
        "wrong",
    ]
    return not any(token in lowered for token in negative_signals)
