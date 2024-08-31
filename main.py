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

class SurveyAutomation:
    def __init__(self):
        self.driver = None
        self.setup_driver()

    def setup_driver(self):
        options = Options()
        options.add_experimental_option('excludeSwitches', config.BROWSER_CONFIG["exclude_switches"])
        options.add_experimental_option('useAutomationExtension', config.BROWSER_CONFIG["use_automation_extension"])
        options.binary_location = config.BROWSER_CONFIG["chrome_binary_location"]

        service = Service(executable_path=config.BROWSER_CONFIG["chromedriver_path"])
        self.driver = webdriver.Chrome(service=service, options=options)

        self.driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument',
                                    {'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'})

    def gundong(self, distance):
        try:
            js = "var q=document.documentElement.scrollTop=" + str(distance)
            self.driver.execute_script(js)
            time.sleep(0.5)
        except Exception as e:
            logging.error(f"Scrolling failed: {e}")

    def danxuan(self):
        try:
            dan = self.driver.find_elements(By.CSS_SELECTOR, config.CSS_SELECTORS["single_choice"])
            if not dan:
                logging.warning("No single choice elements found.")
                return
            for answer in dan:
                ans = answer.find_elements(By.CSS_SELECTOR, '.ui-radio')
                random.choice(ans).click()
                time.sleep(random.randint(0, 1))
        except NoSuchElementException:
            logging.error("Single choice answer elements not found.")

    def duoxuan(self):
        try:
            duo = self.driver.find_elements(By.CSS_SELECTOR, config.CSS_SELECTORS["multiple_choice"])
            if not duo:
                logging.warning("No multiple choice elements found.")
                return
            for answer in duo:
                ans = answer.find_elements(By.CSS_SELECTOR, '.ui-checkbox')
                for i in range(1, 7):
                    random.choice(ans).click()
                time.sleep(random.randint(0, 1))
        except NoSuchElementException:
            logging.error("Multiple choice  answer elements not found.")

    def tiankong(self, num):
        try:
            element = self.driver.find_element(By.CSS_SELECTOR, config.CSS_SELECTORS["fill_in_blank"].format(num=num))
            index = ["A", "B", "C"]
            answer = config.FILL_IN_ANSWERS
            element.send_keys(answer.get(index[random.randint(0, len(index)-1)]))
        except NoSuchElementException:
            logging.error(f"Fill-in-the-blank element not found for num={num}.")

    def renzheng(self):
        try:
            rectBottom = self.driver.find_element(By.CSS_SELECTOR, config.CSS_SELECTORS["rect_bottom"])
            rectBottom.click()
            time.sleep(5)
        except NoSuchElementException:
            logging.error("Rect bottom element not found.")

    def huakuai(self):
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

    def start_survey(self, times):
        for i in range(times):
            url_survey = config.SURVEY_URLS
            self.driver.get(url_survey)
            self.danxuan()
            self.duoxuan()
            self.gundong(600)
            self.tiankong(3)

            time.sleep(random.randint(0, 1))
            try:
                self.driver.find_element(By.CSS_SELECTOR, config.CSS_SELECTORS["submit_button"]).click()
            except NoSuchElementException:
                logging.error("Submit button not found.")
            time.sleep(4)
            self.renzheng()  # 智能认证函数调用
            self.huakuai()  # 滑块函数调用
            logging.info(f'已经提交了 {i + 1} 次问卷.')
            time.sleep(5)
            self.driver.quit()
            if i < times-1:
                self.setup_driver()  # 为下一次迭代重新初始化驱动

if __name__ == "__main__":
    survey_bot = SurveyAutomation()
    survey_bot.start_survey(2)
