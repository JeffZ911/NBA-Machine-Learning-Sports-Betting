import re
import pandas as pd


def main(data):
    # Define the regular expression patterns
    xgboost_pattern = r"---------------XGBoost Model Predictions---------------(.*?)------------Expected Value & Kelly Criterion-----------"
    neural_network_pattern = r"------------Neural Network Model Predictions-----------(.*?)------------Expected Value & Kelly Criterion-----------"
    team_pattern = r"([A-Za-z ]+) \(([\d\.]+)%\) vs ([A-Za-z ]+)|([A-Za-z ]+) vs ([A-Za-z ]+) \(([\d\.]+)%\)"

    # Find the data
    xgboost_data = re.findall(
        team_pattern, re.search(xgboost_pattern, data, re.DOTALL).group(1)
    )
    neural_network_data = re.findall(
        team_pattern, re.search(neural_network_pattern, data, re.DOTALL).group(1)
    )

    # Convert to pandas DataFrame
    df_xgboost = pd.DataFrame(
        xgboost_data,
        columns=[
            "Team1",
            "Win Probability1",
            "Team2",
            "Team3",
            "Team4",
            "Win Probability2",
        ],
    )
    df_neural_network = pd.DataFrame(
        neural_network_data,
        columns=[
            "Team1",
            "Win Probability1",
            "Team2",
            "Team3",
            "Team4",
            "Win Probability2",
        ],
    )

    # Set the model name
    df_xgboost["Model"] = "XGBoost"
    df_neural_network["Model"] = "Neural Network"

    # Append the data
    df = df_xgboost._append(df_neural_network)

    # Process the dataframe to get winning team and winning probability
    df["Winning Team"] = df["Team1"].where(df["Team1"] != "", df["Team4"])
    df["Win Probability (%)"] = df["Win Probability1"].where(
        df["Win Probability1"] != "", df["Win Probability2"]
    )
    df = df[["Winning Team", "Model", "Win Probability (%)"]]

    # Save to CSV
    df.to_csv("Export_File/Win_Rate.csv", index=False)
