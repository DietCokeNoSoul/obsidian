#!/usr/bin/env python3
"""
Obsidian文字提取工具 (Obsidian Text Extractor)
用于从Obsidian笔记库中提取所有文字内容
"""

import os
import re
import argparse
import json
from pathlib import Path
from typing import List, Dict, Set
import markdown
from markdown.extensions import extra

class ObsidianTextExtractor:
    """Obsidian文字提取器"""
    
    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.extracted_content = {}
        self.markdown_files = []
        
    def find_markdown_files(self) -> List[Path]:
        """查找所有Markdown文件"""
        markdown_files = []
        for root, dirs, files in os.walk(self.vault_path):
            # 跳过.obsidian配置文件夹
            if '.obsidian' in root:
                continue
            
            for file in files:
                if file.endswith('.md'):
                    markdown_files.append(Path(root) / file)
        
        self.markdown_files = markdown_files
        return markdown_files
    
    def clean_markdown_text(self, content: str) -> str:
        """清理Markdown格式，提取纯文本"""
        # 移除Obsidian特有的语法
        # 移除内部链接 [[链接]]
        content = re.sub(r'\[\[([^\]]+)\]\]', r'\1', content)
        
        # 移除图片引用 ![[image.png]]
        content = re.sub(r'!\[\[([^\]]+)\]\]', '', content)
        
        # 移除Markdown标题符号
        content = re.sub(r'^#+\s*', '', content, flags=re.MULTILINE)
        
        # 移除Markdown粗体和斜体
        content = re.sub(r'\*\*([^*]+)\*\*', r'\1', content)
        content = re.sub(r'\*([^*]+)\*', r'\1', content)
        
        # 移除代码块
        content = re.sub(r'```[^`]*```', '', content, flags=re.DOTALL)
        content = re.sub(r'`([^`]+)`', r'\1', content)
        
        # 移除列表标记
        content = re.sub(r'^\s*[-*+]\s*', '', content, flags=re.MULTILINE)
        content = re.sub(r'^\s*\d+\.\s*', '', content, flags=re.MULTILINE)
        
        # 移除表格分隔符
        content = re.sub(r'\|', ' ', content)
        content = re.sub(r'^:?-+:?\s*$', '', content, flags=re.MULTILINE)
        
        # 移除多余的空行
        content = re.sub(r'\n\s*\n', '\n\n', content)
        
        # 移除YAML front matter
        content = re.sub(r'^---\n.*?\n---\n', '', content, flags=re.DOTALL)
        
        return content.strip()
    
    def extract_from_markdown(self, file_path: Path) -> Dict[str, str]:
        """从Markdown文件提取文本"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 获取相对路径作为key
            relative_path = file_path.relative_to(self.vault_path)
            
            # 清理并提取文本
            clean_text = self.clean_markdown_text(content)
            
            return {
                'file_path': str(relative_path),
                'raw_content': content,
                'extracted_text': clean_text,
                'word_count': len(clean_text.split()),
                'char_count': len(clean_text)
            }
            
        except Exception as e:
            print(f"提取 {file_path} 时出错: {e}")
            return {}
    
    def extract_all_text(self) -> Dict[str, Dict]:
        """提取所有文本内容"""
        print(f"开始从 {self.vault_path} 提取文本...")
        
        # 查找所有Markdown文件
        markdown_files = self.find_markdown_files()
        print(f"找到 {len(markdown_files)} 个Markdown文件")
        
        extracted_content = {}
        total_words = 0
        total_chars = 0
        
        for file_path in markdown_files:
            print(f"正在处理: {file_path.relative_to(self.vault_path)}")
            content = self.extract_from_markdown(file_path)
            
            if content:
                extracted_content[str(file_path.relative_to(self.vault_path))] = content
                total_words += content.get('word_count', 0)
                total_chars += content.get('char_count', 0)
        
        # 添加统计信息
        extracted_content['_statistics'] = {
            'total_files': len(markdown_files),
            'total_words': total_words,
            'total_characters': total_chars,
            'vault_path': str(self.vault_path)
        }
        
        self.extracted_content = extracted_content
        return extracted_content
    
    def save_extracted_text(self, output_file: str = None, format: str = 'json'):
        """保存提取的文本"""
        if not output_file:
            output_file = f"extracted_text.{format}"
        
        output_path = self.vault_path / output_file
        
        if format == 'json':
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(self.extracted_content, f, ensure_ascii=False, indent=2)
            print(f"提取的内容已保存到: {output_path}")
            
        elif format == 'txt':
            with open(output_path, 'w', encoding='utf-8') as f:
                stats = self.extracted_content.get('_statistics', {})
                f.write(f"=== Obsidian文字提取结果 ===\n")
                f.write(f"库路径: {stats.get('vault_path', '')}\n")
                f.write(f"文件总数: {stats.get('total_files', 0)}\n")
                f.write(f"总字数: {stats.get('total_words', 0)}\n")
                f.write(f"总字符数: {stats.get('total_characters', 0)}\n")
                f.write("\n" + "="*50 + "\n\n")
                
                for file_path, content in self.extracted_content.items():
                    if file_path != '_statistics':
                        f.write(f"=== {file_path} ===\n")
                        f.write(content.get('extracted_text', ''))
                        f.write("\n\n" + "-"*30 + "\n\n")
            
            print(f"提取的文本已保存到: {output_path}")
    
    def print_summary(self):
        """打印提取摘要"""
        if not self.extracted_content:
            print("尚未提取任何内容")
            return
            
        stats = self.extracted_content.get('_statistics', {})
        print(f"\n=== 提取摘要 ===")
        print(f"处理文件: {stats.get('total_files', 0)} 个")
        print(f"总字数: {stats.get('total_words', 0)} 字")
        print(f"总字符数: {stats.get('total_characters', 0)} 字符")
        
        print(f"\n=== 文件列表 ===")
        for file_path, content in self.extracted_content.items():
            if file_path != '_statistics':
                word_count = content.get('word_count', 0)
                print(f"  {file_path}: {word_count} 字")


def main():
    parser = argparse.ArgumentParser(description='Obsidian文字提取工具')
    parser.add_argument('vault_path', nargs='?', default='.', 
                       help='Obsidian库路径 (默认: 当前目录)')
    parser.add_argument('-o', '--output', default='extracted_text',
                       help='输出文件名前缀 (默认: extracted_text)')
    parser.add_argument('-f', '--format', choices=['json', 'txt', 'both'], 
                       default='both', help='输出格式 (默认: both)')
    parser.add_argument('--summary', action='store_true',
                       help='只显示摘要，不保存文件')
    
    args = parser.parse_args()
    
    # 创建提取器
    extractor = ObsidianTextExtractor(args.vault_path)
    
    # 提取文本
    extractor.extract_all_text()
    
    # 显示摘要
    extractor.print_summary()
    
    # 保存结果
    if not args.summary:
        if args.format in ['json', 'both']:
            extractor.save_extracted_text(f"{args.output}.json", 'json')
        if args.format in ['txt', 'both']:
            extractor.save_extracted_text(f"{args.output}.txt", 'txt')


if __name__ == "__main__":
    main()