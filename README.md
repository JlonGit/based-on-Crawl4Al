# Crawl4AI - AI友好的文档爬取工具

Crawl4AI 是一个专门为 AI 训练数据收集设计的文档爬取工具。它能够智能地爬取网页和 PDF 文档，并将内容转换为结构化的、AI 友好的格式。

## 🌟 主要特性

- **智能内容提取**
  - 自动识别并保留文档结构（标题、段落等）
  - 智能清理无关内容（广告、导航栏等）
  - 保持原文格式和层级关系

- **多格式支持**
  - 支持网页文档（HTML）爬取
  - 支持 PDF 文档解析
  - 支持 Markdown 文档处理

- **高级爬取控制**
  - 递归爬取相关页面
  - 可配置的爬取深度
  - 智能去重
  - 域名限制，确保内容相关性

- **AI 友好输出**
  - 生成结构化的 JSON 格式
  - 生成带元数据的 Markdown 文档
  - 自动生成文档目录
  - 支持文档指纹和追踪

## 🚀 快速开始

### 安装

1. 克隆仓库：
```bash
git clone https://github.com/yourusername/Crawl4AI.git
cd Crawl4AI
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

### 基本使用

1. 命令行方式：
```bash
python main.py https://example.com --depth 2 --output ./output
```

2. 作为模块导入：
```python
from crawler import DocumentCrawler

# 创建爬虫实例
crawler = DocumentCrawler(
    base_url="https://example.com",
    max_depth=2
)

# 开始爬取
documents = crawler.start_crawling()
```

## 📝 配置参数

### 命令行参数

- `url`: 要爬取的起始URL（必需）
- `--depth`: 最大爬取深度（默认：1）
- `--output`: 输出目录（默认：output）

### DocumentCrawler 类参数

- `base_url`: 起始URL
- `max_depth`: 最大爬取深度（默认：3）
- `headers`: 自定义请求头
- `allowed_extensions`: 允许的文件类型（默认：['.html', '.htm', '.pdf', '.txt', '.md', '.rst']）

## 📊 输出格式

### JSON 格式
```json
{
    "url1": {
        "content": "文档结构化内容",
        "metadata": {
            "title": "文档标题",
            "timestamp": "爬取时间",
            "word_count": "字数统计"
        }
    }
}
```

### Markdown 格式
- 包含完整的文档元数据
- 保留原始文档结构
- 自动生成目录
- 支持锚点导航
- 每个文档都有唯一标识符

## ⚙️ 高级功能

### 内容清理
- 自动移除广告、导航栏等无关内容
- 智能处理特殊字符
- 保持段落结构
- 支持自定义内容过滤规则

### 去重机制
- 基于内容哈希的文档去重
- 智能判断相似内容
- 避免重复爬取相同URL

### 错误处理
- 完善的异常处理机制
- 详细的日志记录
- 支持断点续爬
- 超时和重试机制

## 📌 注意事项

1. 爬取限制
   - 请遵守网站的 robots.txt 规则
   - 建议设置适当的爬取间隔
   - 避免过度爬取对服务器造成压力

2. 资源占用
   - 注意设置合理的爬取深度
   - 确保足够的存储空间
   - 监控内存使用情况

3. 内容质量
   - 定期检查爬取内容的质量
   - 验证文档结构的完整性
   - 确保元数据的准确性

## 🔄 更新日志

### v1.0.0
- 初始版本发布
- 支持基本的网页和PDF爬取
- 提供JSON和Markdown输出

## 📄 许可证

本项目采用 MIT 许可证。详见 [LICENSE](LICENSE) 文件。

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建特性分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 📮 联系方式

如有问题或建议，请通过以下方式联系：

- 提交 Issue
- 发送邮件至：[your-email@example.com] 