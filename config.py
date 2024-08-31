# config.py

CSS_SELECTORS = {
    "single_choice": 'div.field.ui-field-contain',
    "multiple_choice": '#div2 > div.ui-controlgroup.column1',
    "fill_in_blank": '#q{num}',
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
FILL_IN_ANSWERS = {
    "A": "python真的好用！",
    "B": "这个测试很成功！",
    "C": "填空题随机填写文本"
}
