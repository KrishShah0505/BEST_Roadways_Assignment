import os
import json
import re
from groq import Groq
from dotenv import load_dotenv

from schema import ParsedInquiry
from classifier import is_inquiry_email
from normalizer import normalize_vehicle, normalize_city
from validator import apply_confidence_and_review

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM_PROMPT = """
You are an AI that extracts structured logistics RFQ data from emails.

You MUST output ONLY valid JSON matching this schema:

{
  "is_inquiry": boolean,
  "header": {
    "client_name": string or null,
    "inquiry_type": string or null
  },
  "line_items": [
    {
      "from_location_raw": string or null,
      "to_location_raw": string or null,
      "vehicle_type_raw": string or null,
      "quantity_vehicles": number or null,
      "reporting_datetime": string or null,
      "cargo": string or null,
      "field_confidence": {
         "from_location_raw": number,
         "to_location_raw": number,
         "vehicle_type_raw": number,
         "quantity_vehicles": number,
         "reporting_datetime": number
      }
    }
  ],
  "needs_review": boolean
}

Rules:
- If not a logistics inquiry, set is_inquiry=false and return empty line_items.
- If any critical field is missing (from, to, vehicle, date) set needs_review=true.
- Support multiple line items if multiple lanes present.
- Do not hallucinate.
- Output ONLY JSON. No markdown. No explanation.
"""

def _extract_json(text: str):
    """Extract JSON even if wrapped in markdown"""
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        raise ValueError("No JSON found in model output")
    return match.group(0)

def extract_inquiry(email_text: str) -> ParsedInquiry:
    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": email_text}
        ],
        temperature=0
    )

    raw = completion.choices[0].message.content

    clean_json = _extract_json(raw)
    data = json.loads(clean_json)

    parsed = ParsedInquiry(**data)

    # Override inquiry flag using deterministic classifier
    parsed.is_inquiry = is_inquiry_email(email_text)

    # Normalize fields
    for li in parsed.line_items:
        li.vehicle_type_normalized = normalize_vehicle(li.vehicle_type_raw)
        li.from_location_raw = normalize_city(li.from_location_raw)
        li.to_location_raw = normalize_city(li.to_location_raw)

    # Apply confidence & needs-review logic
    parsed = apply_confidence_and_review(parsed)

    return parsed
