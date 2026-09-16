def execute_suspend_restore(action: str = "suspend", reason: str = "lost_stolen", cirn: str = "") -> dict:
    """Suspend or restore customer service lines.

    Args:
        action: suspend or restore.
        reason: Reason code (lost_stolen, non_payment, travel).
        cirn: Customer reference number.

    Returns:
        dict: New service state and timestamp.
    """
    try:
        new_state = "suspended" if action.lower() == "suspend" else "active"
        return {
            "status": "success",
            "new_state": new_state,
            "effective_iso": "2026-09-15T23:00:00Z",
            "sms_notification_sent": True
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "agent_action": "Inform the caller service status change could not be completed."
        }
