import new.Record as Record
import new.Totalover as Totalover
import new.WinRate as WinRate
import new.allscores as allscores
import new.GameScoreRecord as GameScoreRecord
from datetime import datetime, timedelta
import subprocess
import os
import re
import pandas as pd


def train_models():
    # Define commands and their corresponding working directories
    commands = [
        ("Get_Data", "src/Process-Data"),
        ("Get_Odds_Data", "src/Process-Data"),
        ("Create_Games", "src/Process-Data"),
        ("XGBoost_Model_ML", "src/Train-Models"),
        ("XGBoost_Model_UO", "src/Train-Models"),
    ]

    current_dir = os.getcwd()  # Store the starting directory

    # Execute each command in its directory
    for command, directory in commands:
        target_dir = os.path.join(current_dir, directory)
        if os.getcwd() != target_dir:
            os.chdir(target_dir)
        subprocess.run(["python", "-m", command])

    os.chdir(current_dir)  # Return to the starting directory once at the end


def american_to_decimal(american_odds):
    if american_odds > 0:
        return round((american_odds / 100) + 1, 2)
    else:
        return round((100 / abs(american_odds)) + 1, 2)


def main():
    # 训练模型
    # train_models()
    # 获取当前时间
    current_date = datetime.now()
    # 减去一天
    previous_date = current_date - timedelta(days=1)
    # 格式化日期
    date = previous_date.strftime("%Y-%m-%d")
    Tdate = previous_date.strftime("%Y-%m-%dT00:00:00")

    # 执行你的数据获取和处理
    record = Record.get_output()
    # Totalover.main(record)
    # WinRate.main(record)
    # GameScoreRecord.main(date, Tdate)
    # allscores.main() 可能需要放开注释，如果需要调用这个函数的话

    # Regular expression to match the FanDuel odds
    fanduel_pattern = re.compile(r"FanDuel Odds:\s([\+\-]\d+)")

    # Find all FanDuel odds in the record
    fanduel_matches = fanduel_pattern.findall(record)

    # Convert the FanDuel odds to decimal odds
    decimal_odds_list = [american_to_decimal(int(odds)) for odds in fanduel_matches]

    # Regular expression to match the team names and their corresponding Fraction of Bankroll
    pattern = re.compile(r"(.+?)\sEV:\s[-\d.]+\sFraction of Bankroll:\s([\d.]+)%")

    # Use the regular expression to find all matches in the data
    matches = pattern.findall(record)

    # Create a dictionary to hold the sums of fractions and their counts
    fractions = {}

    # Process the matches
    for team, fraction in matches:
        fraction = float(fraction)
        if fraction > 0:  # We only want positive values
            if team not in fractions:
                fractions[team] = {"total_fraction": 0, "count": 0}
            fractions[team]["total_fraction"] += fraction
            fractions[team]["count"] += 1

    # Calculate the average Fraction of Bankroll for each team
    averages = {
        team: info["total_fraction"] / info["count"] for team, info in fractions.items()
    }

    # Create a DataFrame from the averages dictionary
    df = pd.DataFrame(
        list(averages.items()),
        columns=["Team", "Average Fraction of Bankroll"],
    )

    # Add a timestamp column to the DataFrame
    df["Date"] = datetime.now().strftime("%Y-%m-%d")
    df["Dexsports"] = decimal_odds_list
    # Reorder DataFrame columns to have the Date first
    df = df[["Date", "Team", "Average Fraction of Bankroll", "Dexsports"]]

    csv_file_path = "Export_File/average_fractions.csv"

    file_exists = os.path.isfile(csv_file_path)

    # Export the DataFrame to a CSV file
    df.to_csv(csv_file_path, mode="a", index=False, header=False)


if __name__ == "__main__":
    main()
