from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from recommender import extract_text_from_pdf, recommend_jobs_from_resume
from feedback_logger import log_feedback
from typing import List
import uvicorn
import os
import tempfile

app = FastAPI()

# 跨域配置（前端调用用得到）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 若部署时改为前端域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ 推荐接口：上传简历，返回推荐岗位
@app.post("/recommend_resume")
async def recommend_resume(file: UploadFile = File(...)):
    # 将上传的 PDF 保存为临时文件
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(await file.read())
        tmp_path = tmp_file.name

    # 提取简历文本
    resume_text = extract_text_from_pdf(tmp_path)

    # 获取推荐结果（top3）
    top_jobs = recommend_jobs_from_resume(resume_text, top_k=3)

    # 删除临时文件
    os.remove(tmp_path)

    return {"recommendations": top_jobs}


# ✅ 用户反馈接口：记录“不匹配”岗位
@app.post("/feedback")
async def feedback(
    resume_excerpt: str = Form(...),
    job_title: str = Form(...),
    company: str = Form(...),
    reason: str = Form("not_match")  # 可选字段
):
    log_feedback(resume_excerpt, job_title, company, reason)
    return {"status": "feedback logged"}

# 启动方式：
# uvicorn api_server:app --reload
if __name__ == "__main__":
    uvicorn.run("api_server:app", host="127.0.0.1", port=8000, reload=True)
