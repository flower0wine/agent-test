import os
import platform
import queue
import re
import subprocess
import threading
import time

from langchain_core.tools import tool

UNIX_DANGER_COMMANDS = {
    "rm", "mkfs", "dd", "chmod", "chown", "shutdown", "reboot", "del", "format", "mkfs", 
    "rd", "deltree"
}

POWERSHELL_DANGER_COMMANDS = {
    "out-file",
    "format-volume",
    "clear-disk",
    "initialize-disk",
    "stop-computer",
    "restart-computer",
    "shutdown",
}

POWERSHELL_DANGER_FLAGS = {
    "-recurse",
    "-force",
    "-confirm:$false",
}


DANGER_PATH_PATTERNS = {
    r"^c:\\windows",
    r"^\\\\",          # 网络路径
    r"\*$",            # 通配符
}

READ_ONLY_COMMANDS = {"dir", "ls", "get-childitem"}


def extract_powershell_inner_command(command: str) -> str | None:
    """
    从 powershell -Command "..." 中提取内部命令
    返回 None 表示不是 powershell -Command
    """
    # 匹配 -Command "...", -Command '...'
    match = re.search(
        r"-command\s+(['\"])(.*?)\1",
        command,
        re.IGNORECASE | re.DOTALL,
    )
    if match:
        return match.group(2).strip()
    return None


MAX_RECURSION_DEPTH = 3

def is_dangerous_command(command: str, depth: int = 0) -> bool:
    cmd = command.lower()

    if depth > MAX_RECURSION_DEPTH:
        # 递归过深，直接视为危险
        return True

    if platform.system() == "Windows":
        # 0. 直接封杀编码执行
        if re.search(r"\s-(enc|encodedcommand)\b", cmd):
            return True

        inner_cmd = extract_powershell_inner_command(command)
        if inner_cmd:
            # 对内部 PowerShell 命令再次进行危险检测
            if is_dangerous_command(inner_cmd):
                return True

        # 1. 危险 cmdlet
        for kw in POWERSHELL_DANGER_COMMANDS:
            if kw in cmd:
                return True

        # 2. 危险参数
        for flag in POWERSHELL_DANGER_FLAGS:
            if flag in cmd:
                return True

        if any(cmd.startswith(c) for c in READ_ONLY_COMMANDS):
            # 对只读命令放行通配符
            pass
        else:
            for pattern in DANGER_PATH_PATTERNS:
                if re.search(pattern, cmd):
                    return True

    else:
        # Unix-like
        for kw in UNIX_DANGER_COMMANDS:
            if cmd.startswith(kw + " ") or cmd == kw:
                return True

    return False


CURRENT_OS = platform.system()
SHELL_TYPE = "PowerShell/CMD" if CURRENT_OS == "Windows" else "Bash/Zsh"
DANGER_COMMANDS = UNIX_DANGER_COMMANDS if CURRENT_OS != "Windows" else POWERSHELL_DANGER_COMMANDS

# 全局存储，用于跨工具共享进程状态
class TerminalSessionManager:
    def __init__(self):
        self.sessions: dict[str, subprocess.Popen] = {}
        self.output_queues: dict[str, queue.Queue] = {}

    def get_session(self, task_id: str):
        return self.sessions.get(task_id), self.output_queues.get(task_id)

manager = TerminalSessionManager()

def _read_to_queue(pipe, q):
    try:
        for line in iter(pipe.readline, ''):
            if line:
                q.put(line)
        pipe.close()
    except Exception:
        pass


@tool(description=f"""
    在当前系统 ({CURRENT_OS}) 使用 {SHELL_TYPE} 异步启动一个终端命令。
    
    安全限制：
    - 严禁执行破坏性指令：{', '.join(DANGER_COMMANDS)}。
    
    参数含义:
    - command: 要执行的完整命令。如果是 Windows，请确保符合 PowerShell 语法。
    - task_id: 唯一任务标识符。
    - wait_seconds: 在读取输出前 **等待的秒数**，默认 0.2s。
      主要用于给被监控的进程一点时间刷新输出队列；
      设为 0 可关闭等待。
    """)
def start_task(command: str, task_id: str, wait_time: float = 0.2) -> str:
    
    if is_dangerous_command(command):
        return f"安全拒绝：指令 '{command}' 包含潜在危险操作，已被拦截。"

    if task_id in manager.sessions:
        return f"错误：ID 为 {task_id} 的任务已存在。"

    # 执行逻辑 (复用之前的 Popen 实现)
    process = subprocess.Popen(
        command,
        shell=True,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if os.name == 'nt' else 0
    )
    
    q = queue.Queue()
    t = threading.Thread(target=_read_to_queue, args=(process.stdout, q), daemon=True)
    t.start()
    
    manager.sessions[task_id] = process
    manager.output_queues[task_id] = q
    
    if wait_time > 0:
        time.sleep(wait_time)
    return f"任务 '{task_id}' 已在 {CURRENT_OS} 上启动。请监控输出以处理可能的交互提示。"


@tool
def respond_task(task_id: str, response: str, wait_time: float = 0.1) -> str:
    """
    向特定任务的标准输入(stdin)发送文本。
    常用于处理安装确认 (y/n)、输入参数等交互场景。
    
    参数含义:
    - task_id: 目标任务 ID。
    - response: 响应内容。如果是确认操作，通常为 'y'。
    - wait_seconds: 在读取输出前 **等待的秒数**，默认 0.2s。
      主要用于给被监控的进程一点时间刷新输出队列；
      设为 0 可关闭等待。
    """
    proc, _ = manager.get_session(task_id)
    if not proc or proc.poll() is not None:
        return f"失败：任务 {task_id} 不存在或已退出。"

    try:
        # 针对不同系统的换行符处理（通常 \n 在管道中是通用的）
        input_data = response if response.endswith('\n') else response + '\n'
        
        if proc.stdin:
            proc.stdin.write(input_data)
            proc.stdin.flush()
        
        if wait_time > 0:
            time.sleep(wait_time)

        return f"已向 {task_id} 发送输入。请再次查看 peek_task 确认结果。"
    except Exception as e:
        return f"发送失败: {str(e)}"

@tool
def peek_task(task_id: str, limit: int = 50,
    offset: int = 0, wait_seconds: float = 0.2) -> str:
    """
    查看指定任务当前的终端输出流（分页方式）。

    功能说明:
    - 允许按 “偏移 + 限制” 方式分页获取输出，
      类似 SQL 的 OFFSET / LIMIT。
    - 比如 offset=15, limit=10 会返回第 16~25 行。
    - 等待 wait_seconds 秒再读取输出队列，避免过早读取导致输出丢失。
    
    参数含义:
    - task_id: 启动任务时定义的唯一 ID。
    - limit: 本次返回最多输出行数，默认为 50。
    - offset: 跳过的行数，用于分页，默认为 0。
    - wait_seconds: 在读取输出前 **等待的秒数**，默认 0.2s。
      主要用于给被监控的进程一点时间刷新输出队列；
      设为 0 可关闭等待。
    """
    proc, q = manager.get_session(task_id)
    if not proc or not q:
        return f"未找到任务 {task_id}。"

    # 等待一段时间让输出队列累积
    if wait_seconds > 0:
        import time
        time.sleep(wait_seconds)

    # 先取出所有当前队列剩余内容
    all_lines = []
    try:
        while not q.empty():
            all_lines.append(q.get_nowait())
    except queue.Empty:
        pass

    # 分页处理
    start_index = max(0, offset)
    end_index = start_index + max(0, limit)

    # 获取分页结果
    page_lines = all_lines[start_index:end_index]

    # 统计信息
    total_lines = len(all_lines)
    remaining_lines = max(0, total_lines - end_index)

    # 如果没有内容
    if not page_lines:
        page_text = "[无更多数据或offset越界]"
    else:
        page_text = "".join(page_lines)

    status = (
        "运行中"
        if proc.poll() is None
        else f"已结束 (退出码: {proc.returncode})"
    )

    return (
        f"任务: {task_id} | 状态: {status}\n"
        f"--- 输出 (offset={offset}, limit={limit}) ---\n"
        f"总行数: {total_lines} | 未读取剩余行数: {remaining_lines}\n"
        f"{page_text}"
    )


if __name__ == "__main__":
    print(is_dangerous_command("C:\\Windows\\System32\\cmd.exe"))
