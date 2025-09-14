# Obsidian 文字提取工具

这是一个用于从 Obsidian 笔记库中提取文字内容的工具，支持将所有 Markdown 文件中的文本提取为纯文本格式。

## 功能特点

- 📝 **提取 Markdown 文件**: 自动查找并处理所有 `.md` 文件
- 🧹 **清理格式**: 自动去除 Markdown 格式标记，保留纯文本内容
- 🔗 **处理 Obsidian 语法**: 正确处理 Obsidian 特有的内部链接 `[[]]` 语法
- 📊 **统计信息**: 提供文件数量、字数、字符数等统计信息
- 💾 **多种输出格式**: 支持 JSON 和 TXT 两种输出格式

## 安装依赖

```bash
pip3 install markdown
```

## 使用方法

### 基本用法

```bash
# 在当前目录运行，提取所有文本
python3 text_extractor.py

# 指定 Obsidian 库路径
python3 text_extractor.py /path/to/your/obsidian/vault

# 只显示摘要信息，不保存文件
python3 text_extractor.py --summary
```

### 指定输出格式

```bash
# 只生成 JSON 格式
python3 text_extractor.py --format json

# 只生成 TXT 格式
python3 text_extractor.py --format txt

# 生成两种格式（默认）
python3 text_extractor.py --format both
```

### 自定义输出文件名

```bash
# 自定义输出文件前缀
python3 text_extractor.py -o my_extracted_content
```

## 输出文件说明

### JSON 格式 (`obsidian_extracted_text.json`)
包含完整的结构化数据：
- 每个文件的原始内容和清理后的文本
- 每个文件的字数和字符数统计
- 整体统计信息

### TXT 格式 (`obsidian_extracted_text.txt`)
包含：
- 提取摘要和统计信息
- 按文件分组的纯文本内容
- 易于阅读的格式

## 示例输出

运行工具后会显示类似以下的摘要信息：

```
=== 提取摘要 ===
处理文件: 46 个
总字数: 2238 字
总字符数: 29236 字符

=== 文件列表 ===
  论文写作.md: 125 字
  idea.md: 126 字
  Java/2-基础语法/1.基本语法/2.数据类型.md: 111 字
  ...
```

## 支持的文件类型

- ✅ Markdown 文件 (`.md`)
- ✅ Obsidian 内部链接语法 `[[链接]]`
- ✅ 图片引用 `![[图片.png]]`
- ✅ 中文和英文混合内容

## 处理的格式

工具会自动清理以下 Markdown 格式：
- 标题符号 (`#`, `##`, `###` 等)
- 粗体和斜体标记 (`**text**`, `*text*`)
- 代码块和行内代码
- 列表标记 (`-`, `*`, `1.` 等)
- 表格分隔符
- YAML front matter
- Obsidian 内部链接 `[[链接]]`
- 图片引用 `![[图片]]`

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request 来改进这个工具！