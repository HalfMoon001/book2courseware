# 组件清单 & 决策表

## 必用：Shell（按顺序装配）

| 文件 | 用途 | 插入位置 |
|---|---|---|
| `shell/head.html` | `<!DOCTYPE>` + `<head>` + CSS 设计令牌（含 media/game/editor 样式） + `<body>` 开头 | HTML 最顶部 |
| `shell/nav.html` | 底部导航栏（dots + 页码） | 所有 slide 之后 |
| `shell/scripts.js` | 翻页、填空、选择题、小游戏辅助 | nav 之后，`</body>` 之前 |
| `shell/editor.html` | **浏览器内编辑器**（CSS+UI+JS 全打包，~55KB）—— 提供右上角编辑按钮、抓手/铅笔模式、SVG 编辑、撤销重做、🗑 删页、保存/丢弃、下载 HTML | scripts.js 之后，`</body>` 之前 |

## 内容组件：按内容类型选

| 内容类型 | 推荐组件 | 备选 |
|---|---|---|
| 章节封面 | `cover-slide.html` | — |
| 节次分隔页 | `section-divider.html` | — |
| 概念解释（定义） | `content-two-col.html` + `info-card.html` × 2-4 | — |
| 并列要点（3-5 条） | `content-two-col.html` + `info-card.html` 多种颜色 | `chain-process.html` 如果有顺序 |
| 成分/占比数据 | `bar-chart.html` | — |
| 流程/因果链 | `chain-process.html` | — |
| 对比两种事物 | `comparison-two-col.html` | — |
| 时间发展/历史 | `timeline.html` | — |
| 必背知识点 | `fill-blank-slide.html` | — |
| 有唯一答案的考点 | `mcq-quiz.html` | `fill-blank-slide.html` |
| 真实世界案例/最新数据（文字） | `web-source-card.html`（见 `web-search-workflow.md`） | — |
| 经典实验/演示视频 | `media-embed.html` 视频形态（见 `media-workflow.md`） | — |
| 科学照片/示意图/地理实景 | `media-embed.html` 图片形态（见 `media-workflow.md`） | — |
| 互动游戏（判断/配对/分类） | `mini-game.html` + `shell/scripts.js` 里的 `gamePick()` | — |

## 单页容量建议

| 组件 | 单页最多几个 | 原因 |
|---|---|---|
| info-card | 5 | 超过会挤压字号 |
| bar 柱 | 6 | 柱太多看不清 |
| chain 步骤 | 5 | 超过要拆成多页 |
| fill-blank 空 | 6 | 超过认知负荷过重 |
| mcq 选项 | 4 | 传统单选题 |

## 配色语义

| 颜色变量 | 用于 |
|---|---|
| `--blue` `#4a90d9` | 概念、定义、中性信息 |
| `--red` `#e06b6b` | 关键要点、警告、下降趋势、填空标记 |
| `--green` `#5a9e6f` | 正确、增长趋势 |
| `--gold` `#c8880a` | 流程、高亮框、装饰线 |
| `--purple` `#7b68ee` | 技术性内容、高级知识 |

## 推荐幻灯片序列（一节课 10-20 页）

```
1.  封面 (cover-slide)
2.  节次分隔 (section-divider)
3-5. 概念解释页 (content-two-col + info-card)
6.  数据/占比页 (bar-chart) 若有
7-9. 流程页 (chain-process 整体 + 分步 content-two-col)
10. 对比页 (comparison-two-col) 若有
11. 填空练习 (fill-blank-slide)
12. 选择题练习 (mcq-quiz)
13. **互动小游戏 (mini-game)** —— 至少 1 个，>15 页建议 2 个
14. 真实案例 (web-source-card) 或 经典视频/图片 (media-embed) 若适用
15. 小结 (content-two-col + chain-process 回顾)
```

根据教案内容增减，但**封面 → 分节 → 定义 → 练习 → 游戏**的大结构不要打乱。

## 共享 SVG 箭头 markers（`head.html` 已预置）

画任何方向/矢量箭头一律用：
```html
<line x1=".." y1=".." x2=".." y2=".." stroke="var(--gold)" stroke-width="3" marker-end="url(#arr-gold)"/>
```
可用 marker：`arr-red` / `arr-blue` / `arr-green` / `arr-gold` / `arr-purple` / `arr-dark` / `arr-orange`。
**禁止** 用 `<polygon points="...">` 手画三角形作为箭头 —— 旋转的线上三角坐标算不准。
椭圆/圆切向箭头：在 `(cx, cy+ry)`（底部）放 10px 水平线 + `marker-end`，物理含义 = 右手定则 CCW 时近侧切向。
