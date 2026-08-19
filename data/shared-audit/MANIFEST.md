# 龍魂共享审计数据集 · MANIFEST v1.0

| 项 | 值 |
|:---|:---|
| 数据集文件 | `longhun-shared-audit-dataset-v1.0.jsonl` |
| 总条数 | 19（推理 18 + 监管防火墙 1） |
| 模型覆盖 | longhun-v1.7:latest, longhun-v1.8:latest, regulatory-firewall-v2.0 |
| 类别覆盖 | 伪装权威, 数据泄露, 未分类, 权限审计-🔴, 索要内核代码, 编码绕过, 角色扮演, 道德困境 |
| 源数据 | `11_DATA/feedback_loop/feedback_pool.jsonl`（83条对抗流水线）+ `audit_log.jsonl`（220条审计） |
| 提取引擎 | `08_BIN/lh_shared_audit_extract.py` |
| SHA-256 | `b1a8a650b8038b21505396ea869911008781b26a3adf39ad730edc3d99a2e7f3` |
| 提取时间 | 2026-08-19 |
| 诚实声明 | 只含源日志真实字段；未编造 inference_time_ms/tokens_used |
| DNA | #龍芯⚡️丙午·丙申·癸酉·亥时-SHARED-DATASET-v1.0-UID9622 |
