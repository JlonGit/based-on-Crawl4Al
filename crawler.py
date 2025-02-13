import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from typing import List, Set, Dict, Optional
import PyPDF2
import io
from tqdm import tqdm
import logging
import re
import hashlib

class DocumentCrawler:
    def __init__(self, base_url: str, max_depth: int = 3):
        self.base_url = base_url
        self.max_depth = max_depth
        self.visited_urls: Set[str] = set()
        self.documents: Dict[str, str] = {}
        self.content_hashes: Set[str] = set()  # 用于内容去重
        
        # 设置日志
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
        # 允许的文件类型
        self.allowed_extensions = {'.html', '.htm', '.pdf', '.txt', '.md', '.rst'}
        
        # 设置请求头
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # 需要移除的HTML标签
        self.remove_tags = [
            'script', 'style', 'nav', 'footer', 'header', 'aside',
            'noscript', 'iframe', 'form', 'button', 'input'
        ]
        
        # 需要移除的类名或ID（可以根据需要添加）
        self.remove_classes = {
            'advertisement', 'sidebar', 'comment', 'menu', 'search',
            'social', 'share', 'related', 'widget'
        }

    def is_valid_url(self, url: str) -> bool:
        """检查URL是否有效且属于同一域名"""
        try:
            parsed_url = urlparse(url)
            # 检查文件扩展名
            path = parsed_url.path.lower()
            ext = '.' + path.split('.')[-1] if '.' in path else ''
            if ext and ext not in self.allowed_extensions:
                return False
                
            base_domain = urlparse(self.base_url).netloc
            url_domain = parsed_url.netloc
            return base_domain in url_domain
        except:
            return False

    def extract_text_from_pdf(self, pdf_content: bytes) -> str:
        """从PDF内容中提取文本"""
        try:
            pdf_file = io.BytesIO(pdf_content)
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text
        except Exception as e:
            self.logger.error(f"PDF解析错误: {str(e)}")
            return ""

    def clean_text(self, text: str) -> str:
        """清理文本内容"""
        # 移除多余的空白字符
        text = re.sub(r'\s+', ' ', text)
        # 移除空行
        text = re.sub(r'\n\s*\n', '\n', text)
        # 移除特殊字符
        text = re.sub(r'[^\u4e00-\u9fa5a-zA-Z0-9.,!?，。！？、:：()（）\s]', '', text)
        # 移除重复的标点符号
        text = re.sub(r'([.,!?，。！？、])\1+', r'\1', text)
        return text.strip()

    def get_content_hash(self, content: str) -> str:
        """计算内容的哈希值"""
        return hashlib.md5(content.encode('utf-8')).hexdigest()

    def is_duplicate_content(self, content: str) -> bool:
        """检查内容是否重复"""
        content_hash = self.get_content_hash(content)
        if content_hash in self.content_hashes:
            return True
        self.content_hashes.add(content_hash)
        return False

    def clean_html(self, soup: BeautifulSoup) -> None:
        """清理HTML内容"""
        # 移除不需要的标签
        for tag in self.remove_tags:
            for element in soup.find_all(tag):
                element.decompose()
        
        # 移除不需要的类和ID
        for element in soup.find_all(class_=self.remove_classes):
            element.decompose()
        
        # 移除空标签
        for element in soup.find_all():
            if len(element.get_text(strip=True)) == 0:
                element.decompose()

    def crawl_url(self, url: str, depth: int = 0) -> None:
        """爬取指定URL的内容"""
        if depth > self.max_depth or url in self.visited_urls:
            return

        self.visited_urls.add(url)
        self.logger.info(f"正在爬取: {url}")

        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            if response.status_code != 200:
                self.logger.warning(f"页面访问失败 {url}: {response.status_code}")
                return

            # 处理PDF文件
            if url.lower().endswith('.pdf'):
                text = self.extract_text_from_pdf(response.content)
                if text and not self.is_duplicate_content(text):
                    self.documents[url] = self.clean_text(text)
                return

            # 处理HTML页面
            soup = BeautifulSoup(response.text, 'html.parser')
            self.clean_html(soup)
            
            # 提取正文内容
            content_elements = soup.find_all(['article', 'main', 'div', 'section'])
            if not content_elements:
                content_elements = soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
            
            content = ' '.join([elem.get_text() for elem in content_elements])
            content = self.clean_text(content)
            
            # 检查内容是否重复
            if content and not self.is_duplicate_content(content):
                self.documents[url] = content

            # 提取链接并继续爬取
            if depth < self.max_depth:
                links = soup.find_all('a', href=True)
                for link in links:
                    next_url = urljoin(url, link['href'])
                    if self.is_valid_url(next_url) and next_url not in self.visited_urls:
                        self.crawl_url(next_url, depth + 1)

        except requests.Timeout:
            self.logger.error(f"爬取超时 {url}")
        except requests.RequestException as e:
            self.logger.error(f"请求错误 {url}: {str(e)}")
        except Exception as e:
            self.logger.error(f"爬取错误 {url}: {str(e)}")

    def start_crawling(self) -> Dict[str, str]:
        """开始爬取过程"""
        self.logger.info(f"开始爬取 {self.base_url}")
        self.crawl_url(self.base_url)
        self.logger.info(f"爬取完成，共获取 {len(self.documents)} 个文档")
        return self.documents 