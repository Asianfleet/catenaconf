import re

def extract_content(s):
    # 定义正则表达式模式，并使用捕获组来提取内容
    pattern = r'^\s*@{([^}]*)}\s*$'
    
    # 使用re.match检查字符串并提取内容
    match = re.match(pattern, s)
    if match:
        # 返回捕获组中的内容
        return match.group(1)
    else:
        # 如果不匹配，则返回None
        return None

# 测试示例
test_strings = [
    "   @{example}   ",  # 匹配
    "@{example}",        # 匹配
    "   @{example",      # 不匹配
    "{example}   ",      # 不匹配
    "   @example   ",    # 不匹配
    "   @{example} text",# 不匹配
]

for test in test_strings:
    content = extract_content(test)
    if content is not None:
        print(f"'{test}' -> 内容: '{content}'")
    else:
        print(f"'{test}' -> 不匹配")