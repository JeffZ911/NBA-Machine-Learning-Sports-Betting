import Record
import Totalover
import WinRate
import allscores
import GameScoreRecord
from datetime import datetime, timedelta


def main():
    # 获取当前时间
    current_date = datetime.now()
    # 减去一天
    previous_date = current_date - timedelta(days=1)
    # 格式化日期
    date = previous_date.strftime("%Y-%m-%d")
    Tdate = previous_date.strftime("%Y-%m-%dT00:00:00")

    record = Record.get_output()
    Totalover.main(record)
    WinRate.main(record)
    GameScoreRecord.main(date, Tdate)
    allscores.main()


if __name__ == "__main__":
    main()
