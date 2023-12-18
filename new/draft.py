from selenium import webdriver

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


driver = webdriver.Edge()

try:
    # 访问目标网页
    driver.get("https://dexsport.io/sports/basketball/tournaments/100")

    # 等待页面加载（可能需要根据实际情况增加等待时间）
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.CLASS_NAME, "class-name-of-interesting-element")
        )
    )

    # 比如我们要找的队伍是"Philadelphia 76ers"
    team_name = "Philadelphia 76ers"

    # 使用XPath或其他选择器定位到特定球队的特定赔率
    # 注意：下面的XPath是假设的，需要根据实际页面结构进行调整
    //*[@id="app"]/div/div[3]/div[2]/div/div[2]/div[1]/div[2]/a[1]/div[1]/div[1]/div/div/span
    xpath = f"//div[contains(text(), '{team_name}')]/following-sibling::div[contains(@class, 'outcome__number')]"

    # 获取该XPath对应的元素
    odds_elements = driver.find_elements(By.XPATH, xpath)

    # 打印所有找到的赔率
    for element in odds_elements:
        print(element.text)

except Exception as e:
    print("An error occurred:", e)
finally:
    driver.quit()  # 记得退出，释放资源
