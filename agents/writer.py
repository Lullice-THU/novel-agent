#!/usr/bin/env python3
"""
Writer Agent - 作家
负责章节内容创作
"""

import os
import random
from typing import Dict, List


class WriterAgent:
    """作家Agent - 负责具体章节内容"""
    
    def __init__(self):
        self.model = os.environ.get("WRITER_MODEL", "deepseek")
    
    def write_chapter(
        self,
        outline: Dict,
        chapter_outline: Dict,
        genre: str = "都市"
    ) -> str:
        """
        写作单个章节
        
        Args:
            outline: 故事大纲
            chapter_outline: 章节大纲
            genre: 小说类型
        
        Returns:
            章节内容 (str)
        """
        
        chapter_num = chapter_outline.get("chapter_num", 1)
        chapter_title = chapter_outline.get("title", f"第{chapter_num}章")
        summary = chapter_outline.get("summary", "")
        爽点 = chapter_outline.get("爽点", "")
        
        protagonist = outline.get("protagonist", {})
        protagonist_name = protagonist.get("name", "主角")
        
        golden_finger = outline.get("golden_finger", "金手指")
        world_setting = outline.get("world_setting", "都市")
        
        # 生成章节内容
        content = self._generate_chapter_content(
            chapter_num=chapter_num,
            chapter_title=chapter_title,
            summary=summary,
            爽点=爽点,
            protagonist_name=protagonist_name,
            golden_finger=golden_finger,
            world_setting=world_setting,
            genre=genre
        )
        
        return content
    
    def _generate_chapter_content(
        self,
        chapter_num: int,
        chapter_title: str,
        summary: str,
        爽点: str,
        protagonist_name: str,
        golden_finger: str,
        world_setting: str,
        genre: str
    ) -> str:
        """生成章节正文"""
        
        # 开篇句式
        opening_templates = {
            "都市": [
                f"雨夜，{protagonist_name}站在CBD写字楼门口，雨水顺着他的脸颊滑落。",
                f"这一天，对{protagonist_name}来说，是命运的转折点。",
                f"看着手机里那个羞辱的订单，{protagonist_name}咬紧了牙关。",
            ],
            "玄幻": [
                f"灵气翻涌，{protagonist_name}感受着体内蓬勃的力量。",
                f"神秘空间中，{protagonist_name}缓缓睁开了眼睛。",
                f"丹田之内，那枚金色金丹正在疯狂旋转。",
            ],
            "系统": [
                f"【叮！系统激活成功】机械般的声音在{protagonist_name}脑海中响起。",
                f"看着手机屏幕上突然出现的金色图标，{protagonist_name}愣住了。",
                f"「恭喜宿主完成首单，获得神秘大礼包！」",
            ],
        }
        
        # 中间过渡
        transition_templates = [
            "然而就在这时，意外发生了。",
            "谁也没有想到，事情会发展到这个地步。",
            "就在这时，一道声音在他身后响起。",
            "突然出现的变故，让所有人都措手不及。",
        ]
        
        # 爽点高潮
        climax_templates = {
            "打脸反转": f"「不可能！」对面的人脸色瞬间惨白，\"{protagonist_name}，你到底是什么人？\"",
            "金手指": f"【恭喜宿主，{golden_finger}已激活】系统的声音让{protagonist_name}心中大定。",
            "装逼成功": "众人看向{protagonist_name}的眼神彻底变了",
            "实力突破": f"一股恐怖的气息从{protagonist_name}身上爆发",
            "获得宝物": f"看着手中的宝物，{protagonist_name}露出了笑容",
        }
        
        # 结尾句式
        ending_templates = [
            "这一切，才刚刚开始。",
            "他的嘴角微微上扬，露出一抹神秘的微笑。",
            "属于他的时代，即将来临。",
            "接下来会发生什么，连他自己都不知道。",
        ]
        
        # 组装内容
        content_parts = []
        
        # 标题
        content_parts.append(f"\n\n# {chapter_title}\n\n")
        
        # 开篇
        openings = opening_templates.get(genre, opening_templates["都市"])
        content_parts.append(random.choice(openings))
        
        # 情节展开
        content_parts.append(f"\n{summary}。")
        
        # 插入爽点
        if 爽点 in climax_templates:
            content_parts.append(f"\n\n{climax_templates[爽点]}\n")
        else:
            content_parts.append(f"\n\n{random.choice(list(climax_templates.values()))}\n")
        
        # 过渡
        content_parts.append(f"\n{random.choice(transition_templates)}\n")
        
        # 结尾
        content_parts.append(f"\n{random.choice(ending_templates)}\n")
        
        # 计算字数 (中文约2字/词)
        word_count = len("".join(content_parts)) * 2  # 粗略估算
        content_parts.append(f"\n\n--- ({word_count}字) ---\n")
        
        return "".join(content_parts)
    
    def write_scene(self, scene_type: str, context: Dict) -> str:
        """
        写作特定场景
        
        Args:
            scene_type: 场景类型 (fight/romance/mystery/etc)
            context: 上下文信息
        
        Returns:
            场景描写文字
        """
        
        scene_templates = {
            "fight": [
                "拳风呼啸，两人瞬间战在一起。",
                "恐怖的能量波动，让周围的空间都为之颤抖。",
                "一道身影倒飞而出，重重摔在地上。",
            ],
            "romance": [
                "四目相对，时间仿佛在这一刻静止。",
                "她的眼神中闪过一丝异样的光芒。",
                "气氛变得微妙起来。",
            ],
            "mystery": [
                "这一切的背后，似乎隐藏着某个秘密。",
                "一道神秘的身影，在黑暗中若隐若现。",
                "真相，似乎越来越近了。",
            ],
        }
        
        templates = scene_templates.get(scene_type, scene_templates["fight"])
        return random.choice(templates)
    
    def improve_writing(self, content: str, focus: str = "爽点") -> str:
        """
        润色内容
        
        Args:
            content: 原始内容
            focus: 润色重点 (爽点/文笔/节奏)
        
        Returns:
            润色后的内容
        """
        # 实际应该调用LLM API进行润色
        # 这里返回原内容作为占位
        return content
    
    def expand_outline(self, outline: str, target_words: int = 3000) -> str:
        """
        扩写细纲
        
        Args:
            outline: 简单大纲
            target_words: 目标字数
        
        Returns:
            扩写后的内容
        """
        # 实际应该调用LLM API进行扩写
        return f"{outline}\n\n" + "这里应该有3000字的详细内容...\n" * 10
