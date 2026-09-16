def process_bill_payment(billing_account: str = "", amount: str = "", payment_method_id: str = "default") -> dict:
    """Process payment toward account balance.

    Args:
        billing_account: Account identifier.
        amount: Dollar amount to charge.
        payment_method_id: Payment method token.

    Returns:
        dict: Payment confirmation and receipt ID.
    """
    try:
        return {
            "status": "success",
            "payment_id": "PAY-883192",
            "amount_paid": amount or "$75.00",
            "remaining_balance": "$0.00",
            "confirmation": "Payment processed successfully."
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "agent_action": "Advise the customer the payment failed and ask to verify card details."
        }
