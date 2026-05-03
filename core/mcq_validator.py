def validate_mcq(mcq):
    if not mcq:
        return False

    options = mcq.get("options", {})
    answer = mcq.get("correct_answer")

    return (
        len(options) == 4 and
        answer in ["A", "B", "C", "D"] and
        all(k in options for k in ["A", "B", "C", "D"])
    )