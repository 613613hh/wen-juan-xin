import json
import os
import qianfan
import re
import logging

# 设置环境变量
os.environ["QIANFAN_AK"] = "QcJI8LwewQ4Z3ayP3IRejTAN"
os.environ["QIANFAN_SK"] = "NYbSGzrfVuY2ebVI4s2fTlzIvLpOD0Zk"

# 初始化聊天接口
chat_comp = qianfan.ChatCompletion()

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 示例的初始提示
base_prompt = [
    {
        "role": "user",
        "content": '''{
            "question_index": 61,
            "question_text": "从考评的性质和特点上看，行为导向型的主观评价方法( )。【多选题】",
            "question_type": "multiple_choice",
            "options": [
                {
                    "option_index": 1,
                    "option_text": "A)考评有客观依据",
                    "css_selector": "div#div61 > div:nth-of-type(2) > div > div"
                },
                {
                    "option_index": 2,
                    "option_text": "B)缺乏量化的考评标准",
                    "css_selector": "div#div61 > div:nth-of-type(2) > div:nth-of-type(2) > div"
                },
                {
                    "option_index": 3,
                    "option_text": "C)可用于考评团队绩效",
                    "css_selector": "div#div61 > div:nth-of-type(2) > div:nth-of-type(3) > div"
                },
                {
                    "option_index": 4,
                    "option_text": "D)受考评者主观因素的制约和影响",
                    "css_selector": "div#div61 > div:nth-of-type(2) > div:nth-of-type(4) > div"
                },
                {
                    "option_index": 5,
                    "option_text": "E)通过整体绩效来衡量员工的个体工作绩效",
                    "css_selector": "div#div61 > div:nth-of-type(2) > div:nth-of-type(5) > div"
                }
            ]
        }正确答案输出格式示例[1，3，5]'''
    },
    {
        "role": "assistant",
        "content": "[2，5]"
    }
]


def create_message_from_question(question_data):
    """
    将传入的JSON对象转换为messages结构
    :param question_data: 传入的JSON对象
    :return: 生成的messages列表
    """
    messages = base_prompt + [
        {
            "role": "user",
            "content": json.dumps(question_data) + "正确答案输出格式示例[1，3，5]"
        }
    ]
    return messages


def execute_conversation(messages):
    """
    执行对话并返回响应
    :param messages: 传入的messages列表
    :return: 返回的响应内容
    """
    try:
        response = chat_comp.do(model="ERNIE-4.0-8K", messages=messages)
        raw_output = response["body"]["result"]
        return clean_model_output(raw_output)
    except Exception as e:
        return f"Error: {str(e)}"


def clean_model_output(output):
    """
    使用正则表达式清理大模型的输出，提取正确的答案列表
    :param output: 大模型的原始输出
    :return: 处理后的输出
    """
    match = re.findall(r'\d+', output)  # 匹配所有的数字
    cleaned_output = '[' + ', '.join(match) + ']'  # 将数字列表格式化为所需的输出形式
    return cleaned_output


def log_question_and_answer(question_data, cleaned_output):
    """
    记录题目信息、模型的答案及具体选项内容
    :param question_data: 当前题目的数据
    :param cleaned_output: 模型的清理后输出（答案编号）
    """
    question_index = question_data["question_index"]
    question_text = question_data["question_text"]
    options = question_data["options"]

    # 提取答案编号
    answer_indices = re.findall(r'\d+', cleaned_output)

    # 记录日志
    logging.info(f"题目 {question_index}: {question_text}")
    logging.info(f"答案选项: {cleaned_output}")

    selected_options = []
    for index in answer_indices:
        for option in options:
            if str(option["option_index"]) == index:
                selected_options.append(option["option_text"])
                logging.info(f"选项 {index}: {option['option_text']}")

    logging.info("-----------------------------------------------------")


def process_questions_from_file(file_path):
    with open(file_path, 'r', encoding='gbk') as f:
        all_questions = json.load(f)
        for question_data in all_questions:
            messages = create_message_from_question(question_data)
            response = execute_conversation(messages)
            log_question_and_answer(question_data, response)


# 示例使用
process_questions_from_file('4c008ba8dccfd63029e23c34172b1a64.json')
