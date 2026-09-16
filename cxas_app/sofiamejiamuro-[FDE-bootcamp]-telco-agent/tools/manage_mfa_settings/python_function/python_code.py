def manage_mfa_settings(action: str = "enable", cirn: str = "") -> dict:
    """Update multi-factor authentication preferences.

    Args:
        action: enable or disable.
        cirn: Customer reference number.

    Returns:
        dict: Updated MFA configuration status.
    """
    try:
        return {
            "status": "success",
            "mfa_active": action.lower() == "enable",
            "message": f"MFA successfully {'enabled' if action.lower() == 'enable' else 'disabled'}."
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "agent_action": "Inform customer MFA update failed and ask to retry."
        }
