from pydantic_settings import BaseSettings
from typing import Optional
from pydantic import validator


class Settings(BaseSettings):
    # 微信配置
    WECHAT_APPID: str
    WECHAT_SECRET: str
    WECHAT_TEMPLATE_ID: str
    WECHAT_TOUSER: str = "oaBEg60ox6meGZz9t6RFs6xnKEJk"  # 默认接收者

    # DeepSeek配置
    DEEPSEEK_API_KEY: str
    DEEPSEEK_API_URL: str

    # GitHub配置
    CODE_TOKEN: str
    GITHUB_REPO: Optional[str] = None
    GITHUB_API_TIMEOUT: int = 30
    GITHUB_MAX_RETRIES: int = 3
    GITHUB_RETRY_DELAY: int = 5

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

    @validator('CODE_TOKEN', 'WECHAT_APPID', 'WECHAT_SECRET', 'WECHAT_TEMPLATE_ID')
    def validate_required_fields(cls, v, field):
        if not v:
            raise ValueError(f'{field.name} 不能为空')
        return v

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()