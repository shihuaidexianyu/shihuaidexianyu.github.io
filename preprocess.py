import os
import html
import re
import json


def get_skip_markdown_files(file_path):
    '''
    得到不处理的文件的集合
    '''
    skip_files = set()
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                filename = line.strip()
                if filename:
                    skip_files.add(filename)
    except Exception as e:
        print(f"读取文件 {file_path} 时出错: {e}")
    return skip_files


def check_markdown_content(content):
    '''
    v-pre检测
    '''
    if content.startswith('::: v-pre') and content.rstrip().endswith(':::'):
        return content
    return f'::: v-pre\n{content}\n:::'


def replace_html_entities(content):
    '''
    替换字符串中的HTML实体为对应的普通字符
    '''
    try:
        return html.unescape(content)
    except Exception as e:
        print(f"替换HTML实体时出错: {e}")
        return content

def convert_img_tags_to_markdown(content):
    '''
    将Markdown内容中的HTML <img> 标签替换为Markdown图片语法。
    具体来说，提取每个 <img> 标签的 src 和 alt 属性，并转换为 ![alt](src) 格式。
    处理标签属性的不同顺序和可能的额外属性。
    '''
    try:
        # 匹配所有 <img> 标签
        img_tag_pattern = re.compile(r'<img\s+[^>]*>', re.IGNORECASE)

        def replace_img_tag(match):
            img_tag = match.group()
            # 提取 src 属性
            src_match = re.search(r'src=["\'](.*?)["\']', img_tag, re.IGNORECASE)
            src = src_match.group(1) if src_match else ''
            # 提取 alt 属性
            alt_match = re.search(r'alt=["\'](.*?)["\']', img_tag, re.IGNORECASE)
            alt = alt_match.group(1) if alt_match else ''
            return f'![{alt}]({src})'

        # 替换所有 <img> 标签
        converted_content = img_tag_pattern.sub(replace_img_tag, content)
        return converted_content
    except Exception as e:
        print(f"转换过程中出错: {e}")
        return content


def convert_punctuations(content):
    '''
    将Markdown内容中的中文标点符号替换为对应的英文标点符号。
    '''
    punctuation_map = {
        '，': ',',
        '。': '.',
        '！': '!',
        '？': '?',
        '：': ':',
        '；': ';',
        '“': '"',
        '”': '"',
        '‘': "'",
        '’': "'",
        '（': '(',
        '）': ')',
        '【': '[',
        '】': ']',
        '《': '<',
        '》': '>',
        '……': '...',
        '——': '--',
        '、': ',',
        '～': '~',
        '·': '.',
    }

    try:
        # 创建正则表达式模式，匹配所有中文标点符号
        pattern = re.compile('|'.join(re.escape(key) for key in punctuation_map.keys()))

        # 定义替换函数
        def replace(match):
            return punctuation_map[match.group()]

        # 找到所有 Markdown 图片语句的位置
        image_pattern = re.compile(r'!\[.*?\]\(.*?\)')
        image_blocks = [(m.start(), m.end()) for m in image_pattern.finditer(content)]

        # 执行替换
        def replacement(match):
            match_pos = match.start()
            # 检查是否在 Markdown 图片语句中
            in_image_block = any(start <= match_pos < end for start, end in image_blocks)
            if in_image_block:
                return match.group()  # 不替换
            return replace(match)

        converted_content = pattern.sub(replacement, content)
        return converted_content
    except Exception as e:
        print(f"替换标点符号时出错: {e}")
        return content

actions = "" # 生成的actions内容
themes = ['brand', 'alt'] # 主题列表

def process_markdown_files(directory_path, skip_files):
    global actions
    try:
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                if file.endswith('.md') and file not in skip_files:
                    file_path = os.path.join(root, file)
                    try:
                        # 对文件进行处理的逻辑，例如读取文件内容
                        with open(file_path, 'r+', encoding='utf-8') as f:
                            # 读取f的内容
                            content = f.read()
                            # 将HTML <img> 标签转换为Markdown图片语法
                            content = convert_img_tags_to_markdown(content)
                            # 将中文标点符号替换为英文标点符号
                            # content = convert_punctuations(content)
                            # 替换HTML实体为普通字符
                            content = replace_html_entities(content)
                            # 添加v-pre保护标记
                            content = check_markdown_content(content)
                            # 写回f中
                            f.seek(0)
                            f.truncate()
                            f.write(content)
                            print(f"正在处理文件: {file_path}")
                        # 生成actions内容
                        relative_path = os.path.relpath(file_path, directory_path).replace('\\', '/')
                        relative_path = relative_path.replace('core/', '', 1)
                        file_name = os.path.splitext(file)[0]
                        theme = themes[len(actions.split('\n')) % len(themes)]
                        new_content = f'    - theme: {theme}\n      text: {file_name}\n      link: {relative_path}\n'
                        print(new_content)
                        actions += new_content


                    except Exception as e:
                        print(f"处理文件 {file_path} 时出错: {e}")
    except Exception as e:
        print(f"遍历目录 {directory_path} 时出错: {e}")

# 使用os.path.join()构建跨平台路径
actions_target_file = os.path.join('core', 'note','list.md')

def process_action_file():
    try:
        # 确保文件存在
        if not os.path.exists(actions_target_file):
            print(f'目标文件未找到: {actions_target_file}')
            return

        with open(actions_target_file, 'r+', encoding='utf-8') as file:
            data = file.read()
            actions_index = data.find('actions:')
            if actions_index == -1:
                print(f'在文件 {actions_target_file} 中未找到 actions: 标记')
                return

            header = data[:actions_index + len('actions:')]
            updated_content = f'{header}\n{actions}\n---'

            # 添加调试信息
            print(f'正在写入文件: {actions_target_file}')
            print(f'内容长度: {len(updated_content)}')

            file.seek(0)
            file.truncate()
            file.write(updated_content)
            print('Actions 更新成功')
    except Exception as e:
        print(f'处理文件时出错: {e}')

def get_items(dir, base_path=''):
    items = []
    entries = os.listdir(dir)
    for entry in entries:
        full_path = os.path.join(dir, entry)
        if os.path.isdir(full_path):
            # 遇到目录，递归处理, 最多6层
            sub_items = get_items(full_path, os.path.join(base_path, entry).replace(os.sep, '/'))
            if sub_items:
                items.append({
                    'text': entry,
                    'collapsed': False,# 要在生成的字典中将 'collapsed' 的值设置为布尔值 False 而不是字符串 'false'，可以直接使用 Python 的布尔值 False。
                    'items': sub_items
                })
        elif os.path.isfile(full_path) and entry.endswith('.md'):
            # 遇到 Markdown 文件
            name = os.path.splitext(entry)[0]+os.path.splitext(entry)[1]
            #print(name)

            # 忽略skip_list中的文件
            if name.lower() not in skip_list:
                items.append({
                    'text': name,
                    'link': os.path.join('/', base_path, name).replace(os.sep, '/')
                })
    return items

def generate_sidebar():
    # 定义文档目录
    docs_dir = os.path.join(os.path.dirname(__file__), 'core')
    sidebar_items_file = os.path.join(docs_dir, '.vitepress', 'sidebarItems.js')

    # 获取所有 Markdown 文件，组织为导航菜单项
    sidebar_items = get_items(docs_dir)

    # 定义生成的代码内容
    sidebar_code = f"""// 此文件由 preprocess 自动生成，请勿手动修改
export default {json.dumps(sidebar_items,  ensure_ascii=False,indent=2)};
"""

    # 确保 .vitepress 目录存在
    vitepress_dir = os.path.join(docs_dir, '.vitepress')
    if not os.path.exists(vitepress_dir):
        os.makedirs(vitepress_dir)

    # 将生成的代码写入 sidebarItems.js 文件
    with open(sidebar_items_file, 'w', encoding='utf-8') as f:
        f.write(sidebar_code)

    print('sidebarItems.js 生成成功')

def generate_navigation():
    # 定义文档目录
    docs_dir = os.path.join(os.path.dirname(__file__), 'core')
    navigation_items_file = os.path.join(docs_dir, '.vitepress', 'navItems.js')

    # 获取所有 Markdown 文件，组织为导航菜单项
    navigation_items = get_items(docs_dir)

    # 定义生成的代码内容
    navigation_code = f"""// 此文件由 preprocess 自动生成，请勿手动修改
export default {json.dumps(navigation_items,  ensure_ascii=False,indent=2)};
"""

    # 确保 .vitepress 目录存在
    vitepress_dir = os.path.join(docs_dir, '.vitepress')
    if not os.path.exists(vitepress_dir):
        os.makedirs(vitepress_dir)

    # 将生成的代码写入 navItems.js 文件
    with open(navigation_items_file, 'w', encoding='utf-8') as f:
        f.write(navigation_code)

    print('navItems.js 生成成功')



if __name__ == "__main__":
    directory = 'core'
    skip_list = get_skip_markdown_files('skip_list.txt')
    process_markdown_files(directory, skip_list)
    # 在process_markdown_files之后运行process_action_file
    process_action_file()
    generate_sidebar()
    #generate_navigation()
    print('文档预处理完成')
