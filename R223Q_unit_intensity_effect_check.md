# R223Q unit intensity effect check

stage_id: 1013R_R223Q_TRUE_GENERATION_REGRESSION_GATE  
status: unit_intensity_effect_check

## 三样本密度差异

| sample | unit_phase_role | practice_intensity | 生成表现 |
| --- | --- | --- | --- |
| M_stationery | practice_creation | high | 创作推进更重，教师巡视、过程照片、材料理由、展示迁移更重 |
| N_paper_print | technique_preparation | medium | 材料观察、示范、小块试印、作品保底适中 |
| O_color_collision | intro_understanding | medium | 生活色彩入场、实验记录、色彩表达，不扩成大创作 |

## 判断

`unit_phase_role + practice_intensity` 对生成密度产生了可见影响。文具课明显更重，纸印课与色彩课保持中等密度，但重心不同。

```text
unit_intensity_effect = PASS
```

