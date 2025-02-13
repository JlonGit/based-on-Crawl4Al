from crawler import DocumentCrawler
import json
import os
from datetime import datetime
import argparse
import hashlib
from urllib.parse import urlparse
import re

def save_documents(documents, output_dir="output"):
    """保存爬取的文档"""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # 保存JSON格式
    json_file = os.path.join(output_dir, f"documents_{timestamp}.json")
    sorted_documents = dict(sorted(documents.items(), key=lambda x: len(x[0])))
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(sorted_documents, f, ensure_ascii=False, indent=2)
    
    # 保存AI友好的Markdown格式
    md_file = os.path.join(output_dir, f"documents_{timestamp}.md")
    with open(md_file, 'w', encoding='utf-8') as f:
        # 写入文档信息
        f.write("# 知识库文档集\n\n")
        f.write(f"## 元数据\n\n")
        f.write(f"- **生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"- **文档总数**: {len(sorted_documents)}\n")
        f.write(f"- **知识库ID**: {hashlib.md5(timestamp.encode()).hexdigest()}\n\n")
        
        # 写入目录，使用文档的第一个标题作为标题
        f.write("## 文档目录\n\n")
        seen_titles = set()
        
        # 首先提取所有文档的标题
        doc_titles = {}
        for url, content in sorted_documents.items():
            elements = re.findall(r'<(\w+)>(.*?)</\w+>', content)
            first_title = None
            for tag, text in elements:
                if tag == 'h1' and text.strip():
                    first_title = text.split('-')[0].strip()  # 移除" - SiliconFlow"部分
                    break
            if not first_title:
                # 如果没有找到标题，使用URL的最后一部分
                parsed_url = urlparse(url)
                path_parts = parsed_url.path.split('/')
                first_title = path_parts[-1] if path_parts[-1] else parsed_url.netloc
            doc_titles[url] = first_title
        
        # 写入目录
        for i, url in enumerate(sorted_documents.keys(), 1):
            # 生成锚点链接
            anchor = f"doc-{i}"
            title = doc_titles[url]
            
            # 如果标题已存在，添加计数
            base_title = title
            counter = 1
            while title in seen_titles:
                counter += 1
                title = f"{base_title} ({counter})"
            seen_titles.add(title)
            
            f.write(f"{i}. [{title}](#{anchor})\n")
        f.write("\n---\n\n")
        
        # 写入文档内容
        for i, (url, content) in enumerate(sorted_documents.items(), 1):
            # 计算文档指纹
            doc_hash = hashlib.md5(content.encode()).hexdigest()
            
            # 文档标题和元数据
            f.write(f"## 文档 {i} <span id='doc-{i}'></span>\n\n")
            f.write("### 文档元数据\n\n")
            f.write(f"- **文档ID**: {doc_hash}\n")
            f.write(f"- **来源URL**: {url}\n")
            f.write(f"- **字数统计**: {len(content)}\n")
            f.write(f"- **抓取时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            # 解析和格式化结构化内容
            f.write("### 文档内容\n\n")
            
            # 解析XML样式的标签
            elements = re.findall(r'<(\w+)>(.*?)</\w+>', content)
            
            for tag, text in elements:
                if not text.strip():
                    continue
                    
                # 根据标签类型设置合适的Markdown格式
                if tag == 'h1':
                    f.write(f"# {text}\n\n")
                elif tag == 'h2':
                    f.write(f"## {text}\n\n")
                elif tag == 'h3':
                    f.write(f"### {text}\n\n")
                elif tag == 'h4':
                    f.write(f"#### {text}\n\n")
                elif tag == 'h5':
                    f.write(f"##### {text}\n\n")
                elif tag == 'h6':
                    f.write(f"###### {text}\n\n")
                elif tag == 'p':
                    # 分段落显示，每段都用引用格式
                    lines = text.split('\n')
                    for line in lines:
                        if line.strip():
                            f.write(f"> {line}\n")
                    f.write("\n")
            
            f.write("---\n\n")
    
    print(f"文档已保存到:")
    print(f"- JSON格式: {json_file}")
    print(f"- Markdown格式: {md_file}")
    print(f"共爬取了 {len(documents)} 个文档")

def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description='网页文档爬取工具')
    parser.add_argument('url', help='要爬取的起始URL')
    parser.add_argument('--depth', type=int, default=1, help='最大爬取深度（默认：1）')
    parser.add_argument('--output', default='output', help='输出目录（默认：output）')
    return parser.parse_args()

def main():
    # 解析命令行参数
    args = parse_args()
    
    # 创建爬虫实例
    crawler = DocumentCrawler(args.url, max_depth=args.depth)
    
    try:
        # 开始爬取
        print(f"开始爬取 {args.url}，最大深度：{args.depth}")
        documents = crawler.start_crawling()
        
        # 保存结果
        save_documents(documents, args.output)
        
    except KeyboardInterrupt:
        print("\n爬取被用户中断")
        # 保存已爬取的内容
        if crawler.documents:
            print("正在保存已爬取的内容...")
            save_documents(crawler.documents, args.output)
    except Exception as e:
        print(f"爬取过程中出现错误: {str(e)}")

if __name__ == "__main__":
    main() 