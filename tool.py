import hashlib
import json
import logging
import os
import random

from selenium.webdriver.common.by import By

import config  # 导入配置文件


def generate_filename(url):
    # 使用哈希函数生成URL的唯一标识符
    hash_object = hashlib.md5(url.encode())  # 使用 MD5 哈希函数
    hash_digest = hash_object.hexdigest()
    # 生成文件名
    filename = f"{hash_digest}"  # 生成的文件名，使用 .json 作为扩展名
    return filename


def generate_css_selector(driver, element):
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


def extract_questions_and_options(driver):
    all_data = []

    # 查找所有问题区域
    question_elements = driver.find_elements(By.CSS_SELECTOR, "div.field")

    for index, question_element in enumerate(question_elements, start=1):
        question_text = question_element.find_element(By.CSS_SELECTOR, config.CSS_SELECTORS["question_selector"]).text.strip()
        option_elements = question_element.find_elements(By.CSS_SELECTOR,config.CSS_SELECTORS["option_selector"])

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
                "css_selector": generate_css_selector(driver, fill_in_blank_element)
            }]

        # 如果是单选题或多选题，处理选项
        if question_type in ['single_choice', 'multiple_choice']:
            options = []
            for option_index, option_element in enumerate(option_elements, start=1):
                option_text = option_element.text.strip()
                css_selector = generate_css_selector(driver, option_element)
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

    # 获取当前URL并生成合法的文件名
    current_url = driver.current_url
    filename = generate_filename(current_url)
    # 将数据保存为JSON文件，以URL为文件名
    with open(f'{filename}', 'w') as f:
        json.dump(all_data, f, ensure_ascii=False, indent=4)

def auto_fill_questionnaire(driver,filename):
    with open(f'{filename}', 'r') as f:
        all_data = json.load(f)

    # 逐一使用保存的CSS选择器定位并点击或填写元素
    for question in all_data:
        if question["question_type"] == "fill_in_blank":  # 处理填空题
            for option in question["options"]:
                element = driver.find_element(By.CSS_SELECTOR, option["css_selector"])
                element.send_keys(option["option_text"])
                logging.info(f"Filled in the blank for question {question['question_index']} with text: {option['option_text']}")
        elif question["question_type"] == "single_choice":  # 单选题，随机选择一个
            selected_option = random.choice(question["options"])
            element = driver.find_element(By.CSS_SELECTOR, selected_option["css_selector"])
            element.click()
            logging.info(f"Clicked on option {selected_option['option_index']} of question {question['question_index']}")
        elif question["question_type"] == "multiple_choice":  # 多选题，随机选择多个
            selected_options = random.sample(question["options"], k=random.randint(1, len(question["options"])))
            for selected_option in selected_options:
                element = driver.find_element(By.CSS_SELECTOR, selected_option["css_selector"])
                element.click()
                logging.info(f"Clicked on option {selected_option['option_index']} of question {question['question_index']}")


def execute_questionnaire_autofill(driver):
    # 打开目标网页
    driver.get(config.SURVEY_URLS)

    # 等待页面加载
    driver.implicitly_wait(10)  # 等待元素加载，最多等待10秒

    # 获取当前URL并生成合法的文件名
    current_url = driver.current_url
    filename = generate_filename(current_url) + ".json"  # 确保有扩展名

    # 检查文件是否存在
    if not os.path.exists(filename):
        # 如果文件不存在，提取问题和选项并保存到文件
        extract_questions_and_options(driver)
    else:
        logging.info(f"File '{filename}' already exists. Skipping extraction.")

    # 通过保存的CSS选择器自动填写问卷
    auto_fill_questionnaire(driver,filename)

    logging.info("Auto-fill completed successfully.")

# 执行问卷自动填写功能

