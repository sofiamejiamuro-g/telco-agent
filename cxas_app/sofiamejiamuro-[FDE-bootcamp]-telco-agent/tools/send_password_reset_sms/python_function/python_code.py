def send_password_reset_sms(cirn: str = "") -> dict:
    """Dispatch self-serve password reset link via SMS.

    Args:
        cirn: Customer reference number.

    Returns:
        dict: Dispatch status and validity window.
    """
    try:
        return {
            "status": "success",
            "sent": True,
            "valid_minutes": 30,
            "message": "Password reset link sent successfully via SMS."
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "agent_action": "Apologize and inform the customer that the reset link could not be sent."
        }
