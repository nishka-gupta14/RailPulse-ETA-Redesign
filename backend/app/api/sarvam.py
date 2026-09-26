"""Sarvam AI API endpoints - multilingual voice announcements."""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.sarvam_service import translate_text, text_to_speech, SarvamServiceError

router = APIRouter()

LANGUAGE_MAP = {
    "hi": "hi-IN", "ta": "ta-IN", "te": "te-IN", "bn": "bn-IN",
    "mr": "mr-IN", "gu": "gu-IN", "kn": "kn-IN", "en": "en-IN",
}


class AnnounceRequest(BaseModel):
    text: str
    lang: str = "hi"


class AnnounceResponse(BaseModel):
    translated_text: str
    audio_base64: str
    audio_format: str = "wav"


@router.post("/announce", response_model=AnnounceResponse)
async def announce(payload: AnnounceRequest):
    lang_code = LANGUAGE_MAP.get(payload.lang)
    if not lang_code:
        raise HTTPException(status_code=400, detail=f"Unsupported language '{payload.lang}'")
    try:
        translated = await translate_text(payload.text, target_language_code=lang_code)
        audio_b64 = await text_to_speech(translated, target_language_code=lang_code)
    except SarvamServiceError as e:
        raise HTTPException(status_code=502, detail=str(e))
    return AnnounceResponse(translated_text=translated, audio_base64=audio_b64)
