import re

from langchain_core.tools import tool
from pydantic import BaseModel, Field

# 模拟数据库，实际应用中可以持久化到文件或数据库
# 数据格式: {"1": {"task": "搜索相关论文", "status": "completed"}, ...}
plan_storage: dict[str, dict[str, str]] = {}

class PlanItem(BaseModel):
    plan_id: str = Field(description="任务的唯一标识符，如 '1', '2' 或 'task_1'")
    task: str = Field(description="具体的任务描述内容")
    status: str = Field(description="任务状态，可选值: 'todo', 'in_progress', 'completed', 'failed'")
    
def extract_index(plan_id: str) -> int:
    """辅助函数：从 plan_step_N 格式中提取数字索引"""
    match = re.search(r'plan_step_(\d+)', plan_id)
    
    if match:
        return int(match.group(1))
    else:
        raise ValueError(f"任务 ID 错误: {plan_id}")
    

with open("src/tools/todowrite.txt") as f:
    DESCRIPTION_WRITE = f.read()
    
@tool(description=DESCRIPTION_WRITE)
def init_planning(tasks: list[str]) -> str:
    """
    【规划创建工具】用于创建详细的任务执行步骤和规划。
    
    使用场景：用于在任务开始前，确认评估是否在简单的三个步骤以内难以实现，难以实现则将复杂或者多步骤的目标拆分为有序的计划清单。
    
    注意：
    - 调用此工具会清空已有的计划。
    - 系统会自动生成 ID 格式为 'plan_step_1', 'plan_step_2' 等。
    
    严格约束：
    - 每个具体的步骤之间界限分明，避免互相包含或重复流程。
    
    参数:
    - tasks: 任务描述字符串列表。示例: ["搜索AI最新进展", "分析AI最新进展数据", "编写解析脚本", "检查解析结果"]
    """
    global plan_storage
    plan_storage.clear()
    for i, task_desc in enumerate(tasks, 1):
        plan_id = f"plan_step_{i}"
        plan_storage[plan_id] = {"task": task_desc, "status": "todo"}
    
    return f"计划已初始化，共创建 {len(tasks)} 个步骤。请从 plan_step_1 开始执行。"

@tool
def get_plans(plan_id: str | None = None) -> str:
    """
    【规划查看工具】读取当前的执行计划（Plan/Todo List）。
    
    当你想了解整体进度时，不传 plan_id。
    当你想专注于当前特定任务，避免被其他已完成或无关任务干扰时，请传入特定的 plan_id。
    必须遵循顺序执行，在当前任务状态变为 'completed' 之前，不得处理后续任务。
    
    参数:
    - plan_id: 可选，特定任务的ID。如果不提供，则返回所有任务。
    """
    if not plan_storage:
        return "当前没有计划。请先调用 init_planning 创建计划。"
    
    if plan_id:
        if not plan_id.startswith("plan_step_"):
            return "错误：plan_id 必须以 'plan_step_' 开头，例如 'plan_step_1'。"
        plan = plan_storage.get(plan_id)
        return f"详情 [{plan_id}]: {plan['task']} | 状态: {plan['status']}" if plan else "未找到该步骤。"

    # 逻辑：寻找第一个状态不是 completed 的任务作为“当前任务”
    output = "--- 执行计划清单 ---"
    current_found = False
    for pid, info in plan_storage.items():
        status = info['status']
        prefix = "[ ]"
        suffix = ""
        
        if status == "completed":
            prefix = "[DONE]"
        elif not current_found and status in ["todo", "in_progress"]:
            prefix = "[ACTIVE ->]" # 特别强调
            suffix = " <-- 这是你当前唯一需要关注和执行的任务"
            current_found = True
        
        output += f"\n{prefix} ID: {pid} | 任务: {info['task']} | 状态: {status}{suffix}"
    
    if not current_found:
        output += "\n\n提示：所有任务已完成或没有待办任务。"
    
    return output

@tool
def update_plan(
    plan_id: str, 
    status: str,
) -> str:
    """
    【规划更新工具】仅用于更新现有任务的状态。不能创建新任务。
    
    严格约束：
    - 必须按顺序执行：只有 ID 较小的步骤状态为 'completed'，才能操作下一个步骤。
    - 禁止跨步更新：例如在 plan_step_1 未完成时，禁止更新 plan_step_2。
    - 状态流转建议：todo -> in_progress -> completed。
    
    参数:
    - plan_id: 格式必须为 'plan_step_N' (例如 'plan_step_1')。
    - status: 目标状态 (todo, in_progress, completed, failed)。
    """
    global plan_storage
    if plan_id not in plan_storage:
        return f"错误：任务 {plan_id} 不存在。请使用 get_plans 查看整体 plan 确认"

    sorted_keys = sorted(plan_storage.keys(), key=extract_index)
    current_idx = sorted_keys.index(plan_id)
    
    for i in range(current_idx):
        prev_id = sorted_keys[i]
        if plan_storage[prev_id]["status"] != "completed":
            return f"更新拒绝！前置步骤 {prev_id} 尚未完成。请保持专注，按顺序逐一执行任务。"

    # 更新状态
    plan_storage[plan_id]["status"] = status
    return f"任务 {plan_id} 状态已更新为 {status}。"
