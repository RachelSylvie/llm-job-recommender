# jd_indexer.py
# 将岗位描述向量化并存入 Faiss

import pandas as pd
import numpy as np
import pickle
import faiss
from tqdm import tqdm
from sentence_transformers import SentenceTransformer
import os
os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'
os.environ['HF_HOME'] = 'my_models/huggingface'  # 模型保存路径
# 1. 读取岗位数据
csv_path = 'data_new.csv'  # 爬下来的岗位数据路径
df = pd.read_csv(csv_path)

# 填空字段处理（避免 NaN）
df.fillna('', inplace=True)

# 2. 拼接文本字段作为语义输入（每条JD变成一段“描述文本”）
def build_text(row):
    return f"职位：{row['职位']}，薪资：{row['薪资']}，学历：{row['学历']}，经验：{row['经验']}，技能：{row['技能列表']}，城市：{row['城市']}，公司：{row['公司']}，行业：{row['领域']}，福利：{row['福利列表']}"

texts = df.apply(build_text, axis=1).tolist()

# 3. 加载句向量模型（384维）
model = SentenceTransformer('sentence-transformers/paraphrase-MiniLM-L6-v2')

# 4. 向量化所有岗位文本
print("正在向量化岗位文本...")
embeddings = model.encode(texts, show_progress_bar=True)

# 5. 构建Faiss索引并添加向量
vec_dim = embeddings.shape[1]
index = faiss.IndexFlatL2(vec_dim)
index.add(np.array(embeddings).astype('float32'))

# 6. 保存索引和元信息
data_dir = 'data/vector_db'
faiss.write_index(index, f'{data_dir}/jd.index')

# 提取元信息供展示：职位、公司、薪资、关键词...
metas = df[['关键词', '职位', '公司', '薪资', '城市', '技能列表', '福利列表']].to_dict(orient='records')
with open(f'{data_dir}/jd_metas.pkl', 'wb') as f:
    pickle.dump(metas, f)

print(f"✅ 向量库构建完成，共计 {len(texts)} 条岗位，向量维度 {vec_dim}")
