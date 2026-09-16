def fetch_plan_catalog(lob: str = "internet", customer_type: str = "Existing") -> dict:
    """Retrieve available service plans.

    Args:
        lob: Line of business.
        customer_type: New or Existing.

    Returns:
        dict: Curated list of 2-3 plan options.
    """
    try:
        return {
            "status": "success",
            "plans": [
                {
                    "id": "plan_500m",
                    "name": "Fiber 500 Mbps",
                    "price": "$55/month",
                    "key_features": "Fast and reliable for streaming and browsing"
                },
                {
                    "id": "plan_1g",
                    "name": "Gigabit Fiber 1 Gbps",
                    "price": "$75/month",
                    "key_features": "Ultra-fast speeds for multiple 4K streams and gaming"
                }
            ]
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "agent_action": "Apologize and inform the customer that the catalog is currently unavailable."
        }
