import os
import re
import pandas as pd

# 定義函數來處理單個文件
def process_transcript(file_path, executive_name, year_quarter_str):
    # 讀取文件內容
    with open(file_path, 'r', encoding='utf-8') as file:
        document_content = file.read()

    # 定義正則表達式來搜索特定經理人的發言
    executive_pattern = re.compile(rf"：{executive_name} - .*?[\s\S]*?(?=\n：[\w\s.]+ - |\Z)")

    # 搜索並提取特定經理人的發言
    executive_matches = executive_pattern.findall(document_content)

    # 將找到的發言合併成一個字符串
    executive_speech = "\n".join(executive_matches)

    # 構建文件名
    file_name_component = os.path.basename(file_path).split('.')[0]
    executive_speech_path = os.path.join('/Users/ro9air/Downloads/台積電2023~2002逐字稿/分割逐字稿工作區/分離後', 
                                         f'{file_name_component}_{executive_name}_Speech.txt')

    # 將發言寫入文件
    with open(executive_speech_path, 'w', encoding='utf-8') as file:
        file.write(executive_speech)

    return executive_speech_path

# 定義可能的經理人職稱
executive_titles = [
    'Morris Chang - Chairman and CEO',
    'Lora Ho - SVP and CFO',
    'C. C. Wei - CEO',
    'Wendell Huang - VP & CFO',
    'Jen-Chau Huang - VP & CFO',
    'Lora Ho - SVP, CFO and Spokesperson',
    'Rick Tsai - President and COO',
    'Harvey Chang - SVP and CFO',
    'Harvey Chang - Chief Financial Officer',
    ' - Senior Vice President, Chief Financial Officer',
    'Dr. Lora Ho - VP and CFO',
    'Lora Ho - VP and CFO',
    'Jen-Chau Huang - VP & CFO'
    'C. C. Wei - Vice Chairman & CEO',
    'Lora Ho - CFO',
    'Dr. Rick Tsai - President, COO',
    'Harvey Chang - Chief Financial Officer',
    'Dr. Morris Chang - Chairman and CEO',
    'Dr. Morris Chang - Chairman and CEO',
    'Dr. Rick Tsai - President and COO',
    'Dr. Lora Ho - VP and CFO',

]

# 指定資料夾路徑
directory = '/Users/ro9air/Downloads/台積電2023~2002逐字稿/分割逐字稿工作區/逐字稿'

# 遍歷資料夾內的每個文件
for filename in os.listdir(directory):
    if filename.endswith('.txt'):
        file_path = os.path.join(directory, filename)

        # 從文件名提取年份和季度
        year_quarter = re.search(r'(\d{4}Q\d)', filename)
        if year_quarter:
            year_quarter_str = year_quarter.group()
        else:
            year_quarter_str = 'UnknownYearQuarter'

        # 讀取文件並搜尋經理人
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            for title in executive_titles:
                executive_name = title.split(' - ')[0]
                if title in content:
                    processed_file_path = process_transcript(file_path, executive_name, year_quarter_str)
                    print(f'Processed file for {executive_name}: {processed_file_path}')
