from langchain.tools import ToolRuntime, tool


@tool
def enter_edit_mode(runtime: ToolRuntime) -> str:
    """
    切换到【编辑模式】。
    当你需要修改文档、重写代码、润色文字或进行任何内容创作时，请调用此工具。
    """
    # 实际逻辑由后端的模式管理器处理
    return "已进入编辑模式。"

@tool
def enter_search_mode() -> str:
    """
    切换到【搜索模式】。
    当你需要获取实时信息、查找外部参考资料或进行事实核查时，请调用此工具。
    """
    return "已进入搜索模式。现在的工具箱已更新为：[谷歌搜索, 维基百科查询, 论文检索]"

@tool
def enter_planning_mode() -> str:
    """
    切换到【计划模式】。
    当面对复杂任务需要拆解步骤、制定时间表或分配资源时，请调用此工具。
    """
    return "已进入计划模式。现在的工具箱已更新为：[任务拆解, 时间表生成, 风险评估]"