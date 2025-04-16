import requests
from datetime import datetime
from loguru import logger
from src.core.config import settings


class GitHubService:
    def __init__(self):
        self.token = settings.GITHUB_TOKEN
        self.headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json"
        }

    def create_review_issue(self, repo: str, review_data: dict) -> str:
        """
        创建评审记录Issue
        :param repo: 仓库名称（格式：owner/repo）
        :param review_data: 评审数据
        :return: Issue URL
        """
        try:
            url = f"https://api.github.com/repos/{repo}/issues"

            # 生成Issue标题
            title = f"代码评审 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

            # 生成Issue内容
            body = f"""
## 代码评审结果

### 仓库信息
- 仓库：{review_data.get('repo_name', '')}
- 分支：{review_data.get('branch', '')}
- 提交者：{review_data.get('author', '')}
- 提交信息：{review_data.get('commit_message', '')}

### 评审结果
{review_data.get('full_review', '')}

### 评审状态
状态：{'成功' if review_data.get('status') == 'success' else '失败'}
            """

            data = {
                "title": title,
                "body": body,
                "labels": ["code-review", "automated"]
            }

            response = requests.post(url, headers=self.headers, json=data)

            if response.status_code == 201:
                result = response.json()
                issue_url = result.get("html_url")
                logger.info(f"评审记录已创建: {issue_url}")
                return issue_url
            else:
                error_msg = f"创建评审记录失败: HTTP {response.status_code} - {response.text}"
                logger.error(error_msg)
                raise Exception(error_msg)

        except Exception as e:
            logger.error(f"创建评审记录时发生错误: {str(e)}")
            raise

    def add_review_comment(self, repo: str, issue_number: int, comment: str) -> bool:
        """
        为评审记录添加评论
        :param repo: 仓库名称（格式：owner/repo）
        :param issue_number: Issue编号
        :param comment: 评论内容
        :return: 是否成功
        """
        try:
            url = f"https://api.github.com/repos/{repo}/issues/{issue_number}/comments"

            data = {
                "body": comment
            }

            response = requests.post(url, headers=self.headers, json=data)

            if response.status_code == 201:
                logger.info(f"评论已添加到评审记录 #{issue_number}")
                return True
            else:
                error_msg = f"添加评论失败: HTTP {response.status_code} - {response.text}"
                logger.error(error_msg)
                return False

        except Exception as e:
            logger.error(f"添加评论时发生错误: {str(e)}")
            return False 