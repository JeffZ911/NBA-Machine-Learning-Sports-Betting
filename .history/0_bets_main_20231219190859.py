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
    if american_odds == 0:
        raise ValueError("American odds cannot be zero.")
    if american_odds > 0:
        return round((american_odds / 100) + 1, 2)
    else:
        return round((100 / abs(american_odds)) + 1, 2)


def main():
    # Train models
    train_models()
    # Get the current time
    current_date = datetime.now()
    # Subtract one day
    previous_date = current_date - timedelta(days=1)
    # Format the date
    date = previous_date.strftime("%Y-%m-%d")
    Tdate = previous_date.strftime("%Y-%m-%dT00:00:00")

    # Execute your data retrieval and processing
    record = Record.get_output()
    # Uncomment the following lines if those functions need to be called
    Totalover.main(record)
    WinRate.main(record)
    GameScoreRecord.main(date, Tdate)
    allscores.main()

    # Regular expression to match the FanDuel odds
    fanduel_pattern = re.compile(r"([a-zA-Z\s\.\-']+)\s*\(([\+\-]?\d+)\)")

    # Find all FanDuel odds in the record
    fanduel_matches = fanduel_pattern.findall(record)
    print(fanduel_matches)
    # Convert the FanDuel odds to decimal odds
    decimal_odds_list = [
        american_to_decimal(int(odds)) for team, odds in fanduel_matches
    ]
    print(decimal_odds_list)
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
    # Ensure that the length of decimal_odds_list is equal to the number of teams in the DataFrame
    if len(decimal_odds_list) == len(df):
        df["Dexsports"] = decimal_odds_list
    else:
        raise ValueError("The length of decimal_odds_list does not match the number of teams.")

    # Reorder DataFrame columns to have the Date first
    df = df[["Date", "Team", "Average Fraction of Bankroll", "Dexsports"]]

    csv_file_path = "Export_File/average_fractions.csv"

   ```python
    # Check if the file already exists
    file_exists = os.path.isfile(csv_file_path)

    # Export the DataFrame to a CSV file
    df.to_csv(
        csv_file_path, 
        mode='a', 
        index=False, 
        header=not file_exists  # Only include header if the file did not exist before
    )


if __name__ == "__main__":
    main()