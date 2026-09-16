def fetch_customer_profile(clid: str = "") -> dict:
    """Retrieve customer account profile by phone number.

    Args:
        clid: 10-digit caller ID.

    Returns:
        dict: Customer profile details or error.
    """
    try:
        if not clid or clid == "restricted":
            return {
                "status": "error",
                "error": "Restricted or unidentified caller.",
                "agent_action": "Inform the caller that their caller ID is restricted and ask for their account number."
            }
        return {
            "status": "success",
            "cirn": "CRN-8849",
            "customer_type": "Existing",
            "business_flag": "False",
            "is_prepaid": "False",
            "billing_account": "BA-4921",
            "identification_status": "Pass"
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "agent_action": "Apologize and request the customer provide their account number manually."
        }
