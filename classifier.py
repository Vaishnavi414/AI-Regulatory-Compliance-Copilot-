def classify_compliance(score):
    """
    Classify compliance based on similarity score.
    """

    if score > 0.85:
        return "Fully Compliant"

    elif score > 0.65:
        return "Partially Compliant"

    else:
        return "Not Addressed"


def calculate_risk(results):
    """
    Calculate overall risk score.
    """

    risk = 0

    for r in results:

        if r["Compliance Status"] == "Not Addressed":
            risk += 2

        elif r["Compliance Status"] == "Partially Compliant":
            risk += 1

    return risk