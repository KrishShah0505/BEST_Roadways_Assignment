from pydantic import BaseModel, Field
from typing import List, Optional, Dict

class InquiryHeader(BaseModel):
    source_inbox: Optional[str] = None
    sender_email: Optional[str] = None
    sender_name: Optional[str] = None
    subject: Optional[str] = None
    received_at: Optional[str] = None

    client_name: Optional[str] = None
    inquiry_type: Optional[str] = None
    status: str = "New"
    overall_confidence: float = 0.0

class LineItem(BaseModel):
    from_location_raw: Optional[str] = None
    to_location_raw: Optional[str] = None

    vehicle_type_raw: Optional[str] = None
    vehicle_type_normalized: Optional[str] = None

    quantity_vehicles: Optional[int] = None
    reporting_datetime: Optional[str] = None

    cargo: Optional[str] = None

    field_confidence: Dict[str, float] = {}

class ParsedInquiry(BaseModel):
    is_inquiry: bool
    header: InquiryHeader
    line_items: List[LineItem]
    needs_review: bool
