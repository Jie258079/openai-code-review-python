# AI代码评审工具

这是一个基于ChatGLM的自动化代码评审工具，可以自动获取Git代码变更，使用AI模型进行代码评审，并通过微信推送评审结果。

## 功能特点

- 自动化代码评审流程
- 使用ChatGLM AI模型进行智能评审
- 自动获取Git代码变更
- 评审结果自动保存到GitHub
- 通过微信模板消息推送评审结果
- 支持GitHub Actions集成

## 安装

1. 克隆仓库：
```bash
git clone [repository-url]
cd ai-code-review
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 配置环境变量：
创建`.env`文件并配置以下变量：
```
WECHAT_APPID=your_appid
WECHAT_SECRET=your_secret
WECHAT_TEMPLATE_ID=your_template_id
CHATGLM_API_KEY=your_api_key
CHATGLM_API_URL=your_api_url
GITHUB_TOKEN=your_github_token
```

## 使用方法

1. 直接运行：
```bash
python src/main.py
```

2. 作为GitHub Action使用：
在`.github/workflows`目录下配置工作流文件。

## 项目结构

```
ai-code-review/
├── src/
│   ├── core/
│   │   ├── __init__.py
│   │   ├── code_review.py
│   │   ├── git_operations.py
│   │   └── ai_model.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── wechat_service.py
│   │   └── github_service.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py
│   └── main.py
├── tests/
│   └── __init__.py
├── requirements.txt
└── README.md
```

## 配置说明

### 微信配置
- WECHAT_APPID: 微信应用ID
- WECHAT_SECRET: 微信应用密钥
- WECHAT_TEMPLATE_ID: 消息模板ID

### ChatGLM配置
- CHATGLM_API_KEY: API密钥
- CHATGLM_API_URL: API地址

### GitHub配置
- GITHUB_TOKEN: GitHub访问令牌

## 贡献指南

欢迎提交Issue和Pull Request！

## 许可证

MIT License 