def cancel_service_contract(billing_account: str = "", reason: str = "moving") -> dict:
    """Execute service contract cancellation.

    Args:
        billing_account: Account identifier.
        reason: Customer cancellation reason.

    Returns:
        dict: Cancellation confirmation and effective date.
    """
    try:
        return {
            "status": "success",
            "cancelled": True,
            "effective_date": "2026-09-30",
            "early_termination_fee": "$0.00",
            "confirmation_code": "CNCL-9012"
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "agent_action": "Inform the caller the cancellation could not be processed and offer live assistance."
        }
