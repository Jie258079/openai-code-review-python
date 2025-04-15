from git import Repo
from typing import Tuple, Optional
from loguru import logger

class GitOperations:
    def __init__(self, repo_path: str = "."):
        self.repo = Repo(repo_path)
    
    def get_diff(self, commit_hash: Optional[str] = None) -> Tuple[str, str]:
        """
        获取代码差异
        :param commit_hash: 提交哈希，如果为None则获取最新提交
        :return: (diff_content, commit_message)
        """
        try:
            if commit_hash:
                commit = self.repo.commit(commit_hash)
            else:
                commit = self.repo.head.commit
            
            # 获取与父提交的差异
            if len(commit.parents) > 0:
                diff = self.repo.git.diff(commit.parents[0], commit)
            else:
                # 如果是初始提交
                diff = self.repo.git.show(commit)
            
            return diff, commit.message
        except Exception as e:
            logger.error(f"获取代码差异失败: {str(e)}")
            raise
    
    def get_repo_info(self) -> dict:
        """
        获取仓库信息
        :return: 包含仓库信息的字典
        """
        try:
            return {
                "name": self.repo.working_dir.split("/")[-1],
                "branch": self.repo.active_branch.name,
                "remote_url": self.repo.remotes.origin.url if self.repo.remotes else None
            }
        except Exception as e:
            logger.error(f"获取仓库信息失败: {str(e)}")
            raise
    
    def get_commit_info(self, commit_hash: Optional[str] = None) -> dict:
        """
        获取提交信息
        :param commit_hash: 提交哈希，如果为None则获取最新提交
        :return: 包含提交信息的字典
        """
        try:
            if commit_hash:
                commit = self.repo.commit(commit_hash)
            else:
                commit = self.repo.head.commit
            
            return {
                "hash": commit.hexsha,
                "author": commit.author.name,
                "email": commit.author.email,
                "message": commit.message,
                "date": commit.authored_datetime.isoformat()
            }
        except Exception as e:
            logger.error(f"获取提交信息失败: {str(e)}")
            raise 