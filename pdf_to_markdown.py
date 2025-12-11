#!/usr/bin/env python3
"""
PDF批量转换为Markdown工具
使用PyMuPDF (fitz)提取PDF中的文本和图片，转换为Markdown格式
"""

import os
import sys
import fitz
import argparse
from pathlib import Path
from typing import List, Tuple
import re


class PDFToMarkdown:
    def __init__(self, pdf_dir: str, output_dir: str):
        """
        初始化转换器

        Args:
            pdf_dir: PDF文件所在目录
            output_dir: Markdown输出目录
        """
        self.pdf_dir = Path(pdf_dir)
        self.output_dir = Path(output_dir)
        self.images_dir = self.output_dir / "images"

        # 创建输出目录
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.images_dir.mkdir(parents=True, exist_ok=True)

    def get_pdf_files(self) -> List[Path]:
        """获取目录下所有PDF文件"""
        if not self.pdf_dir.exists():
            raise FileNotFoundError(f"PDF目录不存在: {self.pdf_dir}")

        pdf_files = list(self.pdf_dir.glob("*.pdf"))
        return sorted(pdf_files)

    def sanitize_filename(self, filename: str) -> str:
        """清理文件名，移除非法字符"""
        # 移除或替换Windows文件名中的非法字符
        illegal_chars = r'[<>:"/\\|?*]'
        sanitized = re.sub(illegal_chars, '_', filename)
        return sanitized

    def extract_images(self, page, pdf_name: str, page_num: int) -> List[Tuple[int, str]]:
        """
        从页面提取图片

        Args:
            page: PDF页面对象
            pdf_name: PDF文件名(不含扩展名)
            page_num: 页码

        Returns:
            List of (xref, image_path) tuples
        """
        images_info = []
        image_list = page.get_images(full=True)

        for img_index, img in enumerate(image_list):
            xref = img[0]

            try:
                # 提取图片
                base_image = page.parent.extract_image(xref)
                image_bytes = base_image["image"]
                image_ext = base_image["ext"]

                # 生成图片文件名
                image_filename = f"{pdf_name}_page{page_num}_img{img_index + 1}.{image_ext}"
                image_path = self.images_dir / image_filename

                # 保存图片
                with open(image_path, "wb") as img_file:
                    img_file.write(image_bytes)

                # 返回图片文件名用于Markdown（Obsidian格式）
                images_info.append((xref, image_filename))

            except Exception as e:
                print(f"  警告: 无法提取图片 {img_index + 1} (页面 {page_num}): {e}")
                continue

        return images_info

    def convert_pdf_to_markdown(self, pdf_path: Path) -> str:
        """
        将单个PDF转换为Markdown

        Args:
            pdf_path: PDF文件路径

        Returns:
            Markdown内容
        """
        pdf_name = pdf_path.stem
        markdown_content = []

        # 添加文档标题
        markdown_content.append(f"# {pdf_name}\n\n")

        try:
            doc = fitz.open(pdf_path)
            total_pages = len(doc)

            print(f"  处理中... 共 {total_pages} 页")

            for page_num in range(total_pages):
                page = doc[page_num]

                # 提取文本
                text = page.get_text()

                # 提取图片
                images = self.extract_images(page, pdf_name, page_num + 1)

                # 添加文本内容
                if text.strip():
                    markdown_content.append(text)
                    markdown_content.append("\n\n")

                # 添加图片引用（使用Obsidian格式）
                for _, image_filename in images:
                    markdown_content.append(f"![[images/{image_filename}]]\n\n")

                # 显示进度
                if (page_num + 1) % 10 == 0 or (page_num + 1) == total_pages:
                    print(f"  进度: {page_num + 1}/{total_pages} 页")

            doc.close()

        except Exception as e:
            raise Exception(f"转换PDF时出错: {e}")

        return "".join(markdown_content)

    def process_all_pdfs(self):
        """批量处理所有PDF文件"""
        pdf_files = self.get_pdf_files()

        if not pdf_files:
            print(f"在 {self.pdf_dir} 中没有找到PDF文件")
            return

        print(f"\n找到 {len(pdf_files)} 个PDF文件")
        print(f"输出目录: {self.output_dir}")
        print(f"图片目录: {self.images_dir}\n")
        print("=" * 60)

        success_count = 0
        failed_files = []

        for idx, pdf_path in enumerate(pdf_files, 1):
            print(f"\n[{idx}/{len(pdf_files)}] 正在转换: {pdf_path.name}")

            try:
                # 转换PDF
                markdown_content = self.convert_pdf_to_markdown(pdf_path)

                # 保存Markdown文件
                md_filename = self.sanitize_filename(pdf_path.stem) + ".md"
                md_path = self.output_dir / md_filename

                with open(md_path, "w", encoding="utf-8") as f:
                    f.write(markdown_content)

                print(f"  ✓ 成功: {md_filename}")
                success_count += 1

            except Exception as e:
                print(f"  ✗ 失败: {e}")
                failed_files.append((pdf_path.name, str(e)))

        # 显示汇总信息
        print("\n" + "=" * 60)
        print(f"\n转换完成!")
        print(f"成功: {success_count}/{len(pdf_files)}")

        if failed_files:
            print(f"失败: {len(failed_files)}")
            print("\n失败的文件:")
            for filename, error in failed_files:
                print(f"  - {filename}: {error}")

        print(f"\n输出位置: {self.output_dir.absolute()}")


def main():
    """主函数"""
    # 创建命令行参数解析器
    parser = argparse.ArgumentParser(
        description='PDF批量转换为Markdown工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例:
  %(prog)s -i "C:/PDFs" -o "C:/Markdown"
  %(prog)s --input "PDF文件夹" --output "输出文件夹"
        '''
    )

    parser.add_argument(
        '-i', '--input',
        type=str,
        help='PDF文件所在目录路径'
    )

    parser.add_argument(
        '-o', '--output',
        type=str,
        help='Markdown输出目录路径'
    )

    parser.add_argument(
        '-v', '--version',
        action='version',
        version='%(prog)s 1.0.0'
    )

    args = parser.parse_args()

    # 如果提供了命令行参数，使用参数；否则使用默认值
    if args.input and args.output:
        pdf_directory = args.input
        output_directory = args.output
    else:
        # 默认路径（修改为你自己的路径，或使用命令行参数）
        pdf_directory = r""  # 例如: r"C:\Users\YourName\Documents\PDFs"
        output_directory = r""  # 例如: r"C:\Users\YourName\Documents\Markdown"

        # 如果默认路径为空，提示用户
        if not pdf_directory or not output_directory:
            print("错误: 请提供PDF输入目录和输出目录")
            print("\n使用方法:")
            print("  python pdf_to_markdown.py -i <PDF目录> -o <输出目录>")
            print("\n或者修改脚本中的默认路径")
            parser.print_help()
            sys.exit(1)

    print("=" * 60)
    print("PDF批量转换为Markdown工具")
    print("=" * 60)
    print(f"\nPDF目录: {pdf_directory}")
    print(f"输出目录: {output_directory}")

    try:
        converter = PDFToMarkdown(pdf_directory, output_directory)
        converter.process_all_pdfs()

    except Exception as e:
        print(f"\n错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
