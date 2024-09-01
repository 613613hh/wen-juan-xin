# config.py

CSS_SELECTORS = {
    "question_selector" : "div.topichtml",
    "option_selector" : "div.label",
    "fill_in_blank": '#q{num}',
    "submit_button": '#ctlNext',
    "authentication_button": '#layui-layer1 > div.layui-layer-btn.layui-layer-btn- > a.layui-layer-btn0',
    "rect_bottom": 'div#rectBottom.rect-bottom'
}
OPENAI_KEY="sk-fFfYNs20p9txbUu3PnseAIQ2ZqF9PcijPtpz7DKRYtNMcXmg"
BASEURL="https://api.chatanywhere.tech/v1"


BROWSER_CONFIG = {
    "chrome_binary_location": r'C:\Program Files\Google\Chrome\Application\chrome.exe',
    "chromedriver_path": r'D:\Desktop\wenjuanxin\chromedriver.exe',
    "exclude_switches": ['enable-automation'],
    "use_automation_extension": False
}
# 测试
# SURVEY_URLS = 'https://www.wjx.cn/vm/hiQpVeR.aspx'

SURVEY_URLS = 'https://kaoshi.wjx.top/vm/mqZfxTx.aspx'

SAMPLE_ANSWER = 'Sample answer'

# MODELNAME= {
#     "wenxinyiyan" : "qianfan",
#     "openai" : "openai",
# }
MODELNAME="openai"


question_template=""" "role": "system",
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
        }"""

answer_template="""
        正确答案：[B，D] 
       """


base_prompt = [
    {
        "role": "system",
        "content": "从现在开始，您是人力资源专家,为我解答各种选择题，并按照模板回答(答案需用[]包裹)。"
    },{
        "role": "user",
        "content": question_template
    },{
        "role": "assistant",
        "content": answer_template
    }
]
