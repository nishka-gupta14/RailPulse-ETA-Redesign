"""Sarvam AI integration - translation and text-to-speech for passenger alerts."""

import os
import httpx

SARVAM_API_KEY = os.getenv("SARVAM_API_KEY", "")
SARVAM_BASE_URL = "https://api.sarvam.ai"


class SarvamServiceError(Exception):
    pass


def _headers() -> dict:
    if not SARVAM_API_KEY:
        raise SarvamServiceError("SARVAM_API_KEY is not set in the environment")
    return {
        "api-subscription-key": SARVAM_API_KEY,
        "Content-Type": "application/json",
    }


async def translate_text(text: str, target_language_code: str, source_language_code: str = "en-IN") -> str:
    payload = {
        "input": text,
        "source_language_code": source_language_code,
        "target_language_code": target_language_code,
        "mode": "formal",
        "model": "mayura:v1",
    }
    async with httpx.AsyncClient(timeout=15.0) as client:
        try:
            resp = await client.post(f"{SARVAM_BASE_URL}/translate", headers=_headers(), json=payload)
            resp.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise SarvamServiceError(f"Translate failed: {e.response.status_code} {e.response.text}")
        except httpx.RequestError as e:
            raise SarvamServiceError(f"Translate request error: {e}")
    return resp.json()["translated_text"]


async def text_to_speech(text: str, target_language_code: str, speaker: str = "shubh") -> str:
    payload = {
        "text": text[:1500],
        "target_language_code": target_language_code,
        "speaker": speaker,
        "model": "bulbul:v3",
    }
    async with httpx.AsyncClient(timeout=20.0) as client:
        try:
            resp = await client.post(f"{SARVAM_BASE_URL}/text-to-speech", headers=_headers(), json=payload)
            resp.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise SarvamServiceError(f"TTS failed: {e.response.status_code} {e.response.text}")
        except httpx.RequestError as e:
            raise SarvamServiceError(f"TTS request error: {e}")
    return "".join(resp.json()["audios"])
