#!/usr/bin/env python3
"""
Editor Agent - 审核
负责内容审核、爽点检测、质量把关
"""

import re
from typing import Dict, List, Tuple


class EditorAgent:
    """审核Agent - 从读者视角审核内容"""
    
    def __init__(self):
        self.min_爽点_density = 3  # 每3000字至少3个爽点
    
    def review_chapter(self, content: str, chapter_outline: Dict) -> Dict:
        """
        审核章节
        
        Args:
            content: 章节内容
            chapter_outline: 章节大纲
        
        Returns:
            审核报告
        """
        
        # 检测爽点
        爽点检测 = self.check_爽点(content)
        
        # 检测节奏
        rhythm_score = self.check_rhythm(content)
        
        # 检测问题
        issues = self.check_issues(content)
        
        # 综合评分
        score = self.calculate_score(爽点检测, rhythm_score, issues)
        
        return {
            "score": score,
            "爽点检测": 爽点检测,
            "rhythm_score": rhythm_score,
            "issues": issues,
            "建议": self.generate_suggestions(爽点检测, rhythm_score, issues),
            "通过": score >= 70,
        }
    
    def check_爽点(self, content: str) -> Dict:
        """检测爽点"""
        
        # 常见爽点关键词
        爽点_keywords = [
            "震惊", "惊讶", "不可能", "竟然", "脸色大变",
            "傻眼", "呆住", "震撼", "沸腾", "狂欢",
            "打脸", "反转", "逆袭", "暴涨", "突破",
            "获得", "解锁", "激活", "恭喜", "奖励",
            "功法", "神器", "宝藏", "传承", "金丹",
            "系统", "商城", "抽奖", "礼包", "返利",
        ]
        
        found_爽点 = []
        for keyword in 爽点_keywords:
            if keyword in content:
                found_爽点.append(keyword)
        
        # 计算爽点密度
        content_length = len(content)
        爽点_count = len(found_爽点)
        爽点_density = (爽点_count / content_length) * 1000  # 每千字爽点数
        
        return {
            "found": found_爽点,
            "count": 爽点_count,
            "density": round(爽点_density, 2),
            "pass": 爽点_density >= self.min_爽点_density,
        }
    
    def check_rhythm(self, content: str) -> Dict:
        """检测节奏"""
        
        # 段落数
        paragraphs = content.split("\n\n")
        paragraph_count = len([p for p in paragraphs if p.strip()])
        
        # 句子数 (简单估算)
        sentence_count = len(re.findall(r'[。！？]', content))
        
        # 平均段落长度
        avg_paragraph_length = len(content) / max(paragraph_count, 1)
        
        # 节奏评分
        # 好节奏: 段落适中，句子长短结合
        if 300 <= avg_paragraph_length <= 800:
            rhythm_score = 80
        elif 200 <= avg_paragraph_length <= 1000:
            rhythm_score = 70
        else:
            rhythm_score = 60
        
        return {
            "paragraph_count": paragraph_count,
            "sentence_count": sentence_count,
            "avg_length": round(avg_paragraph_length),
            "score": rhythm_score,
        }
    
    def check_issues(self, content: str) -> List[Dict]:
        """检测问题"""
        
        issues = []
        
        # 检测重复
        words = re.findall(r'.{4,}', content)
        word_counts = {}
        for word in words:
            if len(word) > 8:  # 长词才检测
                word_counts[word] = word_counts.get(word, 0) + 1
        
        for word, count in word_counts.items():
            if count > 3:
                issues.append({
                    "type": "重复",
                    "content": word,
                    "count": count,
                    "severity": "warning",
                })
        
        # 检测过长句子
        long_sentences = re.findall(r'.{50,}[。！？]', content)
        if len(long_sentences) > 5:
            issues.append({
                "type": "句子过长",
                "count": len(long_sentences),
                "severity": "info",
            })
        
        return issues
    
    def calculate_score(self, 爽点检测: Dict, rhythm_score: Dict, issues: List[Dict]) -> int:
        """计算综合评分"""
        
        score = 100
        
        # 爽点扣分
        if not 爽点检测["pass"]:
            score -= 20
        
        # 节奏扣分
        score -= (80 - rhythm_score["score"]) // 2
        
        # 问题扣分
        for issue in issues:
            if issue.get("severity") == "warning":
                score -= 5
        
        return max(0, min(100, score))
    
    def generate_suggestions(self, 爽点检测: Dict, rhythm_score: Dict, issues: List[Dict]) -> List[str]:
        """生成改进建议"""
        
        suggestions = []
        
        if not 爽点检测["pass"]:
            suggestions.append("⚠️ 爽点不足，建议增加打脸、逆转、奖励等爽点情节")
        
        if rhythm_score["score"] < 70:
            suggestions.append("📝 节奏需要调整，建议适当分段或增减句子")
        
        if any(i.get("severity") == "warning" for i in issues):
            suggestions.append("🔄 检测到重复内容，建议润色")
        
        if not suggestions:
            suggestions.append("✅ 质量良好，可以发布")
        
        return suggestions
    
    def batch_review(self, chapters: List[str], outlines: List[Dict]) -> List[Dict]:
        """批量审核"""
        
        results = []
        for content, outline in zip(chapters, outlines):
            result = self.review_chapter(content, outline)
            results.append(result)
        
        # 统计汇总
        total_score = sum(r["score"] for r in results)
        avg_score = total_score / len(results) if results else 0
        
        passed_count = sum(1 for r in results if r["通过"])
        
        return {
            "chapters": results,
            "summary": {
                "total": len(results),
                "passed": passed_count,
                "failed": len(results) - passed_count,
                "avg_score": round(avg_score, 2),
            }
        }
