def get_safety_status(posture):
    """
    Convert posture into safety status.
    """

    if posture == "Standing":
        return "SAFE"
    elif posture == "Sitting":
        return "MONITOR"
    elif posture == "Bending":
        return "RISK"
    else:
        return "UNKNOWN"

# SAFETY RULES - this module contains the get_safety_status function,
# which takes a classified posture as input and determines the corresponding safety status
# based on predefined rules.

# The function maps the "Standing" posture to a "SAFE" status, "Sitting" to "MONITOR", and "Bending" to "RISK".