import httpx
from loguru import logger
from src.core.config import settings
import traceback


class DeepSeekClient:
    def __init__(self):
        self.api_url = settings.DEEPSEEK_API_URL
        self.api_key = settings.DEEPSEEK_API_KEY
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    async def review_code(self, diff_content: str) -> str:
        """
        使用DeepSeek模型评审代码
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
                        "model": "deepseek-coder",  # 使用DeepSeek的代码模型
                        "messages": [
                            {
                                "role": "system",
                                "content": "你是一个专业的代码评审专家，请对代码进行全面的评审。"
                            },
                            {
                                "role": "user",
                                "content": prompt
                            }
                        ],
                        "temperature": 0.7,
                        "max_tokens": 2000
                    }
                )

                if response.status_code == 200:
                    result = response.json()
                    return result.get("choices", [{}])[0].get("message", {}).get("content", "评审失败：未获取到有效响应")
                elif response.status_code == 402:
                    error_msg = "DeepSeek API余额不足，请充值后重试"
                    logger.error(error_msg)
                    return error_msg
                else:
                    error_msg = f"评审失败：HTTP {response.status_code} - {response.text}"
                    logger.error(error_msg)
                    return error_msg

        except Exception as e:
            # 获取完整的异常堆栈
            error_stack = traceback.format_exc()
            error_msg = f"评审过程发生错误: {str(e)}\n堆栈信息: {error_stack}"
            logger.error(error_msg)
            return error_msg

    def format_review_result(self, review_text: str) -> dict:
        """
        格式化评审结果
        :param review_text: 原始评审文本
        :return: 格式化后的评审结果
        """
        try:
            # 检查是否是余额不足错误
            if "余额不足" in review_text:
                return {
                    "summary": "DeepSeek API余额不足，请充值后重试",
                    "full_review": review_text,
                    "status": "error"
                }

            # 检查是否是错误信息
            if "评审过程发生错误" in review_text:
                return {
                    "summary": "代码评审过程中发生错误，请查看完整评审记录",
                    "full_review": review_text,
                    "status": "error"
                }

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