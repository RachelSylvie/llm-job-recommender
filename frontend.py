import streamlit as st
import requests

# FastAPI 服务地址
API_URL = "http://localhost:8000"
API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="智能岗位推荐系统", layout="wide")
st.title("💼 基于 LLM 的智能求职推荐系统")

st.markdown("请上传您的简历（PDF 格式），系统将推荐最匹配的岗位，并提供推荐理由。")

# 上传简历 PDF
uploaded_file = st.file_uploader("上传简历 PDF", type=["pdf"])

if uploaded_file:
    with st.spinner("正在分析简历并生成推荐..."):
        files = {"file": uploaded_file}
        response = requests.post(f"{API_URL}/recommend_resume", files=files)

    if response.status_code == 200:
        results = response.json()["recommendations"]
        st.success("推荐完成！以下是与您的简历匹配度最高的岗位：")

        for i, job in enumerate(results, 1):
            with st.container():
                st.markdown(f"### 🏷️ 推荐岗位 #{i}")
                st.markdown(f"- **职位：** {job['职位']}  |  **公司：** {job['公司']}  |  **薪资：** {job['薪资']}")
                st.markdown(f"- **城市：** {job['城市']}  |  **技能要求：** {job['技能列表']}")
                st.markdown(f"- **匹配分数：** {job['匹配分数']:.2f} / 100")
                st.markdown(f"#### 🔍 推荐理由：\n{job.get('推荐理由', '暂无')}")

                # 不匹配反馈按钮
                if st.button(f"❌ 该岗位不匹配", key=f"feedback_{i}"):
                    feedback_data = {
                        "resume_excerpt": "用户上传简历",  # 简化版本，如需可抽取关键信息
                        "job_title": job['职位'],
                        "company": job['公司'],
                        "reason": "not_match"
                    }
                    resp = requests.post(f"{API_URL}/feedback", data=feedback_data)
                    if resp.status_code == 200:
                        st.info("反馈已记录，谢谢你的参与！")

    else:
        st.error("请求失败，请检查后端服务是否启动。")
