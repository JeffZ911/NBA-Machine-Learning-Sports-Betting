import random


def kelly_betting(win_rate, odds, initial_capital):
    capital = initial_capital
    b = odds - 1
    p = win_rate
    q = 1 - p
    fraction = (b * p - q) / b
    print(f"Bet fraction: {fraction*100:.2f}%.")

    if fraction > 0:
        f = (b * p - q) / b
        bet = f * capital

        # Simulate win or loss
        win = random.random() < p
        if win:
            capital += bet * b
            profit = bet * b
            print(
                f"Bet #{i+1}: Win. Bet: {bet:.4f}. Profit: {profit:.4f}. Capital: {capital:.4f}"
            )
        else:
            capital -= bet
            profit = -bet
            print(
                f"Bet #{i+1}: Loss. Bet: {bet:.4f}. Profit: {profit:.4f}. Capital: {capital:.4f}"
            )
    else:
        print("DO NOT BET")

    return capital


initial_capital, n = 1, 100

for i in range(n):
    win_rate, odds = 0.88, 1.5
    # win_rate, odds = random.uniform(0.8, 0.85), random.uniform(1.4, 1.81)
    final_capital = kelly_betting(win_rate, odds, initial_capital)
    initial_capital = final_capital

print(f"Final capital after {n} bets: {final_capital:.2f}")
