def send_authentication_otp(clid: str = "") -> dict:
    """Dispatch a 6-digit verification code to the customer's device.

    Args:
        clid: 10-digit phone number.

    Returns:
        dict: Dispatch status and expiration seconds.
    """
    try:
        return {
            "status": "success",
            "sent": True,
            "expires_in_sec": 300,
            "destination_last_4": "0142"
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "agent_action": "Inform the customer the security code could not be sent and offer PIN verification."
        }
