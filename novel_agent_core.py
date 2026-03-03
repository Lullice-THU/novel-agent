#!/usr/bin/env python3
"""
NovelAgent Core - 真正的多Agent协作网文创作系统
接入DeepSeek V3 API，实现完整的人机协作写作流程
"""

import os
import json
import time
import requests
from typing import Dict, List, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum
import re


class ModelProvider(Enum):
    DEEPSEEK = "deepseek"
    OPENAI = "openai"
    ANTHROPIC = "anthropic"


@dataclass
class LLMConfig:
    """LLM配置"""
    provider: ModelProvider = ModelProvider.DEEPSEEK
    api_key: str = ""
    base_url: str = "https://api.deepseek.com"
    model: str = "deepseek-chat"
    temperature: float = 0.7
    max_tokens: int = 4096


@dataclass
class ChapterContent:
    """章节内容"""
    chapter_num: int
    title: str
    outline: str
    content: str = ""
    word_count: int = 0
    爽点: List[str] = field(default_factory=list)
    quality_score: float = 0.0
    revision_notes: List[str] = field(default_factory=list)


class LLMWrapper:
    """LLM API封装"""
    
    def __init__(self, config: LLMConfig):
        self.config = config
    
    def chat(
        self,
        messages: List[Dict[str, str]],
        system_prompt: str = "",
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> str:
        """调用LLM API"""
        
        # 构建消息
        full_messages = []
        if system_prompt:
            full_messages.append({"role": "system", "content": system_prompt})
        full_messages.extend(messages)
        
        # 根据provider选择调用方式
        if self.config.provider == ModelProvider.DEEPSEEK:
            return self._call_deepseek(full_messages, temperature, max_tokens)
        elif self.config.provider == ModelProvider.OPENAI:
            return self._call_openai(full_messages, temperature, max_tokens)
        else:
            raise ValueError(f"Unsupported provider: {self.config.provider}")
    
    def _call_deepseek(
        self,
        messages: List[Dict[str, str]],
        temperature: Optional[float],
        max_tokens: Optional[int],
    ) -> str:
        """调用DeepSeek API"""
        url = f"{self.config.base_url}/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.config.api_key}",
            "Content-Type": "application/json",
        }
        
        payload = {
            "model": self.config.model,
            "messages": messages,
            "temperature": temperature or self.config.temperature,
            "max_tokens": max_tokens or self.config.max_tokens,
            "stream": False,
        }
        
        response = requests.post(url, headers=headers, json=payload, timeout=120)
        response.raise_for_status()
        
        result = response.json()
        return result["choices"][0]["message"]["content"]
    
    def _call_openai(
        self,
        messages: List[Dict[str, str]],
        temperature: Optional[float],
        max_tokens: Optional[int],
    ) -> str:
        """调用OpenAI API"""
        url = f"{self.config.base_url}/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.config.api_key}",
            "Content-Type": "application/json",
        }
        
        payload = {
            "model": self.config.model,
            "messages": messages,
            "temperature": temperature or self.config.temperature,
            "max_tokens": max_tokens or self.config.max_tokens,
        }
        
        response = requests.post(url, headers=headers, json=payload, timeout=120)
        response.raise_for_status()
        
        result = response.json()
        return result["choices"][0]["message"]["content"]


class PlannerAgent:
    """策划师Agent - 负责世界观、大纲、人物设定"""
    
    SYSTEM_PROMPT = """你是一位资深网文策划大师，精通各类网文套路和爽点设计。
你的任务是帮助用户设计引人入胜的故事大纲。

【擅长类型】
- 都市爽文（神豪、系统、鉴宝、医武）
- 玄幻修仙（血脉、功法、宗门、异火）
- 系统流（签到、任务、商城、抽奖）
- 穿越重生（魂穿、历史、异界）
- 悬疑推理（烧脑、惊悚、心理）

【核心能力】
1. 世界观设计：构建完整、可信、有吸引力的世界观
2. 人物塑造：设计有层次感的主角、配角、反派
3. 爽点规划：规划密集的爽点情节
4. 节奏把控：设计引人入胜的故事节奏

【输出格式】
请严格按照JSON格式输出，字段如下：
{
    "title": "书名",
    "genre": "类型",
    "synopsis": "一句话简介",
    "target_words": "目标字数",
    "world_setting": {
        "背景": "世界观背景描述",
        "法则": "力量体系/规则",
        "势力": "主要势力分布"
    },
    "protagonist": {
        "name": "主角名",
        "background": "出身背景",
        "personality": "性格特点",
        "golden_finger": "金手指/优势",
        "goal": "核心目标"
    },
    "antagonist": {
        "类型": "反派类型",
        "特点": "反派特点",
        "冲突点": "与主角的矛盾"
    },
    "supporting_chars": [
        {"角色": "角色名", "功能": "作用", "特点": "特点"}
    ],
    "main_arc": "主线剧情概述",
    "story_arcs": [
        {"阶段": "阶段名", "目标": "目标", "爽点": "爽点设计"}
    ],
    "chapters": [
        {"num": 1, "title": "章节名", "summary": "章节概要", "key_points": ["关键点1", "关键点2"]}
    ],
    "爽点设计": ["爽点1", "爽点2", "爽点3"]
}

注意：所有字段都用中文输出，chapters至少包含30章大纲。"""

    def __init__(self, llm: LLMWrapper):
        self.llm = llm
    
    def generate_outline(
        self,
        genre: str,
        title: str,
        synopsis: str,
        target_length: str = "长篇",
    ) -> Dict:
        """生成完整大纲"""
        
        user_message = f"""请为以下小说生成完整大纲：

类型：{genre}
书名：{title}
简介：{synopsis}
目标篇幅：{target_length}

请生成详细的世界观、人物设定、章节大纲。"""
        
        messages = [{"role": "user", "content": user_message}]
        
        response = self.llm.chat(
            messages=messages,
            system_prompt=self.SYSTEM_PROMPT,
            temperature=0.8,
            max_tokens=4096,
        )
        
        # 解析JSON
        try:
            # 尝试提取JSON
            json_match = re.search(r'\{[\s\S]*\}', response)
            if json_match:
                outline = json.loads(json_match.group())
                return outline
        except json.JSONDecodeError:
            pass
        
        # 如果解析失败，返回原始响应
        return {
            "title": title,
            "genre": genre,
            "synopsis": synopsis,
            "raw_response": response,
        }
    
    def expand_chapter_outline(self, chapter_summary: str, genre: str) -> Dict:
        """扩展章节细纲"""
        
        user_message = f"""请为以下章节概要扩展为详细的细纲：

章节概要：{chapter_summary}
类型：{genre}

请生成：
1. 章节标题
2. 本章核心爽点
3. 关键情节点（至少3个）
4. 过渡句/结尾悬念

用JSON格式输出。"""
        
        messages = [{"role": "user", "content": user_message}]
        
        response = self.llm.chat(
            messages=messages,
            system_prompt="你是一位网文大纲专家，擅长扩展章节细节。",
            temperature=0.7,
        )
        
        try:
            json_match = re.search(r'\{[\s\S]*\}', response)
            if json_match:
                return json.loads(json_match.group())
        except:
            pass
        
        return {"summary": chapter_summary, "raw": response}


class WriterAgent:
    """作家Agent - 负责章节内容创作"""
    
    SYSTEM_PROMPT = """你是一位顶级网文作家，擅长写各种类型的网络小说。

【写作风格】
- 节奏紧凑，冲突不断
- 爽点密集，张力十足
- 对话自然，描写生动
- 情绪到位，代入感强

【禁忌】
- 不要水文拖节奏
- 不要重复同样的套路
- 不要出现ai痕迹（机械、冰冷）
- 不要有逻辑漏洞

【技巧】
- 利用"先抑后扬"制造爽点
- 利用"悬念"吸引读者
- 利用"对比"强化冲突
- 利用"细节"增强代入感

【输出要求】
直接输出章节正文，不要有任何markdown格式标记。
每章3000-5000字。
开头要抓住读者，结尾要留悬念。
"""
    
    STYLE_PROMPTS = {
        "都市": "语言要现代都市感，对话接地气，有生活气息。",
        "玄幻": "语言要有古风仙侠感，描写要大气磅礴。",
        "系统": "可以加入系统提示音风格，增加趣味性。",
        "仙侠": "语言要有古典韵味，描写灵气飘逸。",
        "穿越": "现代思维与古代/异界碰撞，制造反差。",
    }

    def __init__(self, llm: LLMWrapper):
        self.llm = llm
    
    def write_chapter(
        self,
        chapter_outline: Dict,
        previous_summary: str,
        genre: str,
        chapter_num: int,
    ) -> str:
        """写作单个章节"""
        
        style_prompt = self.STYLE_PROMPTS.get(genre, "")
        
        user_message = f"""请创作第{chapter_num}章：

【章节大纲】
标题：{chapter_outline.get('title', '')}
概要：{chapter_outline.get('summary', '')}
关键点：{', '.join(chapter_outline.get('key_points', []))}
核心爽点：{chapter_outline.get('key_爽点', '')}

【前情提要】
{previous_summary}

【类型风格】
{style_prompt}

【要求】
1. 3000-5000字
2. 开头抓住读者，结尾留悬念
3. 爽点要到位，情绪要饱满
4. 不要水文，直入主题

直接输出正文。"""
        
        messages = [{"role": "user", "content": user_message}]
        
        response = self.llm.chat(
            messages=messages,
            system_prompt=self.SYSTEM_PROMPT,
            temperature=0.85,  # 稍高温度增加创意
            max_tokens=4096,
        )
        
        return response
    
    def rewrite_section(
        self,
        content: str,
        instructions: str,
    ) -> str:
        """重写指定段落"""
        
        user_message = f"""请根据以下要求重写这段内容：

【原文】
{content}

【要求】
{instructions}

直接输出重写后的内容，不要解释。"""
        
        messages = [{"role": "user", "content": user_message}]
        
        response = self.llm.chat(
            messages=messages,
            system_prompt="你是一位网文润色专家，擅长让文字更具吸引力。",
            temperature=0.7,
        )
        
        return response


class EditorAgent:
    """审核Agent - 负责质量把控"""
    
    SYSTEM_PROMPT = """你是一位资深网文编辑，擅长审核和优化网文内容。

【审核标准】
1. 爽点密度：每1000字至少2个爽点
2. 节奏：章节要有冲突、有推进，不能水文
3. 逻辑：情节要合理，不能有bug
4. 情绪：要有情绪波动，不能平铺直叙
5. 代入感：细节要到位

【问题类型】
- 节奏拖沓
- 爽点不足
- 逻辑漏洞
- 重复套路
- 情绪平淡
- 描写空洞

【输出格式】
JSON格式：
{{
    "score": 85,
    "issues": [
        {{"type": "问题类型", "location": "位置", "description": "描述", "severity": "high/medium/low"}}
    ],
    "strengths": ["优点1", "优点2"],
    "suggestions": ["修改建议1", "修改建议2"],
    "revision_required": true/false,
    "revision_prompt": "如果需要修改，给出具体的修改提示"
}}
"""

    def __init__(self, llm: LLMWrapper):
        self.llm = llm
    
    def review_chapter(self, content: str, chapter_outline: Dict) -> Dict:
        """审核章节"""
        
        user_message = f"""请审核以下章节：

【章节大纲】
标题：{chapter_outline.get('title', '')}
期望爽点：{chapter_outline.get('key_爽点', '')}

【章节内容】
{content[:5000]}  # 只传前5000字

请给出详细的审核报告。"""
        
        messages = [{"role": "user", "content": user_message}]
        
        response = self.llm.chat(
            messages=messages,
            system_prompt=self.SYSTEM_PROMPT,
            temperature=0.3,  # 低温度保持客观
            max_tokens=2048,
        )
        
        try:
            json_match = re.search(r'\{[\s\S]*\}', response)
            if json_match:
                return json.loads(json_match.group())
        except:
            pass
        
        return {
            "score": 70,
            "raw_response": response,
            "revision_required": False,
        }
    
    def generate_revision_prompt(
        self,
        issues: List[Dict],
        content: str,
    ) -> str:
        """生成修改提示"""
        
        issues_text = "\n".join([
            f"- {i.get('type')}: {i.get('description')}"
            for i in issues
        ])
        
        user_message = f"""请根据以下审核问题，生成修改提示：

【审核问题】
{issues_text}

【原文】
{content[:3000]}

请生成具体的修改提示。"""
        
        messages = [{"role": "user", "content": user_message}]
        
        response = self.llm.chat(
            messages=messages,
            system_prompt="你是一位网文编辑，擅长给出具体的修改指导。",
            temperature=0.5,
        )
        
        return response


class NovelAgent:
    """NovelAgent主类 - 协调多Agent协作"""
    
    def __init__(self, llm_config: Optional[LLMWrapper] = None):
        if llm_config:
            self.llm = llm_config
        else:
            # 从环境变量初始化
            api_key = os.environ.get("DEEPSEEK_API_KEY") or os.environ.get("OPENAI_API_KEY", "")
            base_url = os.environ.get("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
            model = os.environ.get("LLM_MODEL", "deepseek-chat")
            
            config = LLMConfig(
                provider=ModelProvider.DEEPSEEK if "deepseek" in base_url else ModelProvider.OPENAI,
                api_key=api_key,
                base_url=base_url,
                model=model,
            )
            self.llm = LLMWrapper(config)
        
        # 初始化Agent团队
        self.planner = PlannerAgent(self.llm)
        self.writer = WriterAgent(self.llm)
        self.editor = EditorAgent(self.llm)
    
    def create_novel(
        self,
        genre: str,
        title: str,
        synopsis: str,
        target_length: str = "长篇",
        num_chapters: int = 10,
        auto_review: bool = True,
        progress_callback: Optional[Callable] = None,
    ) -> List[ChapterContent]:
        """
        创建小说
        
        Args:
            genre: 小说类型
            title: 书名
            synopsis: 一句话简介
            target_length: 目标篇幅
            num_chapters: 写作章节数
            auto_review: 是否自动审核
            progress_callback: 进度回调函数
        
        Returns:
            章节内容列表
        """
        
        chapters = []
        previous_summary = "无（这是第一章）"
        
        # 1. 生成大纲
        if progress_callback:
            progress_callback("正在生成大纲...")
        
        outline = self.planner.generate_outline(genre, title, synopsis, target_length)
        
        # 2. 逐章写作
        for i in range(num_chapters):
            if progress_callback:
                progress_callback(f"正在写作第{i+1}章...")
            
            # 获取章节大纲
            chapter_outline_data = outline.get("chapters", [])[i] if outline.get("chapters") else {}
            
            # 写作
            content = self.writer.write_chapter(
                chapter_outline={
                    "title": chapter_outline_data.get("title", f"第{i+1}章"),
                    "summary": chapter_outline_data.get("summary", ""),
                    "key_points": chapter_outline_data.get("key_points", []),
                    "key_爽点": chapter_outline_data.get("爽点", ""),
                },
                previous_summary=previous_summary,
                genre=genre,
                chapter_num=i+1,
            )
            
            # 审核
            review_result = {}
            if auto_review:
                if progress_callback:
                    progress_callback(f"正在审核第{i+1}章...")
                review_result = self.editor.review_chapter(content, chapter_outline_data)
            
            # 创建章节对象
            chapter = ChapterContent(
                chapter_num=i+1,
                title=chapter_outline_data.get("title", f"第{i+1}章"),
                outline=chapter_outline_data.get("summary", ""),
                content=content,
                word_count=len(content),
                quality_score=review_result.get("score", 0),
                revision_notes=review_result.get("suggestions", []),
            )
            
            chapters.append(chapter)
            
            # 更新前情提要
            previous_summary = f"第{i+1}章: {chapter_outline_data.get('title', '')} - {chapter_outline_data.get('summary', '')}"
            
            # 避免API限流
            time.sleep(1)
        
        return chapters
    
    def write_single_chapter(
        self,
        chapter_outline: Dict,
        previous_summary: str,
        genre: str,
        chapter_num: int,
        auto_review: bool = True,
    ) -> ChapterContent:
        """写作单个章节"""
        
        # 写作
        content = self.writer.write_chapter(
            chapter_outline=chapter_outline,
            previous_summary=previous_summary,
            genre=genre,
            chapter_num=chapter_num,
        )
        
        # 审核
        review_result = {}
        if auto_review:
            review_result = self.editor.review_chapter(content, chapter_outline)
        
        return ChapterContent(
            chapter_num=chapter_num,
            title=chapter_outline.get("title", f"第{chapter_num}章"),
            outline=chapter_outline.get("summary", ""),
            content=content,
            word_count=len(content),
            quality_score=review_result.get("score", 0),
        )


def main():
    """CLI入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description="NovelAgent - AI网文创作系统")
    parser.add_argument("--genre", "-g", default="都市", help="小说类型")
    parser.add_argument("--title", "-t", required=True, help="书名")
    parser.add_argument("--synopsis", "-s", required=True, help="简介")
    parser.add_argument("--chapters", "-c", type=int, default=3, help="章节数")
    parser.add_argument("--api-key", help="API Key")
    parser.add_argument("--output", "-o", default="./output", help="输出目录")
    
    args = parser.parse_args()
    
    # 初始化
    config = LLMConfig(
        api_key=args.api_key or os.environ.get("DEEPSEEK_API_KEY", ""),
    )
    agent = NovelAgent(LLMWrapper(config))
    
    # 创作
    def progress(msg):
        print(f"[{time.strftime('%H:%M:%S')}] {msg}")
    
    chapters = agent.create_novel(
        genre=args.genre,
        title=args.title,
        synopsis=args.synopsis,
        num_chapters=args.chapters,
        progress_callback=progress,
    )
    
    # 保存
    os.makedirs(args.output, exist_ok=True)
    for ch in chapters:
        filename = f"{args.output}/第{ch.chapter_num}章_{ch.title}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"# {ch.title}\n\n")
            f.write(ch.content)
            f.write(f"\n\n--- 字数: {ch.word_count} ---\n")
        
        print(f"✅ 已保存: {filename}")
    
    print(f"\n🎉 完成！共创作 {len(chapters)} 章")


if __name__ == "__main__":
    main()
