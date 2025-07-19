# feedback_logger.py
# 后端记录数据
# 推荐时，将出现多次‘不匹配’的岗位类别权重下调（比如加惩罚项）

import json
import os
from datetime import datetime

LOG_PATH = 'data/feedback_log.jsonl'

def log_feedback(resume_text: str, job_id: str, reason="not_match"):
    record = {
        'timestamp': datetime.now().isoformat(),
        'resume': resume_text[:200],  # 简要存储
        'job_id': job_id,
        'feedback': reason
    }
    with open(LOG_PATH, 'a', encoding='utf-8') as f:
        f.write(json.dumps(record, ensure_ascii=False) + '\n')
