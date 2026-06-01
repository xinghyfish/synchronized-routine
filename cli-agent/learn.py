import json
import os
from typing import Any, Dict, List

from openai import OpenAI


SYSTEM_PROMPT = "你是一个简洁、友好的中文命令行助手。回答要清晰、实用。"
JSON_SYSTEM_PROMPT = """
你是一个严格的 JSON 输出助手。
你必须只输出一个合法 JSON 对象，不要输出 Markdown，不要输出代码块，不要输出解释性文字。

JSON 对象必须符合这个结构：
{
  "summary": "一句话总结用户问题",
  "answer": "直接回答用户问题",
  "todos": ["可执行的下一步建议"],
  "confidence": "high | medium | low"
}

字段要求：
- summary、answer、confidence 必须是字符串。
- todos 必须是字符串数组。
- confidence 只能是 high、medium、low 之一。
- 如果信息不足，也必须输出合法 JSON，并在 answer 中说明缺少什么信息。
""".strip()
SEPARATOR = "-" * 64


def create_prompt_reader():
    try:
        from prompt_toolkit import PromptSession
        from prompt_toolkit.history import InMemoryHistory
    except ImportError:
        return None

    return PromptSession(history=InMemoryHistory())


def read_prompt(session) -> str:
    if session:
        return session.prompt("User> ").strip()

    return input("User> ").strip()


def print_turn(title: str, content: str) -> None:
    print(title, " ", content)
    print(SEPARATOR + "\n")


def parse_json_command(user_input: str) -> tuple[bool, str]:
    if user_input.startswith("/json "):
        return True, user_input.removeprefix("/json ").strip()

    return False, user_input


def pretty_json(text: str) -> str:
    data = json.loads(text)
    return json.dumps(data, ensure_ascii=False, indent=2)


def require_string(data: Dict[str, Any], field: str) -> str:
    value = data.get(field)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"JSON 字段 {field} 必须是非空字符串")

    return value.strip()


def require_todos(data: Dict[str, Any]) -> List[str]:
    value = data.get("todos")
    if not isinstance(value, list):
        raise ValueError("JSON 字段 todos 必须是数组")

    todos = []
    for item in value:
        if not isinstance(item, str) or not item.strip():
            raise ValueError("JSON 字段 todos 中的每一项都必须是非空字符串")
        todos.append(item.strip())

    return todos


def render_json_answer(text: str) -> str:
    data = json.loads(text)
    if not isinstance(data, dict):
        raise ValueError("模型输出必须是 JSON 对象")

    summary = require_string(data, "summary")
    answer = require_string(data, "answer")
    todos = require_todos(data)
    confidence = require_string(data, "confidence")

    if confidence not in {"high", "medium", "low"}:
        raise ValueError("JSON 字段 confidence 只能是 high、medium、low")

    todo_text = "\n".join(
        f"{index}. {todo}"
        for index, todo in enumerate(todos, start=1)
    )
    if not todo_text:
        todo_text = "暂无"

    raw_json = json.dumps(data, ensure_ascii=False, indent=2)

    return f"""总结：
{summary}

回答：
{answer}

下一步：
{todo_text}
"""


class CommandAgent:
    def __init__(self):
        api_key = os.getenv("DEEPSEEK_API_KEY")
        if not api_key:
            raise RuntimeError("未找到 DEEPSEEK_API_KEY，请先设置环境变量。")

        self.client = OpenAI(
            api_key=api_key,
            base_url="https://api.deepseek.com",
        )
        self.model = os.getenv("DEEPSEEK_MODEL", "deepseek-v4-flash")

    def learn(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        json_mode: bool = False,
    ) -> str:
        request = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
        }

        if json_mode:
            request["response_format"] = {"type": "json_object"}

        try:
            response = self.client.chat.completions.create(**request)
        except Exception:
            if not json_mode:
                raise

            request.pop("response_format", None)
            response = self.client.chat.completions.create(**request)

        return response.choices[0].message.content or ""

def main():
    try:
        agent = CommandAgent()
    except RuntimeError as error:
        print(f"配置错误：{error}")
        raise SystemExit(1)

    prompt_session = create_prompt_reader()
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    print("Agent 已启动。输入 exit / quit / q 退出。")
    print("固定 JSON 输出：输入 /json 你的问题")
    if not prompt_session:
        print("提示：安装 prompt_toolkit 后，中文、emoji、删除键和历史输入体验会更好。")

    while True:
        try:
            user_input = read_prompt(prompt_session)
        except (EOFError, KeyboardInterrupt):
            print("\n已退出。")
            break

        if not user_input:
            continue

        if user_input.lower() in {"exit", "quit", "q"}:
            print("已退出。")
            break

        json_mode, prompt = parse_json_command(user_input)

        try:
            if json_mode:
                json_messages = [
                    {"role": "system", "content": JSON_SYSTEM_PROMPT},
                    {"role": "user", "content": prompt},
                ]
                result = agent.learn(
                    json_messages,
                    temperature=0.2,
                    json_mode=True,
                )
                result = render_json_answer(result)
            else:
                messages.append({"role": "user", "content": prompt})
                result = agent.learn(messages)
                messages.append({"role": "assistant", "content": result})
        except Exception as error:
            print_turn("Error", f"调用或解析失败：{error}")
            continue

        print_turn("Agent> \n", result)


def test_tempereture():
    agent = CommandAgent()
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": "请以“亨利走在拉泰的街头“为开头写一篇200字的短文"},
    ]

    print("=== Temperature: 0.0 ===")
    print(agent.learn(messages, temperature=0.0))

    print("\n=== Temperature: 0.7 ===")
    print(agent.learn(messages, temperature=0.7))

    print("\n=== Temperature: 1.0 ===")
    print(agent.learn(messages, temperature=1.0))


if __name__ == "__main__":
    main()
