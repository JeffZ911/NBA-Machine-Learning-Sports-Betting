from nba_api.stats.endpoints import boxscoresummaryv2, leaguegamefinder
import pandas as pd
from datetime import datetime
import csv
import tempfile
import shutil


def game_scores(game_ids, Tdate=None):
    all_games_data = []

    for game_id in game_ids:
        boxscore_summary = boxscoresummaryv2.BoxScoreSummaryV2(game_id=game_id)
        line_score = boxscore_summary.get_data_frames()[5]
        line_score = line_score[
            [
                "GAME_DATE_EST",
                "TEAM_NICKNAME",
                "PTS_QTR1",
                "PTS_QTR2",
                "PTS_QTR3",
                "PTS_QTR4",
                "PTS_OT1",
                "PTS_OT2",
                "PTS_OT3",
                "PTS_OT4",
                "PTS_OT5",
                "PTS_OT6",
                "PTS_OT7",
                "PTS_OT8",
                "PTS_OT9",
                "PTS_OT10",
            ]
        ]
        all_games_data.append(line_score)

    all_games_data = pd.concat(all_games_data)

    # Define the file path where the CSV will be saved
    output_file_path = "Export_File/games_scores.csv"

    # Write the DataFrame to the CSV file
    all_games_data.to_csv(output_file_path, index=False)

    # Optionally filter by Tdate if needed before saving
    if Tdate:
        all_games_data = all_games_data[all_games_data["GAME_DATE_EST"] == Tdate]
        all_games_data.to_csv(output_file_path, index=False)

    # Return the file path
    return output_file_path


def game_ids(season_year, date=None):
    gamefinder = leaguegamefinder.LeagueGameFinder(
        season_nullable=season_year, league_id_nullable="00"
    )
    games = gamefinder.get_data_frames()[0]
    regular_season_games = games[games["SEASON_ID"].str.startswith("2")]

    if date:
        # 过滤出特定日期的比赛ID
        game_ids = (
            regular_season_games[regular_season_games["GAME_DATE"] == date]["GAME_ID"]
            .unique()
            .tolist()
        )
    else:
        # 获取整个赛季的比赛ID
        game_ids = regular_season_games["GAME_ID"].unique().tolist()

    return game_ids


def process_csv(date=None, Tdate=None):
    input_filename = "Export_File/games_scores.csv"
    output_filename = "Export_File/temp_file.csv"
    # 打开原始CSV文件和目标CSV文件
    with open(input_filename, "r") as input_file, open(
        output_filename, "w", newline=""
    ) as output_file:
        reader = csv.reader(input_file)
        writer = csv.writer(output_file)

        # 读取和写入标题行
        header = next(reader)
        new_header = (
            header
            + ["Away_TEAM_NICKNAME", "Away_Team_Score"]
            + [f"Away_{col}" for col in header[2:]]
            + ["Home_Team_Score"]
        )
        writer.writerow(new_header)

        # 逐行处理数据
        rows = list(reader)
        for i in range(0, len(rows), 2):
            # 检查是否有足够的行来组成一组主队和客队数据
            if i + 1 >= len(rows):
                break

            home_team_data = rows[i]
            away_team_data = rows[i + 1]

            # 提取主队和客队的数据
            away_team_score = sum(float(score) for score in away_team_data[2:])
            home_team_score = sum(float(score) for score in home_team_data[2:])

            new_row = (
                home_team_data
                + [away_team_data[1], away_team_score]
                + away_team_data[2:]
                + [home_team_score]
            )
            writer.writerow(new_row)


def main(date=None, Tdate=None):
    current_date = datetime.now()
    season_year = current_date.year
    if current_date.month < 10:
        season_year -= 1
    season = f"{season_year}-{str(season_year+1)[2:]}"
    # date = "2023-12-11"
    # Tdate = "2023-12-11T00:00:00"

    gameids = game_ids(season, date=None)
    game_scores(gameids, Tdate=None)
    process_csv(date=None, Tdate=None)

    score_file = "Export_File/temp_file.csv"

    df = pd.read_csv(score_file)
    column_order = [
        "GAME_DATE_EST",
        "Away_TEAM_NICKNAME",
        "TEAM_NICKNAME",
        "Away_PTS_QTR1",
        "Away_PTS_QTR2",
        "Away_PTS_QTR3",
        "Away_PTS_QTR4",
        "PTS_QTR1",
        "PTS_QTR2",
        "PTS_QTR3",
        "PTS_QTR4",
        "Away_Team_Score",
        "Home_Team_Score",
        "Away_PTS_OT1",
        "Away_PTS_OT2",
        "Away_PTS_OT3",
        "Away_PTS_OT4",
        "Away_PTS_OT5",
        "Away_PTS_OT6",
        "Away_PTS_OT7",
        "Away_PTS_OT8",
        "Away_PTS_OT9",
        "Away_PTS_OT10",
        "PTS_OT1",
        "PTS_OT2",
        "PTS_OT3",
        "PTS_OT4",
        "PTS_OT5",
        "PTS_OT6",
        "PTS_OT7",
        "PTS_OT8",
        "PTS_OT9",
        "PTS_OT10",
    ]
    df = df[column_order]

    df.to_csv("Export_File/games_scores.csv", index=False)


if __name__ == "__main__":
    main()
