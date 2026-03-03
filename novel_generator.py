#!/usr/bin/env python3
"""
NovelAgent Lite - 直接产出小说内容
基于规则引擎的网文生成器
"""

import random
import sys


class NovelGenerator:
    """小说生成器"""
    
    def __init__(self, genre: str, title: str, synopsis: str):
        self.genre = genre
        self.title = title
        self.synopsis = synopsis
        self.protagonist = self._generate_protagonist()
    
    def _generate_protagonist(self):
        names = {
            "都市": ["陈北", "林天", "叶凡", "楚风", "苏铭", "周毅", "赵磊"],
            "玄幻": ["叶尘", "秦风", "萧炎", "林动", "牧尘", "云飞", "羽化"],
            "系统": ["张伟", "王磊", "李阳", "刘洋", "陈凡"],
            "仙侠": ["云飞", "羽化", "道一", "无极", "太初", "逍遥"],
        }
        return {
            "name": random.choice(names.get(self.genre, names["都市"])),
            "age": random.randint(20, 28),
            "background": "普通出身",
        }
    
    def generate_chapter(self, chapter_num: int, chapter_theme: str) -> str:
        """生成单章"""
        
        if self.genre == "都市":
            return self._generate_urban_chapter(chapter_num, chapter_theme)
        elif self.genre == "玄幻":
            return self._generate_fantasy_chapter(chapter_num, chapter_theme)
        elif self.genre == "系统":
            return self._generate_system_chapter(chapter_num, chapter_theme)
        else:
            return self._generate_urban_chapter(chapter_num, chapter_theme)
    
    def _generate_urban_chapter(self, num: int, theme: str) -> str:
        """都市类型章节"""
        
        name = self.protagonist["name"]
        
        openings = [
            f"雨夜，{name}站在CBD写字楼门口，雨水顺着他的脸颊滑落。",
            f"这一天，对{name}来说，是命运的转折点。",
            f"看着手机里那个羞辱的订单，{name}咬紧了牙关。",
            f"霓虹灯闪烁，{name}走进了一家高档会所。",
        ]
        
        conflicts = [
            "被富二代嘲讽",
            "被女友抛弃",
            "被领导辞退",
            "被家人误会",
            "被兄弟背叛",
        ]
        
        turnarounds = [
            "手机突然响起，一个神秘的声音告诉他",
            "就在这时，一个穿着考究的中年人走了过来",
            "突然，一辆劳斯莱斯停在了他面前",
            "他的手机收到了一条短信",
        ]
        
        climax = [
            "所有人瞬间傻眼了！",
            "他们做梦也没想到，",
            "这一刻，全场寂静！",
            "所有人都震惊了！",
        ]
        
        endings = [
            "属于他的时代，才刚刚开始。",
            "他的嘴角微微上扬，露出神秘微笑。",
            "接下来会发生什么，连他自己都不知道。",
            "这一天起，一切都变了。",
        ]
        
        # 组装
        content = f"""
# 第{num}章 {theme}

{random.choice(openings)}

{random.choice(conflicts)}，{name}只感觉心如刀割。

曾经的山盟海誓，在金钱面前显得如此可笑。
那些所谓的兄弟朋友，在利益面前纷纷露出了真面目。

就在他最低落的时候，{random.choice(turnarounds)}

「从今天起，你的人生，将由你自己做主！」

{climax[0]}
{name}的身份，竟然是...

{endings[0]}
"""
        return content
    
    def _generate_fantasy_chapter(self, num: int, theme: str) -> str:
        """玄幻类型章节"""
        
        name = self.protagonist["name"]
        
        openings = [
            f"灵气翻涌，{name}感受着体内蓬勃的力量。",
            f"神秘空间中，{name}缓缓睁开了眼睛。",
            f"丹田之内，那枚金色金丹正在疯狂旋转。",
            f"山峰之巅，{name}负手而立，俯瞰众生。",
        ]
        
        conflicts = [
            "被宗门天才羞辱",
            "被长辈判定为废物",
            "被同门师兄弟陷害",
            "家族被人灭门",
        ]
        
        turnarounds = [
            "突然，体内传来一声轰鸣",
            "识海之中，一道神秘的声音响起",
            "他体内的血脉突然觉醒",
            "祖传玉佩突然发光",
        ]
        
        climax = [
            "恐怖的气息瞬间爆发！",
            "所有人都惊恐地发现，",
            "天地为之变色！",
            "法则为之颤抖！",
        ]
        
        endings = [
            "修仙之路，才刚刚开始。",
            "属于他的传奇，即将书写。",
            "大道尽头，他俯瞰苍生。",
            "这一战后，他的名字传遍整片大陆。",
        ]
        
        content = f"""
# 第{num}章 {theme}

{random.choice(openings)}

{random.choice(conflicts)}，{name}只感觉命运弄人。

曾经的天之骄子，如今成了人人可欺的废物。
那些曾经阿谀奉承的人，如今都躲得远远的。

就在他最绝望的时候，{random.choice(turnarounds)}

「哈哈哈，原来...我是万古无一的天才！」

{climax[0]}
{name}的气息，开始疯狂攀升！

{endings[0]}
"""
        return content
    
    def _generate_system_chapter(self, num: int, theme: str) -> str:
        """系统类型章节"""
        
        name = self.protagonist["name"]
        
        openings = [
            f"【叮！系统激活成功】机械般的声音在{name}脑海中响起。",
            f"看着手机屏幕上突然出现的金色图标，{name}愣住了。",
            f"「恭喜宿主完成首单，获得神秘大礼包！」",
            f"一道光幕在{name}面前展开。",
        ]
        
        conflicts = [
            "被客户投诉",
            "被房东赶出门",
            "被女友分手",
            "被公司裁员",
        ]
        
        turnarounds = [
            "系统突然发布任务",
            "脑海中响起清脆的提示音",
            "手机弹出一个神秘APP",
            "面前出现一道光门",
        ]
        
        climax = [
            "【恭喜宿主，获得一个亿！】",
            "【任务完成，奖励发放中...】",
            "【系统升级成功，各项属性大幅提升】",
            "【检测到宿主生命危险，自动开启保护模式】",
        ]
        
        endings = [
            "有了系统，{name}的人生彻底开挂。",
            "从这一天起，{name}开始逆袭人生。",
            "属于他的神豪人生，正式开启。",
            "这还只是刚刚开始...",
        ]
        
        content = f"""
# 第{num}章 {theme}

{random.choice(openings)}

{name}的人生已经跌入谷底。
{random.choice(conflicts)}，让他感觉整个世界都抛弃了他。

然而，{random.choice(turnarounds)}

{climax[0]}

{endings[0]}
"""
        return content


def main():
    import argparse
    parser = argparse.ArgumentParser(description="NovelAgent Lite - 直接生成小说")
    parser.add_argument("--genre", "-g", default="都市", help="类型")
    parser.add_argument("--title", "-t", required=True, help="书名")
    parser.add_argument("--chapters", "-c", type=int, default=3, help="章节数")
    parser.add_argument("--output", "-o", default=".", help="输出目录")
    
    args = parser.parse_args()
    
    # 主题列表
    themes = [
        "命运转折", "意外惊喜", "身份曝光", "实力初现",
        "打脸反击", "英雄救美", "获得传承", "境界突破",
        "家族大比", "宗门试炼", "生死危机", "奇遇连连",
    ]
    
    generator = NovelGenerator(args.genre, args.title, "一句话简介")
    
    import os
    os.makedirs(args.output, exist_ok=True)
    
    for i in range(1, args.chapters + 1):
        theme = random.choice(themes)
        content = generator.generate_chapter(i, theme)
        
        filename = f"{args.output}/第{i}章_{theme}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        
        print(f"✅ 已生成: {filename}")
    
    print(f"\n🎉 完成！共生成 {args.chapters} 章")


if __name__ == "__main__":
    main()
