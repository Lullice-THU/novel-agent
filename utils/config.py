"""
配置管理模块
"""

import os
import json
from typing import Dict, Optional


class Config:
    """配置管理"""
    
    DEFAULT_CONFIG = {
        "api": {
            "provider": "deepseek",  # openai / deepseek / anthropic
            "api_key": "",
            "base_url": "https://api.deepseek.com",
            "model": "deepseek-chat",
        },
        "writing": {
            "target_words_per_chapter": 3000,
            "max_chapters": 100,
            "auto_review": True,
        },
        "output": {
            "format": "markdown",  # markdown / text / json
            "path": "./output",
        }
    }
    
    @classmethod
    def load(cls, config_path: Optional[str] = None) -> Dict:
        """加载配置"""
        if config_path and os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                if config_path.endswith('.json'):
                    return json.load(f)
                # 可以扩展支持yaml等格式
        
        # 返回默认配置
        config = cls.DEFAULT_CONFIG.copy()
        
        # 从环境变量覆盖
        if os.environ.get("OPENAI_API_KEY"):
            config["api"]["provider"] = "openai"
            config["api"]["api_key"] = os.environ.get("OPENAI_API_KEY")
        
        if os.environ.get("DEEPSEEK_API_KEY"):
            config["api"]["provider"] = "deepseek"
            config["api"]["api_key"] = os.environ.get("DEEPSEEK_API_KEY")
            config["api"]["base_url"] = os.environ.get("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
        
        return config
    
    @classmethod
    def save(cls, config: Dict, config_path: str):
        """保存配置"""
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
    
    @classmethod
    def get_api_key(cls) -> str:
        """获取API Key"""
        config = cls.load()
        return config["api"]["api_key"] or os.environ.get("OPENAI_API_KEY") or os.environ.get("DEEPSEEK_API_KEY", "")
