# config.py

CSS_SELECTORS = {
    "question_selector" : "div.topichtml",
    "option_selector" : "div.label",
    "submit_button": '#ctlNext',
    "authentication_button": '#layui-layer1 > div.layui-layer-btn.layui-layer-btn- > a.layui-layer-btn0',
    "rect_bottom": 'div#rectBottom.rect-bottom'
}

BROWSER_CONFIG = {
    "chrome_binary_location": r'C:\Program Files\Google\Chrome\Application\chrome.exe',
    "chromedriver_path": r'D:\Desktop\wenjuanxin\chromedriver.exe',
    "exclude_switches": ['enable-automation'],
    "use_automation_extension": False
}
# 测试
# SURVEY_URLS = 'https://www.wjx.cn/vm/hiQpVeR.aspx'

SURVEY_URLS = 'https://kaoshi.wjx.top/vm/mqZfxTx.aspx'

