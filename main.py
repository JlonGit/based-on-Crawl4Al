from crawler import DocumentCrawler
import json
import os
from datetime import datetime
import argparse
import hashlib

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
        
        # 写入目录
        f.write("## 文档目录\n\n")
        for i, url in enumerate(sorted_documents.keys(), 1):
            # 生成锚点链接
            anchor = f"doc-{i}"
            title = url.split('/')[-1] or url
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
            
            # 文档内容，使用引用格式并添加段落编号
            f.write("### 文档内容\n\n")
            paragraphs = content.split('\n\n')
            for p_idx, para in enumerate(paragraphs, 1):
                if para.strip():
                    # 添加段落编号和引用符号
                    f.write(f"#### 段落 {p_idx}\n\n")
                    formatted_para = '\n'.join([f'> {line}' if line.strip() else '>' 
                                              for line in para.split('\n')])
                    f.write(f"{formatted_para}\n\n")
            
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