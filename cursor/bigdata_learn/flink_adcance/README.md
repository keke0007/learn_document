# Flink Advance（Time / Window / State / Checkpoint）学习目录

本目录用于补齐 `flink/` 中“基础入门”之外的 **Flink 进阶四件套**学习：**Time（时间）**、**Window（窗口）**、**State（状态）**、**Checkpoint（检查点）**。

推荐阅读顺序：
- `GUIDE.md`：进阶指南（费曼法讲解 + 案例 + 验证数据 + 一页速查）
- `cases/`：拆分后的 4 个可验证案例（Time / Window / State / Checkpoint）
- `data/`：可直接用来验证的小数据集

案例索引：
- `cases/README.md`：案例总览索引页
- `cases/01_time_watermark_lateness.md`：Event Time / Watermark / Allowed Lateness / Side Output
- `cases/02_window_sliding_overlap.md`：滑动窗口重叠（10s 窗口，5s 滑动）
- `cases/03_state_keyed_fail_alert.md`：Keyed State + 定时器（60s 内 3 次 FAIL 告警）
- `cases/04_checkpoint_failover_recovery.md`：Checkpoint + 故障注入 + 重启恢复状态
- `cases/05_production_issues_best_practices.md`：生产常见问题与最佳实践清单（含案例 Runbook）

目录结构：
```
flink_adcance/
├── README.md
├── GUIDE.md
├── cases/          # （可选）拆分后的案例文档
├── data/           # 验证数据
└── scripts/        # （可选）脚本/配置
```

