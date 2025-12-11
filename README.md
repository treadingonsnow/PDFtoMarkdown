# PDF to Markdown 批量转换工具

一个简单高效的PDF批量转换工具，可以将PDF文件转换为Markdown格式，同时提取其中的图片。特别适合将大量PDF文档导入到Obsidian等Markdown笔记软件中。

## 功能特点

- 📄 **批量转换**: 一次性处理多个PDF文件
- 🖼️ **图片提取**: 自动提取PDF中的所有图片并保存
- 📝 **Obsidian优化**: 使用Obsidian图片链接格式，完美支持中文文件名
- 🚀 **高性能**: 基于PyMuPDF，转换速度快
- 📊 **进度显示**: 实时显示转换进度
- 🔧 **灵活配置**: 支持命令行参数和配置文件

## 安装

### 前置要求

- Python 3.7+

### 安装依赖

```bash
pip install -r requirements.txt
```

或手动安装：

```bash
pip install pymupdf pillow
```

## 使用方法

### 方法一：命令行参数

```bash
python pdf_to_markdown.py -i "PDF文件夹路径" -o "输出文件夹路径"
```

示例：

```bash
python pdf_to_markdown.py -i "C:/Documents/PDFs" -o "C:/Documents/Markdown"
```

### 方法二：修改脚本中的默认路径

打开 `pdf_to_markdown.py`，在 `main()` 函数中修改以下两行：

```python
pdf_directory = r"你的PDF文件夹路径"
output_directory = r"你的输出文件夹路径"
```

然后直接运行：

```bash
python pdf_to_markdown.py
```

## 输出结构

```
输出目录/
├── 文件1.md
├── 文件2.md
├── ...
└── images/
    ├── 文件1_page1_img1.png
    ├── 文件1_page2_img1.jpeg
    └── ...
```

## 示例

转换前：
```
输入文件夹/
├── 报告1.pdf
├── 报告2.pdf
└── 报告3.pdf
```

运行转换：
```bash
python pdf_to_markdown.py -i "输入文件夹" -o "输出文件夹"
```

转换后：
```
输出文件夹/
├── 报告1.md
├── 报告2.md
├── 报告3.md
└── images/
    ├── 报告1_page1_img1.png
    ├── 报告2_page1_img1.jpeg
    └── ...
```

## 配置选项

### 图片链接格式

默认使用Obsidian格式：`![[images/图片名.png]]`

如果需要使用标准Markdown格式，可以修改代码中的图片引用部分：

```python
# Obsidian格式（默认）
markdown_content.append(f"![[images/{image_filename}]]\n\n")

# 标准Markdown格式
markdown_content.append(f"![图片](images/{image_filename})\n\n")
```

### 添加页码标记

如果需要在Markdown中保留页码信息，可以取消注释代码中的相关部分：

```python
# 在 convert_pdf_to_markdown 方法中
if total_pages > 1:
    markdown_content.append(f"## 第 {page_num + 1} 页\n\n")
```

## 技术细节

- **PDF处理**: PyMuPDF (fitz)
- **图片处理**: Pillow
- **支持格式**:
  - 输入: PDF
  - 输出: Markdown (.md)
  - 图片: PNG, JPEG, 等PyMuPDF支持的格式

## 常见问题

### Q: 图片在Obsidian中不显示？

A: 确保使用的是Obsidian的wiki-style链接格式 `![[images/图片名]]`，而不是标准Markdown格式。本工具默认使用Obsidian格式。

### Q: 中文文件名乱码？

A: 本工具自动处理中文文件名，使用UTF-8编码保存。如果遇到问题，请检查你的系统编码设置。

### Q: 转换速度慢？

A: PyMuPDF是目前最快的PDF处理库之一。如果文件很大或包含大量图片，转换会需要一些时间。你可以看到实时进度显示。

### Q: 某些PDF转换失败？

A: 可能是PDF文件损坏或加密。检查失败信息，确保PDF文件可以正常打开。

## 贡献

欢迎提交Issue和Pull Request！

## 许可证

MIT License

## 致谢

- [PyMuPDF](https://github.com/pymupdf/PyMuPDF) - 强大的PDF处理库
- [Pillow](https://github.com/python-pillow/Pillow) - Python图像处理库

---

如果这个工具对你有帮助，请给个Star ⭐️
