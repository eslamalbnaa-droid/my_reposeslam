"""Suggestion formatting for the MotoShop smart filter."""


def build_suggestion(item, score: float, query: str) -> dict:
    return {
        "id": item.id,
        "name": item.name,
        "brand": item.get_brand_display(),
        "year": item.model_year,
        "engine_cc": item.engine_cc,
        "label": f"{item.get_brand_display()} {item.name}",
        "score": round(score, 3),
        "corrected": score < 0.98 and query.strip().lower() != item.name.strip().lower(),
        "url_slug": item.slug,
    }
