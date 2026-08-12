"""Arabic normalization helpers for the offline smart bike filter."""
import re


def normalize_arabic(text: str) -> str:
    text = (text or "").strip().lower()
    text = re.sub(r"[إأآٱ]", "ا", text)
    text = text.replace("ة", "ه").replace("ى", "ي")
    text = text.replace("ؤ", "و").replace("ئ", "ي")
    text = re.sub(r"[ًٌٍَُِّْـ]", "", text)
    text = re.sub(r"[^\w\s\u0600-\u06ff-]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()
