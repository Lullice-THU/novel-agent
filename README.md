# NovelAgent - 工业级AI网文创作系统

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue?style=flat-square" alt="Python">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/DeepSeek-V3-FF6B6B?style=flat-square" alt="Model">
</p>

> ⚡ 真正接入LLM的多Agent协作网文创作系统 | 参考星月写作模式 | 工业化质量

## 🎯 项目定位

**不只是简单的脚本，而是一套完整的AI创作解决方案。**

```
┌─────────────────────────────────────────────────────────────────────┐
│                        NovelAgent 架构                               │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐       │
│  │   Planner    │    │   Writer     │    │   Editor     │       │
│  │   策划师      │───▶│   作家       │───▶│   审核        │       │
│  │              │    │              │    │              │       │
│  │ • 世界观     │    │ • 章节扩写   │    │ • 爽点检测   │       │
│  │ • 大纲设计   │    │ • 对话生成   │    │ • 节奏把控   │       │
│  │ • 人物设定   │    │ • 场景描写   │    │ • 质量把关   │       │
│  └──────────────┘    └──────────────┘    └──────────────┘       │
│                                                                      │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │                    LLM Layer (DeepSeek V3)                  │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

## ✨ 核心特性

| 特性 | 说明 |
|------|------|
| 🤖 **真LLM接入** | 接入DeepSeek V3 API，非简单模板 |
| 👥 **多Agent协作** | 策划→写作→审核，完整流程 |
| 🎯 **爽点系统** | 内置网文爽点模式库 |
| 📊 **质量审核** | 自动检测爽点密度、节奏、逻辑 |
| 🔄 **迭代优化** | 审核→修改→再审核闭环 |
| 📖 **多题材支持** | 都市/玄幻/系统/仙侠/穿越 |

## 🚀 快速开始

### 安装

```bash
git clone https://github.com/Lullice-THU/novel-agent.git
cd novel-agent
pip install -r requirements.txt
```

### 配置API

```bash
# 方式1: 环境变量
export DEEPSEEK_API_KEY="your-api-key"

# 方式2: 命令行
python novel_agent_core.py --api-key "your-api-key" ...
```

### 使用

```bash
# 命令行模式
python novel_agent_core.py \
  --genre 都市 \
  --title 超级赘婿 \
  --synopsis "上门女婿逆袭成首富" \
  --chapters 5

# 输出
# [16:30:00] 正在生成大纲...
# [16:30:05] 正在写作第1章...
# [16:30:15] 正在审核第1章...
# ✅ 已保存: output/第1章_第一章.txt
```

## 📁 项目结构

```
novel-agent/
├── novel_agent_core.py   # 核心引擎 (LLM接入版)
├── agents/              # Agent模块 (模板版)
├── prompts/             # 提示词库
│   └── 爽点系统.md     # 🎯 核心爽点模式库
├── main.py              # CLI入口
├── requirements.txt     # 依赖
└── README.md
```

## 🎯 核心优势

### 1. 工业级Prompt工程

```python
# 策划师System Prompt示例
SYSTEM_PROMPT = """你是一位资深网文策划大师，精通各类网文套路和爽点设计。

【擅长类型】
- 都市爽文（神豪，系统、鉴宝、医武）
- 玄幻修仙（血脉、功法、宗门、异火）
...

【输出格式】
请严格按照JSON格式输出...
"""
```

### 2. 爽点系统库

内置6大类、30+小类网文爽点模式：

- ✅ 打脸反转
- ✅ 英雄救美
- ✅ 获得奇遇
- ✅ 越级挑战
- ✅ 身份打脸
- ✅ 系统任务

### 3. 质量闭环

```
写作 → 审核 → 问题反馈 → 改写 → 再次审核 → 通过
```

## 📊 效果示例

### 输入

```
类型: 都市
书名: 超级赘婿
简介: 上门女婿逆袭成首富
```

### 输出 (第1章大纲)

```json
{
  "title": "第一章 雨夜转折",
  "summary": "主角在雨夜被丈母娘赶出家门，意外获得神豪系统",
  "key_points": [
    "雨夜被羞辱场景",
    "系统激活",
    "获得启动资金",
    "丈母娘态度转变"
  ],
  "爽点": ["身份打脸", "系统奖励", "反转"]
}
```

## 🔧 自定义配置

### 修改LLM配置

```python
from novel_agent_core import LLMConfig, LLMWrapper, ModelProvider

config = LLMConfig(
    provider=ModelProvider.DEEPSEEK,
    api_key="your-key",
    base_url="https://api.deepseek.com",
    model="deepseek-chat",
    temperature=0.8,
    max_tokens=4096,
)

llm = LLMWrapper(config)
```

### 添加新题材

```python
# 在 prompts/爽点系统.md 中添加
STYLE_PROMPTS["新题材"] = "你的风格提示词"
```

## 📈 变现思路

1. **小说发布** - 起点/番茄/七猫赚稿费
2. **教程变现** - 出售"AI网文写作"课程
3. **代写服务** - 专业代写小说
4. **工具SaaS** - 打包成在线工具

## 📋 要求

- Python 3.8+
- DeepSeek API Key / OpenAI API Key
- 网络访问 (API调用)

## 🤝 贡献

欢迎提交PR！

## 📄 License

MIT License

---

<p align="center">
  Made with ❤️ by NovelAgent
</p>
