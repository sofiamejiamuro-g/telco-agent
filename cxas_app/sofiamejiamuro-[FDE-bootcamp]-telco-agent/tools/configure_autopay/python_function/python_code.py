def configure_autopay(billing_account: str = "", payment_method: str = "card") -> dict:
    """Configure recurring autopay.

    Args:
        billing_account: Customer billing account.
        payment_method: Payment method type.

    Returns:
        dict: Autopay setup status.
    """
    try:
        return {
            "status": "success",
            "autopay_active": True,
            "next_deduction_date": "2026-10-15"
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "agent_action": "Inform the customer that autopay could not be enabled."
        }
