# 🐉 Longhun Financial Deep Seek · 龍魂·金融深度求索引擎

> DNA: `#龍芯⚡️丙午·丙申·癸亥·巳时·䷒临-FINANCIAL-DEEP-SEEK-v2.0-E7E9A326`
> 创建者: 诸葛鑫（UID9622）· 退役老兵，为中国普通人的数字主权而战
> License: MulanPSL v2 · 开源可商用 · 署名·专利授权

**A transparent, reproducible, audit-ready financial health assessment engine.**
**一个零黑箱、可复现、可对拍的财务健康评估引擎。**

---

## Why It Exists · 为什么存在

This project was born from a real problem surfaced in the DeepSeek-V3 community
discussion (issue #1466): reports whose **numbers cannot be reproduced, whose
formulas are not self-declared, and whose aggregate scores disagree with their
own itemized details**.

龍魂's answer: **no black box**. Every number must trace back to an input, a
formula, and a version. This engine encodes that principle into every output.

本项目源于 DeepSeek-V3 社区讨论（issue #1466）暴露的真实病根：
**数字口径不自声明、不可复现、明细与聚合对不上**。龍魂的答案是：零黑箱——
每个输出可追溯到输入 + 公式 + 版本。

## Core Design · 核心设计

| Principle | Implementation |
|:---|:---|
| ① Content-addressed DNA | Same input + same formula version → same DNA → reproducible & comparable (no more `time.time()`) |
| ② Metric contract / 口径锁 | Every dimension carries `formula + version + inputs_hash` — numbers always declare their own 口径 |
| ③ Detail–aggregate reconciliation / 对拍 | `declared_scores` vs engine recomputation; deviation beyond tolerance → 🟡 MISMATCH |
| ④ Golden regression / 黄金回归 | Fixed anchor data + expected values; `--self-test` proves numbers never drift |
| ⑤ True digital root / 真·数字根 | 369 base: `dr(n) = 1 + ((n-1) mod 9)` |
| ⑥ Weight A-BOM declaration | Weights declare source & rationale; overridable via `--weights` |

**Five dimensions:** liquidity · debt · efficiency · profitability · stability
（流动性 · 负债 · 效率 · 盈利 · 稳定）

## Quick Start · 一键运行

```bash
# No dependencies — pure Python 3.8+ stdlib
python3 lh_financial_deep_seek.py                                   # demo mode
python3 lh_financial_deep_seek.py '{"current_assets":500000,"total_assets":1000000}'   # your data
python3 lh_financial_deep_seek.py --self-test                        # golden regression (12 anchors)
python3 lh_financial_deep_seek.py --explain                          # human-readable explanation
python3 lh_financial_deep_seek.py --weights '{"liquidity":0.3,"debt":0.2,"efficiency":0.2,"profitability":0.2,"stability":0.1}'  # custom weights
```

## Sample Output · 输出示例

```
🐉 Longhun Financial Deep Seek Report
======================================================
DNA: #龍芯⚡️FIN-DEEP-SEEK-v2.0-BB5A8524
Metric Contract: engine=longhun_financial_deep_seek version=v2.0 inputs=921ccee4d332
Composite Score: 0.6896
Digital Root: 6
Risk Level: 🟡 Fair
Reconciliation: SKIPPED
------------------------------
Dimension Scores (formula-versioned):
  liquidity     : 0.8333  | clamp01(current_assets / (current_liabilities × 3))
  debt          : 0.7000  | clamp01(1 - total_debt / total_assets)
  efficiency    : 0.4000  | clamp01(revenue / (total_assets × 2))
  profitability : 0.8000  | clamp01(net_income / (total_assets × 0.15))
  stability     : 0.6750  | clamp01(1 - (volatility + (1 - consistency)) / 2)
======================================================
```

## Verification · 验证

```bash
python3 lh_financial_deep_seek.py --self-test
# golden[healthy_sme]    composite=0.9038 (exp 0.9038) dr=9  level=Excellent  🟢
# golden[mid_sme]        composite=0.6896 (exp 0.6896) dr=6  level=Fair       🟢
# golden[distressed_sme] composite=0.0683 (exp 0.0683) dr=7  level=Critical  🟢
```

## Input Contract · 输入

| Field | Meaning |
|:---|:---|
| `current_assets` | 流动资产 |
| `current_liabilities` | 流动负债 |
| `total_debt` | 总负债 |
| `total_assets` | 总资产 |
| `revenue` | 营业收入 |
| `net_income` | 净利润 |
| `volatility` | 波动率 [0,1] |
| `consistency` | 一致性 [0,1] |
| `declared_scores` (optional) | 外部系统声明的各维度分，用于明细-聚合对拍 |

## 📊 Shared Audit Dataset · 共享审计数据集

> 回应 DeepSeek-V3 #1466 跨框架验证提议：提供一批**真实运行系统中提取**的推理审计日志，
> 供 TAT / Cophy / HeartFlow 等框架在同一批数据上做并排放置验证。

- 数据文件: [`data/shared-audit/longhun-shared-audit-dataset-v1.0.jsonl`](data/shared-audit/longhun-shared-audit-dataset-v1.0.jsonl)
- 校验清单: [`data/shared-audit/MANIFEST.md`](data/shared-audit/MANIFEST.md)
- 提取引擎: [`data/shared-audit/lh_shared_audit_extract.py`](data/shared-audit/lh_shared_audit_extract.py)

**诚实声明**: 19 条记录全部来自真实对抗流水线 + 监管防火墙运行日志，
非人工合成；只含源日志真实字段，未编造 `inference_time_ms` / `tokens_used`；
SHA-256 校验可复现。

```
SHA-256: b1a8a650b8038b21505396ea869911008781b26a3adf39ad730edc3d99a2e7f3
```

## ⚠️ Disclaimer · 免责声明

Output is a financial health screening reference only — **NOT investment advice**.
本引擎输出仅作财务体检参考，**不构成投资建议**。

## Ecosystem · 龍魂生态

龍魂系统（Longhun System）是中国本土 AI 治理与主权算法体系，由退役老兵
UID9622 一个人构建：20 AI 人格 · 192 引擎 · 三色审计 · DNA 全链路追溯 ·
369 洛书不动点底座。本算法是龍魂开源生态的一员。

---

**Made by a Chinese veteran for ordinary people. 退伍老兵，为人民写代码。**
