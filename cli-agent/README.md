# CLI Agent

一个面向 AI Agent 学习路线的中文命令行助手。安装后可以通过 `agent` 命令唤醒。

## 安装

在仓库根目录运行：

```bash
python3 -m pip install -e ./cli-agent
```

## 配置

默认使用 DeepSeek 的 OpenAI 兼容 API：

```bash
export DEEPSEEK_API_KEY="你的_deepseek_key"
```

也可以使用通用配置：

```bash
export AGENT_API_KEY="你的_key"
export AGENT_BASE_URL="https://api.deepseek.com"
export AGENT_MODEL="deepseek-v4-flash"
```

如果要使用 OpenAI 官方 API：

```bash
export OPENAI_API_KEY="你的_openai_key"
export AGENT_PROVIDER="openai"
export AGENT_MODEL="gpt-4.1-mini"
```

## 使用

进入交互模式：

```bash
agent
```

单次提问：

```bash
agent "请解释什么是 RAG"
```

指定模式：

```bash
agent --mode compare "RAG 和 Tool Calling"
agent --mode quiz "OpenAI Agents SDK"
```

查看配置来源：

```bash
agent --show-config
```
