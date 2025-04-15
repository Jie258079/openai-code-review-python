from pydantic import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # 微信配置
    WECHAT_APPID: str
    WECHAT_SECRET: str
    WECHAT_TEMPLATE_ID: str
    
    # ChatGLM配置
    CHATGLM_API_KEY: str
    CHATGLM_API_URL: str
    
    # GitHub配置
    GITHUB_TOKEN: str
    GITHUB_REPO: Optional[str] = None
    
    # 评审配置
    REVIEW_PROMPT: str = """
    请对以下代码变更进行评审，重点关注：
    1. 代码质量和最佳实践
    2. 潜在的bug和安全隐患
    3. 性能优化建议
    4. 代码可维护性
    5. 架构设计合理性
    
    代码变更如下：
    {diff}
    """
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings() 