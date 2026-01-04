import json
import os
import subprocess


def ripgrep_search_with_paging(
    file_path: str,
    query: str,
    offset: int = 0,
    limit: int | None = 50
) -> str:
    """
    使用 ripgrep 搜索并返回分页信息 + 匹配列表。

    Args:
        file_path:  要搜索的文件或目录路径
        query:      搜索字符串或正则表达式
        offset:     跳过前 offset 条
        limit:      最多返回 limit 条

    Returns:
        JSON 字符串，包含:
          - offset
          - limit
          - total_matches
          - returned_count
          - has_more (bool)
          - results (list of "path:line:content")
    """

    # 检查路径
    if not os.path.exists(file_path):
        return json.dumps({
            "error": f"路径不存在: {file_path}"
        })

    # 调用 ripgrep 输出 JSON
    cmd = ["rg", "--json", query, file_path]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError as e:
        return json.dumps({
            "error": "rg 执行失败",
            "details": e.stderr.strip()
        })

    # 解析 JSON 输出
    all_matches = []
    for line in proc.stdout.splitlines():
        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            continue
        if record.get("type") != "match":
            continue

        d = record["data"]
        p = d["path"]["text"]
        ln = d["line_number"]
        text = d["lines"]["text"].rstrip("\n")
        all_matches.append((p, ln, text))

    # 按路径 + 行号排序
    all_matches.sort(key=lambda x: (x[0], x[1]))

    # 计算分页
    total = len(all_matches)
    paged = all_matches[offset : offset + limit] if limit is not None else all_matches[offset:]
    returned = len(paged)
    has_more = (offset + returned) < total

    # 结果结构
    response = {
        "offset": offset,
        "limit": limit,
        "total_matches": total,
        "returned_count": returned,
        "has_more": has_more,
        "results": [f"{p}:{ln}:{txt}" for p, ln, txt in paged]
    }

    return json.dumps(response, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    print(ripgrep_search_with_paging("C:/me", "flowerwine"))