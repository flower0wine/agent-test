import os

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

load_dotenv()

api_key = os.getenv("VOLCENGINE_API_KEY")

model = ChatOpenAI(
    base_url="https://ark.cn-beijing.volces.com/api/v3",
    # model="deepseek-v3-2-251201",
    model="deepseek-v3-1-terminus",
    api_key=api_key,
    temperature=0.1,
    timeout=60,
    stream_usage=True
)

@tool
def collaborative_discussion(expert_system_prompt: str, discussion_topic: str) -> str:
    """
    【讨论工具】与外部专家级 LLM 进行深度对话，获取决策支持或方案评估。
    
    当当前 plan_step 涉及复杂决策、方案设计或需要多维度考量时使用。
    
    参数:
    - expert_system_prompt: 赋予外部 LLM 的专家身份和行为准则。
      必须包含：专家背景、评估标准。
    - discussion_topic: 需要讨论的具体问题、当前 Plan 的背景以及你遇到的瓶颈，还有你缺少的信息。
    
    返回：
    - 专家 LLM 的详细建议。Agent 应当根据此建议更新当前 Plan 状态或细化后续步骤。
    """
    
    messages = [
        SystemMessage(content=expert_system_prompt),
        HumanMessage(content=discussion_topic)
    ]
    
    try:
        response = model.invoke(messages)
        # 格式化输出，方便 Agent 吸收信息
        formatted_response = (
            f"--- 外部专家讨论结果 ---\n"
            f"提示: 参考下述建议，你如果还需要建议，可以进行多次交谈。\n"
            f"---------------------------\n"
            f"{response.content}\n"
        )
        return formatted_response
    except Exception as e:
        return f"讨论工具调用失败: {str(e)}"
