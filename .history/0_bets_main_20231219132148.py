import new.Record as Record
import new.Totalover as Totalover
import new.WinRate as WinRate
import new.allscores as allscores
import new.GameScoreRecord as GameScoreRecord
from datetime import datetime, timedelta
import subprocess
import os


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


def main():
    # 训练模型
    train_models()
    # 获取当前时间
    current_date = datetime.now()
    # 减去一天
    previous_date = current_date - timedelta(days=1)
    # 格式化日期
    date = previous_date.strftime("%Y-%m-%d")
    Tdate = previous_date.strftime("%Y-%m-%dT00:00:00")

    # 执行你的数据获取和处理
    record = Record.get_output()
    Totalover.main(record)
    WinRate.main(record)
    GameScoreRecord.main(date, Tdate)
    # allscores.main() 可能需要放开注释，如果需要调用这个函数的话


if __name__ == "__main__":
    main()
