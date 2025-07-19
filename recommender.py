# recommender.py
# 用户上传 PDF 简历 → 提取文本 → 匹配岗位 → 返回 Top3 推荐结果

import pickle
import faiss
import numpy as np
import fitz  # PyMuPDF
from sentence_transformers import SentenceTransformer
import argparse
from explainer import explain_match  # 引入推荐理由解释模块
from feedback_logger import log_feedback
import json



# 模型加载（同 indexer）
model = SentenceTransformer('sentence-transformers/paraphrase-MiniLM-L6-v2')

# 载入向量索引 & 元信息
data_dir = 'data/vector_db'
index = faiss.read_index(f'{data_dir}/jd.index')
with open(f'{data_dir}/jd_metas.pkl', 'rb') as f:
    metas = pickle.load(f)

# 提取 PDF 简历文本
def extract_text_from_pdf(pdf_path: str) -> str:
    doc = fitz.open(pdf_path)
    text = ''
    for page in doc:
        text += page.get_text()
    return text.strip()

def build_jd_text(job: dict) -> str:
    return f"职位：{job['职位']}，公司：{job['公司']}，薪资：{job['薪资']}，城市：{job['城市']}，技能要求：{job['技能列表']}，福利：{job['福利列表']}"
# 推荐函数
# def recommend_jobs_from_resume(resume_text: str, top_k: int = 3):
#     query_vec = model.encode([resume_text])
#     query_vec = np.array(query_vec).astype('float32')
#
#     D, I = index.search(query_vec, top_k)
#     results = []
#     # 欧氏距离代表匹配度，越小越好
#     for i, idx in enumerate(I[0]):
#         if idx >= 0:
#             job = metas[idx]
#             score = 100-float(D[0][i])
#             job['匹配分数']=score
#
#             # 构造JD文本并调用LLM解释理由
#             jd_text = build_jd_text(job)
#             reason = explain_match(resume_text, jd_text)
#             job['推荐理由'] = reason
#             results.append(job)
    # for i, idx in enumerate(I[0]):
    #     if idx >= 0:
    #         job = metas[idx]
    #         # 百分制匹配度（值越高越好）
    #
    #         raw_scores = D[0]  # 当前查询的 Top-K 距离
    #         min_dist, max_dist = raw_scores.min(), raw_scores.max()
    #         # 归一化并反转（距离越小 → 分数越高）
    #         normalized_scores = 1 - (raw_scores - min_dist) / (max_dist - min_dist + 1e-6)  # 避免除零
    #         match_score = 100 * normalized_scores[i]  # 百分制
    #         job['匹配分数'] = round(match_score, 2)
    #         results.append(job)
    # return results
def load_feedback_penalties():
    penalties = {}
    try:
        with open('data/feedback_log.jsonl', 'r') as f:
            for line in f:
                record = json.loads(line)
                job_key = f"{record['job_title']}_{record['company']}"
                penalties[job_key] = penalties.get(job_key, 0) + 1
    except FileNotFoundError:
        pass
    return penalties


def recommend_jobs_from_resume(resume_text: str, top_k: int = 3):
    """核心推荐逻辑（整合反馈惩罚）"""
    # 1. 加载反馈惩罚数据
    penalties = load_feedback_penalties()

    # 2. 向量搜索（扩大候选集以应对惩罚过滤）
    query_vec = model.encode([resume_text])
    query_vec = np.array(query_vec).astype('float32')
    D, I = index.search(query_vec, top_k + 10)  # 多查10个备选

    # 3. 处理结果并应用惩罚
    results = []
    for i, idx in enumerate(I[0]):
        if idx >= 0:
            job = metas[idx]
            job_key = f"{job['职位']}_{job['公司']}"

            # 计算基础分数（欧氏距离转百分制）
            base_score = 100 - float(D[0][i])

            # 应用反馈惩罚（每次反馈扣5分）
            penalty = penalties.get(job_key, 0) * 5
            final_score = max(0, base_score - penalty)  # 确保分数非负

            if final_score >= 30:  # 过滤低分岗位
                job['匹配分数'] = round(final_score, 2)

                # 生成推荐理由（仅对最终结果调用以节省资源）
                jd_text = build_jd_text(job)
                job['推荐理由'] = explain_match(resume_text, jd_text)
                results.append(job)

    # 4. 按分数排序并返回TopK
    return sorted(results, key=lambda x: -x['匹配分数'])[:top_k]

# 命令行运行入口
if __name__ == '__main__':
    # parser = argparse.ArgumentParser()
    # parser.add_argument('--pdf', type=str, required=True, help='D:/learn/2025推免/基本信息pdf版合集/简历.pdf')
    # args = parser.parse_args()
    pdf_path = "D:/learn/2025推免/基本信息pdf版合集/简历.pdf"
    resume_text = extract_text_from_pdf(pdf_path)
    recommendations = recommend_jobs_from_resume(resume_text, top_k=3)
    # resume_text = extract_text_from_pdf(args.pdf)
    # recommendations = recommend_jobs_from_resume(resume_text, top_k=3)

    for i, job in enumerate(recommendations, 1):
        print(f"\n推荐岗位 #{i}")
        print(f"职位：{job['职位']}  | 公司：{job['公司']}  | 薪资：{job['薪资']}")
        print(f"城市：{job['城市']}  | 技能：{job['技能列表']}")
        print(f"匹配分数：{job['匹配分数']:.4f}")
        print(f"推荐理由：{job['推荐理由']}")


