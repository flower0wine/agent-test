import operator
import os
from typing import Annotated, Any

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.messages import AnyMessage, ToolMessage
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain_openai import ChatOpenAI
from typing_extensions import TypedDict

from src.tools.commands import peek_task, respond_task, start_task
from src.tools.e2b import e2b_read_file, e2b_write_file, python_code_executor
from src.tools.file import edit_file_by_line, read_file, write_file
from src.tools.mind import collaborative_discussion
from src.tools.plan import get_plans, init_planning, update_plan
from src.tools.web import browserless_web_loader, google_search

load_dotenv()

search = GoogleSerperAPIWrapper()

api_key = os.getenv("VOLCENGINE_API_KEY")

model = ChatOpenAI(
    base_url="https://ark.cn-beijing.volces.com/api/v3",
    model="deepseek-v3-2-251201",
    # model="deepseek-v3-1-terminus",
    api_key=api_key,
    temperature=0.1,
    timeout=30,
    stream_usage=True,
)






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




tools = [get_plans, init_planning, update_plan, collaborative_discussion]
tools_by_name = {tool.name: tool for tool in tools}
model_with_tools = model.bind_tools(tools)

class MessagesState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]
    llm_calls: int
    
    
def tool_node(state: dict[str, Any]):
    """Performs the tool call"""

    result = []
    for tool_call in state["messages"][-1].tool_calls:
        tool = tools_by_name[tool_call["name"]]
        observation = tool.invoke(tool_call["args"])
        result.append(ToolMessage(content=observation, tool_call_id=tool_call["id"]))
    return {"messages": result}

# agent = create_agent(
#     model=model,
#     tools=[get_plans, init_planning, update_plan, collaborative_discussion],
#     system_prompt="""
#     你是一个专注的架构师，软件工程师，熟知系统架构搭建整体流程，对任务的规划有着清晰的认知。
#     只需要制定计划，不需要具体执行，有任何的困惑或者需要专业建议可以询问专家
#     """,
# )



agent = create_agent(
    model=model,
    tools=[get_plans, init_planning, update_plan, collaborative_discussion, read_file, write_file, edit_file_by_line, start_task, respond_task, peek_task, google_search, browserless_web_loader, e2b_read_file, e2b_write_file, python_code_executor],
    system_prompt="""
    你是一个专注的架构师，软件工程师，熟知系统架构搭建整体流程，对任务的规划有着清晰的认知，擅长使用现代化的技术来搭建项目，为了减少重复造轮子，你会收集项目最佳实践。你擅长分析用户的简单需求，将其实现，专注于用户需求本身，
    对于自己已有的知识，你始终保持着质疑，你会使用搜索工具去探索现代化的项目最佳实践。你不会手动安装依赖，而是使用推荐的包管理器来安装依赖确保依赖正确。
    项目初始化应该使用最佳实践推荐的方式来进行，尽可能避免手动初始化项目。
    只需要制定计划，不需要具体执行，有任何的困惑或者需要专业建议可以询问专家。
    
    对于一些最佳实践，你可以使用网络搜索来获取最新的最佳实践，并且不要仅获取摘要，要查看网页内容。
    
    涉及计算问题则需要使用python_code_executor编写代码来处理，这样会更精准、更快，避免心算
    
    不要随意生成用户可能不需要的内容，这样的内容你应该询问用户，不用编写用户手册或使用文档。
    """,
)

