import httpx
from loguru import logger
from .config import settings

class ChatGLMClient:
    def __init__(self):
        self.api_url = settings.CHATGLM_API_URL
        self.api_key = settings.CHATGLM_API_KEY
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    async def review_code(self, diff_content: str) -> str:
        """
        使用ChatGLM模型评审代码
        :param diff_content: 代码差异内容
        :return: 评审结果
        """
        try:
            prompt = settings.REVIEW_PROMPT.format(diff=diff_content)
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.api_url,
                    headers=self.headers,
                    json={
                        "prompt": prompt,
                        "temperature": 0.7,
                        "max_tokens": 2000
                    }
                )
                
                if response.status_code == 200:
                    result = response.json()
                    return result.get("response", "评审失败：未获取到有效响应")
                else:
                    error_msg = f"评审失败：HTTP {response.status_code} - {response.text}"
                    logger.error(error_msg)
                    return error_msg
                    
        except Exception as e:
            error_msg = f"评审过程发生错误: {str(e)}"
            logger.error(error_msg)
            return error_msg
    
    def format_review_result(self, review_text: str) -> dict:
        """
        格式化评审结果
        :param review_text: 原始评审文本
        :return: 格式化后的评审结果
        """
        try:
            # 这里可以添加更多的格式化逻辑
            return {
                "summary": review_text[:200] + "..." if len(review_text) > 200 else review_text,
                "full_review": review_text,
                "status": "success" if "失败" not in review_text else "error"
            }
        except Exception as e:
            logger.error(f"格式化评审结果失败: {str(e)}")
            return {
                "summary": "评审结果格式化失败",
                "full_review": review_text,
                "status": "error"
            } 