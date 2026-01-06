import base64
from collections.abc import Iterator
from typing import Literal

from e2b.sandbox.filesystem.filesystem import WriteEntry
from e2b_code_interpreter import Sandbox
from langchain.tools import tool

sandbox: Sandbox | None = None


def get_sandbox() -> Sandbox:
    """懒加载 sandbox，避免提前创建"""
    global sandbox
    if sandbox is None:  # 检查是否已关闭
        sandbox = Sandbox.create()  # 可选：Sandbox(timeout=600) 延长存活时间
    return sandbox




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
