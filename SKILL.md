---
name: book2courseware
description: Convert any lesson plan (教案/课本章节) into a single-file interactive HTML courseware. Subject-agnostic — reuses fixed, tested components (封面、分节、填空、选择题、流程链、柱状图、对比、时间轴、信息卡、网络来源卡、视频/图片嵌入、小游戏) and bundles an in-browser editor. Use when user asks to turn 教案/课本/textbook into 互动课件/PPT/HTML, or mentions "教案转HTML", "做课件", "生成互动页面", "book2ppt".
---

# book2courseware — 教案转互动 HTML 课件

## 核心原则

**不要从零写 CSS、布局、交互 JS。全部从 `shell/` 和 `components/` 里取固定代码，只替换占位符。**

这是为了保证"及格线"质量：组件已经在 `book2ppt` 项目的 30 页参考实现里跑通过，视觉、打印、键盘翻页、填空、选择题反馈都验证过。从零生成很容易样式错位、字号太小、交互坏掉。

## 设计规则（用户强制反馈，不要违背）

1. **字号要大** —— body 22px / 标题 36px / 封面 64px，这套令牌锁死，不要改小
2. **关键词用彩色高亮** —— 用 `.keyword-red/blue/green/gold/purple` 类，每个关键词 1.1em 加粗带浅色背景
3. **SVG 插图优先** —— 每个概念至少配一个视觉元素；纯文本页是最后手段
4. **填空只给必背内容** —— 不要一整页都是填空
5. **禁止点击翻转卡片** —— 不适合打印复习，用填空或选择题代替
6. **先解释概念再测试** —— 新概念第一次出现必须有定义页
7. **流程要分两种页面** —— 一页是整体 SVG 动画，后续每一步单独一页（左侧整体图+当前步骤高亮，右侧细节文字）
8. **必须有互动小游戏** —— 每份课件**至少 1 个**小游戏（>15 页的建议 2 个）。用 `components/mini-game.html` 模板，配合 `shell/scripts.js` 里的 `gamePick()` 函数。游戏适合：应用场景配对、规则判断（如右手定则）、分类、顺序判断。不适合纯计算或开放题。**没有游戏的课件视为不及格。**
9. **选择题可替代填空** —— 对有唯一答案但不必死记的知识点，用选择题
10. **打印友好** —— 所有交互元素在 `@media print` 下必须显示答案，导航栏隐藏（shell 里已实现，不要破坏）
11. **SVG 箭头用 marker，不要手画三角形** —— head.html 里已预置 7 个共享 marker（`arr-red/blue/green/gold/purple/dark/orange`）。画矢量/方向指示时一律用 `<line ... marker-end="url(#arr-gold)"/>` 或 `marker-start`，禁止 `<polygon points="...">` 当箭头——旋转的线上坐标会算错，视觉上三角会"飘"。椭圆/圆上的切向箭头：在 `(cx, cy+ry)`（底部）放一条 10px 水平线 `<line x1="cx-10" ... x2="cx" y2="cy+ry" marker-end="url(#arr-*)"/>`，物理含义=右手定则 CCW 在近侧的切向。
12. **页面允许垂直滚动** —— slide 内容超过一屏时，页面会自然变高，用户用鼠标滚轮 / Up/Down 键可以滑动查看。`.slide` 用 `min-height:100vh` 不是 `height`，`.slide-col` 不再 `overflow:hidden`。**不要重新加 `overflow:hidden`** ——那会把内容截掉导致"有东西看不到"。
13. **编辑器打包进每份课件** —— `shell/editor.html`（约 55KB）里封装了完整的浏览器内编辑器（抓手/铅笔模式、SVG 属性面板、撤销/重做、🗑 删页、保存/下载）。**必须**插到 `</body>` 前。右上角的"✏️ 编辑模式"按钮是入口；开启后用户可以直接在浏览器里改文字、改 SVG、调整布局、删除整页，然后点"📥 下载"导出修改版。编辑器内部 override 了 `window.goTo` 以支持结构性变化（新增/删除 slide），`getSlideContent` 以 `outerHTML` 快照，保证删页也能撤回。

## 依赖的其它 skill（本 skill 会调用）

本 skill 在工作流里会**主动调用**以下其它 skill，发现匹配场景立即按名字 invoke，不要自己复写它们的工作：

| 场景 | 该用哪个 skill | 用途 |
|---|---|---|
| 读取 `.pdf` 教案 / 教材 | **`pdf`** | 文字型 PDF 提取文字、表格、结构；扫描型 PDF 渲染页面图像后再视觉读取 |
| 读取 `.docx` 教案 | **`docx`** | Word 文档解析 |
| **任何联网操作**（搜图、找视频、抓 URL、下载素材） | **`web-access`** | 统一入口。包括 WebSearch / WebFetch / 浏览器交互 / 登录后操作 / 动态渲染页面。细节见下面 Step 4。 |

> ⚠️ 本 skill 文档里出现的 `WebSearch(...)` / `WebFetch(...)` 等调用，**在实际 session 里都应走 `web-access` skill**，不要直接调用原始工具。`web-access` 负责处理防盗链、登录态、referer 等细节。

## 工作流

### Step 1 — 读教案
用户会给一个 docx/pdf 教案，或者直接粘贴大纲。

**读取方式**：
- `.pdf` → 调用 **`pdf` skill**
- `.docx` → 调用 **`docx` skill**
- 纯文本 / markdown → 直接 Read

**扫描版 PDF 的特殊处理**（重要 · 本 session 踩过）：
教材帮、教辅、老课本等常常是**扫描件**，PDF 里没有文字层。`pdf` skill 的文本提取会返回空。这时：
1. 用 `pdf` skill 或 `pymupdf` (`fitz`) 把每一页（或目标章节附近的页）**渲染成低分辨率 PNG**（matrix 0.5–0.8 即可）
2. 用 Read 工具**逐页视觉读取**（Claude 是多模态，可以直接看图）
3. 先看目录页（前 5–10 页）→ 定位目标章节大致页码 → 再渲染那段区间的每一页

示例骨架：
```python
import fitz
doc = fitz.open(path)
mat = fitz.Matrix(0.6, 0.6)
for i in range(start, end):
    doc[i].get_pixmap(matrix=mat).save(f'/tmp/p{i:03d}.png')
```
然后 `Read('/tmp/p069.png')` 看具体内容。

然后**不要直接生成 HTML**，先做结构化分解：

```
Chapter: {{chapter name}}
  Section 1: {{section title}}
    - Concept A (definition) → 需要解释页
    - Concept B (list of N items) → 需要并列信息卡页
    - Process C (N steps) → 需要流程整体页 + N 个步骤页
    - Data D (percentages/numbers) → 需要柱状图/时间轴
    - Must-memorize fact E → 需要填空页
    - Judgment question F → 需要选择题页
    - Real-world example G → 可能需要 web-source-card（调用 WebSearch）
```

输出这份结构化清单给用户确认，**再**开始装配。

### Step 2 — 为每块内容挑组件
查 `MANIFEST.md` 的决策表。每个内容类型有推荐组件，别自己发明。

### Step 3 — 装配 HTML
顺序：
1. 复制 `shell/head.html` 作为 HTML 头（含所有 CSS 令牌、字体、基础框架、共享 SVG markers）
2. 在 `<body>` 里按顺序插入 slides：`封面 → 分节 → 内容页... → 封底`
3. 每个 slide 从 `components/` 挑模板，替换 `{{PLACEHOLDER}}`
4. 插入 `shell/nav.html`，根据 slide 数量生成对应数量的 nav dots
5. 插入 `shell/scripts.js`
6. **插入 `shell/editor.html`**（约 55KB，含编辑器 CSS + UI DOM + JS IIFE）—— 必须紧贴文档末尾
7. 关闭 `</body></html>`

**装配时的硬性规则（违反一个就翻车）**：
- **不要用 `str.replace('</body>', ...)` 作为插入锚点**。装配完直接在字符串末尾手动追加 `'\n</body>\n</html>\n'`；需要取末尾位置就用 `rfind('</body>')`。历史上 `shell/nav.html` 和 `shell/editor.html` 的头注释里写过字面量 `</body>`（现已移除），一旦 `replace` 命中注释里的那份，所有补丁会被塞进 HTML 注释里，运行时静默失效。
- **不要手 patch `shell/editor.html` / `shell/scripts.js` / `shell/nav.html`**。这三个文件里原本存在的若干运行时 bug 已在 skill 级别全部修复（见下方 "Editor bug fixes baked in"）。对它们二次加工意味着新 courseware 会丢掉这些修复。
- 最终输出里 `</body>` 必须恰好出现 1 次。JS 注释/字符串里的 `</body>` literal 不算。

### Editor bug fixes baked in（shell 已修好，不要重新引入）
1. **scripts.js 闭包 bug** — 以前缓存 `slides` / `current` / `total`，editor.html 后续覆盖 `window.goTo` 后闭包失效，左右翻页卡在第 2 页。现在每次从 DOM 重读 `.slide.active`。
2. **edit-mode 布局漂移** — `body.edit-mode .slide { padding-top: 52px }` 原本触发 flex reflow，`justify-content:center` 的子元素按比例吸收半数 shrink，导致拖动过的元素退出编辑模式时相对未拖动元素漂移。现在改成 `body.edit-mode .slide.active { transform: translateY(40px) }`（纯视觉，不触发 reflow）。
3. **globalAddText 百分号 transform** — 原来用 `transform: translate(-50%, -50%)` 做居中，`moveHtmlElement` 的 regex 只识别 `translate(Npx, Npx)`，拖动时把居中 transform 整个覆盖掉，元素视觉上跳半个自身尺寸。现在新增文字用纯 px `left/top` 定位。
4. **moveHtmlElement 对百分号 transform 的鲁棒性** — 现在进入拖动前会检测 `translate(..%..)`，若存在就先把元素转成 `position:absolute; left/top: Npx` 再动。任何源头产生的脏 transform 都被规范化。
5. **undo/redo 跳首页** — `restoreSlideContent` 原来无条件 `goTo(0)`。现在会先记录 `prevIdx`，restore 完 clamp 到新 slide 数并 `goTo(prevIdx)`。
6. **"保存" 实际上不保存** — 原 `editorSave` 只更新内存 baseline，不写盘。现在同时写 `localStorage['book2ppt:' + pathname]`，页面加载时 `restoreSlideContent` 会自动恢复，用户得到"保存→刷新→还在"的行为。配套暴露 `window.editorResetSaved()` 可在 console 清除保存版本。

### Step 4 — 网络素材（**默认必做**，不是可选）

**所有联网操作都走 `web-access` skill**——这是全局约束，不要绕过它去直接调 WebSearch/WebFetch。`web-access` 会帮你处理防盗链、referer、登录态、动态渲染等恶心细节。

每份课件**都应当有至少 2-3 条联网素材**（而不是只在教案明确引用时才加）。原因：教材里的知识本来就需要"真实世界锚点"才不枯燥——看到真实 Cl₂ 气体的黄绿色、真实的漂白粉颗粒、真实的 84 消毒液瓶子，远比手绘 SVG 有冲击力。组件选择：
- `components/media-embed.html` —— 嵌入真实图片/视频（详见 `components/media-workflow.md`）
- `components/web-source-card.html` —— 嵌入事实文字卡（详见 `web-search-workflow.md`）

#### 图片素材决策树（本 skill 的硬性约定）

```
课件语言 = 中文？
├── 是 → 首选：百度百科 `baike.baidu.com/item/<主题>`
│        CDN: bkimg.cdn.bcebos.com （允许 hotlink，无 referer 限制）
│        备胎：搜狗百科、官方站（中科院、新华社、博物馆）
│
└── 否（英文/国际主题）→ Wikimedia Commons `upload.wikimedia.org/...`
```

**严格禁止** 的图片来源：
- ❌ 百度图片搜索（`image.baidu.com` 跳转的第三方 URL）—— 有防盗链，99% hotlink 会变红叉
- ❌ 微博、Pinterest、CSDN/简书 图床 —— 不稳定 + 版权风险
- ❌ 搜索引擎缩略图 —— 会过期

#### 🔒 强制规则：图片必须 base64 内嵌

**不要**直接在 `<img src="https://...">` 里写远程 URL——断网就白屏、CDN 封 referer 就白屏、网页下架就白屏。正确做法：**下载 → base64 → data URI**。

```python
import urllib.request, base64
def img_data_uri(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=15) as r:
        data = r.read()
        mime = r.headers.get('Content-Type', 'image/png').split(';')[0]
    return f'data:{mime};base64,' + base64.b64encode(data).decode('ascii')
```

下载后、嵌入前，**必须 Read 看一眼图片实际内容**——百科网页里的 alt/caption 经常不准（session 里踩过：百度百科"氯气"条目里标的一张"钠在氯气中燃烧"实际是一团抽象的黄绿色火焰），看到实际内容再决定 caption 怎么写。

**文件大小预算**：
- 单张图 100–300 KB 常态
- 3–5 张图 → HTML 最终 0.5–1.5 MB，这是可接受区间
- 超过 2 MB 才需要考虑降采样或保留远程 URL

**允许远程 URL 的唯一例外**：
- `iframe` 视频（bilibili/YouTube）—— 这些本来就是在线内容，没办法 inline，保留远程 URL 即可。给 iframe 加 `referrerpolicy="no-referrer"` + `sandbox="allow-top-navigation allow-same-origin allow-forms allow-scripts"`。

详细操作流程见 `components/media-workflow.md`。

### Step 5 — 质量自检（及格线检查）
装配完后，用这个 checklist 自查：
- [ ] **字体链接包含 Nunito**（没有的话英文/数字字形会很糟）—— head.html 里的 `<link href="...Nunito...">`
- [ ] **CSS vars 把 Nunito 放最前**：`--font-body: 'Nunito', 'Ma Shan Zheng', ...`（保证 Latin 字符走 Nunito、中文走 Ma Shan Zheng）
- [ ] **至少有 1 个 mini-game slide**（class 用 `game-card` + `game-opt-btn`，onclick 用 `gamePick(this, 'KEY')`）
- [ ] **编辑器 bundle 已插入** —— `</body>` 前能搜到 `edit-toolbar` / `svg-prop-panel` / `edit-toggle`，右上角有"✏️ 编辑模式"按钮
- [ ] **页面可垂直滚动** —— CSS 里 html/body 是 `overflow-y:auto`；`.slide` 是 `min-height:100vh`（不是 `height:100vh`）；没有 `overflow:hidden`
- [ ] **所有方向箭头都走 shared marker** —— 搜 `<polygon` 应为 0 个（除非是非箭头的图形）；箭头统一 `<line ... marker-end="url(#arr-*)"/>`
- [ ] **椭圆/圆的切向箭头在底部水平线** —— 位置 `(cx, cy+ry)`，长度 10px
- [ ] **至少有 2-3 条联网素材** —— `media-embed` 图片 / `media-embed` 视频 / `web-source-card` 三选二，全走 `web-access` skill 抓取
- [ ] **中文课件的图片走百度百科 CDN**（`bkimg.cdn.bcebos.com`），不用 `image.baidu.com` 的搜索结果
- [ ] **所有 `<img>` 都是 base64 data URI** —— 搜 `src="data:image/` 应大于 0；搜 `src="http` 在 `<img>` 标签里应为 0（`<iframe>` 除外）
- [ ] **下载的图片都用 Read 工具视觉验证过** —— 百科站的 alt/caption 不可信，必须自己看一眼再写 caption
- [ ] 每页标题下有 3px 金色横线（`.slide-title::after` 自带）
- [ ] 每个关键词用了 `.keyword-*` 类，不是裸文本
- [ ] 没有任何 `click-to-reveal` 卡片
- [ ] 填空只出现在"必背"内容，不超过总页数的 1/5
- [ ] 每个流程概念既有整体页也有分步页
- [ ] 所有 SVG 加了 `class="hand-drawn"`
- [ ] 字号没有小于 20px 的正文（信息卡最小 20px，其他更大）
- [ ] 导航栏 dots 数量等于 slide 数量
- [ ] 在浏览器打开，按左右键能翻页，上下键/滚轮能滑动长页，填空可点击，选择题和小游戏能反馈，编辑模式开启后能改文字/SVG 并下载

## 组件清单

见 `MANIFEST.md`。简单说：
- `shell/` — head、nav、scripts，**必须**按顺序用
- `components/` — 内容块，按需组合
- `web-search-workflow.md` — web-source-card 的用法

## 占位符约定

所有模板用 `{{SNAKE_CASE}}` 作为占位符。装配时做字符串替换，不要留任何 `{{...}}` 在最终输出里。

常用占位符：
- `{{TITLE}}`, `{{SUBTITLE}}`, `{{CONTENT}}`
- `{{SLIDE_INDEX}}` — 从 0 开始
- `{{COLOR}}` — `red`/`blue`/`green`/`gold`/`purple`
- `{{CHAPTER_NUM}}`, `{{CHAPTER_NAME}}`
- `{{N_SLIDES}}` — 总页数（给 nav 用）

## 绝不要做的事

- ❌ 重写 CSS 令牌（`:root` 里的颜色、字号、字体）
- ❌ 重新实现导航 JS / 填空 JS / 选择题 JS
- ❌ 用现代 CSS 框架（Tailwind/Bootstrap）代替手工 CSS —— 会破坏"手绘笔记本"风格
- ❌ 把多个组件混在一起改造 —— 要么整块用，要么别用
- ❌ 在一页里塞超过 5 个信息卡 —— 字会变小
- ❌ 输出多文件 —— 最终必须是单个 `.html` 文件
- ❌ 改 `font-size` 比模板里小 —— 用户强制要求大字号
- ❌ 用 `<polygon points="x1,y1 x2,y2 x3,y3">` 手画箭头三角形 —— 旋转的线上坐标算不准会"飘"。一律用 `<line ... marker-end="url(#arr-gold)"/>`，marker 由 head.html 自动注入。
- ❌ 在 `html/body/.slide/.slide-col` 上加 `overflow: hidden` —— 会把超出一屏的内容截掉。head.html 已经把滚动打开了，保持现状。
- ❌ 在 `.slide` 上用 `height: 100vh` —— 必须是 `min-height: 100vh`，否则长页内容无法撑开。
- ❌ 漏插 `shell/editor.html` —— 没有它右上角的"✏️ 编辑模式"按钮会缺失，用户就无法二次编辑/下载修改版。
- ❌ 用占位符 URL 假装是 web 素材 —— 用 `media-embed` 时必须真正通过 `web-access` skill 拿到可访问的 bilibili/百度百科/wikimedia 地址。
- ❌ 直接在 HTML 里留 `<img src="https://image.baidu.com/...">` 之类的百度图片搜索结果 —— 有防盗链，会变红叉。中文图片一律走**百度百科 CDN + base64 内嵌**。
- ❌ hotlink 任何远程图片 URL 到 `<img src>` —— 所有图片必须下载后 base64 data URI 内嵌（iframe 视频例外）。打开课件的人可能没网。
- ❌ 仅凭网页 alt/caption 写图注 —— 下载后必须用 Read 工具打开图片视觉确认实际内容，再写 caption。百科站的标注经常不准。
- ❌ 忽略 `web-access` skill 直接调 WebSearch/WebFetch —— 所有联网操作走 web-access，由它处理防盗链/referer/登录态。
- ❌ 跳过 Step 4（联网素材） —— 纯 SVG 手绘的课件是不完整的，必须有真实世界锚点（至少 2-3 张真实图片或视频）。
