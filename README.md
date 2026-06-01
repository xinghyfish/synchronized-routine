# synchronized-routine

从学校毕业快一年了，在一个相对安逸的环境中从事着古老的技术，直到某次人事调动，才惊觉同步前沿技术的必要性。也逐渐明白了，未来唯一不变的就是变化本身。拥抱变化才是常态。保持一颗学徒的心态，多元化扩展职业以及职业之外的路线。因此创立这个仓库，用来记录这个过程中的学习内容和笔记。

## CLI Agent

`cli-agent/` 是一个中文命令行 AI Agent 学习助手。安装后可以通过 `agent` 命令唤醒：

```bash
python3 -m pip install -e ./cli-agent
export DEEPSEEK_API_KEY="你的_deepseek_key"
agent
```

也支持单次提问：

```bash
agent "请解释什么是 RAG"
agent --mode compare "RAG 和 Tool Calling"
```
