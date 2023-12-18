from nba_api.stats.endpoints import boxscoresummaryv2
from nba_api.stats.endpoints import teamgamelog
from nba_api.stats.static import teams
import pandas as pd


def get_all_team_ids():
    all_teams = teams.get_teams()
    team_ids = {
        team["id"]: team["nickname"] for team in all_teams
    }  # 修改为返回一个字典，包含球队的ID和昵称
    return team_ids


def get_team_scores(team_id, team_name, season="2023"):
    gamelog = teamgamelog.TeamGameLog(team_id, season)
    games = gamelog.get_data_frames()[0]

    scores_df = pd.DataFrame()

    for game_id in games["Game_ID"].unique():
        boxscore_summary = boxscoresummaryv2.BoxScoreSummaryV2(game_id=game_id)
        game_summary = boxscore_summary.game_summary.get_data_frame()

        home_team = game_summary["HOME_TEAM_ID"].values[0]
        game_date = game_summary["GAME_DATE_EST"].values[0]  # 获取比赛日期

        if team_id == home_team:
            location = "Home"
        else:
            location = "Away"

        line_score = boxscore_summary.line_score.get_data_frame()

        scores = line_score[line_score["TEAM_ID"] == team_id][
            ["PTS_QTR1", "PTS_QTR2", "PTS_QTR3", "PTS_QTR4"]
        ].values[0]

        total_score = sum(scores)  # 计算总分

        scores_series = pd.Series(
            {
                "Game_Date": game_date,
                "Team_Name": team_name,
                "Location": location,
                "Q1": scores[0],
                "Q2": scores[1],
                "Q3": scores[2],
                "Q4": scores[3],
                "Total_Score": total_score,
            }
        )

        scores_df = scores_df._append(scores_series, ignore_index=True)

    return scores_df


def main():
    team_ids = get_all_team_ids()

    all_scores_df = pd.DataFrame()  # 创建一个空的 DataFrame 用于保存所有球队的得分数据

    for team_id, team_name in team_ids.items():
        scores_df = get_team_scores(team_id, team_name)
        all_scores_df = all_scores_df._append(scores_df, ignore_index=True)

    # 输出汇总的数据
    # print(all_scores_df)
    all_scores_df.to_csv("Export_File/all_scores.csv", index=False)


if __name__ == "__main__":
    main()
