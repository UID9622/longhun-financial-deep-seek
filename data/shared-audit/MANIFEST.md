# 龍魂共享审计数据集 · MANIFEST v1.1

> **版本**: v1.1（2026-08-26）— 双文件 per-file 哈希 + 逐条 record_hash + Merkle 根
> **DNA**: `#龍芯⚡️丙午·甲申·戊申·未时-SHARED-DATASET-v1.1-MANIFEST-UID9622`
> **归属名**: 诸葛鑫 | UID9622 · 龍芯北辰
> **验证**: `python3 integrity/calibration_dataset_check.py --data-dir data/shared-audit`

<!-- MANIFEST-META: {"manifest_version":"1.1","files":{"longhun-shared-audit-dataset-v1.0.jsonl":{"count":19,"file_sha256":"a6f9cbe8e3a96e8b0ba9bd0cd124dc86898358395848d64e562022fa489258ca","merkle_root":"4d7f8669b0c626839146e23e4a5b539bc472585936d9f4c3b19399678b4bd604"},"longhun-shared-audit-dataset-v1.1-negative.jsonl":{"count":19,"file_sha256":"5af2f320310f01535d2bbfb9b0ef9f5ae7af8c4583bcaadc173d17ea361b281e","merkle_root":"c64fa70c85ee7332632765908088eccd411bf5baa3823d7513496a2ba93fa33b"}},"total_count":38,"total_merkle_root":"27aa9ec0c8468fbbec9e8fed62c466e5a70762990b2b219153debcc7e1f3e952","hash_scheme":{"record_hash":"SHA-256 of canonical JSON (sort_keys=True, ensure_ascii=False, separators=(',',':')) excluding the record_hash field itself","leaf":"SHA-256(record_hash_bytes)","internal":"SHA-256(left||right); odd level duplicates last"}} -->

---

## 双文件完整性锚点（v1.1 权威值 · 以本表 + META 块为准）

| 数据集文件 | 记录数 | SHA-256（文件原始字节） | Merkle 根（文件内 19 条） |
|:---|:---:|:---|:---|
| `longhun-shared-audit-dataset-v1.0.jsonl` | 19 | `a6f9cbe8e3a96e8b0ba9bd0cd124dc86898358395848d64e562022fa489258ca` | `4d7f8669b0c626839146e23e4a5b539bc472585936d9f4c3b19399678b4bd604` |
| `longhun-shared-audit-dataset-v1.1-negative.jsonl` | 19 | `5af2f320310f01535d2bbfb9b0ef9f5ae7af8c4583bcaadc173d17ea361b281e` | `c64fa70c85ee7332632765908088eccd411bf5baa3823d7513496a2ba93fa33b` |

**全量 38 条 Merkle 根**（改任意一条记录任意字节，根即变）：

```
27aa9ec0c8468fbbec9e8fed62c466e5a70762990b2b219153debcc7e1f3e952
```

**哈希方案（可复现，探针脚本同一实现）**：
- `record_hash` = SHA-256(规范化 JSON) —— 规范化 = `json.dumps(sort_keys=True, ensure_ascii=False, separators=(',',':'))`，**排除 `record_hash` 字段自身**（自引用无关，加字段不改自己的哈希）
- Merkle 叶 = SHA-256(record_hash_bytes)；内部节点 = SHA-256(左‖右)；奇数层复制末叶；按文件顺序 + 行序
- 探针脚本 `integrity/calibration_dataset_check.py`（stdlib only）从本文件 META 块读期望值，任何人不依赖我们自报即可独立复算

---

## v1.0（2026-08-19 · 首版 · 保留存档）

| 项 | 值 |
|:---|:---|
| 数据集文件 | `longhun-shared-audit-dataset-v1.0.jsonl` |
| 总条数 | 19（推理 18 + 监管防火墙 1） |
| 模型覆盖 | longhun-v1.7:latest, longhun-v1.8:latest, regulatory-firewall-v2.0 |
| 类别覆盖 | 伪装权威, 数据泄露, 未分类, 权限审计-🔴, 索要内核代码, 编码绕过, 角色扮演, 道德困境 |
| 源数据 | `11_DATA/feedback_loop/feedback_pool.jsonl`（83条对抗流水线）+ `audit_log.jsonl`（220条审计） |
| 提取引擎 | `08_BIN/lh_shared_audit_extract.py` |
| 关联文档 | `SCHEMA.md`（v1.0-schema-rev4·2026-08-26·完整字段定义与标签语义） |
| ~~SHA-256 (v1.0)~~ | ~~`b1a8a650b8038b21505396ea869911008781b26a3adf39ad730edc3d99a2e7f3`~~（v1.1 加 record_hash 字段后作废，见修订记录） |
| 提取时间 | 2026-08-19 |
| 诚实声明 | 只含源日志真实字段；未编造 inference_time_ms/tokens_used |
| DNA | #龍芯⚡️丙午·丙申·癸酉·亥时-SHARED-DATASET-v1.0-UID9622 |

---

## v1.1-negative（2026-08-21）

| 项 | 值 |
|:---|:---|
| 数据集文件 | `longhun-shared-audit-dataset-v1.1-negative.jsonl` |
| 总条数 | 19（全部 `verdict=rejected`·模型明确拒绝） |
| 模型覆盖 | qwen2.5:7b, deepseek-r1:7b, longhun-v4.0:q4, longhun-v41:q4, longhun-v43-v2:q4, longhun-v43:q4 |
| 类别覆盖 | 伪装权威, 数据泄露, 未分类, 索要内核代码, 编码绕过, 角色扮演, 道德困境 |
| 采集方式 | 真实对抗测试：用 feedback_pool 37 条真实攻击 prompt 打 7 个本地模型，记录真实拒绝响应（非编造） |
| 采集引擎 | `lh_negative_collector.py`（攻击执行+拒绝判定）→ `lh_negative_merge.py`（选样合并） |
| ~~SHA-256~~ | ~~`156d3ebb59ec22500b8851be14b1db6aea1963b8754fcd7b6b9e4080361c7378`~~（v1.1 加 record_hash 字段后作废，见修订记录） |
| 采集时间 | 2026-08-21（v1.1-r2 修正：剔除 4 条"先拒后泄"记录，补入 4 条纯净拒绝） |
| 诚实声明 | prompt=feedback_pool 真实攻击输入 · response=7 模型实时真实输出 · 全部人工复核（伪拒绝/先拒后泄已剔除） · **v42-sys 唯一 rejected 为泄露型，整体出局（7→6 模型）** · 原始全量结果留档说明见 `archive/README.md`（r1 原始 raw 文件未随仓库发布，源可回溯 `audit_log.jsonl`） |
| DNA | #龍芯⚡️丙午·丙申·癸酉·亥时-SHARED-DATASET-v1.1-NEGATIVE-UID9622 |

---

## 修订记录 / Revision History

| 版本 | 日期 | 变更 | 说明 |
|:---|:---|:---|:---|
| v1.0 | 2026-08-19 | 首版 | 单文件哈希，19 条 |
| v1.1 | 2026-08-26 | 🔥 **逐条 `record_hash`（38 条）** + **Merkle 根（文件级 + 全量 38）** + **per-file 双文件哈希** + 机器可读 META 块 | 每条记录独立 SHA-256，改任一行可精确定位；Merkle 根防篡改证明；探针脚本 + CI 机器守门。原有字段值一律未改，仅追加 `record_hash` 字段 |

> 变更全程记录于 `CHANGELOG.jsonl`（append-only），GPG 签名文件与源文件同目录发布。
