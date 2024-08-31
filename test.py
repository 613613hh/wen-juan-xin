import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import config  # 导入配置文件
import json

# 配置日志记录器
logging.basicConfig(level=logging.INFO,  # 设置日志级别为INFO
                    format='%(asctime)s - %(levelname)s - %(message)s',  # 日志格式
                    handlers=[logging.StreamHandler()])  # 输出到控制台


def setup_driver():
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


def get_css_selector(driver, element):
    # 获取元素的CSS路径
    script = """
    function cssPath(el) {
        if (!(el instanceof Element)) 
            return;
        var path = [];
        while (el.nodeType === Node.ELEMENT_NODE) {
            var selector = el.nodeName.toLowerCase();
            if (el.id) {
                selector += '#' + el.id;
                path.unshift(selector);
                break;
            } else {
                var sib = el, nth = 1;
                while (sib = sib.previousElementSibling) {
                    if (sib.nodeName.toLowerCase() == selector)
                       nth++;
                }
                if (nth != 1)
                    selector += ":nth-of-type("+nth+")";
            }
            path.unshift(selector);
            el = el.parentNode;
        }
        return path.join(" > ");
    }
    return cssPath(arguments[0]);
    """
    return driver.execute_script(script, element)


def save_questions_and_options(driver):
    # 定义包含问题和选项的CSS选择器
    question_selector = "div.topichtml"
    option_selector = "div.label"

    all_data = []

    # 查找所有问题区域
    question_elements = driver.find_elements(By.CSS_SELECTOR, "div.field")

    for index, question_element in enumerate(question_elements, start=1):
        question_text = question_element.find_element(By.CSS_SELECTOR, question_selector).text.strip()
        option_elements = question_element.find_elements(By.CSS_SELECTOR, option_selector)

        # 判断题型
        if len(option_elements) > 1 and "【多选题】" in question_text:
            question_type = 'multiple_choice'
        elif len(option_elements) > 1:
            question_type = 'single_choice'
        else:
            question_type = 'fill_in_blank'
            # 保存填空题的CSS选择器
            fill_in_blank_element = question_element.find_element(By.CSS_SELECTOR, config.CSS_SELECTORS["fill_in_blank"].format(num=index))
            options = [{
                "option_index": "1",
                "option_text": "Sample answer",  # 你可以用动态答案生成逻辑替换此处
                "css_selector": get_css_selector(driver, fill_in_blank_element)
            }]

        # 如果是单选题或多选题，处理选项
        if question_type in ['single_choice', 'multiple_choice']:
            options = []
            for option_index, option_element in enumerate(option_elements, start=1):
                option_text = option_element.text.strip()
                css_selector = get_css_selector(driver, option_element)
                options.append({
                    "option_index": option_index,
                    "option_text": option_text,
                    "css_selector": css_selector
                })

        all_data.append({
            "question_index": index,
            "question_text": question_text,
            "question_type": question_type,
            "options": options
        })

        logging.info(f"Saved question {index} ({question_type}) with {len(options)} options.")

    # 将数据保存为JSON文件
    with open('questions_and_options.json', 'w') as f:
        json.dump(all_data, f, ensure_ascii=False, indent=4)



def click_all_elements_with_saved_css_selectors(driver):
    with open('questions_and_options.json', 'r') as f:
        all_data = json.load(f)

    # 逐一使用保存的CSS选择器定位并点击或填写元素
    for question in all_data:
        if question["question_type"] == "fill_in_blank":  # 处理填空题
            for option in question["options"]:
                element = driver.find_element(By.CSS_SELECTOR, option["css_selector"])
                element.send_keys(option["option_text"])
                logging.info(f"Filled in the blank for question {question['question_index']} with text: {option['option_text']}")
        else:
            for option in question["options"]:
                element = driver.find_element(By.CSS_SELECTOR, option["css_selector"])
                element.click()
                logging.info(f"Clicked on option {option['option_index']} of question {question['question_index']}")


def test_click_all_elements_with_saved_css_selectors():
    driver = setup_driver()
    try:
        # 打开目标网页
        driver.get(config.SURVEY_URLS)

        # 等待页面加载
        driver.implicitly_wait(10)  # 等待元素加载，最多等待10秒

        # 保存问题和选项的CSS选择器
        save_questions_and_options(driver)

        # 模拟页面刷新或其他动作

        # 通过保存的CSS选择器重新定位并点击所有元素
        click_all_elements_with_saved_css_selectors(driver)

        # 测试成功
        logging.info("Test passed: All elements clicked and fill-in-the-blanks answered using saved CSS selectors.")

    except Exception as e:
        logging.error(f"Test failed due to an error: {e}")
    finally:
        driver.quit()


# 执行测试
test_click_all_elements_with_saved_css_selectors()
