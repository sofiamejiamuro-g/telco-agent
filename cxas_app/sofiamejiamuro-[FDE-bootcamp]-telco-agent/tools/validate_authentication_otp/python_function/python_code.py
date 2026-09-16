def validate_authentication_otp(code: str = "") -> dict:
    """Validate entered 6-digit OTP code.

    Args:
        code: 6-digit verification code.

    Returns:
        dict: Validation outcome with auth_status.
    """
    try:
        clean_code = str(code).strip()
        # In mock/eval scenarios, any 6-digit code or "123456" is accepted unless specified
        if clean_code in ["000000", "999999", "wrong"]:
            return {
                "status": "error",
                "auth_status": "Fail",
                "error": "Invalid verification code.",
                "attempts_remaining": 2,
                "agent_action": "Inform the customer that the code was incorrect and invite them to try again."
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
            "agent_action": "Acknowledge system verification issue and offer retry or human assistance."
        }
