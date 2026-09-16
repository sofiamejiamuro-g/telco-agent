def execute_live_agent_handover(reason: str = "user_requested_agent") -> dict:
    """Transfer session to live representative queue.

    Args:
        reason: Escalation reason code.

    Returns:
        dict: Handover confirmation and queue identifier.
    """
    try:
        queue = "general_support"
        if "fraud" in reason:
            queue = "24_7_fraud_specialist"
        elif "business" in reason:
            queue = "business_care"
        elif "secondary" in reason:
            queue = "spanish_support"

        return {
            "status": "success",
            "handover_id": "HND-33019",
            "queue": queue,
            "reason": reason,
            "session_context_preserved": True
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "agent_action": "Transfer call immediately to operator."
        }
