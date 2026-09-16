def evaluate_routing_rules(utterance: str = "") -> dict:
    """Classify intent and determine routing path.

    Args:
        utterance: Customer statement or intent text.

    Returns:
        dict: Recommended route and auth requirements.
    """
    try:
        text = (utterance or "").lower()
        route = "billing"
        requires_auth = True

        if any(w in text for w in ["person", "agent", "human", "representative", "operator"]):
            route = "live_agent"
            requires_auth = False
        elif any(w in text for w in ["internet", "tv", "wifi", "signal", "down", "broken", "repair", "outage"]):
            route = "tech_support"
        elif any(w in text for w in ["plan", "buy", "upgrade", "phone", "device", "warranty", "order", "sales"]):
            route = "sales"
        elif any(w in text for w in ["appointment", "technician", "schedule", "reschedule", "visit"]):
            route = "appointment"
        elif any(w in text for w in ["password", "mfa", "fraud", "cancel", "port", "suspend", "restore"]):
            route = "account"

        return {
            "status": "success",
            "route": route,
            "confidence": 0.95,
            "requires_auth": requires_auth
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "agent_action": "Ask caller to clarify their request."
        }
