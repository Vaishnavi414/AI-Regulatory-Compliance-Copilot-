
def classify_score(score):

    if score > 0.85:
        return "Fully Compliant"

    elif score > 0.60:
        return "Partially Compliant"

    else:
        return "Not Addressed"
