def commit_appointment_reschedule(appt_id: str = "", new_slot: str = "", action: str = "reschedule") -> dict:
    """Update or cancel scheduled technician visit.

    Args:
        appt_id: Appointment ID.
        new_slot: Chosen appointment window.
        action: reschedule, book, or cancel.

    Returns:
        dict: Booking confirmation and updated time.
    """
    try:
        return {
            "status": "success",
            "confirmed": True,
            "appt_id": appt_id or "APT-55912",
            "new_date": new_slot or "Tomorrow 8:00 AM - 12:00 PM",
            "sms_sent": True
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "agent_action": "Acknowledge scheduling error and offer to check alternative days."
        }
