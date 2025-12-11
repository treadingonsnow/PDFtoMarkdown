"""
配置文件示例
复制此文件为 config.py 并修改为你自己的路径
"""

# PDF文件所在目录
PDF_INPUT_DIR = r"C:\Users\YourName\Documents\PDFs"

# Markdown输出目录
MARKDOWN_OUTPUT_DIR = r"C:\Users\YourName\Documents\Markdown"

# 图片链接格式
# "obsidian" - 使用 ![[images/图片名]] 格式（推荐用于Obsidian）
# "standard" - 使用 ![](images/图片名) 标准Markdown格式
IMAGE_LINK_FORMAT = "obsidian"

# 是否在Markdown中添加页码标记
INCLUDE_PAGE_NUMBERS = False

# 进度显示间隔（每处理多少页显示一次进度）
PROGRESS_INTERVAL = 10
