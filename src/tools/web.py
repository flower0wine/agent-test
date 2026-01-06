import os

from dotenv import load_dotenv
from langchain.tools import tool
from langchain_community.document_loaders import BrowserlessLoader
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain_core.documents import Document

from .e2b import get_sandbox

load_dotenv()

search = GoogleSerperAPIWrapper()

@tool
def google_search(query: str) -> dict:
    """
    使用 Google 搜索实时事件、事实或网络信息。
    
    参数规范与策略：
    1. 关键词质量：输入应为高度概括、专业且非句式的关键词组合。避免提问式输入，优先使用行业术语。
    2. 语言策略：
       - 默认原则：优先使用【英文】进行搜索，以获取全球范围内更广泛、更具权威性或技术性的信息。
       - 本地化原则：若查询涉及特定国家的文化、政策、本地生活或特定地理位置信息，请使用【该国官方语言】。
    3. 结果处理：输出为包含标题、摘要及来源链接的相关网页列表。
    """
    return search.results(query)




@tool
def browserless_web_loader(
    urls: list[str],
    file_paths: list[str],
    text_content: bool = True,
) -> list[dict]:
    """
    使用 Browserless 服务加载一个或多个网页的内容。
    适合处理需要 JavaScript 渲染的动态网站（例如 SPA、需要登录的页面等）。获取到的网页内容将会保存到 E2B 沙箱中。你可以使用读取文件工具读取

    Args:
        urls: 要加载的网页 URL 列表（支持多个）。
        file_paths: 每个网页对应的文件路径列表（支持多个），必须填写。类似于["/path/to/file"]
        text_content: 如果为 True，返回清理后的纯文本（默认推荐）；如果为 False，返回原始 HTML。

    Returns:
        写入文件后的路径列表
    """
    api_token = os.getenv("BROWSERLESS_API_TOKEN")
    if not api_token:
        raise ValueError("错误：未找到 BROWSERLESS_API_TOKEN 环境变量。请在 .env 文件中设置。")

    try:
        loader = BrowserlessLoader(
            api_token=api_token,
            urls=urls,
            text_content=text_content
        )
        documents: list[Document] = loader.load()

        results = []
        for doc, file_path, url in zip(documents, file_paths, urls):
            source = doc.metadata.get("source", "未知来源")
            content = doc.page_content

            results.append({
                "path": file_path,
                "content": content,
                "source": source,
                "url": url
            })

        try:
            sbx = get_sandbox()
            sbx.set_timeout(600)

            for item in results:
                sbx.files.write_files([
                    {
                        "path": item["path"], 
                        "data": item["content"]
                    }
                ])
        except Exception as e:
            raise Exception(f"写入文件时出错: {e}")
        return results

    except Exception as e:
        raise Exception(f"加载网页时出错: {str(e)}")
