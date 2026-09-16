def fetch_availability_slots(zip_code: str = "94043", service_type: str = "repair") -> dict:
    """Find available technician visit slots.

    Args:
        zip_code: Service location postal code.
        service_type: Installation or repair.

    Returns:
        dict: List of 2 to 3 arrival windows.
    """
    try:
        return {
            "status": "success",
            "slots": [
                {"date": "Tomorrow", "window": "8:00 AM - 12:00 PM", "technician_id": "TECH-101"},
                {"date": "Tomorrow", "window": "1:00 PM - 5:00 PM", "technician_id": "TECH-102"},
                {"date": "Friday", "window": "8:00 AM - 12:00 PM", "technician_id": "TECH-103"}
            ]
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "agent_action": "Inform customer that schedule lookup failed and offer callback."
        }
