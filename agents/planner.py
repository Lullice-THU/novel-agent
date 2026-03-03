#!/usr/bin/env python3
"""
Planner Agent - 策划师
负责世界观设计、故事大纲、人物设定
"""

import os
import json
from typing import Dict, Optional


class PlannerAgent:
    """策划师Agent - 负责故事世界观和大纲"""
    
    def __init__(self, model: str = "claude"):
        self.model = model
        self.api_key = os.environ.get("OPENAI_API_KEY") or os.environ.get("DEEPSEEK_API_KEY")
        self.base_url = os.environ.get("API_BASE") or os.environ.get("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
    
    def generate_outline(
        self,
        genre: str,
        title: str,
        synopsis: str,
        style: str = "",
        target_length: str = "中篇"
    ) -> Dict:
        """
        生成完整大纲
        
        Args:
            genre: 小说类型
            title: 书名
            synopsis: 一句话简介
            style: 风格偏好
            target_length: 目标篇幅
        
        Returns:
            包含世界观、人物、大纲的字典
        """
        
        # 网文类型对应的经典模式
        genre_templates = {
            "都市": {
                "world": "现代都市，存在隐藏的豪门世家、武道传承、神秘组织",
                "golden_finger": "系统/神豪/鉴宝/医武传承",
                "protagonist_style": "屌丝逆袭/豪门弃子/上门女婿",
            },
            "玄幻": {
                "world": "灵气复苏的修仙世界，宗门林立，法则为尊",
                "golden_finger": "血脉传承/老爷爷/神级悟性/戒指空间",
                "protagonist_style": "废柴崛起/家族弃子/穿越者",
            },
            "系统": {
                "world": "现代都市+系统空间",
                "golden_finger": "神级系统(签到/任务/抽奖/商城)",
                "protagonist_style": "普通青年获得系统后逆袭",
            },
            "仙侠": {
                "world": "修仙世界，灵气稀薄，宗门为王",
                "golden_finger": "仙府传承/灵根变异/功法变异",
                "protagonist_style": "散修崛起/宗门弟子/魔道枭雄",
            },
            "穿越": {
                "world": "古代/异界+现代知识",
                "golden_finger": "现代知识/信息差/跨时代认知",
                "protagonist_style": "魂穿/身穿/胎穿",
            },
        }
        
        # 获取对应模板或使用默认
        template = genre_templates.get(genre, genre_templates["都市"])
        
        # 生成详细大纲
        length_map = {
            "短篇": "10-20章，每章2000-3000字",
            "中篇": "50-100章，每章3000-5000字",
            "长篇": "200+章，每章3000-5000字",
        }
        
        outline = {
            "title": title,
            "genre": genre,
            "synopsis": synopsis,
            "target_length": length_map.get(target_length, length_map["中篇"]),
            
            # 世界观设定
            "world_setting": template["world"],
            "golden_finger": template["golden_finger"],
            "power_system": self._get_power_system(genre),
            
            # 人物设定
            "protagonist": self._generate_protagonist(genre, synopsis),
            "antagonist": self._generate_antagonist(genre),
            "supporting_chars": self._generate_supporting(genre),
            
            # 核心冲突
            "main_conflict": f"{synopsis} -> 主角通过{template['golden_finger']}逐步成长",
            "story_arcs": self._generate_arcs(genre, target_length),
            
            # 章节大纲
            "chapters": self._generate_chapters(genre, title, target_length),
            
            # 爽点设计
            "爽点设计": self._get爽点(genre),
        }
        
        return outline
    
    def _get_power_system(self, genre: str) -> str:
        """获取修炼体系"""
        systems = {
            "都市": "金钱+武力+人脉三重标准",
            "玄幻": "灵气等级: 练气->筑基->金丹->元婴->化神->渡劫",
            "系统": "系统积分+任务成就+商城兑换",
            "仙侠": "灵根资质+功法等级+法宝强弱",
            "穿越": "现代知识+武技+智慧",
        }
        return systems.get(genre, systems["都市"])
    
    def _generate_protagonist(self, genre: str, synopsis: str) -> Dict:
        """生成主角设定"""
        names = {
            "都市": ["陈北", "林天", "叶凡", "楚风", "苏铭"],
            "玄幻": ["叶尘", "秦风", "萧炎", "林动", "牧尘"],
            "系统": ["张伟", "王磊", "李阳", "赵强", "刘洋"],
            "仙侠": ["云飞", "羽化", "道一", "无极", "太初"],
        }
        
        import random
        name = random.choice(names.get(genre, names["都市"]))
        
        return {
            "name": name,
            "gender": "男",
            "age": "25左右",
            "background": "普通出身/屌丝/废柴",
            "personality": "沉稳内敛 / 阳光热血 / 腹黑低调",
            "initial_state": "社会底层/被人歧视/意外获得机遇",
        }
    
    def _generate_antagonist(self, genre: str) -> Dict:
        """生成反派设定"""
        return {
            "类型": "富二代/世家子弟/宗门天骄/竞争对手",
            "特点": "仗势欺人/目中无人/阴险狡诈",
            "冲突点": "与主角争夺资源/面子/女人",
        }
    
    def _generate_supporting(self, genre: str) -> list:
        """生成配角设定"""
        return [
            {"角色": "红颜知己", "功能": "情感线/帮助主角", "特点": "温柔漂亮/背景深厚"},
            {"角色": "兄弟/帮手", "功能": "并肩作战", "特点": "忠诚可靠/各有特长"},
            {"角色": "师父/前辈", "功能": "金手指指引", "特点": "神秘强大/亦师亦友"},
        ]
    
    def _generate_arcs(self, genre: str, target_length: str) -> list:
        """生成故事大纲"""
        arc_count = {"短篇": 3, "中篇": 5, "长篇": 8}.get(target_length, 5)
        
        arcs = []
        for i in range(arc_count):
            arcs.append({
                "阶段": f"第{i+1}幕",
                "目标": f"解决{['小boss', '中等挑战', '核心敌人'][i % 3]}",
                "爽点": f"主角突破/打脸反派/获得宝藏",
            })
        
        return arcs
    
    def _generate_chapters(self, genre: str, title: str, target_length: str) -> list:
        """生成章节大纲"""
        chapter_count = {"短篇": 15, "中篇": 50, "长篇": 100}.get(target_length, 50)
        
        chapters = []
        chapter_templates = [
            ("获得金手指", "主角意外获得系统/传承/宝物"),
            ("初次装逼", "小试牛刀，获得关注"),
            ("实力提升", "通过努力或悟性变强"),
            ("打脸反派", "当众羞辱对手"),
            ("英雄救美", "结识重要女性角色"),
            ("获得资源", "发现宝藏/获得机缘"),
            ("势力扩张", "建立自己的班底"),
            ("越级挑战", "以弱胜强，大杀四方"),
        ]
        
        import random
        for i in range(chapter_count):
            template = chapter_templates[i % len(chapter_templates)]
            chapters.append({
                "chapter_num": i + 1,
                "title": f"第{i+1}章 {template[0]}",
                "summary": template[1],
                "爽点": template[0],
            })
        
        return chapters
    
    def _get爽点(self, genre: str) -> list:
        """获取爽点设计"""
        common_爽点 = [
            "打脸反转 - 前期被打压，后期强势反击",
            "金手指 - 获得特殊能力或系统",
            "红颜环绕 - 多个美女主动靠近",
            "兄弟义气 - 关键时刻有人帮忙",
            "装逼成功 - 当众展示实力",
            "敌人后悔 - 反派求饶或后悔",
            "实力突破 - 境界提升",
            "获得宝物 - 仙草/功法/法宝",
        ]
        
        return common_爽点
