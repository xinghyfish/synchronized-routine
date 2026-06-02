# 第二周

- [ ] 角色设定、任务边界、输入上下文、输出格式、反例约束。
- [ ] Few-shot examples 的使用场景。
- [ ] 结构化输出、JSON Schema、函数参数 schema。
- [ ] prompt 注入、数据与指令混淆、系统指令保护。


## Prompt 优化

Prompt 优化的目标在于让模型在约束下做正确的事情，让模型调用变得可控。分别需要解决以下五个问题：

```
角色设定：你是谁？
任务边界：你能做什么，不能做什么？
输入上下文：这次任务有哪些已知信息？
输出格式：你必须怎么返回？
反例约束：哪些回答方式是错误的？
```

### 1. 角色设定

角色设定是告诉模型：它应该以什么身份、能力范围、表达风格来回答。

不是为了“演戏”，而是为了让模型选择合适的知识、语气和判断标准。

正例：
```
你是一名资深 Python 后端工程师，擅长设计命令行 Agent 应用。
你需要用中文回答，解释时优先使用工程实践例子。
```

这个角色很清楚：
```
身份：资深 Python 后端工程师
领域：命令行 Agent 应用
语言：中文
偏好：工程实践
```

简而言之就是：**给定模型思考的域（Field），限定模型的搜索域和输出域的范围**。

### 2. 任务边界

任务边界是告诉模型：这次任务应该做什么，不应该做什么。它的价值是防止模型跑题、过度发挥、越权执行。

正例：
```
你的任务是解释概念并给出学习建议。
不要编造官方定义。
不要假装已经运行过代码。
如果不确定，请明确说明“不确定”。
```

实例：
```python
TASK_BOUNDARY = """
任务边界：
1. 只回答 AI Agent 学习、Prompt Engineering、Python CLI 开发相关问题。
2. 如果用户要求你删除文件、提交代码、调用真实外部服务，只能给建议，不能声称已经执行。
3. 如果问题缺少必要信息，先指出缺少的信息，再给出合理假设下的答案。
4. 不要输出和用户问题无关的背景科普。
""".strip()
```

概括来说，设定人物边界的目的是：**让模型在尽可能受控的状态下进行采样。**

### 3. 输入上下文

输入上下文是这次请求里提供给模型的事实材料。比如用户的问题、项目代码片段、报错信息、配置、历史对话，都属于输入上下文。

```
项目背景：
这是一个 Python 命令行 Agent demo，入口文件是 learn.py。
当前使用 DeepSeek 的 OpenAI 兼容 API。
用户希望通过 /json 命令让模型输出固定 JSON。

用户问题：
如何校验 JSON 输出？
```

代码示例如下：

```python
def build_messages(user_input: str, project_context: str) -> list[dict[str, str]]:
    return [
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        },
        {
            "role": "user",
            "content": f"""
项目上下文：
{project_context}

用户问题：
{user_input}
""".strip(),
        },
    ]

PROJECT_CONTEXT = """
当前应用是一个 Python 命令行 AI Agent demo。
使用 openai Python SDK 调用 DeepSeek API。
支持普通问答和 /json 固定 JSON 输出模式。
JSON 输出需要包含 summary、answer、todos、confidence。
""".strip()

messages = build_messages(
    user_input="如何让模型稳定输出 JSON？",
    project_context=PROJECT_CONTEXT,
)
```

概括来说，输入上下文是为了**让模型拥有更多的后验知识，让采样空间更精确**。

### 4. 输出格式

输出格式是告诉模型：结果必须长什么样。如果你希望程序继续处理模型结果，输出格式尤其重要。输出格式的设定更多是出于工程化考虑，让LLM能够以稳定的形式输出程序可处理的响应，以便于下游的代码进行操作。

关键的原则是：
```
Prompt 负责引导模型。
代码负责校验结果。
不要只靠 prompt 保证正确性。
```

### 5. 反例约束

反例约束是明确告诉模型：哪些输出是不允许的。

它比单纯说“请输出 JSON”更有效，因为模型经常会“好心”加解释。

不过注意：prompt 里的反例如果写了代码块，模型有时会模仿代码块。更稳的做法是用文字描述反例，不直接放完整代码块。

比如：

```python
JSON_SYSTEM_PROMPT = """
禁止行为：
1. 不要用 Markdown 代码块包裹 JSON。
2. 不要在 JSON 前写“下面是结果”。
3. 不要省略任何字段。
4. 不要把 todos 输出成字符串。
5. 不要把 confidence 输出为中文。
""".strip()
```

### 综合范式

一个比较标准的开发范式是：

```python
def build_json_messages(user_input: str) -> list[dict[str, str]]:
    return [
        {
            "role": "system",
            "content": """
你是一个严格的 JSON 输出助手。
你必须只输出合法 JSON 对象，不要输出 Markdown、代码块或解释文字。

输出结构：
{
  "summary": "一句话总结用户问题",
  "answer": "直接回答用户问题",
  "todos": ["可执行的下一步建议"],
  "confidence": "high | medium | low"
}

约束：
- 所有字段都必须存在
- todos 必须是数组
- confidence 只能是 high、medium、low
""".strip(),
        },
        {
            "role": "user",
            "content": f"用户问题：{user_input}",
        },
    ]
```

调用模型：
```python
result = agent.learn(
    build_json_messages(user_input),
    temperature=0.2,
    json_mode=True,
)
```

解析校验：
```python
data = parse_agent_json(result)
```

渲染给用户：
```python
print(render_json_answer(data))
```

LLM 调用到后处理的操作链路如下：
```
角色设定
-> 任务边界
-> 输入上下文
-> 输出格式
-> 反例约束
-> 模型响应
-> 本地解析
-> 本地校验
-> 控制台渲染
```

一言以蔽之：**Prompt 负责让模型“尽量做对”，代码负责保证系统“不能错着往下跑”。**

