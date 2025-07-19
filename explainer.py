
from openai import OpenAI
import os

# 初始化客户端
# client = (OpenAI(api_key=os.getenv("OPENAI_API_KEY")))
api_key = os.getenv("DEEPSEEK_API_KEY")  # 从环境变量读取
client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")


# 构造提示词（Prompt）
def build_prompt(resume_text: str, jd_text: str) -> str:
    return f"""
你是一个智能求职推荐系统，请根据以下内容为用户生成推荐理由。

【用户简历】：
{resume_text}

【岗位信息】：
{jd_text}

请用一段自然的中文回答：
为什么该岗位推荐给这个用户？
"""

# def explain_match(resume_text: str, jd_text: str, model="gpt-3.5-turbo") -> str:
def explain_match(resume_text: str, jd_text: str, model="deepseek-chat"):
    prompt = build_prompt(resume_text, jd_text)

    response = client.chat.completions.create(  # 新调用方式
        model=model,
        messages=[
            {"role": "system", "content": "你是一个擅长人岗匹配的招聘专家。"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.6,
        max_tokens=150,
    )

    return response.choices[0].message.content.strip()  # 注意 .content 替代 ['content']
# 示例运行
def demo():
    resume = "三年Java开发经验，熟悉SpringBoot、MySQL，有电商系统开发背景。"
    jd = "Java开发工程师，要求熟悉SpringBoot，参与后台系统设计，最好有大型项目经验。"

    reason = explain_match(resume, jd)
    print("推荐理由：", reason)


if __name__ == "__main__":
    demo()