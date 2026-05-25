# AI Agent 前沿学习路线清单

适用背景：软件工程专业毕业、工作约 1 年、AI 基础较少，希望系统进入 Agent 方向。目标不是“先把所有理论学完”，而是在 8-12 周内完成从基础认知到可运行 Agent 项目的跃迁。

## 0. 学习目标

- [ ] 能解释 LLM、Prompt、Embedding、RAG、Tool Calling、Agent、Workflow 的区别。
- [ ] 能用 Python 或 TypeScript 调用主流大模型 API，完成结构化输出和函数调用。
- [ ] 能实现一个带工具、记忆、检索、评测和日志追踪的 Agent。
- [ ] 能理解 MCP、LangGraph、OpenAI Agents SDK、AutoGen/CrewAI 等生态的定位。
- [ ] 能判断一个业务场景是否适合使用 Agent，而不是盲目套 Agent。
- [ ] 能构建一个可展示的毕业级/求职级 Agent 项目。

## 1. 第 1 周：AI 与 LLM 基础补齐

### 学习目标

- [ ] 能解释 AI、机器学习、深度学习、生成式 AI、LLM 的关系。
- [ ] 能说清 token、上下文窗口、temperature、top_p、max_tokens 的作用。
- [ ] 能独立调用一次大模型 API，并知道一次请求的输入、输出、成本大概由什么决定。
- [ ] 能识别 LLM 的典型风险：幻觉、过时知识、上下文遗漏、格式不稳定。

### 学习内容

- [ ] Transformer 高层原理：attention、token、上下文窗口，不要求手写模型。
- [ ] Chat Completions/Responses 类 API 的基本调用方式。
- [ ] system/user/developer message 的职责。
- [ ] 常见参数对输出稳定性和创造性的影响。

### 实践 Step

- [ ] Step 1：创建一个 `week01-llm-basics` 小项目。
- [ ] Step 2：写一个命令行聊天程序，输入问题后打印模型回答。
- [ ] Step 3：用同一个问题分别设置低 temperature 和高 temperature，保存 3 组输出对比。
- [ ] Step 4：让模型输出固定 JSON，例如 `{ "summary": "", "todos": [] }`。
- [ ] Step 5：写一个 JSON 解析与校验逻辑，解析失败时打印错误。

### 实践检验方式

- [ ] 程序能连续完成 5 轮问答。
- [ ] JSON 输出能被本地代码成功解析。
- [ ] 你能用自己的话解释为什么高 temperature 输出更发散。
- [ ] 你能举出 3 个 LLM 不适合直接回答的场景。

### 输出物

- [ ] 一个可运行的最小 LLM CLI。
- [ ] 一篇短笔记：`LLM 为什么不是数据库，也不是搜索引擎？`

## 2. 第 2 周：Prompt Engineering 与结构化输出

### 学习目标

- [ ] 能把模糊需求改写成清晰 prompt。
- [ ] 能设计稳定的结构化输出格式。
- [ ] 能用 JSON Schema 或类似方式验证模型输出。
- [ ] 能识别简单的 prompt 注入与越权指令。

### 学习内容

- [ ] 角色设定、任务边界、输入上下文、输出格式、反例约束。
- [ ] Few-shot examples 的使用场景。
- [ ] 结构化输出、JSON Schema、函数参数 schema。
- [ ] prompt 注入、数据与指令混淆、系统指令保护。

### 实践 Step

- [ ] Step 1：建立 `prompt-lab`，收集 5 类 prompt：总结、分类、抽取、改写、规划。
- [ ] Step 2：实现“需求分析助手”，输入一句需求，输出模块、接口、风险、验收标准。
- [ ] Step 3：为输出定义 JSON Schema，并在本地做校验。
- [ ] Step 4：加入 3 个 few-shot 示例，比较前后输出稳定性。
- [ ] Step 5：输入恶意 prompt，例如“忽略之前所有规则”，观察并记录结果。

### 实践检验方式

- [ ] 连续输入 10 条不同需求，至少 8 条能输出合法 JSON。
- [ ] 输出字段不能缺失关键项：模块、接口、风险、验收标准。
- [ ] 模型遇到越权指令时不应泄露系统约束或改变任务目标。
- [ ] 你能总结出 5 条自己最常用的 prompt 编写规则。

### 输出物

- [ ] 一个 `prompt-lab` 小项目。
- [ ] 一份 `prompt-patterns.md`，记录有效 prompt 模板和失败案例。

## 3. 第 3 周：Embedding、向量数据库与 RAG

### 学习目标

- [ ] 能解释 embedding 与关键词搜索的区别。
- [ ] 能实现一个最小 RAG 流程。
- [ ] 能理解 chunk size、top_k、rerank、引用来源对答案质量的影响。
- [ ] 能判断 RAG 答案是否有可靠依据。

### 学习内容

- [ ] 文档加载、文本切分、向量化、向量检索、上下文拼接、答案生成。
- [ ] chunking 策略：按长度、按标题、按语义边界。
- [ ] top_k、相似度阈值、rerank 的基本意义。
- [ ] RAG 常见问题：召回失败、上下文污染、答案无引用。

### 实践 Step

- [ ] Step 1：准备 5-10 篇 Markdown 或 PDF 资料作为知识库。
- [ ] Step 2：写脚本完成文档读取和 chunk 切分。
- [ ] Step 3：生成 embedding，并保存到 Chroma、FAISS、SQLite 扩展或本地 JSON。
- [ ] Step 4：实现命令行问答，回答时必须附带来源文件名和片段。
- [ ] Step 5：分别测试 chunk size 为 300、800、1500 时的回答质量。
- [ ] Step 6：准备 10 个问题，记录召回片段是否真的包含答案。

### 实践检验方式

- [ ] 至少 8 个问题能检索到相关片段。
- [ ] 回答必须包含引用来源，不能凭空回答。
- [ ] 当知识库没有答案时，系统能回答“不知道”或“资料中未找到”。
- [ ] 你能说清一个 RAG 系统失败时应该先检查召回还是生成。

### 输出物

- [ ] 一个“个人知识库问答”Demo。
- [ ] 一份 `rag-eval.md`，记录 10 个问题、召回片段、回答质量和改进点。

## 4. 第 4 周：Tool Calling 与函数调用

### 学习目标

- [ ] 能设计一个安全、清晰、可验证的工具 schema。
- [ ] 能实现模型选择工具、程序执行工具、结果回传模型的完整循环。
- [ ] 能处理工具失败、参数错误和重试。
- [ ] 能理解工具权限与危险操作确认。

### 学习内容

- [ ] Tool Calling / Function Calling 的执行流程。
- [ ] 工具命名、参数描述、返回值格式设计。
- [ ] 多工具选择与工具结果总结。
- [ ] 工具执行的安全边界、幂等性、超时和错误处理。

### 实践 Step

- [ ] Step 1：实现 4 个工具：计算器、文件搜索、文本摘要、待办事项生成。
- [ ] Step 2：为每个工具定义参数 schema 和返回格式。
- [ ] Step 3：让模型根据用户问题自动选择工具，而不是在代码里写死。
- [ ] Step 4：为工具加入错误场景，例如文件不存在、参数为空、计算表达式非法。
- [ ] Step 5：加入工具调用日志，记录工具名、参数、耗时、结果摘要。

### 实践检验方式

- [ ] 输入 10 条任务，模型能在至少 8 条中选择正确工具。
- [ ] 工具失败时，Agent 能解释失败原因并尝试修正参数。
- [ ] 日志能完整展示一次工具调用链路。
- [ ] 你能说明为什么删除文件、发邮件、提交代码这类工具必须加人工确认。

### 输出物

- [ ] 一个“多工具命令助手”。
- [ ] 一份 `tools.md`，记录每个工具的 schema、用途、风险等级。

## 5. 第 5 周：Agent 基础架构

### 学习目标

- [ ] 能区分 Agent、普通聊天机器人、固定 workflow。
- [ ] 能手写一个最小 Agent Loop。
- [ ] 能理解 ReAct：Reasoning + Acting + Observation。
- [ ] 能为 Agent 增加步数限制、状态记录和人工确认。

### 学习内容

- [ ] Agent 的核心组成：目标、状态、工具、循环、观察、完成条件。
- [ ] Planning、Reflection、Memory、Multi-Agent 的基础模式。
- [ ] Agent 无限循环、错误工具调用、目标漂移等常见问题。
- [ ] 人机协作与权限控制。

### 实践 Step

- [ ] Step 1：基于第 4 周工具，手写一个 Agent Loop。
- [ ] Step 2：每一步让模型输出下一步动作：继续思考、调用工具、请求用户确认、完成任务。
- [ ] Step 3：加入最大步数限制，例如最多 8 步。
- [ ] Step 4：把每一步的 action、observation、final answer 保存到日志。
- [ ] Step 5：实现一个“代码仓库问答 + 修改建议 Agent”，能搜索文件并给出修改建议。

### 实践检验方式

- [ ] Agent 能完成“帮我找出项目入口文件并总结职责”这类多步任务。
- [ ] Agent 不会无限循环，超过最大步数能安全停止。
- [ ] 涉及文件修改建议时，Agent 只给方案，不直接改文件。
- [ ] 你能画出自己 Agent Loop 的流程图。

### 输出物

- [ ] 一个“代码仓库问答 + 修改建议 Agent”。
- [ ] 一份 `agent-loop.md`，解释状态、工具、循环和退出条件。

## 6. 第 6 周：Agent 框架与工作流编排

### 学习目标

- [ ] 能理解框架解决的是工程编排问题，不只是封装 API。
- [ ] 能用 LangGraph 或 OpenAI Agents SDK 实现一个可控工作流。
- [ ] 能比较 graph/workflow 与 autonomous loop 的区别。
- [ ] 能理解 handoff、guardrail、checkpoint、tracing 的价值。

### 学习内容

- [ ] OpenAI Agents SDK：工具、handoff、guardrail、tracing。
- [ ] LangGraph：状态图、节点、边、checkpoint、人机协作。
- [ ] AutoGen：多 Agent 对话和协作。
- [ ] CrewAI：角色、任务、流程编排。
- [ ] LlamaIndex：RAG 与数据连接场景。

### 实践 Step

- [ ] Step 1：选择 LangGraph 或 OpenAI Agents SDK 作为主框架。
- [ ] Step 2：实现“需求 -> 设计 -> 代码建议 -> 测试建议”的 4 步流程。
- [ ] Step 3：把其中一步设计成人工确认节点。
- [ ] Step 4：加入失败重试，例如代码建议为空时重新生成。
- [ ] Step 5：把第 5 周手写 Agent 的同类功能迁移到框架版本。

### 实践检验方式

- [ ] 能从一次输入稳定生成设计、代码建议、测试建议。
- [ ] 人工确认节点能暂停流程并等待输入。
- [ ] 你能说明什么时候选 LangGraph，什么时候手写 workflow 就够了。
- [ ] 你能指出框架带来的复杂度成本。

### 输出物

- [ ] 一个框架版 Agent workflow。
- [ ] 一篇对比笔记：`手写 Agent Loop、LangGraph、OpenAI Agents SDK 的差异`。

## 7. 第 7 周：MCP 与 Agent 工具生态

### 学习目标

- [ ] 能解释 MCP 是什么，以及它和 Tool Calling、HTTP API 的关系。
- [ ] 能跑通一个现成 MCP server。
- [ ] 能写一个最小 MCP server 暴露本地工具。
- [ ] 能把 MCP 工具接入 Agent。

### 学习内容

- [ ] MCP 的角色：Host、Client、Server。
- [ ] MCP 的能力：tools、resources、prompts。
- [ ] MCP server 的启动、连接、权限与配置。
- [ ] MCP 在 IDE、桌面助手、企业内部工具中的价值。

### 实践 Step

- [ ] Step 1：跑通一个现成 MCP server，例如文件系统、Git、数据库或浏览器自动化。
- [ ] Step 2：用 MCP inspector 或兼容客户端测试工具调用。
- [ ] Step 3：自己写一个 `dev-helper-mcp`，提供 `list_files`、`search_code`、`summarize_file` 三个工具。
- [ ] Step 4：把 MCP server 接入一个 Agent，让 Agent 通过 MCP 搜索项目文件。
- [ ] Step 5：为高风险工具增加只读限制或人工确认。

### 实践检验方式

- [ ] MCP server 能被客户端发现并列出工具。
- [ ] 至少 3 个工具能成功调用并返回结构化结果。
- [ ] Agent 能通过 MCP 工具回答“这个项目有哪些模块？”。
- [ ] 你能说明 MCP 带来的好处和额外部署成本。

### 输出物

- [ ] 一个“本地开发助手 MCP Server”。
- [ ] 一份 `mcp-notes.md`，记录 MCP server 配置、工具列表和接入方式。

## 8. 第 8 周：记忆、上下文工程与长期任务

### 学习目标

- [ ] 能区分短期上下文、长期记忆、任务状态和用户画像。
- [ ] 能为 Agent 增加会话摘要和任务状态。
- [ ] 能理解上下文压缩和检索记忆的适用场景。
- [ ] 能让一个任务中断后继续执行。

### 学习内容

- [ ] 上下文工程：放什么、丢什么、总结什么、检索什么。
- [ ] 摘要记忆、向量记忆、事件日志、任务状态表。
- [ ] durable execution 与 checkpoint。
- [ ] 长期 Agent 的成本控制、状态一致性和可解释性。

### 实践 Step

- [ ] Step 1：为第 5 或第 6 周 Agent 增加会话摘要。
- [ ] Step 2：设计任务状态表，记录任务目标、当前阶段、已完成步骤、下一步。
- [ ] Step 3：把历史对话压缩为摘要，再继续下一轮任务。
- [ ] Step 4：实现一个“长期研究助手”，能分多轮收集资料并保存进度。
- [ ] Step 5：模拟程序中断，重启后从状态文件恢复任务。

### 实践检验方式

- [ ] Agent 能在第 2 天继续昨天未完成的任务。
- [ ] 摘要不会丢失任务目标、关键约束和已完成步骤。
- [ ] 状态文件能解释 Agent 当前为什么执行下一步。
- [ ] 你能判断哪些信息应该进入长期记忆，哪些只留在短期上下文。

### 输出物

- [ ] 一个“长期研究助手”。
- [ ] 一份 `memory-design.md`，说明记忆结构、状态字段和恢复策略。

## 9. 第 9 周：评测、可观测性与安全

### 学习目标

- [ ] 能为 Agent 设计固定测试集。
- [ ] 能记录模型调用、工具调用、错误、耗时和成本。
- [ ] 能识别 Agent 的安全风险并设置防线。
- [ ] 能写出一个 Agent 测试报告。

### 学习内容

- [ ] Agent 评测：任务成功率、工具选择准确率、引用准确率、人工干预次数。
- [ ] 测试集设计：正常任务、边界任务、恶意输入、工具失败。
- [ ] tracing：模型输入输出、工具参数、工具结果、错误栈、耗时。
- [ ] 安全：权限最小化、敏感数据保护、人工确认、审计日志。

### 实践 Step

- [ ] Step 1：为你的 Agent 设计 20 条固定测试用例。
- [ ] Step 2：实现一个 `run_eval` 脚本，批量执行测试任务并保存结果。
- [ ] Step 3：记录每一步模型输入、输出、工具调用、耗时和错误。
- [ ] Step 4：加入 5 条恶意或越权测试，例如要求读取敏感文件、删除文件、绕过规则。
- [ ] Step 5：为高风险工具加入确认机制和审计日志。

### 实践检验方式

- [ ] 测试报告能统计成功率、失败原因、平均步骤数。
- [ ] 至少能复现 3 个失败案例，并说明改进方向。
- [ ] Agent 遇到危险操作时必须拒绝或请求人工确认。
- [ ] 你能说明“看起来回答对了”和“可验证地完成任务”有什么不同。

### 输出物

- [ ] 一个 `eval` 测试集与批量运行脚本。
- [ ] 一个 Agent 测试报告：成功率、失败案例、改进方案。

## 10. 第 10-12 周：综合项目

选择一个项目做深，不要同时做太多。目标是做出一个可以放进简历、GitHub README 和面试讲解的作品。

### 学习目标

- [ ] 能把前 9 周能力整合成一个完整 Agent 应用。
- [ ] 能写清楚项目架构、关键设计取舍和安全边界。
- [ ] 能提供 demo、测试结果和已知限制。
- [ ] 能把项目从“能跑”推进到“别人能理解、能复现、能评估”。

### 可选项目方向

- [ ] 方向 A：AI 编程助手。读取代码仓库结构、搜索相关文件、回答代码问题、生成修改计划、运行测试并总结失败原因。
- [ ] 方向 B：个人知识库 Agent。导入 Markdown、PDF、网页，支持语义检索、引用来源、多轮追问和定期总结。
- [ ] 方向 C：自动化办公 Agent。读取邮件、表格或文档，抽取待办事项，生成回复草稿，汇总周报，对发送和删除类动作加人工确认。
- [ ] 方向 D：研究型 Agent。自动拆解研究问题，搜索资料，交叉验证来源，生成带引用的报告，输出不确定性与待确认问题。

### 第 10 周：项目 MVP

- [ ] Step 1：确定项目方向、目标用户和 3 个核心使用场景。
- [ ] Step 2：画出架构图：前端/CLI、Agent、工具、数据源、日志、评测。
- [ ] Step 3：实现最小主流程，只保留最关键的 1-2 个工具。
- [ ] Step 4：写 5 条端到端测试任务。
- [ ] Step 5：完成 README 初稿，写清如何运行。

### 第 11 周：增强能力

- [ ] Step 1：加入 RAG、MCP、框架 workflow 或长期记忆中的至少一项。
- [ ] Step 2：加入日志追踪，记录模型调用和工具调用。
- [ ] Step 3：加入错误处理和失败恢复。
- [ ] Step 4：加入人工确认机制，覆盖高风险操作。
- [ ] Step 5：扩展到 15 条测试任务。

### 第 12 周：打磨与展示

- [ ] Step 1：补充评测报告，统计成功率、失败类型、平均耗时。
- [ ] Step 2：录制 2-3 分钟 demo 或准备截图。
- [ ] Step 3：补充 README：架构图、技术栈、核心流程、已知限制、后续计划。
- [ ] Step 4：整理代码结构，移除无关实验文件。
- [ ] Step 5：准备一段面试讲解：为什么这样设计、遇到什么问题、如何评测。

### 实践检验方式

- [ ] 项目能被别人根据 README 在本地跑起来。
- [ ] 至少 15 条测试任务中有明确通过/失败记录。
- [ ] Agent 的每次关键工具调用都有日志。
- [ ] 高风险动作不会在无确认的情况下执行。
- [ ] 你能在 5 分钟内讲清项目架构和技术取舍。

### 输出物

- [ ] 一个完整 GitHub 项目。
- [ ] 一个可展示 demo。
- [ ] 一份评测报告。
- [ ] 一份面试讲解稿。

## 11. 必备工程能力清单

- [ ] Python 或 TypeScript 至少精通一个。
- [ ] 熟悉 HTTP API、异步编程、错误处理、日志。
- [ ] 熟悉 JSON Schema、数据库、缓存、消息队列的基础用法。
- [ ] 熟悉 Docker，能把 Agent 服务容器化。
- [ ] 熟悉基本前端，能做一个简单可用的 Agent UI。
- [ ] 熟悉单元测试、集成测试、端到端测试。
- [ ] 熟悉 GitHub Actions 或其他 CI。

## 12. 推荐学习顺序

1. LLM API 基础
2. Prompt 与结构化输出
3. Embedding 与 RAG
4. Tool Calling
5. 手写 Agent Loop
6. LangGraph 或 OpenAI Agents SDK
7. MCP
8. Agent 评测与可观测性
9. 安全与权限控制
10. 综合项目

## 13. 前沿关键词雷达

- [ ] Agentic Workflow
- [ ] Tool Calling / Function Calling
- [ ] Computer Use
- [ ] Browser Agent
- [ ] Code Agent
- [ ] Multi-Agent Collaboration
- [ ] Human-in-the-loop
- [ ] Model Context Protocol, MCP
- [ ] Long-term Memory
- [ ] Context Engineering
- [ ] Durable Execution
- [ ] Agent Evaluation
- [ ] Guardrails
- [ ] Tracing / Observability
- [ ] Sandbox
- [ ] Retrieval-Augmented Generation, RAG
- [ ] Structured Outputs
- [ ] Voice Agent / Realtime Agent

## 14. 推荐资料

### 官方文档

- [ ] [OpenAI API 文档](https://platform.openai.com/docs)：学习模型调用、工具、结构化输出、多模态输入。
- [ ] [OpenAI Agents SDK 文档](https://platform.openai.com/docs/guides/agents-sdk)：学习 Agent、工具、handoff、guardrail、tracing。
- [ ] [OpenAI Agents SDK Python](https://github.com/openai/openai-agents-python)：阅读 SDK 源码、examples 和多 Agent 工作流实现。
- [ ] [OpenAI Cookbook](https://github.com/openai/openai-cookbook)：学习可运行的 API、RAG、工具调用和 Agent 示例。
- [ ] [Model Context Protocol 官方文档](https://modelcontextprotocol.io/)：学习 MCP 的协议、工具、资源、prompt 和传输机制。
- [ ] [MCP 官方 Server 示例](https://github.com/modelcontextprotocol/servers)：学习文件系统、Git、数据库、浏览器等 MCP server 的写法。
- [ ] [LangGraph 文档](https://langchain-ai.github.io/langgraph/)：学习可恢复、有状态、可控的 Agent 工作流。
- [ ] [LangGraph GitHub](https://github.com/langchain-ai/langgraph)：阅读 graph、checkpoint、人机协作、多 Agent 示例。
- [ ] [LlamaIndex 文档](https://docs.llamaindex.ai/)：学习 RAG、数据连接、索引和 Agentic RAG。
- [ ] [AutoGen 文档](https://microsoft.github.io/autogen/)：学习微软多 Agent 编程框架。
- [ ] [CrewAI 文档](https://docs.crewai.com/)：学习角色化、多任务 Agent 编排。

### 系统课程

- [ ] [Hugging Face AI Agents Course](https://huggingface.co/learn/agents-course/unit0/introduction)：免费、偏系统，覆盖 Agent 基础、smolagents、LlamaIndex、LangGraph、Agentic RAG、评测与最终项目。
- [ ] [Hugging Face AI Agents Course 中文版](https://huggingface.co/learn/agents-course/zh-CN/unit0/introduction)：如果你希望先用中文建立整体概念，可以从这里开始。
- [ ] [DeepLearning.AI: AI Agents in LangGraph](https://www.deeplearning.ai/courses/ai-agents-in-langgraph)：短课，适合第 5-6 周学习手写 Agent Loop 与 LangGraph 的对应关系。
- [ ] [DeepLearning.AI: Multi AI Agent Systems with CrewAI](https://www.deeplearning.ai/short-courses/multi-ai-agent-systems-with-crewai/)：适合理解角色分工、任务拆解和多 Agent 协作。
- [ ] [DeepLearning.AI: Building Agentic RAG with LlamaIndex](https://www.deeplearning.ai/short-courses/building-agentic-rag-with-llamaindex/)：适合第 3 周 RAG 后继续理解 Agentic RAG。
- [ ] [DeepLearning.AI: Evaluating AI Agents](https://www.deeplearning.ai/short-courses/evaluating-ai-agents/)：适合第 9 周学习 Agent 评测方法。

### YouTube 视频与频道

- [ ] [Andrej Karpathy: Intro to Large Language Models](https://www.youtube.com/watch?v=zjkBMFhNj_g)：LLM 入门必看，适合第 1 周建立直觉。
- [ ] [Andrej Karpathy: Deep Dive into LLMs like ChatGPT](https://www.youtube.com/watch?v=7xTGNNLPyMI)：更深入理解 token、训练、推理、能力边界。
- [ ] [3Blue1Brown: Attention in Transformers](https://www.youtube.com/watch?v=eMlx5fFNoYc)：用可视化方式理解 attention。
- [ ] [LangChain YouTube](https://www.youtube.com/@LangChain)：关注 LangGraph、LangSmith、Agent workflow、RAG 相关实战视频。
- [ ] [DeepLearning.AI YouTube](https://www.youtube.com/@Deeplearningai)：关注 Andrew Ng 团队的 Agent、RAG、评测和应用课程发布。
- [ ] [OpenAI YouTube](https://www.youtube.com/@OpenAI)：关注模型、API、Agent、Realtime 和开发者发布。
- [ ] [IBM Technology YouTube](https://www.youtube.com/@IBMTechnology)：适合用概念视频补齐 RAG、Agent、向量数据库、安全等基础。
- [ ] [AssemblyAI YouTube](https://www.youtube.com/@AssemblyAI)：适合看 LLM 应用、RAG、语音 Agent、函数调用的工程教程。
- [ ] [Mervin Praison YouTube](https://www.youtube.com/@MervinPraison)：常做 Agent 框架和工具链对比，适合了解生态变化。
- [ ] [Cole Medin YouTube](https://www.youtube.com/@ColeMedin)：偏实践，常覆盖 n8n、LangGraph、MCP、OpenAI Agents SDK 等端到端 Agent 构建。

### 经典论文与文章

- [ ] [Attention Is All You Need](https://arxiv.org/abs/1706.03762)：Transformer 基础。
- [ ] [Chain-of-Thought Prompting Elicits Reasoning in Large Language Models](https://arxiv.org/abs/2201.11903)：理解推理提示的来源。
- [ ] [ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629)：Agent “思考 + 行动 + 观察”模式的经典论文。
- [ ] [Toolformer](https://arxiv.org/abs/2302.04761)：理解模型如何学习使用工具。
- [ ] [Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://arxiv.org/abs/2005.11401)：RAG 基础论文。
- [ ] [Reflexion](https://arxiv.org/abs/2303.11366)：理解反思、自我反馈和多步任务改进。
- [ ] [Generative Agents: Interactive Simulacra of Human Behavior](https://arxiv.org/abs/2304.03442)：理解记忆、规划、反思如何构成更长期的 Agent 行为。
- [ ] [Voyager](https://arxiv.org/abs/2305.16291)：理解开放环境中技能库、探索和自我改进。
- [ ] [SWE-agent](https://arxiv.org/abs/2405.15793)：理解软件工程 Agent 如何处理 GitHub issue。
- [ ] [OpenHands: An Open Platform for AI Software Developers as Generalist Agents](https://arxiv.org/abs/2407.16741)：理解代码 Agent 的平台化设计。

### 代码实践资源

- [ ] [openai/openai-cookbook](https://github.com/openai/openai-cookbook)：OpenAI API、RAG、工具调用、评测、Agent 示例。
- [ ] [openai/openai-agents-python](https://github.com/openai/openai-agents-python)：Agents SDK 官方 Python 实现与 examples。
- [ ] [langchain-ai/langgraph](https://github.com/langchain-ai/langgraph)：状态图、checkpoint、多 Agent、人机协作示例。
- [ ] [run-llama/llama_index](https://github.com/run-llama/llama_index)：RAG、数据连接、Agentic RAG 示例。
- [ ] [microsoft/autogen](https://github.com/microsoft/autogen)：多 Agent 对话、协作和 AutoGen Studio。
- [ ] [crewAIInc/crewAI](https://github.com/crewAIInc/crewAI)：角色化 Agent 编排框架。
- [ ] [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers)：MCP server 参考实现。
- [ ] [browser-use/browser-use](https://github.com/browser-use/browser-use)：浏览器自动化 Agent，适合研究 web agent 如何观察页面并执行动作。
- [ ] [OpenHands/OpenHands](https://github.com/OpenHands/OpenHands)：开源软件工程 Agent 平台，适合研究代码 Agent、沙箱、事件流和执行环境。
- [ ] [Significant-Gravitas/AutoGPT](https://github.com/Significant-Gravitas/AutoGPT)：早期自主 Agent 项目，适合了解 Agent 生态演化，但学习时要重点看设计问题而不是照搬架构。

### 建议阅读顺序

1. 第 1 周：Karpathy LLM 视频 + OpenAI API 文档。
2. 第 2 周：OpenAI Cookbook 的 structured outputs、tool calling 示例。
3. 第 3 周：LlamaIndex 文档 + RAG 论文 + 一个 RAG demo。
4. 第 4-5 周：ReAct 论文 + 手写 Agent Loop + OpenAI Agents SDK examples。
5. 第 6 周：DeepLearning.AI LangGraph 课程 + LangGraph examples。
6. 第 7 周：MCP 官方文档 + MCP servers 示例。
7. 第 8-9 周：OpenHands、browser-use、AutoGen、CrewAI 选 1-2 个读源码，不要一次全啃。
8. 第 10-12 周：围绕你的综合项目，只查能解决当前问题的资料。

## 15. 面向就业/转岗的作品集建议

最终至少完成 2 个项目：

- [ ] 一个 RAG 项目：证明你能处理数据、检索、引用和回答质量。
- [ ] 一个 Agent 项目：证明你能处理工具调用、多步任务、状态、日志和安全边界。

每个项目 README 至少包含：

- [ ] 项目背景。
- [ ] 架构图。
- [ ] 技术栈。
- [ ] 核心流程。
- [ ] 如何运行。
- [ ] Demo 截图或视频。
- [ ] 评测结果。
- [ ] 已知限制。
- [ ] 后续优化方向。

## 16. 每周复盘模板

```md
## 本周学习内容

- 

## 本周完成的代码

- 

## 我真正理解的概念

- 

## 仍然模糊的问题

- 

## 下周计划

- 
```

## 17. 判断自己是否入门

如果你能独立回答下面问题，基本说明已经进入 Agent 方向的大门：

- [ ] 什么时候应该用 Agent，什么时候普通 workflow 就够了？
- [ ] Tool Calling 和 MCP 分别解决什么问题？
- [ ] RAG 失败通常有哪些原因？
- [ ] Agent 为什么需要 tracing？
- [ ] 如何避免 Agent 无限循环或执行危险操作？
- [ ] 多 Agent 是刚需，还是复杂度陷阱？
- [ ] 如何评测一个 Agent 的效果？
- [ ] 如何把一个 Demo 变成可上线的 Agent 服务？

## 18. 当前前沿趋势总结

- Agent 正从“聊天机器人”走向“可使用工具的工作流系统”。
- 单纯追求全自动并不可靠，真实生产系统更强调可控、可观测、可恢复。
- MCP 正在成为 Agent 连接外部工具和数据源的重要协议。
- RAG 仍是企业知识库和私有数据场景的核心能力。
- LangGraph 这类有状态图工作流适合复杂任务编排。
- Agents SDK 这类框架强调工具、handoff、guardrail 和 tracing 的一体化。
- 评测、安全和权限控制会越来越重要，甚至比“模型会不会回答”更决定项目能否上线。

## 19. 建议的第一个项目

项目名：`repo-agent`

目标：做一个能理解本地代码仓库的 Agent。

### 功能清单

- [ ] 扫描项目目录。
- [ ] 根据问题搜索相关代码。
- [ ] 总结文件职责。
- [ ] 回答“某个功能在哪里实现”。
- [ ] 给出修改建议。
- [ ] 生成 patch 草案。
- [ ] 运行测试命令。
- [ ] 总结测试失败原因。
- [ ] 所有文件修改前需要人工确认。

### 技术栈建议

- [ ] Python + FastAPI，或者 TypeScript + Node.js。
- [ ] OpenAI/Anthropic 等模型 API。
- [ ] 向量数据库可先用 Chroma、FAISS 或 SQLite 扩展。
- [ ] Agent 框架可先手写，再迁移到 LangGraph 或 Agents SDK。
- [ ] 前端可用 React + Vite 做一个简单界面。

### 验收标准

- [ ] 能在任意小型 GitHub 项目中回答代码问题。
- [ ] 回答必须引用文件路径。
- [ ] 修改建议必须说明风险。
- [ ] 工具调用有日志。
- [ ] 至少有 10 条测试任务。
