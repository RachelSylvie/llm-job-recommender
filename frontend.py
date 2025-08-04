import streamlit as st
from recommender import extract_text_from_pdf, recommend_jobs_from_resume
from feedback_logger import log_feedback
import tempfile
import os


st.set_page_config(page_title="LLM Job Recommender", layout="wide")
st.title("💼 LLM Job Recommender")

st.markdown("请上传您的简历（PDF 格式），系统将推荐最匹配的岗位。")

# ✅ 上传简历
uploaded_file = st.file_uploader("上传简历 PDF", type=["pdf"])

if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_path = tmp_file.name

    # 提取简历文本
    resume_text = extract_text_from_pdf(tmp_path)

    # 获取推荐结果（top 3）
    top_jobs = recommend_jobs_from_resume(resume_text, top_k=3)

    os.remove(tmp_path)

    # 展示推荐结果
    st.subheader("📌 推荐岗位（Top 3）")
    for i, job in enumerate(top_jobs, 1):
        # st.markdown(f"### {i}. {job['title']} - {job['company']}")
        # st.markdown(f"- **匹配理由**: {job['reason']}")
        # st.markdown("---")
        with st.container():
            st.markdown(f"### 🏷️ 推荐岗位 #{i}")
            st.markdown(f"- **职位：** {job['职位']}  |  **公司：** {job['公司']}  |  **薪资：** {job['薪资']}")
            st.markdown(f"- **城市：** {job['城市']}  |  **技能要求：** {job['技能列表']}")
            st.markdown(f"- **匹配分数：** {job['匹配分数']:.2f} / 100")
            st.markdown(f"#### 🔍 推荐理由：\n{job.get('推荐理由', '暂无')}")

        # 用户反馈区域
        with st.expander("❌ 觉得不太匹配？点我反馈"):
            reason = st.text_input(f"反馈原因（岗位 {i}）", key=f"reason_{i}")
            if st.button(f"提交反馈（岗位 {i}）", key=f"btn_{i}"):
                log_feedback(
                    resume_text=resume_text[:200],  # 改为 resume_text（原 resume_excerpt）
                    job_id=job['职位'],
                    reason=reason or "not_match"  # company 参数去掉，因为函数不支持
                )

                st.success("✅ 反馈已记录，感谢你的帮助！")