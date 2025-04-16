import asyncio
from loguru import logger
from core.git_operations import GitOperations
from core.ai_model import DeepSeekClient
from services.wechat_service import WeChatService
from services.github_service import GitHubService
from core.config import settings


class CodeReviewer:
    def __init__(self):
        self.git_ops = GitOperations()
        self.ai_client = DeepSeekClient()
        self.wechat_service = WeChatService()
        self.github_service = GitHubService()

    async def review_code(self, commit_hash: str = None):
        """
        执行代码评审流程
        :param commit_hash: 提交哈希，如果为None则评审最新提交
        """
        try:
            # 1. 获取代码差异
            logger.info("正在获取代码差异...")
            diff_content, commit_message = self.git_ops.get_diff(commit_hash)

            # 2. 获取仓库和提交信息
            repo_info = self.git_ops.get_repo_info()
            commit_info = self.git_ops.get_commit_info(commit_hash)

            # 3. 使用AI模型评审代码
            logger.info("正在使用DeepSeek模型评审代码...")
            review_text = await self.ai_client.review_code(diff_content)
            review_result = self.ai_client.format_review_result(review_text)

            # 4. 创建GitHub评审记录
            logger.info("正在创建GitHub评审记录...")
            review_data = {
                "repo_name": repo_info["name"],
                "branch": repo_info["branch"],
                "author": commit_info["author"],
                "commit_message": commit_info["message"],
                "full_review": review_result["full_review"],
                "status": review_result["status"]
            }

            issue_url = self.github_service.create_review_issue(
                settings.GITHUB_REPO,
                review_data
            )

            # 5. 发送微信通知
            logger.info("正在发送微信通知...")
            notification_data = {
                "repo_name": repo_info["name"],
                "branch": repo_info["branch"],
                "author": commit_info["author"],
                "commit_message": commit_info["message"],
                "review_summary": review_result["summary"],
                "review_url": issue_url
            }

            self.wechat_service.send_review_notification(notification_data)

            logger.info("代码评审流程完成！")
            return {
                "status": "success",
                "review_url": issue_url,
                "review_summary": review_result["summary"]
            }

        except Exception as e:
            error_msg = f"代码评审过程发生错误: {str(e)}"
            logger.error(error_msg)
            return {
                "status": "error",
                "error": error_msg
            }


async def main():
    reviewer = CodeReviewer()
    result = await reviewer.review_code()
    print(result)


if __name__ == "__main__":
    asyncio.run(main()) 