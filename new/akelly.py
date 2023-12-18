import random
import pandas as pd


def load_data():
    # Read the CSV file
    df = pd.read_csv("NBA_Records.csv")
    # df = pd.read_excel("NBA_Records.xlsx", sheet_name="Consider")
    df = df.dropna()

    # Extract the columns into the variables
    team_names = df["Team"].tolist()
    odds = df["Odds"]
    win_rate = df["Average"]
    # print(team_names)
    return odds, win_rate, team_names


def kelly_betting(team_names, bets, initial_capital, n):
    capital = initial_capital
    total_profit = 0

    for (win_rate, odds), team_name in zip(bets, team_names):
        b = odds - 1
        p = win_rate
        q = 1 - p
        fraction = (b * p - q) / b

        print(f"\nBet {team_name} fraction: {fraction*100:.2f}%.")

        if fraction > 0:
            for i in range(n):
                bet = fraction * capital

                # Simulate win or loss
                win = random.random() < p
                if win:
                    capital += bet * b
                    profit = bet * b
                    total_profit += profit
                    print(
                        f"{team_name}, #{i+1} Bet: Win. Bet: {bet:.4f}. Profit: {profit:.4f}. Capital: {capital:.4f}"
                    )
                else:
                    capital -= bet
                    profit = -bet
                    total_profit += profit
                    print(
                        f"{team_name}, #{i+1} Bet: Loss. Bet: {bet:.4f}. Profit: {profit:.4f}. Capital: {capital:.4f}"
                    )
        else:
            pass
            print("DO NOT BET")

    return capital, total_profit


def run_bets(n):
    total_profits = []
    for _ in range(n):
        total_profit, final_capital, num_bets, num_runs = main()
        total_profits.append(total_profit)
        # print(
        #     f"\nTotal bet profit: {total_profit:.2f}. Final capital after {num_bets} bets run {num_runs} times: {final_capital:.2f}"
        # )

    average_profit = sum(total_profits) / len(total_profits)
    print(f"\nAverage total bet profit over {n} runs: {average_profit:.2f}")
    return average_profit


def main():
    odds, win_rate, team_names = load_data()
    # odds, win_rate = [1.4, 1.37, 1.5], [0.83, 0.74, 0.73]
    bets = list(zip(win_rate, odds))
    # print(bets)
    initial_capital, n = 1, 1

    final_capital, total_profit = kelly_betting(team_names, bets, initial_capital, n)
    print(
        f"\nTotal bet profit: {total_profit:.2f}. Final capital after {len(bets)} bets run {n} times: {final_capital:.2f}\n"
    )
    return total_profit, final_capital, len(bets), n


if __name__ == "__main__":
    main()
