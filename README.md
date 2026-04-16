# book2courseware

把任何**教案 / 课本章节**一键转成**单文件互动 HTML 课件**的 Claude Code skill。

- 📐 固定的视觉令牌（大字号、手绘笔记本风、彩色关键词高亮）
- 🧩 13 个内容组件（封面、流程链、对比、柱状图、时间轴、填空、选择题、小游戏、网络素材卡……）
- 🎮 强制至少 1 个互动小游戏
- ✏️ 浏览器内编辑器内置 —— 用户可以在打开的课件里直接改文字 / 改 SVG / 删页 / 下载修改版
- 🖨️ 打印友好（填空在 print 模式自动显示答案，导航栏隐藏）
- 🌐 联网素材自动嵌入（百度百科图 / bilibili 视频，全部 base64 内嵌，断网也能看）
- 🖥️ 单 HTML 文件输出，零依赖，发邮件 / U 盘拷贝即可分发

## 在线 demo

`examples/` 目录有 4 份成品课件，直接双击 `.html` 在浏览器打开：

| # | 学科 | 章节 | 文件 |
|---|---|---|---|
| 01 | 地理 · 必修一 | 第二章 地球上的大气 | [`examples/01-地理-大气组成与垂直分层/index.html`](examples/01-地理-大气组成与垂直分层/index.html) |
| 02 | 物理 · 必修三 | 第十三章 电磁感应与电磁波初步 | [`examples/02-物理-电磁感应与电磁波/第十三章_电磁感应.html`](examples/02-物理-电磁感应与电磁波/第十三章_电磁感应.html) |
| 03 | 地理 · 必修二 | 第四章 交通运输布局与区域发展 | [`examples/03-地理-交通运输布局/地理必修二第四章.html`](examples/03-地理-交通运输布局/地理必修二第四章.html) |
| 04 | 化学 · 必修一 | 第二章第二节 氯及其化合物 | [`examples/04-化学-氯及其化合物/chlorine_courseware.html`](examples/04-化学-氯及其化合物/chlorine_courseware.html) |

每份课件包含 15–25 张幻灯片：封面 → 节次 → 概念解释 → 流程图 → 对比页 → 填空 → 选择题 → 小游戏 → 真实联网素材 → 小结。

操作快捷键：
- `← →` 翻页
- `↑ ↓` / 滚轮 滑动长页
- 点击填空查看答案
- 点击选择题选项立即反馈
- 右上角 `✏️ 编辑模式` 可二次编辑并下载

## 安装为 Claude Code skill

```bash
git clone https://github.com/HalfMoon001/book2courseware.git
mkdir -p ~/.claude/skills
cp -R book2courseware ~/.claude/skills/
```

之后在 Claude Code 里随便说一句"用这份教案生成互动课件"，skill 会自动触发。

也可以用 slash command 直接调起：

```
/book2courseware 用教案/4/中的内容，节选第二章第二节生成一份互动课件
```

## 工作流（Claude 会自动按这个顺序走）

```
1. 读教案    →  调用 pdf / docx skill；扫描版 PDF 渲染图像后视觉读取
2. 结构化分解 →  把章节拆成 概念页 / 流程页 / 对比页 / 填空 / 测验 / 游戏
3. 装配 HTML  →  从 shell/ 和 components/ 取固定模板替换占位符
4. 联网素材   →  调用 web-access skill 抓百度百科图 / bilibili 视频 → base64 内嵌
5. 质量自检   →  跑 30 项 checklist（字号、关键词高亮、游戏数量、编辑器、打印友好…）
```

## 仓库结构

```
book2courseware/
├── SKILL.md                    # skill 入口（含完整工作流和硬性规则）
├── MANIFEST.md                 # 组件清单 + 决策表
├── web-search-workflow.md      # web-source-card 文字卡的抓取流程
├── shell/                      # 必用骨架，按顺序装配
│   ├── head.html               #   CSS 设计令牌 + 字体 + 共享 SVG markers
│   ├── nav.html                #   底部导航栏
│   ├── scripts.js              #   翻页 / 填空 / 选择题 / 小游戏
│   └── editor.html             #   ~55KB 浏览器内编辑器（55K 行 IIFE，独立 bundle）
├── components/                 # 13 个内容组件，按需组合
│   ├── cover-slide.html        #   封面页
│   ├── section-divider.html    #   节次分隔页
│   ├── content-two-col.html    #   左 SVG + 右信息卡（最常用）
│   ├── info-card.html          #   彩色信息卡
│   ├── chain-process.html      #   流程链
│   ├── comparison-two-col.html #   对比两栏
│   ├── bar-chart.html          #   柱状图
│   ├── timeline.html           #   时间轴
│   ├── fill-blank-slide.html   #   填空（点击揭示）
│   ├── mcq-quiz.html           #   选择题（即时反馈）
│   ├── mini-game.html          #   互动小游戏
│   ├── web-source-card.html    #   网络文字卡
│   ├── media-embed.html        #   网络图片 / 视频卡
│   └── media-workflow.md       #   抓百度百科 + base64 内嵌操作流程
└── examples/                   # 4 份完整成品课件
    ├── 01-地理-大气组成与垂直分层/
    ├── 02-物理-电磁感应与电磁波/
    ├── 03-地理-交通运输布局/
    └── 04-化学-氯及其化合物/
        ├── chlorine_courseware.html   # 24 页成品
        └── _build_chlorine.py          # 装配脚本（参考实现）
```

## 设计原则（用户强制反馈，违反一条就翻车）

1. **字号锁死**：body 22 px / 标题 36 px / 封面 64 px —— 不可改小
2. **关键词彩色高亮**：用 `.keyword-red/blue/green/gold/purple`，1.1 em 加粗带浅底
3. **SVG 插图优先**：每个概念都要有视觉元素，纯文本页是最后手段
4. **填空只给必背内容**：一份课件 ≤ 1/5 的页是填空
5. **禁止点击翻转卡片**：不利于打印复习
6. **先解释再测试**：新概念第一次出现必须有定义页
7. **流程要分两种页面**：一页整体 SVG 动画 + 后续每一步单独一页
8. **必须有互动小游戏**：每份课件至少 1 个，>15 页建议 2 个
9. **打印友好**：`@media print` 下显示填空答案、隐藏导航
10. **SVG 箭头走 shared marker**：禁止 `<polygon>` 手画三角形
11. **垂直滚动允许**：`.slide` 用 `min-height:100vh`，不要 `overflow:hidden`
12. **编辑器必须打包**：`shell/editor.html` 必须插到 `</body>` 前

## 联网素材的硬性规则

中文学科课件首选**百度百科 CDN**（`bkimg.cdn.bcebos.com`，允许 hotlink），国际/英文主题用 Wikimedia Commons。**所有图片必须下载后 base64 data URI 内嵌**到 HTML —— 远程 URL 一律不允许（防盗链 / 离线打开 / 网页下架风险）。视频用 bilibili `iframe` 是唯一例外。

详见 [`components/media-workflow.md`](components/media-workflow.md)。

## 依赖的其它 skill

- **`pdf`** — 读取 PDF 教案（含扫描件 fallback）
- **`docx`** — 读取 Word 教案
- **`web-access`** — 所有联网操作的统一入口

这些 skill 由 book2courseware 的 SKILL.md 工作流主动调用。

## 反馈与协作

教案文件因为版权原因没有放进仓库。想自己跑一遍：
1. 准备一份你自己的 `.docx` / `.pdf` 教案
2. 在 Claude Code 里说："用这份教案生成互动课件"
3. 大约 5–10 分钟后 `output/` 目录会出现一份成品 HTML

欢迎提 issue 反馈：组件不够、布局漂移、新学科适配等。

## License

MIT —— skill 代码、组件模板、shell 骨架、装配示例均可自由使用、修改、分发。

`examples/` 中嵌入的少量百度百科图片（4 张化学教学示意图）属于教育用途引用，归原作者所有，不在 MIT 范围内。如需删除请提 issue。
