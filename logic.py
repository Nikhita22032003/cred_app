# logic.py

def calculate_coins(amount, cibil, streak, fraud):
    """
    Calculate reward coins based on business rules.
    Returns: coins, explanation
    """

    if amount <= 0:
        return 0, "Invalid amount"

    coins = amount * 0.02 * (1 + streak * 0.1)

    explanation = f"Base coins from amount {amount} and streak {streak}. "

    # CIBIL bonus
    if cibil >= 750:
        coins *= 1.2
        explanation += "High CIBIL bonus applied. "

    # Fraud penalty
    if fraud:
        coins *= 0.5
        explanation += "Fraud penalty applied. "

    coins = round(coins, 2)

    return coins, explanation


def calculate_risk_score(cibil, days_late):
    """
    Risk score between 0 and 1 (lower is safer)
    """

    risk = 0.5

    if cibil >= 750:
        risk -= 0.2
    elif cibil < 600:
        risk += 0.2

    risk += days_late * 0.02

    risk = max(0, min(1, risk))

    return round(risk, 2)
