CRITICAL_FIELDS = [
    "from_location_raw",
    "to_location_raw",
    "vehicle_type_raw",
    "reporting_datetime"
]

def apply_confidence_and_review(parsed):
    needs_review = False
    total_conf = 0
    count = 0

    for li in parsed.line_items:
        for field in CRITICAL_FIELDS:
            val = getattr(li, field)
            if not val:
                li.field_confidence[field] = 0.0
                needs_review = True
            else:
               
                if field not in li.field_confidence or li.field_confidence[field] == 0:
                    li.field_confidence[field] = 0.8

            total_conf += li.field_confidence[field]
            count += 1

    if count > 0:
        parsed.header.overall_confidence = round((total_conf / count) * 100, 2)
    else:
        parsed.header.overall_confidence = 0

    parsed.needs_review = needs_review
    return parsed
