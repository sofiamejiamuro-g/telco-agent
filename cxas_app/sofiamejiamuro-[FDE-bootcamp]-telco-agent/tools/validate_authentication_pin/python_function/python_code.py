def validate_authentication_pin(pin: str = "") -> dict:
    """Validate entered 4-digit DTMF security PIN.

    Args:
        pin: 4-digit numeric PIN.

    Returns:
        dict: Validation outcome with auth_status.
    """
    try:
        clean_pin = str(pin).strip()
        if clean_pin in ["0000", "wrong"]:
            return {
                "status": "error",
                "auth_status": "Fail",
                "error": "Incorrect PIN.",
                "attempts_remaining": 2,
                "agent_action": "Inform the caller the PIN was incorrect and ask them to re-enter it."
            }
        return {
            "status": "success",
            "auth_status": "Pass",
            "attempts_remaining": 3
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "agent_action": "Acknowledge system error and offer to transfer to a representative."
        }
