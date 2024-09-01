from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import random
import time
import pyautogui
import logging
import config  # 导入配置文件
from selenium.common.exceptions import NoSuchElementException

from tool import execute_questionnaire_autofill
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
def initialize_webdriver():
    options = Options()
    options.add_experimental_option('excludeSwitches', config.BROWSER_CONFIG["exclude_switches"])
    options.add_experimental_option('useAutomationExtension', config.BROWSER_CONFIG["use_automation_extension"])
    options.binary_location = config.BROWSER_CONFIG["chrome_binary_location"]

    service = Service(executable_path=config.BROWSER_CONFIG["chromedriver_path"])
    driver = webdriver.Chrome(service=service, options=options)

    # 隐藏 webdriver 标识
    driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument',
                           {'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'})
    return driver


def renzheng(driver):
    try:
        rect_bottom = driver.find_element(By.CSS_SELECTOR, config.CSS_SELECTORS["rect_bottom"])
        rect_bottom.click()
        time.sleep(5)
    except NoSuchElementException:
        logging.error("Rect bottom element not found.")


def huakuai():
    try:
        pyautogui.moveTo(random.randint(494, 496), 791, 0.2)
        time.sleep(1)
        pyautogui.dragTo(random.randint(888, 890), 791, 1)
        time.sleep(1)
        pyautogui.click(random.randint(652, 667), random.randint(793, 795))
        time.sleep(1)
        pyautogui.moveTo(random.randint(494, 496), 791, 0.2)
        time.sleep(1)
        pyautogui.dragTo(random.randint(888, 890), 791, 1)
    except Exception as e:
        logging.error(f"Slider interaction failed: {e}")


def start_survey(times):
    for i in range(times):
        driver = initialize_webdriver()  # 初始化WebDriver
        execute_questionnaire_autofill(driver)
        time.sleep(random.randint(0, 1))
        try:
            driver.find_element(By.CSS_SELECTOR, config.CSS_SELECTORS["submit_button"]).click()
        except NoSuchElementException:
            logging.error("Submit button not found.")
        time.sleep(4)
        # renzheng(driver)  # 调用智能认证函数
        # huakuai()  # 调用滑块函数
        logging.info(f'已经提交了 {i + 1} 次问卷.')
        time.sleep(5)
        driver.quit()  # 关闭当前WebDriver实例
        if i < times - 1:
            time.sleep(2)  # 短暂等待以避免过快的重启



if __name__ == "__main__":
    start_survey(1)
