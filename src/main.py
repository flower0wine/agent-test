import base64
import os
from collections.abc import Iterator
from pathlib import Path
from typing import Literal

from dotenv import load_dotenv
from e2b.sandbox.filesystem.filesystem import WriteEntry
from e2b_code_interpreter import Sandbox
from langchain.agents import create_agent
from langchain_community.document_loaders import BrowserlessLoader
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain_core.documents import Document
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

# from src.commands import peek_task, respond_task, start_task
from src.plan import get_plans, init_planning, update_plan

load_dotenv()

search = GoogleSerperAPIWrapper()

api_key = os.getenv("VOLCENGINE_API_KEY")

model = ChatOpenAI(
    base_url="https://ark.cn-beijing.volces.com/api/v3",
    # model="deepseek-v3-2-251201",
    model="deepseek-v3-1-terminus",
    api_key=api_key,
    temperature=0.1,
    timeout=30,
    stream_usage=True
)


sandbox: Sandbox | None = None

def get_sandbox() -> Sandbox:
    """懒加载 sandbox，避免提前创建"""
    global sandbox
    if sandbox is None:  # 检查是否已关闭
        sandbox = Sandbox.create()  # 可选：Sandbox(timeout=600) 延长存活时间
    return sandbox

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
def e2b_read_file(path: str, format: Literal["text", "bytes", "stream"] = "text", user: str | None = "user") -> str | bytearray | Iterator[bytes]:
    """
    Read a file from E2B sandbox.

    Args:
        path: 文件在 E2B Sandox 中的路径
        format: 读取格式 ("text", "bytes", "stream")
        user: 可选用户命名

    Returns:
        文件内容（text 默认返回 str）
    """
    sbx = get_sandbox()
    sbx.set_timeout(600)

    # 调用 E2B 文件读取
    try:
        content = sbx.files.read(path=path, format=format, user=user)
    except Exception as e:
        return f"读取文件时出错: {e}"
    return content


@tool
def e2b_write_file(path: str, data: str, user: str | None = "user") -> str:
    """
    Write a single file to E2B sandbox.

    Args:
        path: 写入的文件路径
        data: 写入内容
        user: 可选用户命名

    Returns:
        结果信息
    """
    sbx = get_sandbox()
    sbx.set_timeout(600)

    try:
        sbx.files.write(path=path, data=data, user=user)
    except Exception as e:
        return f"写入文件时出错: {e}"
    return f"OK: wrote file at {path}"


@tool
def e2b_write_files(files: list[WriteEntry], user: str | None = "user") -> str:
    """
    Write multiple files at once to E2B sandbox.

    Args:
        files: List of dict with keys 'path' and 'data'
        user: 可选用户命名

    Returns:
        结果信息
    """
    sbx = get_sandbox()
    sbx.set_timeout(600)

    # 批量写
    try:
        sbx.files.write_files(files, user=user)
    except Exception as e:
        return f"写入文件时出错: {e}"
    return f"OK: wrote {len(files)} files"


@tool
def python_code_executor(code: str) -> str:
    """
    在安全的云端沙箱中执行 Python 代码，并返回执行结果。
    
    Args:
        code: 要执行的完整 Python 代码字符串。
    
    Returns:
        执行结果（stdout + stderr）以及可能的错误信息。
    """
    sbx = get_sandbox()
    sbx.set_timeout(600)
    
    try:
        # 执行代码
        execution = sbx.run_code(code, timeout=30)
        
        # 1. 优先处理运行时的错误
        if execution.error:
            logs = "\n".join(execution.logs.stdout + execution.logs.stderr)
            return f"代码执行出错:\n{execution.error.name}: {execution.error.value}\n{execution.error.traceback}\n\n日志:\n{logs}"

        # 2. 安全检查是否有结果（如图表）
        if execution.results:
            first_result = execution.results[0]
            if first_result.png:
                with open('chart.png', 'wb') as f:
                    f.write(base64.b64decode(first_result.png))
                print('✅ 图表已保存为 chart.png')
        else:
            print('ℹ️ 未检测到生成的图表结果。')

        # 3. 合并并返回日志
        logs = "\n".join(execution.logs.stdout + execution.logs.stderr)
        return f"代码执行成功！\n输出:\n{logs}" if logs.strip() else "代码执行成功，无输出。"
    
    except Exception as e:
        # 这里的 e 就会捕获到之前的 list index out of range
        return f"处理结果时发生异常: {e}"



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

@tool
def read_file(file_path: str, start_line: int = 1, end_line: int | None = None) -> str:
    """
    读取指定文件的内容，支持分页读取。如果传入路径是目录，则返回该目录下的内容（不递归）。
    
    参数说明:
    - file_path (str): 目标文件的绝对或相对路径。
    - start_line (int): 起始行号，从 1 开始计数。默认为 1。
    - end_line (int, 可选): 结束行号。如果不指定，且未传 start_line，默认读取前 200 行；
                            若指定了 start_line 但未传 end_line，则默认读取从 start_line 开始的后 200 行。
                            
    行为说明:
    - 文件：按行分页读取，默认 200 行
    - 目录：返回当前目录下的文件 / 子目录列表（不递归）
    
    注意: 
    - 工具会自动处理越界：如果行号超出实际范围，将返回实际存在的有效行。
    - 输出会包含行号，格式为 "行号: 内容"。
    """
    try:
        if not os.path.exists(file_path):
            return f"错误：文件 {file_path} 不存在。"
        
        if os.path.isdir(file_path):
            entries = sorted(os.listdir(file_path))
            if not entries:
                return f"目录为空：{file_path}"

            output = [f"--- 目录内容: {file_path} (不递归) ---"]
            for name in entries:
                full_path = os.path.join(file_path, name)
                if os.path.isdir(full_path):
                    output.append(f"[DIR ] {name}")
                else:
                    output.append(f"[FILE] {name}")

            output.append(f"--- 共 {len(entries)} 项 ---")
            return "\n".join(output)

        with open(file_path, encoding='utf-8') as f:
            all_lines = f.readlines()

        total_lines = len(all_lines)
        if total_lines == 0:
            return "文件内容为空。"

        # 默认逻辑处理：如果未指定结束行，默认读取 200 行
        actual_start = max(1, start_line)
        if end_line is None:
            actual_end = actual_start + 199
        else:
            actual_end = end_line

        # 鲁棒性处理：确保索引不越界
        # 将 1-based 转换为 0-based 索引
        idx_start = min(actual_start - 1, total_lines - 1)
        idx_end = min(actual_end, total_lines)

        # 如果 start 大于实际总行数
        if idx_start >= total_lines:
            return f"提示：起始行号 {start_line} 超过了文件总行数 {total_lines}。"

        selected_lines = all_lines[idx_start:idx_end]
        
        # 格式化输出，带上原始行号
        output = []
        for i, line in enumerate(selected_lines):
            current_line_num = idx_start + i + 1
            output.append(f"{current_line_num}: {line.rstrip()}")

        header = f"--- 读取文件: {file_path} (第 {actual_start} 至 {idx_end} 行，总计 {total_lines} 行) ---\n"
        return header + "\n".join(output)

    except Exception as e:
        return f"读取文件时发生未知错误: {str(e)}"

@tool
def write_file(file_path: str, content: str) -> str:
    """
    创建新文件或覆盖已有文件。会自动创建路径中不存在的目录。

    使用场景：
    - 当需要创建新文件，或者想要直接覆盖已有文件时，或者修改那些内容不是很长的文件。例如行数小于 200 行，并且修改的内容很多，或者是整个文件需要重写，可以使用这个工具。
    
    参数:
    - file_path: 文件路径（例如 'data/logs/2024/test.txt'）。
    - content: 要写入的完整文本内容。
    """
    try:
        # 将字符串转换为 Path 对象
        path = Path(file_path)
        
        # 核心优化：创建父目录
        # parents=True 表示递归创建所有不存在的父目录
        # exist_ok=True 表示如果目录已存在，不抛出异常
        path.parent.mkdir(parents=True, exist_ok=True)
        
        # 写入文件
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
            
        return f"成功：目录已补齐，内容已写入 {file_path}。"
    except Exception as e:
        return f"写入失败: {str(e)}"

@tool
def edit_file_by_line(file_path: str, start_line: int, end_line: int, new_text: str) -> str:
    """
    按指定行号范围编辑文件内容（替换区间内行，并在必要时挤开后续内容）。

    使用场景：当文件内容过长时，例如行数超过了 200 行，并且需要修改指定的部分内容或较小内容变动时，可以使用这个工具。

    功能说明：
    - 将文件中从 start_line 到 end_line （包含两端）这一段替换为 new_text。
    - 当 new_text 的行数 **大于** (end_line - start_line + 1) 时，
      会 **挤开原本位于 end_line 之后的内容**，而不是覆盖它。
    - 当 new_text 的行数 **小于或等于** (end_line - start_line + 1) 时，
      会正好替换该区间，并保持之后内容不变。
    - 如果文件是空的、start_line 在文件末尾之外，则 new_text 会追加到文件末尾。
    - 文本插入时，自动确保每行以换行符结束。

    参数：
        file_path (str): 目标文件路径。
        start_line (int): 起始行号（从 1 开始）。
        end_line (int): 结束行号（从 1 开始，>= start_line）。
        new_text (str): 要插入的新内容，可以包含多行，以换行符分隔。

    行号处理规则：
        - start_line < 1 会被视为 1。
        - end_line < start_line 会返回错误信息。
        - start_line > 文件总行数时，会将 new_text 追加到文件末尾。
        - new_text 中的每一行都保证以 '\\n' 结尾（自动添加缺失的换行符）。

    返回：
        str: 操作结果信息（成功或失败原因）。

    示例行为：
        原始文件：
            1 a
            2 b
            3 c
            4 d

        edit_file_by_line("f.txt", 2, 3, "x\ny\nz")
        => 文件结果：
            1 a
            2 x
            3 y
            4 z
            5 d
    """
    try:
        if not os.path.exists(file_path):
            return f"错误：文件 {file_path} 不存在。"

        with open(file_path, encoding="utf-8") as f:
            lines = f.readlines()

        total_lines = len(lines)

        # 限制行号在合理区间
        start = max(1, start_line)
        end = max(1, end_line)
        if start > end:
            return f"错误：起始行 {start_line} 不能大于结束行 {end_line}。"

        # 处理越界
        start = min(start, total_lines + 1)
        end = min(end, total_lines)

        # new_text 处理成单行列表
        new_lines = new_text.splitlines(keepends=True)
        if not new_lines:
            new_lines = []

        # 实际替换区间长度
        old_segment_len = end - start + 1 if total_lines > 0 else 0

        # 先删除旧行片段
        # 如果 start 在文件末尾之后，则不删除
        if start <= total_lines:
            del lines[start-1:start-1+old_segment_len]

        # 再插入 new_lines
        insert_pos = start - 1
        for i, ln in enumerate(new_lines):
            # 确保每行以换行符结束
            lines.insert(insert_pos + i, ln if ln.endswith("\n") else ln + "\n")

        with open(file_path, "w", encoding="utf-8") as f:
            f.writelines(lines)

        return f"成功：文件 {file_path} 的第 {start_line} 到 {end_line} 行已更新。"

    except Exception as e:
        return f"编辑失败: {str(e)}"

# agent = create_agent(
#     model=model,
#     tools=[read_file, write_file, edit_file_by_line, start_task, respond_task, peek_task, google_search, browserless_web_loader],
#     system_prompt="你是个专注的高级软件工程师，架构师，擅长分析用户的简单需求，将其实现，专注于用户需求本身，不要随意生成用户可能不需要的内容，这样的内容你应该询问用户。不用编写用户手册或使用文档",
# )

# agent = create_agent(
#     model=model,
#     tools=[read_file, write_file, edit_file_by_line, start_task, respond_task, peek_task, google_search, browserless_web_loader],
#     system_prompt="""
#     你是个专注的高级软件工程师，架构师，擅长使用现代化的技术来搭建项目，为了减少重复造轮子，你会收集项目最佳实践。
#     对于自己已有的知识，你始终保持着质疑，你会使用搜索工具去探索现代化的项目最佳实践。
#     你不会手动安装依赖，而是使用推荐的包管理器来安装依赖确保依赖正确。
#     项目初始化应该使用最佳实践推荐的方式来进行，尽可能避免手动初始化项目。
#     """,
# )

agent = create_agent(
    model=model,
    tools=[get_plans, init_planning, update_plan],
    system_prompt="""
    你是一个专注的架构师，软件工程师，熟知系统架构搭建整体流程，对任务的规划有着清晰的认知。
    """,
)

# Run the agent
# response = agent.invoke(
#     {"messages": [{"role": "user", "content": "请你说明斐波那契数列第十一个数字是什么，并展示给我计算过程"}]}
# )

# print(response)
