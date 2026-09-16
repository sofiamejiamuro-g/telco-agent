def fetch_recent_bills(billing_account: str = "") -> dict:
    """Retrieve recent billing records.

    Args:
        billing_account: Customer billing account identifier.

    Returns:
        dict: Billing statements and itemized charges.
    """
    try:
        return {
            "status": "success",
            "current_balance": "$75.00",
            "due_date": "2026-10-15",
            "bills": [
                {
                    "id": "INV-2026-09",
                    "date": "2026-09-01",
                    "amount": "$75.00",
                    "line_items": [
                        {"description": "Unlimited Fiber Internet 500M", "amount": "$60.00"},
                        {"description": "AppleStreaming Subscription", "amount": "$12.50"},
                        {"description": "Regulatory Fee", "amount": "$2.50"}
                    ]
                }
            ]
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "agent_action": "Inform the customer billing details are temporarily unavailable."
        }
