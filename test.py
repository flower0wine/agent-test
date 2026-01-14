from dotenv import load_dotenv
from e2b_code_interpreter import Sandbox

load_dotenv()

sandbox: Sandbox | None = None


def get_sandbox() -> Sandbox:
    """懒加载 sandbox，避免提前创建"""
    global sandbox
    if sandbox is None:  # 检查是否已关闭
        sandbox = Sandbox.create()  # 可选：Sandbox(timeout=600) 延长存活时间
    return sandbox


if __name__ == "__main__":
    sandbox = get_sandbox()
    print(sandbox)
