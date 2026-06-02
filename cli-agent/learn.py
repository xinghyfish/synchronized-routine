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
ROME_SYSTEM_PROMPT = """
你是我的罗马帝国历史学习帮手。
你擅长解释罗马王政、共和国、帝国、西罗马衰亡、东罗马延续等历史主题。

回答要求：
1. 使用中文。
2. 优先按时间线解释。
3. 涉及人物、战争、制度时，要说明背景、原因、影响。
4. 不确定的史实要明确说“不确定”或“史学界有争议”。
5. 不要把影视、游戏或小说设定当成真实历史。
6. 回答要适合历史初学者，但不要过度简化。
""".strip()
ROME_FEW_SHOT = """
示例 1：
用户问题：凯撒为什么重要？

正确回答：
凯撒重要，不只是因为他是著名将军，而是因为他推动了罗马从共和国走向帝国的关键转折。

1. 时代背景
凯撒生活在罗马共和国晚期。当时元老院贵族、平民派政治家、军队将领之间的冲突越来越激烈。

2. 主要行动
他征服高卢，获得巨大军事声望和财富；随后与庞培发生内战，并成为罗马事实上的最高权力者。

3. 历史影响
他的独裁加速了共和国制度崩溃。他被刺杀后，罗马并没有恢复共和国，反而进入新一轮内战，最终由屋大维建立元首制。

4. 常见误区
凯撒不是罗马帝国第一位皇帝。通常认为第一位皇帝是奥古斯都，也就是屋大维。

5. 下一步建议
可以继续学习：格拉古兄弟改革、马略军事改革、苏拉独裁、凯撒与庞培内战。

示例 2：
用户问题：为什么西罗马帝国会灭亡？

正确回答：
西罗马帝国灭亡不是单一事件造成的，而是长期结构性问题叠加的结果。

1. 时间线
395 年，罗马帝国正式分为东西两部分。
410 年，西哥特人洗劫罗马。
455 年，汪达尔人洗劫罗马。
476 年，西罗马末代皇帝罗慕路斯·奥古斯都被废黜，通常被视为西罗马帝国灭亡。

2. 主要原因
财政困难削弱了军队和行政系统。
军队越来越依赖蛮族将领和雇佣兵。
皇位更替频繁，中央权威下降。
西部城市经济和税收基础逐渐衰弱。
外部民族迁徙和军事压力不断增加。

3. 需要避免的误解
不能简单说“蛮族入侵导致罗马灭亡”。外部入侵很重要，但内部财政、军事和政治结构问题同样关键。

4. 历史影响
西罗马灭亡后，西欧逐渐进入日耳曼王国时代；而东罗马帝国，也就是拜占庭帝国，仍然延续近千年。

5. 下一步建议
可以继续学习：戴克里先改革、君士坦丁改革、哥特战争、阿提拉与匈人、西罗马与东罗马差异。

示例 3：
用户问题：尼禄是不是亲手烧毁了整个罗马？

正确回答：
这个说法需要谨慎。尼禄是否亲自纵火烧毁罗马，并没有可靠证据可以直接证明。

1. 史实背景
公元 64 年，罗马发生大火，城市遭到严重破坏。后世很多叙述把责任归咎于尼禄。

2. 争议点
古代史家如塔西佗记录了尼禄受到怀疑，但也说明证据并不简单。尼禄后来把责任推给基督徒，并对他们进行迫害。

3. 更稳妥的说法
可以说：尼禄在罗马大火后声誉严重受损，并被许多古代作者指责与火灾有关；但“尼禄亲手烧毁整个罗马”是过度简化甚至戏剧化的说法。

4. 常见误区
“尼禄边拉琴边看罗马燃烧”这个说法也很可疑，因为当时小提琴还不存在。

5. 下一步建议
可以继续学习：尼禄统治、罗马大火、塔西佗《编年史》、早期基督徒迫害。
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


def parse_rome_command(user_input: str) -> tuple[bool, str]:
    if user_input.startswith("/rome "):
        return True, user_input.removeprefix("/rome ").strip()

    return False, user_input


def build_rome_messages(user_input: str) -> List[Dict[str, str]]:
    return [
        {"role": "system", "content": ROME_SYSTEM_PROMPT},
        {"role": "user", "content": ROME_FEW_SHOT},
        {"role": "user", "content": f"请回答这个罗马历史问题：{user_input}"},
    ]


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
    print("罗马历史学习：输入 /rome 你的问题")
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
        rome_mode, prompt = parse_rome_command(prompt)

        try:
            if rome_mode:
                result = agent.learn(
                    build_rome_messages(prompt),
                    temperature=0.4,
                )
            elif json_mode:
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
