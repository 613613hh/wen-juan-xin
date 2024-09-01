import json
import logging
import re
from selenium.webdriver.common.by import By
import config
from models.openai_model import OpenAIModel
from models.qianfan_model import QianfanModel


def get_model_instance(model_name):
    if model_name == "qianfan":
        return QianfanModel()
    elif model_name == "openai":
        return OpenAIModel()
    else:
        raise ValueError("Unsupported model name")



def create_message_from_question(question_data):
    messages = config.base_prompt + [
        {
            "role": "user",
            "content": json.dumps(question_data)
        }
    ]
    return messages


def execute_conversation(messages, model):
    try:
        # 使用传入的模型实例来执行对话
        raw_output = model.get_response(messages)
        logging.info(f"Messages: {raw_output}")
        return clean_model_output(raw_output)
    except Exception as e:
        logging.error(f"Error during conversation execution: {str(e)}")
        return f"Error: {str(e)}"



def clean_model_output(output):
    match = re.findall(r'\[(.*?)\]', output)  # 匹配[]内的内容
    if match:
        if match[0]:  # 如果括号内非空
            letters = re.findall(r'[a-zA-Z]+', match[0])  # 匹配括号内的字母
        else:  # 如果括号内为空
            letters = re.findall(r'[a-zA-Z]+', output)  # 匹配全局字母
    else:
        letters = re.findall(r'[a-zA-Z]+', output)  # 如果没有括号，匹配全局字母

    # 将字母转换为对应的数字字符
    numbers = [str(ord(letter.lower()) - ord('a') + 1) for letter in letters]

    return numbers



def log_question_and_answer(question_data, cleaned_output):
    question_index = question_data["question_index"]
    question_text = question_data["question_text"]
    options = question_data["options"]

    logging.info(f"题目 {question_index}: {question_text}")
    logging.info(f"答案选项: {cleaned_output}")

    selected_options = []
    for index in cleaned_output:
        for option in options:
            if option["option_index"] == index:
                selected_options.append(option["option_text"])
                logging.info(f"选项 {index}: {option['option_text']}")

    logging.info("-----------------------------------------------------")


def process_choicequestion(question, driver):
    model = get_model_instance(config.MODELNAME)
    element_list = []
    # 创建消息列表
    messages = create_message_from_question(question)
    # 获取模型的响应
    ans_list = execute_conversation(messages, model)
    # 记录问题和答案
    log_question_and_answer(question, ans_list)
    for option in question["options"]:
        if option["option_index"] in ans_list:
            element = driver.find_element(By.CSS_SELECTOR, option["css_selector"])
            element_list.append(element)
    # 执行点击操作
    for element in element_list:
        element.click()

# def process_questions_from_file(file_path):
#     driver = webdriver.Chrome()  # 根据实际使用的浏览器驱动实例化 WebDriver
#     driver.get(config.SURVEY_URLS)  # 替换为实际目标页面的 URL
#
#     with open(file_path, 'r', encoding='GBK') as f:
#         all_questions = json.load(f)
#         for question in all_questions:
#             process_choicequestion(question, driver)
#     driver.quit()

# process_questions_from_file('4c008ba8dccfd63029e23c34172b1a64.json')
