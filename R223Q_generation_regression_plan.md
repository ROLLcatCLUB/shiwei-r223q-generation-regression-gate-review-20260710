# R223Q true generation regression gate plan

stage_id: 1013R_R223Q_TRUE_GENERATION_REGRESSION_GATE  
status: fixture_driven_generation_regression_gate  
decision: PASS_CONTINUE_TO_R223R_V0_2_CANDIDATE_PILOT_ROUTE_PLANNING

## 定位

R223Q 验证 R223P-5 锁定的 `R223M classroom_event_standard v0.2 candidate` 是否能进入“生成回归门”。本轮只做 fixture-driven / sandbox generation regression，不接正式 runtime，不接 provider/model，不改 prompt，不写库，不改 R223M/N/O 既有稿。

## 本轮验证什么

1. `unit_phase_role` 和 `practice_intensity` 是否能控制课堂展开密度。
2. 是否能选择合适的课堂实践模式。
3. 示范、小练、赏析等条件字段是否只在需要时启用。
4. 教师默认稿是否仍然是成熟教案文稿，不出现字段墙。
5. review ledger 是否完整保存新字段。
6. 大屏、组件、学习单、评价证据是否从课堂事件派生。
7. 未注册组件和 new surface candidate 是否不进入教师默认稿。

## 样本

| sample_id | 课题 | 课型侧重 | 期望密度 |
| --- | --- | --- | --- |
| M_stationery | 我为文具代言 第三阶段 | 设计应用 / 高实践密度 | high |
| N_paper_print | 有趣的纸印 | 材料技法 / 中实践密度 | medium |
| O_color_collision | 色彩的碰撞 | 色彩感知 / 理解导入 | medium |

## 通过线

```text
每个样本生成教师默认稿
每个样本生成 review ledger
教师默认稿无字段名外露
review ledger 有 unit_phase_role、practice_intensity、primary_pattern、组件状态
不同课型展开密度有可见差异
未注册组件不进入教师默认稿
不发布正式 v0.2
不接正式 runtime/model/prompt/db
```

