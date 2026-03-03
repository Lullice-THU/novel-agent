#!/usr/bin/env python3
"""
NovelAgent - AI网文创作团队
主入口
"""

import argparse
import os
import sys
from agents.planner import PlannerAgent
from agents.writer import WriterAgent
from agents.editor import EditorAgent
from utils.config import Config


def print_banner():
    banner = """
    ╔═══════════════════════════════════════╗
    ║       NovelAgent - AI网文创作团队       ║
    ║         🖊️✍️📖 自动化网文生成器          ║
    ╚═══════════════════════════════════════╝
    """
    print(banner)


def interactive_mode():
    """交互模式"""
    print("\n🎯 欢迎使用 NovelAgent 网文创作系统\n")
    
    # 收集基本信息
    print("请回答以下问题：\n")
    
    genre = input("📚 小说类型 (都市/玄幻/仙侠/系统/穿越/其他): ").strip() or "都市"
    title = input("📖 书名: ").strip() or "未命名小说"
    synopsis = input("📝 故事简介 (一句话): ").strip() or "主角逆袭人生"
    
    # 可选配置
    style = input("🎨 风格偏好 (轻松/热血/甜宠/虐心/直接回车默认): ").strip()
    target_length = input("📏 目标篇幅 (短篇/中篇/长篇/直接回车默认): ").strip() or "中篇"
    
    print("\n" + "="*50)
    print(f"📋 确认信息:")
    print(f"  类型: {genre}")
    print(f"  书名: {title}")
    print(f"  简介: {synopsis}")
    print(f"  风格: {style or '默认'}")
    print(f"  篇幅: {target_length}")
    print("="*50 + "\n")
    
    return {
        'genre': genre,
        'title': title,
        'synopsis': synopsis,
        'style': style,
        'target_length': target_length
    }


def generate_novel(config):
    """生成小说"""
    print("🚀 开始创作...\n")
    
    # 1. 策划阶段
    print("📝 阶段1: 策划世界观和大纲...")
    planner = PlannerAgent()
    outline = planner.generate_outline(
        genre=config['genre'],
        title=config['title'],
        synopsis=config['synopsis'],
        style=config.get('style', ''),
        target_length=config.get('target_length', '中篇')
    )
    print(f"✅ 大纲生成完成 ({len(outline.get('chapters', []))} 章)\n")
    
    # 显示大纲
    print("📋 故事大纲:")
    print("-" * 40)
    print(f"世界观: {outline.get('world_setting', 'N/A')}")
    print(f"主角: {outline.get('protagonist', 'N/A')}")
    print(f"核心冲突: {outline.get('main_conflict', 'N/A')}")
    print(f"金手指: {outline.get('golden_finger', 'N/A')}")
    print("-" * 40)
    
    # 2. 写作阶段
    print("\n✍️ 阶段2: 开始写作...")
    writer = WriterAgent()
    
    chapters_to_write = input("写前几章? (数字,默认3): ").strip() or "3"
    num_chapters = int(chapters_to_write)
    
    chapters = outline.get('chapters', [])[:num_chapters]
    
    for i, chapter in enumerate(chapters):
        print(f"\n  写作第{i+1}章: {chapter.get('title', '未命名')}")
        content = writer.write_chapter(
            outline=outline,
            chapter_outline=chapter,
            genre=config['genre']
        )
        print(f"  ✅ 完成 ({len(content)} 字)")
    
    # 3. 审核阶段
    print("\n🔍 阶段3: 审核优化...")
    editor = EditorAgent()
    
    print("\n" + "="*50)
    print("🎉 创作完成!")
    print("="*50)
    
    return {
        'outline': outline,
        'status': 'completed'
    }


def main():
    parser = argparse.ArgumentParser(description='NovelAgent - AI网文创作团队')
    parser.add_argument('--genre', '-g', default='都市', help='小说类型')
    parser.add_argument('--title', '-t', default='未命名小说', help='书名')
    parser.add_argument('--synopsis', '-s', default='', help='故事简介')
    parser.add_argument('--style', help='风格偏好')
    parser.add_argument('--length', '--target-length', dest='target_length', default='中篇', help='目标篇幅')
    parser.add_argument('--interactive', '-i', action='store_true', help='交互模式')
    parser.add_argument('--config', '-c', help='配置文件路径')
    
    args = parser.parse_args()
    
    print_banner()
    
    # 加载配置
    config = Config.load(args.config) if args.config else {}
    
    if args.interactive or not (args.title or args.synopsis):
        # 交互模式
        user_input = interactive_mode()
        config.update(user_input)
    else:
        # 命令行模式
        config.update({
            'genre': args.genre,
            'title': args.title,
            'synopsis': args.synopsis,
            'style': args.style,
            'target_length': args.target_length
        })
    
    # 生成小说
    result = generate_novel(config)
    
    print("\n📁 输出已保存到 output/ 目录")


if __name__ == '__main__':
    main()
