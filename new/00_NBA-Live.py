import time
from nba_api.live.nba.endpoints import scoreboard
from dingtalkchatbot.chatbot import DingtalkChatbot, ActionCard, CardItem


def info():
    webhook = "https://oapi.dingtalk.com/robot/send?access_token=4d21a6c6ee4f0759912da670739324b8f8e923d131c9837f1972bd834345ed9f"
    secret = "SEC31054b609a1f427aed7ba39dd42dd795d12c125c7d7e9a6514c57af2435e2571"
    return webhook, secret


def teams():
    team_dict = {
        1: "76ers",
        2: "Bucks",
        3: "Bulls",
        4: "Cavaliers",
        5: "Celtics",
        6: "Clippers",
        7: "Grizzlies",
        8: "Hawks",
        9: "Heat",
        10: "Hornets",
        11: "Jazz",
        12: "Kings",
        13: "Knicks",
        14: "Lakers",
        15: "Magic",
        16: "Mavericks",
        17: "Nets",
        18: "Nuggets",
        19: "Pacers",
        20: "Pelicans",
        21: "Pistons",
        22: "Raptors",
        23: "Rockets",
        24: "Spurs",
        25: "Suns",
        26: "Thunder",
        27: "Timberwolves",
        28: "Trail Blazers",
        29: "Warriors",
        30: "Wizards",
    }
    return team_dict


def print_score_board(bets_team):
    webhook, secret = info()
    dd_bot = DingtalkChatbot(webhook, secret=secret)
    # Fetch the latest scoreboard information initially to print all game teams
    games = scoreboard.ScoreBoard()
    games_dict = games.get_dict()

    while True:
        # Fetch the latest scoreboard information
        games = scoreboard.ScoreBoard()
        games_dict = games.get_dict()

        # Extract the relevant game information
        games_to_print = []
        for game in games_dict["scoreboard"]["games"]:
            game_status_text = game["gameStatusText"]
            home_team = game["homeTeam"]["teamName"]
            away_team = game["awayTeam"]["teamName"]

            # Skip if the game is final or neither of the teams is in the bets_team list
            if (
                "Final" in game_status_text
                or " pm" in game_status_text
                or (home_team not in bets_team and away_team not in bets_team)
            ):
                continue

            home_score = game["homeTeam"]["score"]
            away_score = game["awayTeam"]["score"]

            # Strongly remind if your bet team score is less than its opponent
            if (home_team in bets_team and home_score < away_score) or (
                away_team in bets_team and away_score < home_score
            ):
                warn_msg = f"!!!WARNING!!! {game_status_text}: {home_team} vs {away_team}: {home_score} - {away_score}"
                games_to_print.append(warn_msg)
                dd_bot.send_text(msg=warn_msg)
            else:
                games_to_print.append(
                    f"{game_status_text}: {home_team} vs {away_team}: {home_score} - {away_score}"
                )

        # Print the scores for ongoing games
        for game_info in games_to_print:
            print(game_info)
        print()

        # Check if there are any ongoing games left to print
        if not games_to_print:
            print("All Games Has Over")
            break

        # Wait for 10 seconds before the next update
        time.sleep(10)


def main():
    team_dict = teams()
    bets_numbers = [1, 2, 13, 6]
    bets_team = [team_dict[number] for number in bets_numbers]

    print_score_board(bets_team)


if __name__ == "__main__":
    main()
