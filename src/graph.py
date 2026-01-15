import operator
import os
from typing import Literal

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain.messages import AnyMessage, SystemMessage, ToolMessage
from langchain.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph
from typing_extensions import Annotated, TypedDict


class MessagesState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]
    llm_calls: int


load_dotenv()

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


# Define tools
@tool
def multiply(a: float, b: float) -> float:
    """Multiply `a` and `b`.

    Args:
        a: First float
        b: Second float
    """
    return a * b


@tool
def add(a: float, b: float) -> float:
    """Adds `a` and `b`.

    Args:
        a: First float
        b: Second float
    """
    return a + b


@tool
def divide(a: float, b: float) -> float:
    """Divide `a` and `b`.

    Args:
        a: First int
        b: Second int
    """
    return a / b


# Augment the LLM with tools
tools = [add, multiply, divide]
tools_by_name = {tool.name: tool for tool in tools}
model_with_tools = model.bind_tools(tools)


def llm_call(state: dict):
    """LLM decides whether to call a tool or not"""

    return {
        "messages": [
            model_with_tools.invoke(
                [
                    SystemMessage(
                        content="You are the **arithmetic orchestrator**.\n"
                        "Your job is to:\n"
                        "- Understand the user's math question\n"
                        "- Break it into independent + - × ÷ operations\n"
                        "- 你可以并行计算多个式子，只要结果不会受到并行的影响\n"
                        "- After getting results, combine them into final answer\n\n"
                    )
                ]
                + state["messages"]
            )
        ],
        "llm_calls": state.get("llm_calls", 0) + 1,
    }


def tool_node(state: dict):
    """Performs the tool call"""

    result = []
    for tool_call in state["messages"][-1].tool_calls:
        tool = tools_by_name[tool_call["name"]]
        observation = tool.invoke(tool_call["args"])
        result.append(
            ToolMessage(content=observation, tool_call_id=tool_call["id"])
        )
    return {"messages": result}


def should_continue(state: MessagesState) -> Literal["tool_node", END]:
    """Decide if we should continue the loop or stop based upon whether the LLM made a tool call"""

    messages = state["messages"]
    last_message = messages[-1]

    # If the LLM makes a tool call, then perform an action
    if last_message.tool_calls:
        return "tool_node"

    # Otherwise, we stop (reply to the user)
    return END


# Build workflow
agent_builder = StateGraph(MessagesState)

# Add nodes
agent_builder.add_node("llm_call", llm_call)
agent_builder.add_node("tool_node", tool_node)

# Add edges to connect nodes
agent_builder.add_edge(START, "llm_call")
agent_builder.add_conditional_edges(
    "llm_call", should_continue, ["tool_node", END]
)
agent_builder.add_edge("tool_node", "llm_call")

# Compile the agent
agent = agent_builder.compile()
