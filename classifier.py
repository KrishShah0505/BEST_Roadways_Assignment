KEYWORDS = [
    "truck", "vehicle", "pickup", "load", "delivery",
    "container", "trailer", "dispatch", "lane"
]

def is_inquiry_email(text: str) -> bool:
    text = text.lower()
    hits = sum(1 for k in KEYWORDS if k in text)
    return hits >= 2
