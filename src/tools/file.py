import os
from pathlib import Path

from langchain.tools import tool


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