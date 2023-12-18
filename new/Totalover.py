import re
import pandas as pd


def main(data):
    # 找到所有的预测行
    predictions = re.findall(
        r"(XGBoost|Neural Network) Model Predictions(.*?)Expected Value & Kelly Criterion",
        data,
        re.DOTALL,
    )

    # 定义空列表来保存最后的数据
    final_data = []

    # 遍历所有找到的预测
    for model, prediction_data in predictions:
        # 找到所有的预测行
        prediction_lines = re.findall(
            r"(([^:]+) vs ([^:]+): (OVER|UNDER) (\d+\.?\d*) \(\d+\.?\d*%\))",
            prediction_data.strip(),
            re.DOTALL,
        )

        # 遍历所有的预测行
        for line in prediction_lines:
            # 提取球队名称和预测值
            teams = line[1:3]
            over_under = line[3]
            value = line[4]

            # 添加到最后的数据列表
            final_data.append(
                [model, teams[0].strip(), teams[1].strip(), over_under, value]
            )

    # 创建DataFrame并保存到CSV
    df = pd.DataFrame(
        final_data, columns=["Model", "Team1", "Team2", "Over_Under", "Value"]
    )
    df.to_csv("Export_File/total_over.csv", index=False)
