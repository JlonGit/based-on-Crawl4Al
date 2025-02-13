# Crawl4AI - 文档爬取工具

这是一个用于爬取文档并生成AI知识库的工具。它可以爬取网页和PDF文档，并将内容保存为结构化数据。

## 功能特点

- 支持网页文档爬取
- 支持PDF文档解析
- 自动提取正文内容
- 递归爬取相关页面
- 域名限制，确保只爬取目标网站
- 详细的日志记录
- JSON格式保存结果

## 安装

1. 克隆仓库：
```bash
git clone https://github.com/yourusername/Crawl4AI.git
cd Crawl4AI
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

## 使用方法

1. 基本使用：
```python
from crawler import DocumentCrawler

# 创建爬虫实例
crawler = DocumentCrawler("https://example.com", max_depth=2)

# 开始爬取
documents = crawler.start_crawling()
```

2. 运行示例程序：
```bash
python main.py
```

## 配置说明

- `base_url`: 起始URL
- `max_depth`: 最大爬取深度（默认为3）
- `output_dir`: 输出目录（默认为"output"）

## 输出格式

爬取的文档将以JSON格式保存，格式如下：
```json
{
    "url1": "文档内容1",
    "url2": "文档内容2",
    ...
}
```

## 注意事项

1. 请遵守网站的robots.txt规则
2. 建议设置适当的爬取深度，避免过度爬取
3. 确保有足够的存储空间保存爬取的文档

## 许可证

MIT License 