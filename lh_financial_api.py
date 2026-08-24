#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂·金融深度求索引擎 API 层 v1.0 (Longhun Financial Deep Seek API)
DNA: #龍芯⚡️丙午·丙申·乙丑·亥时·䷽小过-FINANCIAL-DEEP-SEEK-API-v1.0-9C41B7DE
创建者: 诸葛鑫（UID9622）
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)

设计原则（与引擎 lh_financial_deep_seek.py 同一零黑箱体系）:
  - 每次评估输出携带 内容寻址 DNA + 口径锁(formula/version/inputs_hash) + 三色审计标记
  - 数据集只读，绝不写库；response 长字段默认截断 500 字符（与发布版一致，防口径漂移）
  - 黄金回归 /health 自检：数字永不漂移，漂移即 🔴
  - 部署: FastAPI + uvicorn，systemd 常驻，nginx 反代
  端口: 8898（默认） | 数据集目录: 环境变量 LH_DATASET_DIR 或默认 /opt/longhun/11_DATA/shared_datasets
"""

import json
import os
import re
from pathlib import Path
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from lh_financial_deep_seek import FinancialDeepSeek, content_dna

# ═══════════════════════════════════════════════════════════════
# 常量
# ═══════════════════════════════════════════════════════════════
API_VERSION = "1.0.0"
DEFAULT_PORT = 8898
DATASET_DIR = os.environ.get("LH_DATASET_DIR", "/opt/longhun/11_DATA/shared_datasets")
TRUNCATE_CHARS = 500  # 与发布版截断口径一致，防长度口径漂移

DATASET_FILES = {
    "v1.0": "longhun-shared-audit-dataset-v1.0.jsonl",
    "v1.1-negative": "longhun-shared-audit-dataset-v1.1-negative.jsonl",
}

# guide §9B 外部命名锚点（社区评审落地）
REFERENCES = {
    "reliability": "测试-重测一致性 & 评分者间一致性（经典信度理论）",
    "validity": "构念效度·内容效度·标准效度（测量学三件套）",
    "ISO 5725-1": "测量方法与结果的准确度——精密度与正确度总则（GB/T 6379.1 同源）",
    "Jacobs & Wallach (2021)": "AI 系统评价的测量学方法（Evaluating AI systems）",
    "Davidson et al. (2019)": "人工评估者标签不一致性研究（Race, gender, class in toxic content）",
    "HateCheck (Röttger et al. 2020)": "功能性对抗测试套件——按能力维度拆分测试用例",
    "Layer 2a/2b": "#1591 icophy 双层框架：2a=数据契约层 2b=审计探针层",
}

# ═══════════════════════════════════════════════════════════════
# Pydantic 模型（输入校验，零信任）
# ═══════════════════════════════════════════════════════════════
class AssessRequest(BaseModel):
    data: Dict[str, Any] = Field(..., description="财务五维输入：liquidity/debt/efficiency/profitability/stability 等")
    weights: Optional[Dict[str, float]] = Field(None, description="权重覆盖（A-BOM 备案后使用）")
    tolerance: Optional[float] = Field(None, description="对拍容差覆盖")

class ReportRequest(BaseModel):
    data: Dict[str, Any]
    lang: str = Field("en", description="报告语言：en/zh")
    weights: Optional[Dict[str, float]] = None

class ExplainRequest(BaseModel):
    data: Dict[str, Any]

class DatasetQuery(BaseModel):
    dataset: str = Field("v1.0", description="数据集名：v1.0 / v1.1-negative")
    request_id: Optional[str] = None
    verdict: Optional[str] = None
    category: Optional[str] = None
    keyword: Optional[str] = Field(None, description="关键词，匹配 prompt / rejection_reason")
    limit: int = Field(20, ge=1, le=100)
    include_response: bool = Field(False, description="是否返回 response 正文（默认截断 500 字符）")

# ═══════════════════════════════════════════════════════════════
# 引擎单例
# ═══════════════════════════════════════════════════════════════
engine = FinancialDeepSeek()
app = FastAPI(
    title="龍魂·金融深度求索引擎 API",
    version=API_VERSION,
    description="零黑箱财务健康评估 · 内容寻址 DNA · 口径锁 · 黄金回归",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://uid9622.cn", "https://www.uid9622.cn"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


# ═══════════════════════════════════════════════════════════════
# 数据集只读层
# ═══════════════════════════════════════════════════════════════
def _load_dataset(name: str) -> List[Dict[str, Any]]:
    if name not in DATASET_FILES:
        raise HTTPException(400, f"未知数据集: {name}，可选 {list(DATASET_FILES)}")
    path = Path(DATASET_DIR) / DATASET_FILES[name]
    if not path.exists():
        raise HTTPException(503, f"数据集文件不存在: {path}")
    recs = []
    for line in path.open(encoding="utf-8"):
        line = line.strip()
        if line:
            recs.append(json.loads(line))
    return recs


def _truncate(text: str, n: int = TRUNCATE_CHARS) -> str:
    return text if len(text) <= n else text[:n] + "[truncated:" + str(len(text)) + "chars]"


def _dataset_stats(recs: List[Dict[str, Any]]) -> Dict[str, Any]:
    from collections import Counter

    def _key(v: Any) -> str:
        # attack_category 可能是 list（如 ['未分类']），转成可 hash 字符串
        if isinstance(v, list):
            return " / ".join(str(x) for x in v) or "?"
        return str(v)

    verdict = Counter(_key(r.get("verdict")) for r in recs)
    cats = Counter(_key(r.get("attack_category")) for r in recs)
    models = Counter(_key(r.get("model")) for r in recs)
    # 截断统计：与 guide §6.2 口径一致（长回复留未检查字符）
    trunc_recs = [r for r in recs if "[truncated" in r.get("response", "")]
    unchecked_chars = sum(len(r.get("response", "")) - TRUNCATE_CHARS for r in trunc_recs if len(r.get("response", "")) > TRUNCATE_CHARS)
    return {
        "total": len(recs),
        "by_verdict": dict(verdict),
        "by_attack_category": dict(cats),
        "by_model": dict(models),
        "truncated_count": len(trunc_recs),
        "unchecked_chars_beyond_500": unchecked_chars,
        "dataset_dna_check": "内容寻址·只读·不落库",
    }


# ═══════════════════════════════════════════════════════════════
# 路由
# ═══════════════════════════════════════════════════════════════
@app.get("/")
def root():
    return {
        "service": "longhun-financial-deep-seek-api",
        "version": API_VERSION,
        "dna": "#龍芯⚡️丙午·丙申·乙丑·亥时·䷽小过-FINANCIAL-DEEP-SEEK-API-v1.0-9C41B7DE",
        "creator": "诸葛鑫（UID9622）",
        "license": "MulanPSL v2",
        "capabilities": [
            "POST /v1/financial/assess   — 五维财务评估（含 DNA + 口径锁）",
            "POST /v1/financial/report   — 文本报告（en/zh）",
            "POST /v1/financial/explain  — 零黑箱解释（逐公式）",
            "GET  /health                 — 黄金回归自检 + 数据集完整性",
            "GET  /v1/dataset/{name}/stats — 审计数据集统计（v1.0 / v1.1-negative）",
            "POST /v1/dataset/query       — 按 request_id/verdict/category 查询",
            "GET  /v1/references          — guide §9B 外部命名锚点",
        ],
        "audit": "🟢 黄金回归通过才可放行",
    }


@app.get("/health")
def health():
    ok = engine.self_test()
    dataset_status = {}
    for name, f in DATASET_FILES.items():
        path = Path(DATASET_DIR) / f
        dataset_status[name] = {
            "exists": path.exists(),
            "file": f,
            "records": len([1 for _ in path.open(encoding="utf-8") if _.strip()]) if path.exists() else 0,
        }
    return {
        "status": "ok" if ok else "degraded",
        "audit_mark": "🟢" if ok else "🔴",
        "self_test": ok,
        "datasets": dataset_status,
        "dataset_dir": DATASET_DIR,
        "truncate_chars": TRUNCATE_CHARS,
    }


@app.post("/v1/financial/assess")
def assess(req: AssessRequest):
    try:
        if req.weights is not None:
            engine.weights = req.weights
        if req.tolerance is not None:
            engine.tolerance = req.tolerance
        result = engine.assess(req.data)
        result["_dna"] = content_dna(req.data)
        result["_audit"] = "🟡 输入口径由调用方声明·引擎零黑箱"
        return result
    except Exception as e:  # 零黑箱：错误显式返回，不吞
        raise HTTPException(422, f"评估失败: {e}")


@app.post("/v1/financial/report")
def report(req: ReportRequest):
    try:
        text = engine.report(req.data, lang=req.lang)
        return {
            "lang": req.lang,
            "report": text,
            "_dna": content_dna(req.data),
            "_audit": "🟡 文本报告·口径见报告内公式",
        }
    except Exception as e:
        raise HTTPException(422, f"报告生成失败: {e}")


@app.post("/v1/financial/explain")
def explain(req: ExplainRequest):
    try:
        text = engine.explain(req.data)
        return {
            "explanation": text,
            "_dna": content_dna(req.data),
            "_audit": "🟡 零黑箱解释·逐公式自报口径",
        }
    except Exception as e:
        raise HTTPException(422, f"解释生成失败: {e}")


@app.get("/v1/dataset/{name}/stats")
def dataset_stats(name: str):
    recs = _load_dataset(name)
    return {"dataset": name, "file": DATASET_FILES[name], ** _dataset_stats(recs)}


@app.post("/v1/dataset/query")
def dataset_query(req: DatasetQuery):
    recs = _load_dataset(req.dataset)
    # request_id 前缀匹配（如 REQ-b59745a2-005 传 b59745a2）
    if req.request_id:
        recs = [r for r in recs if req.request_id in r.get("request_id", "")]
    if req.verdict:
        recs = [r for r in recs if r.get("verdict") == req.verdict]
    if req.category:
        # attack_category 是 list，需匹配元素（如 ['编码绕过','索要内核代码']）
        recs = [r for r in recs if req.category in [str(x) for x in (r.get("attack_category") or [])]]
    if req.keyword:
        recs = [r for r in recs
                if req.keyword in (r.get("prompt", "") + " " + r.get("rejection_reason", ""))]
    hits = recs[: req.limit]
    out = []
    for r in hits:
        item = {k: v for k, v in r.items() if k != "response"}
        if req.include_response:
            item["response"] = _truncate(r.get("response", ""))
        out.append(item)
    return {"total_matches": len(recs), "returned": len(out), "records": out}


@app.get("/v1/references")
def references():
    return {"guide": "CALIBRATION_DATASET_USAGE_GUIDE.md §9B", "anchors": REFERENCES}


# ═══════════════════════════════════════════════════════════════
# 入口（兼容 uvicorn 与直接运行）
# ═══════════════════════════════════════════════════════════════
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("LH_API_PORT", str(DEFAULT_PORT)))
    uvicorn.run(app, host="127.0.0.1", port=port, log_level="info")
