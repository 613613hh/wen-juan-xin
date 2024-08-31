# -*- coding: utf-8 -*-
import os
import qianfan

# 设置环境变量
os.environ["QIANFAN_AK"] = "QcJI8LwewQ4Z3ayP3IRejTAN"
os.environ["QIANFAN_SK"] = "NYbSGzrfVuY2ebVI4s2fTlzIvLpOD0Zk"

chat_comp = qianfan.ChatCompletion()

# 定义消息内容
messages = [
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
    },
    {
        "role": "user",
        "content": '''{
            "question_index": 70,
            "question_text": "( )属于组合工资结构。【多选题】",
            "question_type": "multiple_choice",
            "options": [
                {
                    "option_index": 1,
                    "option_text": "A)岗位技能工资",
                    "css_selector": "div#div70 > div:nth-of-type(2) > div > div"
                },
                {
                    "option_index": 2,
                    "option_text": "B)能力资格工资",
                    "css_selector": "div#div70 > div:nth-of-type(2) > div:nth-of-type(2) > div"
                },
                {
                    "option_index": 3,
                    "option_text": "C)岗位效益工资",
                    "css_selector": "div#div70 > div:nth-of-type(2) > div:nth-of-type(3) > div"
                },
                {
                    "option_index": 4,
                    "option_text": "D)技术等级工资",
                    "css_selector": "div#div70 > div:nth-of-type(2) > div:nth-of-type(4) > div"
                },
                {
                    "option_index": 5,
                    "option_text": "E)薪点工资",
                    "css_selector": "div#div70 > div:nth-of-type(2) > div:nth-of-type(5) > div"
                }
            ]
        }正确答案输出格式示例[1，3，5]'''
    }
]

# 执行对话
resp = chat_comp.do(model="ERNIE-4.0-8K", messages=messages)

# 打印响应内容
print(resp["body"]["result"])
