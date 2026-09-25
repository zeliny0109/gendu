# 中考题库数据格式

所有整理后的数据放在 `zhongkao/data/<科目>/`，会提交到公开仓库；`zhongkao/raw/` 只在本机（.gitignore 排除）。

科目代号：yuwen 语文 · shuxue 数学 · yingyu 英语 · wuli 物理 · huaxue 化学 · daofa 道德与法治 · lishi 历史

## 1. 考点表 `data/<科目>/kp.json`

```json
{
  "subject": "wuli",
  "modules": [
    { "id": "M1", "name": "声学", "kps": [
      { "id": "wuli.sound.production", "name": "声音的产生与传播", "grade": "八上", "desc": "一句话说明考什么" }
    ]}
  ]
}
```
- 考点按**教材章节/课标主题**分模块，粒度以“一节课能讲清、一道题主要考它”为准，每科 40–120 个。
- `grade`：该知识点在人教/仁爱等福建通用教材里所在年级学期（七上/七下/八上/八下/九上/九下），不确定写 `"?"`。
- id 只用小写字母、数字、点、下划线，一经使用不再改名。

## 2. 真题 `data/<科目>/papers/<年份>.json`

```json
{
  "subject": "wuli", "year": 2026, "source": "福建省教育考试院《试题、参考答案》合订本（福州市教育局转载）URL",
  "total": 100, "minutes": 90,
  "materials": [
    { "id": "m1", "text": "共用材料/阅读文章/情境（Markdown，可含 $LaTeX$）", "figures": ["figs/2026-m1-1.png"] }
  ],
  "questions": [
    {
      "id": "wuli-2026-12",            // <科目>-<年份>-<题号>[-<小问>]
      "no": "12",                      // 试卷上的题号（小问写 "17(2)"）
      "section": "选择题",              // 试卷上的大题名
      "type": "choice",                // choice 单选 | multi 多选 | blank 填空 | short 简答/解答/材料题 | draw 作图 | essay 写作 | listening 听力
      "score": 2,
      "material": "m1",                // 可选：引用 materials 里的 id
      "stem": "题干（Markdown；公式用 $...$ 的 LaTeX；空用 ____）",
      "options": ["A. …", "B. …", "C. …", "D. …"],   // 选择题才有
      "figures": ["figs/2026-12-1.png"],             // 题目用到的图，路径相对 data/<科目>/
      "answer": "官方参考答案原文（选择题只写字母）",
      "rubric": "官方评分要点（如有）",
      "kp": ["wuli.sound.production"],  // 1–3 个，必须存在于 kp.json；第一个是主考点
      "difficulty": 2,                  // 1 易 2 中 3 难（你的判断）
      "note": "转录存疑之处（看不清的字、图中信息缺失等），没有就省略"
    }
  ]
}
```
- **只转录，不改写**：题干、选项、答案照官方原文；看不清的用 `[?]` 标出并写进 note，绝不猜测补全。
- 答案以官方参考答案为准；官方没有的写 `""`，不要自己编。
- 图：从页面图裁出（PIL），PNG，宽不超过 800px，放 `data/<科目>/figs/`。纯文字能描述清楚的表格改成 Markdown 表格，不要截图。
- 英语听力：只收录题目和答案，音频没有，`type` 写 `listening`。

## 3. 统计 `data/<科目>/stats.json`（由脚本生成，不手写）
`python3 tools/zk_stats.py <科目>`：每个考点出现的年份、次数、总分值。

## 校验
`python3 tools/zk_validate.py <科目>`：检查 JSON 结构、id 唯一、kp 都存在、图文件存在、分值合计等于 total。

## 4. 讲解 `data/<科目>/lessons.json`

```json
{ "wuli.elec.ohm": "## 考什么\n…\n\n## 要点\n- …\n\n## 易错点\n- …\n\n## 真题精讲\n### 2025 年第 30 题 [[q:wuli-2025-30-1]]\n…" }
```
- 键是考点 id，值是 Markdown。App 支持：`## 小标题`、`- 列表` / `1. 列表`、`**粗体**`、表格、`![](figs/…)` 图、数理化的 `$LaTeX$`，以及 `[[q:题目id]]`（渲染成“做这道真题”链接）。段落之间空一行。
- 固定四节：**考什么**（福建近年怎么考：题型、位置、分值、趋势，依据 stats 和真题）→ **要点**（知识、公式、方法、答题模板）→ **易错点** → **真题精讲**（1–2 道，写思路和完整过程，结论必须与官方答案一致）。
- 300–900 字，写给九年级学生看，口语化、短句，不堆术语。
