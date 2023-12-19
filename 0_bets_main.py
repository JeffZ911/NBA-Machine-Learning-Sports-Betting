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
    # train_models()
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
    # Totalover.main(record)
    # WinRate.main(record)
    # GameScoreRecord.main(date, Tdate)
    # allscores.main()

    # Regular expression to match the FanDuel odds
    fanduel_pattern = re.compile(r"([a-zA-Z\s\.\-']+)\s*\(([\+\-]?\d+)\)")

    # Find all FanDuel odds in the record
    fanduel_matches = fanduel_pattern.findall(record)
    print(fanduel_matches)
    # Convert the FanDuel odds to decimal odds
    decimal_odds_list = [
        american_to_decimal(int(odds)) for team, odds in fanduel_matches
    ]

    # Regular expression to match the team names and their corresponding Fraction of Bankroll
    pattern = re.compile(r"(.+?)\sEV:\s[-\d.]+\sFraction of Bankroll:\s([\d.]+)%")

    # Use the regular expression to find all matches in the data
    matches = pattern.findall(record)

    # Create a dictionary to hold the team names and their fractions
    team_fractions = {
        team.strip(): float(fraction)
        for team, fraction in matches
        if float(fraction) > 0
    }

    # Find all FanDuel odds in the record and convert them to decimal odds
    fanduel_matches = fanduel_pattern.findall(record)
    team_odds = {
        team.strip(): american_to_decimal(int(odds)) for team, odds in fanduel_matches
    }

    # Create lists to hold your data
    teams = []
    fractions = []
    odds_list = []

    # Go through each team in the team_fractions dictionary
    for team, fraction in team_fractions.items():
        teams.append(team)
        fractions.append(fraction)
        # Look up the decimal odds for the team and add to the list
        if team in team_odds:
            odds_list.append(team_odds[team])
        else:
            # Handle the case where the team's odds are not found
            print(f"No odds found for {team}, skipping.")
            continue  # Skip the team if no odds are found

    # Now you can create a DataFrame using the lists
    df = pd.DataFrame(
        {
            "Team": teams,
            "Average Fraction of Bankroll": fractions,
            "Dexsports": odds_list,
            "Date": datetime.now().strftime("%Y-%m-%d"),
        }
    )

    # Reorder DataFrame columns to have the Date first
    df = df[["Date", "Team", "Average Fraction of Bankroll", "Dexsports"]]

    csv_file_path = "Export_File/average_fractions.csv"

    # Check if the file already exists
    file_exists = os.path.isfile(csv_file_path)

    # Export the DataFrame to a CSV file
    df.to_csv(
        csv_file_path,
        mode="a",
        index=False,
        header=not file_exists,  # Only include header if the file did not exist before
    )


if __name__ == "__main__":
    main()
