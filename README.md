# 🧠 LLM Job Recommender

基于大语言模型的智能岗位推荐系统  
上传个人简历 PDF，自动解析简历内容，并结合语义向量相似度，从岗位库中推荐匹配职位。支持用户反馈并持续优化推荐结果。

## 🚀 项目特点

- **📄 简历上传**：自动从 PDF 中提取文本
- **🤖 大模型解析**：使用 LLM 提取用户技能、经历等关键信息
- **🧠 语义匹配**：使用向量化技术（如 SentenceTransformers）与岗位库进行 FAISS 检索
- **📬 推荐可解释性**：展示推荐匹配度与推荐理由
- **🔁 用户反馈机制**：用户可对推荐结果进行打分反馈，帮助后续优化

## 📁 项目结构
```
llm-job-recommender/  
│  
├── Boss招聘职位信息_爬虫.py    # 获取岗位信息  
├── frontend.py                # Streamlit 前端+后端：负责用户交互界面，处理简历上传、推荐逻辑  
├── recommender.py             # 岗位推荐核心逻辑  
├── explainer.py               # 推荐解释模块  
├── feedback_logger.py         # 用户反馈记录与存储  
├── jd_indexer                 # 将岗位描述向量化并存入 Faiss  
├── requirements.txt           # 所需依赖  
└── README.md  
```

## ⚙️ 环境配置
```bash
pip install -r requirements.txt
```
## 🛠 启动方式
## 步骤 1：设置 API Key## 
将你的 DeepSeek API Key 设置为环境变量：

```bash
$env:DEEPSEEK_API_KEY="sk-xxxxxxxx"  # Windows PowerShell  
export DEEPSEEK_API_KEY="sk-xxxxxxxx"  # Linux/macOS  
```
## 步骤 2：启动前后端##
```bash
streamlit run frontend.py
```
## ✅ 示例截图

![4153dcc42e17e98cc32eecba32c314f](https://github.com/user-attachments/assets/422a167d-b48e-4b1e-ae1c-399d01ba224c)
![dcb02bff7a29e69402995318beff2a7](https://github.com/user-attachments/assets/46088ea3-667d-4563-82aa-b4afd92a9289)
![3fd1003c279eb1510091723c2ec1ffd](https://github.com/user-attachments/assets/55026982-84bf-4ae3-88b1-cbfae43d6032)
![59744e62e104f3dada32b35e1e89560](https://github.com/user-attachments/assets/94f94568-29a6-4b32-891b-057082c404e4)

## 🧠 推荐逻辑简述
- 解析 PDF 简历 → 生成用户向量表示

- 读取岗位库（通过爬虫采集） → 向量化表示 → 构建 FAISS 索引

- 使用 LLM 对每次推荐进行解释，提升可读性

- 用户反馈（匹配度评分）记录至本地 CSV，用于后续模型迭代

## 🙋‍♀️ 关于作者
项目由 RachelSylvie 开发，旨在展示大语言模型结合推荐系统的落地能力。

