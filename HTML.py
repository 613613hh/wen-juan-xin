import json
from bs4 import BeautifulSoup
from selenium import webdriver
import config  # 导入配置文件

# 初始化浏览器
driver = webdriver.Chrome()  # 确保你已安装ChromeDriver或其他浏览器的驱动

# 打开目标网页
driver.get(config.SURVEY_URLS)

# 等待并手动或自动通过验证码
# 通过验证码后，你可以用BeautifulSoup继续处理
page_source = driver.page_source
soup = BeautifulSoup(page_source, "html.parser")

# 提取标题
title = soup.find('h1', class_='htitle').text.strip()

# 提取描述，可能存在或不存在
description_tag = soup.find('span', class_='description')
description = description_tag.text.strip() if description_tag else ""

# 提取问题和选项，并补充题号和选项的CSS地址
questions = []
for index, field in enumerate(soup.find_all('div', class_='field'), start=1):
    question_text = field.find('div', class_='topichtml').text.strip()
    options = []

    # 遍历每个选项
    for option_index, label in enumerate(field.find_all('div', class_='label'), start=1):
        option_text = label.text.strip()

        # 构建CSS路径，结合Selenium获取唯一路径
        element_id = label.get_attribute('id') if label.has_attr('id') else None
        css_path = f"#{element_id}" if element_id else f"div.field:nth-of-type({index}) div.label:nth-of-type({option_index})"

        options.append({
            'text': option_text,
            'css_path': css_path
        })

    questions.append({
        'question_number': index,
        'question': question_text,
        'options': options
    })

# 组织数据
data = {
    'title': title,
    'description': description,
    'questions': questions
}

# 保存为JSON文件
with open('survey_data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print("Data saved to survey_data.json")

# 关闭浏览器
driver.quit()
