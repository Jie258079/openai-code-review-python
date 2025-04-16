import requests
from loguru import logger
from src.core.config import settings


class WeChatService:
    def __init__(self):
        self.appid = settings.WECHAT_APPID
        self.secret = settings.WECHAT_SECRET
        self.template_id = settings.WECHAT_TEMPLATE_ID
        self.access_token = None

    def get_access_token(self) -> str:
        """
        获取微信访问令牌
        :return: access_token
        """
        try:
            url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={self.appid}&secret={self.secret}"
            response = requests.get(url)

            if response.status_code == 200:
                result = response.json()
                if "access_token" in result:
                    self.access_token = result["access_token"]
                    return self.access_token
                else:
                    error_msg = f"获取access_token失败: {result.get('errmsg', '未知错误')}"
                    logger.error(error_msg)
                    raise Exception(error_msg)
            else:
                error_msg = f"获取access_token失败: HTTP {response.status_code}"
                logger.error(error_msg)
                raise Exception(error_msg)

        except Exception as e:
            logger.error(f"获取access_token时发生错误: {str(e)}")
            raise

    def send_review_notification(self, review_data: dict) -> bool:
        """
        发送代码评审通知
        :param review_data: 评审数据
        :return: 是否发送成功
        """
        try:
            if not self.access_token:
                self.get_access_token()

            url = f"https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={self.access_token}"

            data = {
                "touser": review_data.get("touser", "@all"),
                "template_id": self.template_id,
                "url": review_data.get("review_url", ""),
                "data": {
                    "first": {
                        "value": "代码评审通知",
                        "color": "#173177"
                    },
                    "keyword1": {
                        "value": review_data.get("repo_name", ""),
                        "color": "#173177"
                    },
                    "keyword2": {
                        "value": review_data.get("branch", ""),
                        "color": "#173177"
                    },
                    "keyword3": {
                        "value": review_data.get("author", ""),
                        "color": "#173177"
                    },
                    "keyword4": {
                        "value": review_data.get("commit_message", ""),
                        "color": "#173177"
                    },
                    "remark": {
                        "value": review_data.get("review_summary", ""),
                        "color": "#173177"
                    }
                }
            }

            response = requests.post(url, json=data)

            if response.status_code == 200:
                result = response.json()
                if result.get("errcode") == 0:
                    logger.info("评审通知发送成功")
                    return True
                else:
                    error_msg = f"发送通知失败: {result.get('errmsg', '未知错误')}"
                    logger.error(error_msg)
                    return False
            else:
                error_msg = f"发送通知失败: HTTP {response.status_code}"
                logger.error(error_msg)
                return False

        except Exception as e:
            logger.error(f"发送评审通知时发生错误: {str(e)}")
            return False 