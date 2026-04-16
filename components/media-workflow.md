# media-embed 使用流程

`components/media-embed.html` 是一个可以嵌入**互联网视频或图片**的幻灯片组件。这份文件讲清楚：**何时触发、如何搜真实素材、如何填嵌入 URL**。

## 何时触发

扫描教案时，以下类型的内容值得用 media-embed：

| 场景 | 建议用 |
|---|---|
| 经典实验的照片/动图 | 📷 图片（Wikipedia Commons / 百科） |
| 实验演示视频 | 🎬 视频（bilibili / YouTube） |
| 科学家肖像 / 历史照片 | 📷 图片（Wikipedia） |
| 地理实景 / 天文图像 | 📷 图片 |
| 工业应用动画 | 🎬 视频 |
| 科普讲座片段 | 🎬 视频 |

**控制数量**：单份课件 **2-4 个 media-embed** 最合适。太多会让文件体积爆炸，而且 iframe 视频可能在某些网络环境下被墙。

## 工作流

### Step 1 · 构造查询

和 web-source-card 类似，但要加上"视频"/"图片"等关键词：

| 教案原文 | 查询 | 期望类型 |
|---|---|---|
| "法拉第的电磁感应实验" | `法拉第 电磁感应 演示实验 bilibili` | 🎬 |
| "奥斯特小磁针实验" | `奥斯特 电流磁效应 wikipedia commons` | 📷 |
| "喀斯特地貌" | `喀斯特地貌 航拍 bilibili` | 🎬 |
| "叶绿体结构" | `叶绿体 电子显微镜 图片` | 📷 |

### Step 2 · 搜索并筛选

```
WebSearch(query="...")
```

**视频来源优先级**：
1. 🎬 bilibili（B 站，embed 友好，国内可访问）
2. 🎬 YouTube（国外优质教学视频，国内需梯子）
3. ⚠️ 优酷/腾讯视频（embed 限制多，避免）

**图片来源优先级**：

**中文学科内容（中学语数外理化生史地政 · 教材帮 · 人教版 等）** ← 默认走这条路线：
1. 📷 **百度百科**（`baike.baidu.com/item/<主题>`）—— CDN 是 `bkimg.cdn.bcebos.com`，**允许 hotlink 无需 referer**，且图片与中国课本配图风格一致（教学仪器照片、国产品牌实物、中文标注的示意图）。**这是 Chinese 课件的首选。**
2. 📷 搜狗百科（`baike.sogou.com`）作为 Baidu 失效时的备胎
3. 📷 中国国家博物馆、故宫博物院、中国科学院、新华社图库等官方站（历史/科学/地理主题）

**国际 / 通用内容（英文专业词、世界地理、外国科学家）**：
1. 📷 Wikipedia / Wikimedia Commons（`upload.wikimedia.org`，CDN 稳定、免费、CC 许可）
2. 📷 维基百科词条中直接引用的图片（到 `commons.wikimedia.org/wiki/File:xxx` 找原图）

**绝对避免**：
- ❌ **百度图片搜索结果**（`image.baidu.com` 跳转到的第三方 URL）—— **有防盗链**，hotlink 到 HTML 里 99% 是"红叉图"
- ❌ 微博图床、Pinterest、CSDN/简书的图床 —— 不稳定 + 版权风险
- ❌ 搜索引擎缩略图（`tn3-q.mm.bing.net` 之类）—— 会过期

### Step 2.5 · 百度百科抓图实操

给 `WebFetch` 一个百科页 URL，让它找 `bkimg.cdn.bcebos.com` 上的图：

```
WebFetch(
  url="https://baike.baidu.com/item/氯气",
  prompt="Extract all image URLs hosted on bkimg.cdn.bcebos.com or bkimg.baidu.com.
          For each image, include the full URL and a one-line description of what it shows."
)
```

返回的 URL 通常有两种格式：
- **Thumb**：`https://bkimg.cdn.bcebos.com/smart/<hash>-bkimg-process,v_1,rw_258,rh_252,...?x-bce-process=image/format,f_auto`
  - 服务端已 resize，体积小，适合嵌入
- **Raw**：`https://bkimg.cdn.bcebos.com/pic/<hash>`
  - 原图，较大，适合需要清晰度时

**两种都可以直接 `<img src="...">` 使用**，不需要 referer / token。

### Step 3 · 提取嵌入 URL

#### 🎬 视频：bilibili

从搜索结果里拿到视频页面 URL（形如 `https://www.bilibili.com/video/BVxxxxxxxxx/`），提取 **BV 号**。

然后拼接 embed URL：
```
https://player.bilibili.com/player.html?bvid=BVxxxxxxxxx&page=1&autoplay=0&danmaku=0
```

**例子**：
- 原链接：`https://www.bilibili.com/video/BV1KY411G7Sx/`
- BV 号：`BV1KY411G7Sx`
- embed：`https://player.bilibili.com/player.html?bvid=BV1KY411G7Sx&page=1&autoplay=0&danmaku=0`

#### 🎬 视频：YouTube

从 `https://www.youtube.com/watch?v=VIDEO_ID` 提取 `VIDEO_ID`，然后：
```
https://www.youtube.com/embed/VIDEO_ID
```

#### 📷 图片：百度百科（中文内容首选）

见 Step 2.5。拿到 `bkimg.cdn.bcebos.com` 开头的 URL 就能直接用。

#### 📷 图片：Wikipedia（国际/英文内容）

要拿到直链 URL（以 `https://upload.wikimedia.org/wikipedia/commons/...` 开头）：
1. `WebFetch(url="https://zh.wikipedia.org/zh-hans/<主题>", prompt="Find all image URLs (upload.wikimedia.org links) on this page and return them with captions")`
2. 从返回的 URL 列表里挑选最相关的一张
3. 直接作为 `{{IMG_URL}}`

如果只有缩略图 URL（形如 `thumb/a/bc/File.jpg/300px-File.jpg`），可以保留缩略图（速度快）或去掉 `thumb/.../300px-` 得到原图。

#### 🔒 （推荐）把图下载下来 base64 内嵌 —— 最可靠

即使 CDN 允许 hotlink，嵌入 URL 的图片依赖网络，断网/离线就白屏。最稳妥的做法是**把图下载下来转 base64 data URI**，HTML 就彻底自洽了。

```python
import urllib.request, base64
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req, timeout=15) as r:
    data = r.read()
    ctype = r.headers.get('Content-Type', 'image/png')
data_uri = f'data:{ctype.split(";")[0]};base64,' + base64.b64encode(data).decode('ascii')
# 然后：<img src="{data_uri}" ...>
```

**用下载前先 Read 图片验证**——百科站的图片描述不一定准确，下载后用 Read 工具查看实际内容，再决定要不要用。本 session 踩过的坑：百科条目里一张"钠在氯气中燃烧"的图片实际是一束黄绿色火焰，虽然仍符合"Cl₂ 颜色"的用途，但需要改 caption。

**文件体积预算**：
- 单张图 100–300 KB 是常态
- 一份课件 3–5 张图，base64 后 HTML 总大小 0.5–1.5 MB 都属于可接受范围
- 超过 2 MB 就要考虑用 CDN URL（接受网络依赖）或者降采样
- ⚠️ 不要为了"省字节"而降级 Wikimedia 上的高清图——浏览器处理 base64 的瓶颈是解码，不是字节

**base64 vs hotlink 取舍**：

| 方案 | 离线可见 | 文件大小 | 风险 |
|---|---|---|---|
| hotlink 百度百科 CDN | ❌ | 小（HTML 轻） | 图片下架 / CDN 封 referer |
| hotlink Wikimedia | ❌ | 小 | 基本无风险，但慢 |
| base64 内嵌 | ✅ | 大（每图 +几百 KB） | 无 |

**默认选 base64**。只有在用户明确要求"HTML 尽量小" / "图片可以在线加载" 时才保留 URL。

### Step 4 · 填入模板

打开 `components/media-embed.html`，选择模板 A（图片）或 B（视频），替换占位符：

```html
<div class="media-card">
  <span class="media-card-badge">🎬 网络视频</span>
  <div class="media-card-title">法拉第电磁感应演示实验</div>
  <div class="media-card-body">
    <iframe src="https://player.bilibili.com/player.html?bvid=BV1KY411G7Sx&page=1&autoplay=0&danmaku=0"
            allowfullscreen scrolling="no" frameborder="0"></iframe>
  </div>
  <div class="media-card-caption">人教版九年级物理 · 磁生电 · 可直接复现法拉第 1831 年原始实验</div>
  <div class="media-card-source">
    <span>来源：<a href="https://www.bilibili.com/video/BV1KY411G7Sx/" target="_blank" rel="noopener">bilibili · 磁生电教学视频</a></span>
    <span>抓取于 2026-04-10</span>
  </div>
</div>
```

## 质量红线

1. **URL 必须真实** —— 只能用 WebSearch/WebFetch 实际返回的 URL，**不要凭印象编 BV 号或 video ID**。凡是记不清的，重新搜一次。
2. **iframe URL 必须是 embed 专用** —— bilibili 必须用 `player.bilibili.com/player.html?bvid=...`，不能直接用 `bilibili.com/video/BVxxx`（前者是专用播放器 URL，后者会被 x-frame-options 拒绝）。
3. **图片必须是直链** —— 确保 URL 以 `.jpg/.png/.svg/.webp/.gif` 结尾或是稳定 CDN；HTML 页面 URL 不能当图片用。
4. **来源要可点击** —— `.media-card-source` 里的 `<a href>` 要指向原视频/图片的页面（不是 embed URL）。
5. **提供 fallback 说明** —— 网络故障时 iframe 可能白屏，卡片下方的 caption 和 source 链接要能独立传达信息。
6. **不要自动播放** —— bilibili embed 的 `autoplay=0`、`danmaku=0` 必须保留，尊重阅读节奏。

## 失败处理

- **Bilibili iframe 白屏** → 多半是 referrer 检查。给 iframe 加 `referrerpolicy="no-referrer"` 或 `sandbox` 属性（模板里已加）。国内网络没问题，国外可能需要代理。
- **Wikipedia 图片 403** → 改用 Wikipedia Commons 的直链（`commons.wikimedia.org/wiki/Special:FilePath/<文件名>`，这会自动重定向到原图）。
- **搜不到合适的素材** → 降级为 `web-source-card`，只保留文字摘要。

## 跟 web-source-card 的区别

| 维度 | web-source-card | media-embed |
|---|---|---|
| 用途 | 抽取**事实文字**（日期、数字、人物生平） | 嵌入**媒体**（图片/视频） |
| 必要工具 | WebSearch + WebFetch | WebSearch + （可选）WebFetch |
| 文件大小影响 | 小（纯文本） | 图片几百 KB / 视频零额外（iframe） |
| 离线可见 | ✅ | ❌（iframe 需要网络，图片 hot-link 也需要） |
| 适用内容 | 人物生平、数据、理论发展史 | 实验演示、实景、显微镜图像、动画 |

两个可以**组合使用**：比如讲法拉第，同时放一张 web-source-card（生平事实）和一张 media-embed（实验视频）。
