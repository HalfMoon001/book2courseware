#!/usr/bin/env python3
"""Assemble 氯及其化合物 courseware from shell + inline slide HTML."""
from pathlib import Path

SKILL = Path('/Users/halfm/.claude/skills/book2courseware')
OUT = Path('/Users/halfm/Desktop/claudecode/book2ppt/out/chlorine_courseware.html')

head = (SKILL / 'shell/head.html').read_text(encoding='utf-8')
nav_tpl = (SKILL / 'shell/nav.html').read_text(encoding='utf-8')
scripts_js = (SKILL / 'shell/scripts.js').read_text(encoding='utf-8')
editor_html = (SKILL / 'shell/editor.html').read_text(encoding='utf-8')

head = head.replace('{{COURSEWARE_TITLE}}', '氯及其化合物 · 第二章第二节')

# =========================================================
#  SLIDES
# =========================================================
SLIDES = []

# ------- 0. Cover -------
cover_svg = '''
<svg width="520" height="240" viewBox="0 0 520 240" class="hand-drawn">
  <defs>
    <radialGradient id="cl-gas" cx="50%" cy="50%" r="60%">
      <stop offset="0%" stop-color="#d4f5a3" stop-opacity="0.9"/>
      <stop offset="100%" stop-color="#7ac142" stop-opacity="0.3"/>
    </radialGradient>
  </defs>
  <ellipse cx="260" cy="120" rx="220" ry="90" fill="url(#cl-gas)" opacity="0.8"/>
  <circle cx="160" cy="110" r="38" fill="none" stroke="#5a9e6f" stroke-width="3"/>
  <circle cx="160" cy="110" r="5" fill="#5a9e6f"/>
  <text x="160" y="116" text-anchor="middle" font-size="26" fill="#2c3e50" font-weight="bold">Cl</text>
  <circle cx="360" cy="110" r="38" fill="none" stroke="#5a9e6f" stroke-width="3"/>
  <circle cx="360" cy="110" r="5" fill="#5a9e6f"/>
  <text x="360" y="116" text-anchor="middle" font-size="26" fill="#2c3e50" font-weight="bold">Cl</text>
  <line x1="198" y1="110" x2="322" y2="110" stroke="#c8880a" stroke-width="4"/>
  <line x1="198" y1="102" x2="322" y2="102" stroke="#c8880a" stroke-width="2" opacity="0.6"/>
  <line x1="198" y1="118" x2="322" y2="118" stroke="#c8880a" stroke-width="2" opacity="0.6"/>
  <text x="260" y="205" text-anchor="middle" font-size="22" fill="#5a9e6f" font-weight="bold">Cl₂ · 黄绿色气体</text>
</svg>
'''
SLIDES.append(f'''
<div class="slide cover-slide active" data-slide="0">
  {cover_svg}
  <div class="cover-chapter">人教版化学必修一 · 第二章第二节</div>
  <div class="cover-title">氯及其化合物</div>
  <div style="font-family:var(--font-subtitle); font-size:26px; color:var(--blue); margin-top:12px; opacity:0.75;">Chlorine and its Compounds</div>
  <div style="font-family:var(--font-subtitle); font-size:18px; color:#999; margin-top:26px;">按 ← → 方向键翻页 &nbsp;|&nbsp; 点击填空查看答案 &nbsp;|&nbsp; 右上角可进入编辑模式</div>
</div>
''')

# ------- 1. Section divider -------
SLIDES.append('''
<div class="slide section-slide" data-slide="1">
  <div class="section-number">02</div>
  <div class="section-divider"></div>
  <div class="section-main-title">氯及其化合物</div>
  <div class="section-divider"></div>
  <div style="font-family:var(--font-subtitle); font-size:22px; color:#999; margin-top:10px;">从结构 → 性质 → 制备 → 检验 → 应用</div>
</div>
''')

# ------- 2. 氯元素的发现（timeline）-------
SLIDES.append('''
<div class="slide" data-slide="2">
  <div class="slide-title">氯元素的发现史</div>
  <div class="slide-subtitle">从实验室到工业原料</div>
  <div class="timeline">
    <div class="timeline-item">
      <div class="timeline-dot"></div>
      <div class="timeline-date">1774</div>
      <div class="timeline-label">瑞典化学家<span class="keyword keyword-blue">舍勒</span>用软锰矿与浓盐酸反应首次制得氯气</div>
    </div>
    <div class="timeline-item">
      <div class="timeline-dot"></div>
      <div class="timeline-date">1810</div>
      <div class="timeline-label">英国化学家<span class="keyword keyword-gold">戴维</span>确认它是一种<span class="keyword keyword-red">新元素</span>，命名为 chlorine</div>
    </div>
    <div class="timeline-item">
      <div class="timeline-dot"></div>
      <div class="timeline-date">化合态</div>
      <div class="timeline-label">自然界中 Cl 主要以<br><span class="keyword keyword-green">NaCl、KCl、MgCl₂</span> 存在于海水与盐湖</div>
    </div>
    <div class="timeline-item">
      <div class="timeline-dot"></div>
      <div class="timeline-date">游离态</div>
      <div class="timeline-label">仅存在于<span class="keyword keyword-purple">火山喷口</span>的少量气体中</div>
    </div>
  </div>
  <div class="highlight-box" style="max-width:900px; margin:20px auto 0;">
    💡 "chlorine" 来自希腊语 <b>χλωρός</b>（khlōros），意为<span class="keyword keyword-green">"黄绿色"</span>——正是氯气的颜色。
  </div>
</div>
''')

# ------- 3. 物理性质 -------
gas_jar_svg = '''
<svg width="320" height="380" viewBox="0 0 320 380" class="hand-drawn">
  <defs>
    <linearGradient id="cl-yellow" x1="0" x2="0" y1="0" y2="1">
      <stop offset="0%" stop-color="#e0ef5a" stop-opacity="0.9"/>
      <stop offset="100%" stop-color="#7ac142" stop-opacity="0.85"/>
    </linearGradient>
  </defs>
  <!-- 集气瓶 -->
  <path d="M80 60 L80 50 Q80 40 90 40 L230 40 Q240 40 240 50 L240 60 L260 80 L260 330 Q260 350 240 350 L80 350 Q60 350 60 330 L60 80 Z"
        fill="url(#cl-yellow)" stroke="#2c3e50" stroke-width="3"/>
  <!-- 瓶颈 -->
  <rect x="80" y="40" width="160" height="20" fill="none" stroke="#2c3e50" stroke-width="3"/>
  <!-- 玻璃反光 -->
  <path d="M90 90 L90 320" stroke="white" stroke-width="4" opacity="0.5"/>
  <!-- 气体分子 -->
  <circle cx="130" cy="130" r="6" fill="#5a9e6f" opacity="0.9"/>
  <circle cx="142" cy="130" r="6" fill="#5a9e6f" opacity="0.9"/>
  <circle cx="200" cy="180" r="6" fill="#5a9e6f" opacity="0.9"/>
  <circle cx="212" cy="180" r="6" fill="#5a9e6f" opacity="0.9"/>
  <circle cx="150" cy="230" r="6" fill="#5a9e6f" opacity="0.9"/>
  <circle cx="162" cy="230" r="6" fill="#5a9e6f" opacity="0.9"/>
  <circle cx="190" cy="280" r="6" fill="#5a9e6f" opacity="0.9"/>
  <circle cx="202" cy="280" r="6" fill="#5a9e6f" opacity="0.9"/>
  <text x="160" y="210" text-anchor="middle" font-size="30" fill="#2c3e50" font-weight="bold">Cl₂</text>
  <!-- 标签 -->
  <text x="160" y="375" text-anchor="middle" font-size="20" fill="#5a9e6f" font-weight="bold">黄绿色气体</text>
</svg>
'''
SLIDES.append(f'''
<div class="slide" data-slide="3">
  <div class="slide-title">氯气的物理性质</div>
  <div class="slide-subtitle">一看 · 二闻 · 三掂量</div>
  <div class="slide-row">
    <div class="slide-col-svg">{gas_jar_svg}</div>
    <div class="slide-col">
      <div class="info-card card-green"><b>颜色</b> · <span class="keyword keyword-green">黄绿色</span>气体</div>
      <div class="info-card card-red"><b>气味</b> · <span class="keyword keyword-red">刺激性</span>气味，<span class="keyword keyword-red">有毒</span>（闻时用手扇气）</div>
      <div class="info-card card-blue"><b>密度</b> · 比空气<span class="keyword keyword-blue">大</span>（M=71 &gt; 29），<b>向上排空气法</b>收集</div>
      <div class="info-card card-gold"><b>溶解性</b> · 能溶于水，常温下 1 体积水约溶 <span class="keyword keyword-gold">2 体积</span> Cl₂</div>
      <div class="info-card card-purple"><b>状态</b> · 常温为气体；加压、降温易液化为<span class="keyword keyword-purple">液氯</span>（纯净物）</div>
    </div>
  </div>
</div>
''')

# ------- 4. 氯原子结构与强氧化性 -------
atom_svg = '''
<svg width="360" height="360" viewBox="0 0 360 360" class="hand-drawn">
  <!-- 三个电子层 -->
  <circle cx="180" cy="180" r="40" fill="none" stroke="#4a90d9" stroke-width="2" stroke-dasharray="4 3"/>
  <circle cx="180" cy="180" r="85" fill="none" stroke="#4a90d9" stroke-width="2" stroke-dasharray="4 3"/>
  <circle cx="180" cy="180" r="140" fill="none" stroke="#e06b6b" stroke-width="3"/>
  <!-- 核 -->
  <circle cx="180" cy="180" r="22" fill="#c8880a"/>
  <text x="180" y="176" text-anchor="middle" font-size="14" fill="white" font-weight="bold">+17</text>
  <text x="180" y="192" text-anchor="middle" font-size="11" fill="white">Cl</text>
  <!-- K 层 2 电子 -->
  <circle cx="140" cy="180" r="5" fill="#4a90d9"/>
  <circle cx="220" cy="180" r="5" fill="#4a90d9"/>
  <!-- L 层 8 电子 -->
  <circle cx="180" cy="95" r="5" fill="#4a90d9"/>
  <circle cx="240" cy="120" r="5" fill="#4a90d9"/>
  <circle cx="265" cy="180" r="5" fill="#4a90d9"/>
  <circle cx="240" cy="240" r="5" fill="#4a90d9"/>
  <circle cx="180" cy="265" r="5" fill="#4a90d9"/>
  <circle cx="120" cy="240" r="5" fill="#4a90d9"/>
  <circle cx="95" cy="180" r="5" fill="#4a90d9"/>
  <circle cx="120" cy="120" r="5" fill="#4a90d9"/>
  <!-- M 层 7 电子 -->
  <circle cx="180" cy="40"  r="6" fill="#e06b6b"/>
  <circle cx="300" cy="110" r="6" fill="#e06b6b"/>
  <circle cx="320" cy="180" r="6" fill="#e06b6b"/>
  <circle cx="300" cy="260" r="6" fill="#e06b6b"/>
  <circle cx="180" cy="320" r="6" fill="#e06b6b"/>
  <circle cx="60"  cy="260" r="6" fill="#e06b6b"/>
  <circle cx="40"  cy="180" r="6" fill="#e06b6b"/>
  <!-- 强调最外层 -->
  <text x="330" y="60" font-size="18" fill="#e06b6b" font-weight="bold">7 e⁻</text>
  <text x="330" y="80" font-size="14" fill="#e06b6b">最外层</text>
  <!-- 得电子箭头 -->
  <line x1="40" y1="180" x2="0" y2="180" stroke="#c8880a" stroke-width="3" marker-end="url(#arr-gold)"/>
  <text x="5" y="165" font-size="16" fill="#c8880a">得 1 e⁻</text>
  <text x="5" y="205" font-size="16" fill="#c8880a">→ Cl⁻</text>
</svg>
'''
SLIDES.append(f'''
<div class="slide" data-slide="4">
  <div class="slide-title">氯原子的结构 → 强氧化性</div>
  <div class="slide-subtitle">"结构决定性质"</div>
  <div class="slide-row">
    <div class="slide-col-svg">{atom_svg}</div>
    <div class="slide-col">
      <div class="info-card card-blue"><b>电子排布</b> · 2, 8, <span class="keyword keyword-red">7</span> &nbsp;—— 最外层 7 个电子</div>
      <div class="info-card card-red"><b>得失倾向</b> · 只需得 <span class="keyword keyword-red">1 个电子</span> 即可达到 8 电子稳定结构，非常容易得电子</div>
      <div class="info-card card-gold"><b>化学性质</b> · 表现出<span class="keyword keyword-gold">强氧化性</span>，典型非金属</div>
      <div class="info-card card-green"><b>常见反应</b> · 与<span class="keyword keyword-green">金属</span>、<span class="keyword keyword-green">非金属</span>、<span class="keyword keyword-green">水</span>、<span class="keyword keyword-green">碱</span>都能反应</div>
      <div class="highlight-box">💡 变价金属与 Cl₂ 反应一般生成<span class="keyword keyword-red">高价态</span>氯化物（如 FeCl₃、CuCl₂）</div>
    </div>
  </div>
</div>
''')

# ------- 5. Cl₂ + 金属 整体 -------
SLIDES.append('''
<div class="slide" data-slide="5">
  <div class="slide-title">氯气与金属的反应 · 总览</div>
  <div class="slide-subtitle">Cl₂ 是"烟雾大师"——不同金属产生不同颜色的烟</div>
  <div class="chain-box">
    <div class="chain-step step-blue">Na · 钠</div>
    <span class="chain-arrow">+ Cl₂ →</span>
    <div class="chain-step step-red">白烟 NaCl</div>
  </div>
  <div class="chain-box">
    <div class="chain-step step-blue">Fe · 铁</div>
    <span class="chain-arrow">+ Cl₂ →</span>
    <div class="chain-step step-gold">棕褐色烟 FeCl₃</div>
  </div>
  <div class="chain-box">
    <div class="chain-step step-blue">Cu · 铜</div>
    <span class="chain-arrow">+ Cl₂ →</span>
    <div class="chain-step step-green">棕黄色烟 CuCl₂</div>
  </div>
  <div class="highlight-box" style="max-width:900px; margin:25px auto 0;">
    ⚠️ 反应条件都是<span class="keyword keyword-red">点燃</span>或<span class="keyword keyword-red">加热</span>；与变价金属 Fe、Cu 反应时一律生成<span class="keyword keyword-gold">高价态</span>氯化物。
  </div>
  <div style="text-align:center; font-size:18px; color:#999; margin-top:14px;">
    👉 下面 3 页分别详细演示每个反应
  </div>
</div>
''')

# ------- 6. Na + Cl₂ -------
na_svg = '''
<svg width="340" height="320" viewBox="0 0 340 320" class="hand-drawn">
  <!-- 集气瓶 -->
  <rect x="60" y="40" width="220" height="240" rx="6" fill="#f5fff0" stroke="#2c3e50" stroke-width="3"/>
  <!-- Na 燃烧盘 -->
  <ellipse cx="170" cy="250" rx="60" ry="8" fill="#888"/>
  <ellipse cx="170" cy="245" rx="55" ry="6" fill="#c8880a"/>
  <!-- 黄色火焰 -->
  <path d="M140 245 Q150 180 170 150 Q190 180 200 245 Z" fill="#ffd54f" stroke="#c8880a" stroke-width="2"/>
  <path d="M150 245 Q160 200 170 180 Q180 200 190 245 Z" fill="#ffc107"/>
  <!-- 白烟 -->
  <circle cx="120" cy="100" r="18" fill="white" stroke="#bbb" stroke-width="2" opacity="0.9"/>
  <circle cx="170" cy="80"  r="24" fill="white" stroke="#bbb" stroke-width="2" opacity="0.9"/>
  <circle cx="220" cy="100" r="18" fill="white" stroke="#bbb" stroke-width="2" opacity="0.9"/>
  <circle cx="140" cy="130" r="14" fill="white" stroke="#bbb" stroke-width="2" opacity="0.8"/>
  <circle cx="200" cy="125" r="14" fill="white" stroke="#bbb" stroke-width="2" opacity="0.8"/>
  <text x="170" y="300" text-anchor="middle" font-size="20" fill="#2c3e50" font-weight="bold">剧烈燃烧 · 产生白烟</text>
</svg>
'''
SLIDES.append(f'''
<div class="slide" data-slide="6">
  <div class="slide-title">反应 ① Na + Cl₂</div>
  <div class="slide-subtitle">金属钠的燃烧</div>
  <div class="slide-row">
    <div class="slide-col-svg">{na_svg}</div>
    <div class="slide-col">
      <div class="info-card card-gold"><b>现象</b> · 钠在氯气中<span class="keyword keyword-red">剧烈燃烧</span>，发出<span class="keyword keyword-gold">黄色火焰</span>，产生<span class="keyword keyword-red">白烟</span></div>
      <div class="info-card card-blue"><b>化学方程式</b><br>
        <span style="font-size:24px;">2Na + Cl₂ <span class="keyword keyword-red">━点燃→</span> 2NaCl</span></div>
      <div class="info-card card-green"><b>产物</b> · <span class="keyword keyword-green">NaCl</span>（白色固体，即食盐）</div>
      <div class="info-card card-purple"><b>关键判断</b> · "烟"是<span class="keyword keyword-purple">固体小颗粒</span>，不是"雾"；"雾"才是液滴</div>
    </div>
  </div>
</div>
''')

# ------- 7. Fe + Cl₂ -------
fe_svg = '''
<svg width="340" height="320" viewBox="0 0 340 320" class="hand-drawn">
  <rect x="60" y="40" width="220" height="240" rx="6" fill="#f5fff0" stroke="#2c3e50" stroke-width="3"/>
  <!-- 铁丝螺旋 -->
  <path d="M170 60 Q180 100 170 130 Q160 160 170 190 Q180 220 170 245" fill="none" stroke="#555" stroke-width="4"/>
  <!-- 红热部分 -->
  <path d="M168 150 Q180 180 168 210" fill="none" stroke="#e06b6b" stroke-width="6"/>
  <!-- 棕褐色烟 -->
  <ellipse cx="120" cy="100" rx="22" ry="14" fill="#8b5a2b" opacity="0.7"/>
  <ellipse cx="180" cy="80" rx="30" ry="18" fill="#a0633a" opacity="0.7"/>
  <ellipse cx="230" cy="100" rx="22" ry="14" fill="#8b5a2b" opacity="0.7"/>
  <ellipse cx="150" cy="130" rx="18" ry="12" fill="#a0633a" opacity="0.65"/>
  <ellipse cx="210" cy="125" rx="18" ry="12" fill="#a0633a" opacity="0.65"/>
  <text x="170" y="300" text-anchor="middle" font-size="20" fill="#2c3e50" font-weight="bold">剧烈燃烧 · 棕褐色烟</text>
</svg>
'''
SLIDES.append(f'''
<div class="slide" data-slide="7">
  <div class="slide-title">反应 ② Fe + Cl₂</div>
  <div class="slide-subtitle">铁丝在氯气中燃烧</div>
  <div class="slide-row">
    <div class="slide-col-svg">{fe_svg}</div>
    <div class="slide-col">
      <div class="info-card card-red"><b>现象</b> · 铁丝<span class="keyword keyword-red">剧烈燃烧</span>，产生<span class="keyword keyword-gold">棕褐色烟</span></div>
      <div class="info-card card-blue"><b>化学方程式</b><br>
        <span style="font-size:24px;">2Fe + 3Cl₂ <span class="keyword keyword-red">━点燃→</span> 2FeCl₃</span></div>
      <div class="info-card card-gold"><b>产物</b> · <span class="keyword keyword-gold">FeCl₃</span>（棕黄色）——铁表现 <span class="keyword keyword-red">+3 价</span></div>
      <div class="info-card card-purple"><b>重要结论</b><br>① Cl₂ 是<span class="keyword keyword-purple">强氧化剂</span>，能把 Fe 氧化到<span class="keyword keyword-red">最高价 +3</span><br>② 与稀盐酸对比：Fe + 2HCl = FeCl₂ + H₂↑（+2 价）</div>
    </div>
  </div>
</div>
''')

# ------- 8. Cu + Cl₂ -------
cu_svg = '''
<svg width="340" height="320" viewBox="0 0 340 320" class="hand-drawn">
  <rect x="60" y="40" width="220" height="240" rx="6" fill="#f5fff0" stroke="#2c3e50" stroke-width="3"/>
  <!-- 铜丝 -->
  <rect x="165" y="100" width="10" height="140" fill="#b87333" stroke="#7a4f1f" stroke-width="2"/>
  <circle cx="170" cy="96" r="10" fill="#b87333" stroke="#7a4f1f" stroke-width="2"/>
  <!-- 棕黄色烟 -->
  <ellipse cx="130" cy="90"  rx="22" ry="14" fill="#daa520" opacity="0.75"/>
  <ellipse cx="180" cy="70"  rx="30" ry="18" fill="#daa520" opacity="0.75"/>
  <ellipse cx="225" cy="95"  rx="22" ry="14" fill="#daa520" opacity="0.75"/>
  <ellipse cx="155" cy="125" rx="18" ry="12" fill="#daa520" opacity="0.7"/>
  <ellipse cx="210" cy="120" rx="18" ry="12" fill="#daa520" opacity="0.7"/>
  <!-- 溶水后的现象指示 -->
  <g transform="translate(35,200)">
    <rect x="0" y="0" width="30" height="50" rx="3" fill="#48a4d8" stroke="#2c3e50" stroke-width="2"/>
    <text x="15" y="75" text-anchor="middle" font-size="12" fill="#4a90d9">溶水蓝色</text>
  </g>
  <text x="170" y="300" text-anchor="middle" font-size="20" fill="#2c3e50" font-weight="bold">棕黄色烟</text>
</svg>
'''
SLIDES.append(f'''
<div class="slide" data-slide="8">
  <div class="slide-title">反应 ③ Cu + Cl₂</div>
  <div class="slide-subtitle">铜丝在氯气中燃烧</div>
  <div class="slide-row">
    <div class="slide-col-svg">{cu_svg}</div>
    <div class="slide-col">
      <div class="info-card card-red"><b>现象</b> · 铜丝<span class="keyword keyword-red">剧烈燃烧</span>，产生<span class="keyword keyword-gold">棕黄色烟</span></div>
      <div class="info-card card-blue"><b>化学方程式</b><br>
        <span style="font-size:24px;">Cu + Cl₂ <span class="keyword keyword-red">━点燃→</span> CuCl₂</span></div>
      <div class="info-card card-gold"><b>产物溶水</b> · CuCl₂ 溶于少量水呈<span class="keyword keyword-green">绿色</span>，溶于较多水呈<span class="keyword keyword-blue">蓝色</span></div>
      <div class="info-card card-purple"><b>规律小结</b><br>Cl₂ + 变价金属 → <span class="keyword keyword-red">高价</span>氯化物</div>
    </div>
  </div>
</div>
''')

# ------- 9. Cl₂ + H₂ -------
h2_svg = '''
<svg width="360" height="320" viewBox="0 0 360 320" class="hand-drawn">
  <rect x="70" y="40" width="220" height="240" rx="6" fill="#f5fff0" stroke="#2c3e50" stroke-width="3"/>
  <!-- 氢气燃烧产生苍白色火焰 -->
  <g transform="translate(180,230)">
    <path d="M-45 0 Q-30 -80 0 -120 Q30 -80 45 0 Z" fill="#e6e6f5" stroke="#9999cc" stroke-width="2"/>
    <path d="M-25 0 Q-15 -60 0 -90 Q15 -60 25 0 Z" fill="#f0f0ff" opacity="0.9"/>
  </g>
  <!-- 瓶口白雾 -->
  <ellipse cx="180" cy="55" rx="80" ry="12" fill="white" opacity="0.95"/>
  <ellipse cx="180" cy="45" rx="60" ry="8" fill="white" opacity="0.9"/>
  <ellipse cx="180" cy="35" rx="40" ry="6" fill="white" opacity="0.85"/>
  <!-- 下方管子送 H2 -->
  <rect x="175" y="240" width="10" height="60" fill="#aaa" stroke="#555" stroke-width="2"/>
  <text x="180" y="318" text-anchor="middle" font-size="16" fill="#7b68ee" font-weight="bold">H₂ 导入</text>
  <text x="180" y="305" text-anchor="middle" font-size="14" fill="#999">苍白色火焰 + 瓶口白雾</text>
</svg>
'''
SLIDES.append(f'''
<div class="slide" data-slide="9">
  <div class="slide-title">反应 ④ Cl₂ + H₂ · 非金属反应</div>
  <div class="slide-subtitle">"苍白色火焰 + 瓶口白雾"</div>
  <div class="slide-row">
    <div class="slide-col-svg">{h2_svg}</div>
    <div class="slide-col">
      <div class="info-card card-blue"><b>点燃条件下</b><br>
        <span style="font-size:24px;">H₂ + Cl₂ <span class="keyword keyword-red">━点燃→</span> 2HCl</span><br>
        <span style="font-size:16px;color:#666;">现象：苍白色火焰；瓶口有白雾（HCl 遇空气中水汽）</span></div>
      <div class="info-card card-red"><b>光照条件下</b><br>
        H₂ + Cl₂ <span class="keyword keyword-red">━光照→</span> <span class="keyword keyword-red">爆炸</span>（剧烈反应）</div>
      <div class="info-card card-gold"><b>现象辨析</b><br>
        "烟"是<span class="keyword keyword-gold">固体小颗粒</span>；"雾"是<span class="keyword keyword-blue">小液滴</span><br>
        HCl 气体遇水汽 → 盐酸小液滴 = <span class="keyword keyword-blue">白雾</span></div>
      <div class="info-card card-purple"><b>结论</b> · Cl₂ 能与很多非金属（H₂、P、S…）直接化合，体现其<span class="keyword keyword-purple">强氧化性</span></div>
    </div>
  </div>
</div>
''')

# ------- 10. Cl₂ + H₂O -------
water_svg = '''
<svg width="340" height="320" viewBox="0 0 340 320" class="hand-drawn">
  <!-- 烧杯 -->
  <path d="M70 80 L70 260 Q70 280 90 280 L250 280 Q270 280 270 260 L270 80" fill="#f0fff0" stroke="#2c3e50" stroke-width="3"/>
  <line x1="60" y1="80" x2="280" y2="80" stroke="#2c3e50" stroke-width="3"/>
  <!-- 黄绿色液体 -->
  <path d="M75 260 Q75 278 92 278 L248 278 Q265 278 265 260 L265 160 L75 160 Z" fill="#b8d97a" opacity="0.7"/>
  <!-- 波纹 -->
  <path d="M75 160 Q100 150 130 160 Q160 170 190 160 Q220 150 265 160" fill="none" stroke="#5a9e6f" stroke-width="2"/>
  <!-- Cl2 气泡 -->
  <circle cx="150" cy="200" r="8" fill="#a6e055" opacity="0.6"/>
  <circle cx="180" cy="220" r="6" fill="#a6e055" opacity="0.6"/>
  <circle cx="200" cy="190" r="7" fill="#a6e055" opacity="0.6"/>
  <!-- 标签 -->
  <text x="170" y="230" text-anchor="middle" font-size="24" fill="#5a9e6f" font-weight="bold">氯水</text>
  <text x="170" y="250" text-anchor="middle" font-size="16" fill="#5a9e6f">浅黄绿色</text>
  <text x="170" y="305" text-anchor="middle" font-size="16" fill="#2c3e50">新制氯水 · 现用现配</text>
</svg>
'''
SLIDES.append(f'''
<div class="slide" data-slide="10">
  <div class="slide-title">反应 ⑤ Cl₂ + H₂O · 氯水的生成</div>
  <div class="slide-subtitle">部分反应 · 是<u>可逆反应</u></div>
  <div class="slide-row">
    <div class="slide-col-svg">{water_svg}</div>
    <div class="slide-col">
      <div class="info-card card-blue" style="font-size:22px;"><b>化学方程式</b><br>
        Cl₂ + H₂O <span class="keyword keyword-red">⇌</span> HCl + <span class="keyword keyword-gold">HClO</span></div>
      <div class="info-card card-red"><b>HClO · 次氯酸</b><br>
        · <span class="keyword keyword-red">弱酸</span>，酸性比碳酸还弱<br>
        · 具有<span class="keyword keyword-red">强氧化性</span>（漂白、杀菌）<br>
        · <span class="keyword keyword-red">不稳定</span>：2HClO <span class="keyword keyword-red">━光→</span> 2HCl + O₂↑</div>
      <div class="info-card card-gold"><b>新制氯水 · 外观</b> · <span class="keyword keyword-gold">浅黄绿色</span>，有刺激性气味</div>
      <div class="info-card card-purple"><b>应用</b> · 自来水消毒；<span class="keyword keyword-purple">漂白</span>（有色物质永久褪色）</div>
    </div>
  </div>
</div>
''')

# ------- 11. 新制 vs 久置氯水 -------
SLIDES.append('''
<div class="slide" data-slide="11">
  <div class="slide-title">新制氯水 vs 久置氯水</div>
  <div class="compare-grid">
    <div class="compare-card compare-left">
      <h3>🌿 新制氯水</h3>
      <div style="font-size:20px;">
        <div class="info-card card-blue"><b>颜色</b> · <span class="keyword keyword-green">浅黄绿色</span></div>
        <div class="info-card card-blue"><b>主要成分</b><br>
        <span class="keyword keyword-red">3 分子</span>：Cl₂、HClO、H₂O<br>
        <span class="keyword keyword-red">4 离子</span>：H⁺、Cl⁻、ClO⁻、OH⁻</div>
        <div class="info-card card-blue"><b>性质</b> · 兼具<b>酸性 + 氧化性 + 漂白性</b></div>
        <div class="info-card card-blue"><b>使用</b> · 见光分解，必须<span class="keyword keyword-red">现用现配</span>，棕色瓶避光保存</div>
      </div>
    </div>
    <div class="compare-card compare-right">
      <h3>⏳ 久置氯水</h3>
      <div style="font-size:20px;">
        <div class="info-card card-red"><b>颜色</b> · <span class="keyword keyword-gold">无色</span></div>
        <div class="info-card card-red"><b>主要成分</b><br>
        2 分子：<span class="keyword keyword-gold">H₂O</span><br>
        2 离子：<span class="keyword keyword-gold">H⁺、Cl⁻</span></div>
        <div class="info-card card-red"><b>实质</b> · 几乎就是<span class="keyword keyword-red">稀盐酸</span></div>
        <div class="info-card card-red"><b>原因</b><br>2HClO <span class="keyword keyword-red">━光→</span> 2HCl + O₂↑<br>HClO 慢慢分解耗尽，Cl₂ 持续消耗</div>
      </div>
    </div>
  </div>
</div>
''')

# ------- 12. Cl₂ + 碱 -------
SLIDES.append('''
<div class="slide" data-slide="12">
  <div class="slide-title">反应 ⑥ Cl₂ + 碱</div>
  <div class="slide-subtitle">工业制备漂白剂 · 尾气吸收</div>
  <div class="compare-grid">
    <div class="compare-card compare-left">
      <h3>💧 NaOH 溶液</h3>
      <div style="font-size:20px;">
        <div class="info-card card-blue" style="font-size:22px;"><b>方程式</b><br>
          Cl₂ + 2NaOH = <span class="keyword keyword-gold">NaCl</span> + <span class="keyword keyword-red">NaClO</span> + H₂O</div>
        <div class="info-card card-blue"><b>用途</b> · 实验室<span class="keyword keyword-red">尾气吸收</span>（Cl₂ 有毒不能排入空气）</div>
        <div class="info-card card-blue"><b>产品</b> · 含 NaClO 的溶液 = <span class="keyword keyword-purple">"84" 消毒液</span>（漂白液）</div>
      </div>
    </div>
    <div class="compare-card compare-right">
      <h3>🔆 Ca(OH)₂ 悬浊液</h3>
      <div style="font-size:20px;">
        <div class="info-card card-red" style="font-size:22px;"><b>方程式</b><br>
          2Cl₂ + 2Ca(OH)₂ = <span class="keyword keyword-gold">Ca(ClO)₂</span> + <span class="keyword keyword-gold">CaCl₂</span> + 2H₂O</div>
        <div class="info-card card-red"><b>产品</b> · 混合物 → <span class="keyword keyword-red">漂白粉</span><br>有效成分 <span class="keyword keyword-red">Ca(ClO)₂</span></div>
        <div class="info-card card-red"><b>漂白原理</b> · Ca(ClO)₂ + CO₂ + H₂O → CaCO₃ + 2<span class="keyword keyword-gold">HClO</span>（生成 HClO 才能漂白）</div>
      </div>
    </div>
  </div>
</div>
''')

# ------- 13. 实验室制法整体流程 -------
SLIDES.append('''
<div class="slide" data-slide="13">
  <div class="slide-title">氯气的实验室制法 · 全流程</div>
  <div class="slide-subtitle">MnO₂ + 浓 HCl → Cl₂</div>
  <div class="chain-box" style="margin-top:30px;">
    <div class="chain-step step-blue">① 发生<br><span style="font-size:15px;">固液加热</span></div>
    <span class="chain-arrow">→</span>
    <div class="chain-step step-gold">② 除 HCl<br><span style="font-size:15px;">饱和食盐水</span></div>
    <span class="chain-arrow">→</span>
    <div class="chain-step step-gold">③ 除 H₂O<br><span style="font-size:15px;">浓 H₂SO₄</span></div>
    <span class="chain-arrow">→</span>
    <div class="chain-step step-blue">④ 收集<br><span style="font-size:15px;">向上排空气法</span></div>
  </div>
  <div class="chain-box" style="margin-top:20px;">
    <div class="chain-step step-blue">⑤ 验满<br><span style="font-size:15px;">湿润淀粉 KI 试纸变蓝</span></div>
    <span class="chain-arrow">→</span>
    <div class="chain-step step-red">⑥ 尾气处理<br><span style="font-size:15px;">NaOH 溶液吸收</span></div>
  </div>
  <div class="highlight-box" style="max-width:900px; margin:30px auto 0; font-size:24px;">
    🔑 核心反应：<b>MnO₂ + 4HCl(浓) <span class="keyword keyword-red">━Δ→</span> MnCl₂ + Cl₂↑ + 2H₂O</b>
  </div>
  <div style="text-align:center; font-size:18px; color:#999; margin-top:15px;">
    ⚠️ 必须是<b>浓</b>盐酸；<b>稀盐酸不反应</b>（氧化性不足）
  </div>
</div>
''')

# ------- 14. 实验室制法装置详解 -------
apparatus_svg = '''
<svg width="460" height="360" viewBox="0 0 460 360" class="hand-drawn">
  <!-- 发生装置 圆底烧瓶 + 酒精灯 -->
  <circle cx="80" cy="150" r="45" fill="#fff8e7" stroke="#2c3e50" stroke-width="3"/>
  <rect x="72" y="95" width="16" height="20" fill="none" stroke="#2c3e50" stroke-width="3"/>
  <text x="80" y="158" text-anchor="middle" font-size="14" fill="#c8880a" font-weight="bold">MnO₂</text>
  <text x="80" y="175" text-anchor="middle" font-size="12" fill="#e06b6b">+浓HCl</text>
  <!-- 酒精灯 -->
  <path d="M60 210 L100 210 L95 230 L65 230 Z" fill="#c8880a"/>
  <path d="M75 195 Q80 175 85 195 Z" fill="#ff9800"/>
  <!-- 管路 -->
  <path d="M80 95 L80 70 L170 70" fill="none" stroke="#2c3e50" stroke-width="3"/>
  <!-- 洗气瓶 1：饱和食盐水 -->
  <rect x="150" y="65" width="50" height="80" fill="#e0f5ff" stroke="#2c3e50" stroke-width="3"/>
  <rect x="150" y="105" width="50" height="40" fill="#a8d8f0" opacity="0.7"/>
  <text x="175" y="160" text-anchor="middle" font-size="12" fill="#4a90d9">饱和NaCl</text>
  <line x1="160" y1="100" x2="160" y2="130" stroke="#4a90d9" stroke-width="2"/>
  <path d="M200 70 L240 70" fill="none" stroke="#2c3e50" stroke-width="3"/>
  <!-- 洗气瓶 2：浓硫酸 -->
  <rect x="230" y="65" width="50" height="80" fill="#fffff0" stroke="#2c3e50" stroke-width="3"/>
  <rect x="230" y="105" width="50" height="40" fill="#f0e68c" opacity="0.7"/>
  <text x="255" y="160" text-anchor="middle" font-size="12" fill="#c8880a">浓H₂SO₄</text>
  <line x1="240" y1="100" x2="240" y2="130" stroke="#c8880a" stroke-width="2"/>
  <path d="M280 70 L330 70" fill="none" stroke="#2c3e50" stroke-width="3"/>
  <!-- 收集瓶 -->
  <rect x="320" y="65" width="60" height="110" fill="#e0f5a8" opacity="0.6" stroke="#2c3e50" stroke-width="3"/>
  <text x="350" y="125" text-anchor="middle" font-size="16" fill="#5a9e6f" font-weight="bold">Cl₂</text>
  <text x="350" y="145" text-anchor="middle" font-size="11" fill="#5a9e6f">向上排空气</text>
  <line x1="335" y1="70" x2="335" y2="100" stroke="#2c3e50" stroke-width="2"/>
  <!-- 尾气处理 -->
  <path d="M380 90 L410 90 L410 250 L360 250" fill="none" stroke="#2c3e50" stroke-width="3"/>
  <rect x="320" y="240" width="70" height="60" fill="#ffebeb" stroke="#2c3e50" stroke-width="3"/>
  <rect x="320" y="260" width="70" height="40" fill="#ffc5c5" opacity="0.7"/>
  <text x="355" y="290" text-anchor="middle" font-size="13" fill="#e06b6b">NaOH吸收</text>
  <!-- 标注 -->
  <text x="80" y="250" text-anchor="middle" font-size="14" fill="#2c3e50" font-weight="bold">① 发生</text>
  <text x="175" y="50" text-anchor="middle" font-size="14" fill="#2c3e50" font-weight="bold">② 除HCl</text>
  <text x="255" y="50" text-anchor="middle" font-size="14" fill="#2c3e50" font-weight="bold">③ 干燥</text>
  <text x="350" y="50" text-anchor="middle" font-size="14" fill="#2c3e50" font-weight="bold">④ 收集</text>
  <text x="355" y="320" text-anchor="middle" font-size="14" fill="#e06b6b" font-weight="bold">⑤ 尾气处理</text>
</svg>
'''
SLIDES.append(f'''
<div class="slide" data-slide="14">
  <div class="slide-title">实验室制 Cl₂ · 装置详解</div>
  <div class="slide-row">
    <div class="slide-col-svg">{apparatus_svg}</div>
    <div class="slide-col">
      <div class="info-card card-blue"><b>① 发生</b> · 固液加热型（MnO₂ 固体 + 浓 HCl）</div>
      <div class="info-card card-gold"><b>② 除 HCl</b> · <span class="keyword keyword-gold">饱和食盐水</span><br>
        <span style="font-size:16px;">Cl₂ 在饱和 NaCl 中溶解度很小，HCl 易溶</span></div>
      <div class="info-card card-gold"><b>③ 干燥</b> · <span class="keyword keyword-gold">浓 H₂SO₄</span><br>
        <span style="font-size:16px;">注意：浓 H₂SO₄ 不氧化 Cl₂（Cl₂ 本就高氧化性）</span></div>
      <div class="info-card card-blue"><b>④ 收集</b> · <span class="keyword keyword-blue">向上排空气法</span>（Cl₂ 密度大于空气）</div>
      <div class="info-card card-red"><b>⑤ 验满</b> · 用<span class="keyword keyword-red">湿润的淀粉碘化钾试纸</span>靠近瓶口，变蓝即满<br>
        <span style="font-size:15px;">原理：Cl₂ + 2KI = 2KCl + I₂（I₂ 使淀粉变蓝）</span></div>
      <div class="info-card card-red"><b>⑥ 尾气</b> · <span class="keyword keyword-red">NaOH 溶液吸收</span>，防止污染空气</div>
    </div>
  </div>
</div>
''')

# ------- 15. 氯离子检验 -------
cl_check_svg = '''
<svg width="340" height="340" viewBox="0 0 340 340" class="hand-drawn">
  <!-- 试管 -->
  <path d="M100 60 L100 280 Q100 310 140 310 Q180 310 180 280 L180 60 Z" fill="#f0faff" stroke="#2c3e50" stroke-width="3"/>
  <!-- 溶液 -->
  <path d="M105 280 Q105 305 140 305 Q175 305 175 280 L175 150 L105 150 Z" fill="#d0e8f5" opacity="0.7"/>
  <!-- 白色沉淀 AgCl -->
  <circle cx="120" cy="260" r="7" fill="white" stroke="#999" stroke-width="2"/>
  <circle cx="140" cy="270" r="7" fill="white" stroke="#999" stroke-width="2"/>
  <circle cx="160" cy="260" r="7" fill="white" stroke="#999" stroke-width="2"/>
  <circle cx="130" cy="250" r="6" fill="white" stroke="#999" stroke-width="2"/>
  <circle cx="150" cy="250" r="6" fill="white" stroke="#999" stroke-width="2"/>
  <circle cx="145" cy="280" r="5" fill="white" stroke="#999" stroke-width="2"/>
  <text x="230" y="210" font-size="20" fill="#2c3e50" font-weight="bold">AgCl↓</text>
  <text x="230" y="232" font-size="15" fill="#2c3e50">白色沉淀</text>
  <text x="230" y="252" font-size="14" fill="#c8880a">不溶于稀 HNO₃</text>
  <line x1="225" y1="215" x2="175" y2="260" stroke="#c8880a" stroke-width="2" marker-end="url(#arr-gold)"/>
  <!-- 上方滴管 -->
  <rect x="125" y="20" width="30" height="40" fill="#ccc" stroke="#2c3e50" stroke-width="2"/>
  <path d="M130 60 L150 60 L140 70 Z" fill="#c8880a"/>
  <text x="140" y="18" text-anchor="middle" font-size="13" fill="#c8880a" font-weight="bold">AgNO₃</text>
</svg>
'''
SLIDES.append(f'''
<div class="slide" data-slide="15">
  <div class="slide-title">氯离子 Cl⁻ 的检验</div>
  <div class="slide-subtitle">"白色沉淀 · 稀硝酸不溶"</div>
  <div class="slide-row">
    <div class="slide-col-svg">{cl_check_svg}</div>
    <div class="slide-col">
      <div class="info-card card-blue"><b>操作步骤</b><br>
        1️⃣ 取少量待测液于试管<br>
        2️⃣ 先滴入少量<span class="keyword keyword-gold">稀 HNO₃</span>（排除 CO₃²⁻ 等干扰）<br>
        3️⃣ 再滴入少量 <span class="keyword keyword-blue">AgNO₃ 溶液</span></div>
      <div class="info-card card-red"><b>现象与结论</b> · 若产生<span class="keyword keyword-red">白色沉淀</span>，证明含 Cl⁻</div>
      <div class="info-card card-gold"><b>离子方程式</b><br>
        <span style="font-size:22px;">Ag⁺ + Cl⁻ = <span class="keyword keyword-gold">AgCl↓</span></span></div>
      <div class="info-card card-purple"><b>为什么先加稀 HNO₃？</b><br>
        排除 CO₃²⁻、SO₃²⁻ 等干扰（它们与 Ag⁺ 也生成白色沉淀，但会被稀 HNO₃ 溶解）</div>
    </div>
  </div>
</div>
''')

# ------- 16. 填空 -------
SLIDES.append('''
<div class="slide" data-slide="16">
  <div class="slide-title">必背方程式 · 填空练习</div>
  <div style="max-width:1000px;margin:0 auto;">
    <div class="info-card card-blue" style="font-size:22px;line-height:2;">
      <b>1️⃣ 氯气与钠：</b>
      2Na + <span class="blank" data-answer="Cl₂">Cl₂</span> <span class="keyword keyword-red">━点燃→</span> <span class="blank" data-answer="2NaCl">2NaCl</span>　（<span class="blank" data-answer="白烟">白烟</span>）<br>

      <b>2️⃣ 氯气与铁：</b>
      <span class="blank" data-answer="2Fe">2Fe</span> + 3Cl₂ <span class="keyword keyword-red">━点燃→</span> <span class="blank" data-answer="2FeCl₃">2FeCl₃</span>　（<span class="blank" data-answer="棕褐色烟">棕褐色烟</span>）<br>

      <b>3️⃣ 氯气与水：</b>
      Cl₂ + H₂O ⇌ <span class="blank" data-answer="HCl">HCl</span> + <span class="blank" data-answer="HClO">HClO</span><br>

      <b>4️⃣ 氯气与氢氧化钠（尾气处理）：</b>
      Cl₂ + <span class="blank" data-answer="2NaOH">2NaOH</span> = NaCl + <span class="blank" data-answer="NaClO">NaClO</span> + H₂O<br>

      <b>5️⃣ 制漂白粉：</b>
      2Cl₂ + 2Ca(OH)₂ = <span class="blank" data-answer="Ca(ClO)₂">Ca(ClO)₂</span> + CaCl₂ + 2H₂O<br>

      <b>6️⃣ 实验室制 Cl₂：</b>
      MnO₂ + <span class="blank" data-answer="4HCl(浓)">4HCl(浓)</span> <span class="keyword keyword-red">━Δ→</span> <span class="blank" data-answer="MnCl₂">MnCl₂</span> + Cl₂↑ + <span class="blank" data-answer="2H₂O">2H₂O</span>
    </div>
    <div style="text-align:center;margin-top:18px;">
      <button onclick="revealAllBlanks(this)" style="padding:10px 30px;border:2px dashed var(--red);background:rgba(224,107,107,0.05);border-radius:20px;font-family:var(--font-title);font-size:20px;color:var(--red);cursor:pointer;">✨ 显示所有答案</button>
    </div>
    <div style="text-align:center; font-size:16px; color:#999; margin-top:8px;">💡 点击任一填空也可单独揭示</div>
  </div>
</div>
''')

# ------- 17. 选择题 -------
SLIDES.append('''
<div class="slide" data-slide="17">
  <div class="slide-title">选择题 · 辨析判断</div>
  <div style="max-width:1000px;margin:0 auto;">
    <div class="info-card" style="font-size:22px;margin-top:8px;">
      <b>📝 题目 1：</b>下列关于新制氯水的叙述中，正确的是（　）<br>
      <label style="cursor:pointer;display:block;padding:4px 0;" onclick="checkAnswer(this,'wrong')">A. 新制氯水中只含有 Cl₂ 和 H₂O 分子</label>
      <label style="cursor:pointer;display:block;padding:4px 0;" onclick="checkAnswer(this,'correct')">B. 新制氯水含 Cl₂、HClO、H₂O 三种分子和 H⁺、Cl⁻、ClO⁻、OH⁻ 四种离子</label>
      <label style="cursor:pointer;display:block;padding:4px 0;" onclick="checkAnswer(this,'wrong')">C. 新制氯水放置一段时间后颜色变深</label>
      <label style="cursor:pointer;display:block;padding:4px 0;" onclick="checkAnswer(this,'wrong')">D. 新制氯水的漂白作用来源于 Cl₂ 分子</label>
    </div>
    <div class="info-card" style="font-size:22px;margin-top:10px;">
      <b>📝 题目 2：</b>下列做法能达到实验目的的是（　）<br>
      <label style="cursor:pointer;display:block;padding:4px 0;" onclick="checkAnswer(this,'wrong')">A. 用稀盐酸代替浓盐酸与 MnO₂ 反应制 Cl₂</label>
      <label style="cursor:pointer;display:block;padding:4px 0;" onclick="checkAnswer(this,'wrong')">B. 用 NaOH 溶液洗去 Cl₂ 中混有的 HCl</label>
      <label style="cursor:pointer;display:block;padding:4px 0;" onclick="checkAnswer(this,'correct')">C. 用湿润的淀粉 KI 试纸检验 Cl₂ 是否收集满</label>
      <label style="cursor:pointer;display:block;padding:4px 0;" onclick="checkAnswer(this,'wrong')">D. 用排水法收集 Cl₂</label>
    </div>
    <div class="info-card" style="font-size:22px;margin-top:10px;">
      <b>📝 题目 3：</b>检验某溶液中是否含 Cl⁻，应选用的试剂和顺序是（　）<br>
      <label style="cursor:pointer;display:block;padding:4px 0;" onclick="checkAnswer(this,'wrong')">A. 先加 AgNO₃ 再加稀 HNO₃</label>
      <label style="cursor:pointer;display:block;padding:4px 0;" onclick="checkAnswer(this,'correct')">B. 先加稀 HNO₃ 再加 AgNO₃</label>
      <label style="cursor:pointer;display:block;padding:4px 0;" onclick="checkAnswer(this,'wrong')">C. 先加 BaCl₂ 再加稀 HNO₃</label>
      <label style="cursor:pointer;display:block;padding:4px 0;" onclick="checkAnswer(this,'wrong')">D. 只加盐酸即可</label>
    </div>
  </div>
</div>
''')

# ------- 18. 小游戏 1：现象配对 -------
SLIDES.append('''
<div class="slide" data-slide="18">
  <div class="slide-title">🎮 小游戏 ① · 现象侦探</div>
  <div class="slide-subtitle">看到下面的现象，判断是哪个反应</div>
  <div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:14px; flex:1; padding:5px;">
    <div class="game-card" data-id="1" data-correct="na">
      <div class="game-card-label">
        <span class="emoji">🟡</span>
        发出<b>黄色</b>火焰<br>产生<b>白烟</b>
      </div>
      <div class="game-opts">
        <button class="game-opt-btn" onclick="gamePick(this,'na')">Na + Cl₂</button>
        <button class="game-opt-btn" onclick="gamePick(this,'fe')">Fe + Cl₂</button>
        <button class="game-opt-btn" onclick="gamePick(this,'cu')">Cu + Cl₂</button>
        <button class="game-opt-btn" onclick="gamePick(this,'h2')">H₂ + Cl₂</button>
      </div>
    </div>
    <div class="game-card" data-id="2" data-correct="fe">
      <div class="game-card-label">
        <span class="emoji">🟤</span>
        产生<b>棕褐色</b>的烟<br>产物 +3 价氯化物
      </div>
      <div class="game-opts">
        <button class="game-opt-btn" onclick="gamePick(this,'na')">Na + Cl₂</button>
        <button class="game-opt-btn" onclick="gamePick(this,'fe')">Fe + Cl₂</button>
        <button class="game-opt-btn" onclick="gamePick(this,'cu')">Cu + Cl₂</button>
        <button class="game-opt-btn" onclick="gamePick(this,'h2')">H₂ + Cl₂</button>
      </div>
    </div>
    <div class="game-card" data-id="3" data-correct="cu">
      <div class="game-card-label">
        <span class="emoji">🟧</span>
        产生<b>棕黄色</b>烟<br>溶于水呈蓝色
      </div>
      <div class="game-opts">
        <button class="game-opt-btn" onclick="gamePick(this,'na')">Na + Cl₂</button>
        <button class="game-opt-btn" onclick="gamePick(this,'fe')">Fe + Cl₂</button>
        <button class="game-opt-btn" onclick="gamePick(this,'cu')">Cu + Cl₂</button>
        <button class="game-opt-btn" onclick="gamePick(this,'h2')">H₂ + Cl₂</button>
      </div>
    </div>
    <div class="game-card" data-id="4" data-correct="h2">
      <div class="game-card-label">
        <span class="emoji">🕯️</span>
        <b>苍白色</b>火焰<br>瓶口白雾
      </div>
      <div class="game-opts">
        <button class="game-opt-btn" onclick="gamePick(this,'na')">Na + Cl₂</button>
        <button class="game-opt-btn" onclick="gamePick(this,'fe')">Fe + Cl₂</button>
        <button class="game-opt-btn" onclick="gamePick(this,'cu')">Cu + Cl₂</button>
        <button class="game-opt-btn" onclick="gamePick(this,'h2')">H₂ + Cl₂</button>
      </div>
    </div>
    <div class="game-card" data-id="5" data-correct="h2o">
      <div class="game-card-label">
        <span class="emoji">🌿</span>
        浅黄绿色溶液<br>可逆反应
      </div>
      <div class="game-opts">
        <button class="game-opt-btn" onclick="gamePick(this,'h2o')">Cl₂ + H₂O</button>
        <button class="game-opt-btn" onclick="gamePick(this,'naoh')">Cl₂ + NaOH</button>
        <button class="game-opt-btn" onclick="gamePick(this,'caoh')">Cl₂ + Ca(OH)₂</button>
        <button class="game-opt-btn" onclick="gamePick(this,'na')">Na + Cl₂</button>
      </div>
    </div>
    <div class="game-card" data-id="6" data-correct="caoh">
      <div class="game-card-label">
        <span class="emoji">🧺</span>
        生成漂白粉<br>有效成分 Ca(ClO)₂
      </div>
      <div class="game-opts">
        <button class="game-opt-btn" onclick="gamePick(this,'h2o')">Cl₂ + H₂O</button>
        <button class="game-opt-btn" onclick="gamePick(this,'naoh')">Cl₂ + NaOH</button>
        <button class="game-opt-btn" onclick="gamePick(this,'caoh')">Cl₂ + Ca(OH)₂</button>
        <button class="game-opt-btn" onclick="gamePick(this,'fe')">Fe + Cl₂</button>
      </div>
    </div>
  </div>
  <div id="game-feedback" style="text-align:center; font-size:22px; margin-top:10px;">
    💡 已答 <span id="game-score" style="color:var(--gold); font-weight:bold;">0</span> / 6 题
  </div>
</div>
''')

# ------- 19. 小游戏 2：氯水成分分类 -------
SLIDES.append('''
<div class="slide" data-slide="19">
  <div class="slide-title">🎮 小游戏 ② · 氯水"三分子四离子"</div>
  <div class="slide-subtitle">判断下面每种粒子是否存在于新制氯水中</div>
  <div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:14px; flex:1; padding:5px;">
    <div class="game-card" data-id="1" data-correct="yes">
      <div class="game-card-label"><span class="emoji">🟢</span><b>Cl₂ 分子</b></div>
      <div class="game-opts">
        <button class="game-opt-btn" onclick="gamePick(this,'yes')">✅ 存在</button>
        <button class="game-opt-btn" onclick="gamePick(this,'no')">❌ 不存在</button>
      </div>
    </div>
    <div class="game-card" data-id="2" data-correct="yes">
      <div class="game-card-label"><span class="emoji">💧</span><b>HClO 分子</b></div>
      <div class="game-opts">
        <button class="game-opt-btn" onclick="gamePick(this,'yes')">✅ 存在</button>
        <button class="game-opt-btn" onclick="gamePick(this,'no')">❌ 不存在</button>
      </div>
    </div>
    <div class="game-card" data-id="3" data-correct="no">
      <div class="game-card-label"><span class="emoji">🚫</span><b>HCl 分子</b><br><span style="font-size:14px;color:#999;">HCl 在水中完全电离</span></div>
      <div class="game-opts">
        <button class="game-opt-btn" onclick="gamePick(this,'yes')">✅ 存在</button>
        <button class="game-opt-btn" onclick="gamePick(this,'no')">❌ 不存在</button>
      </div>
    </div>
    <div class="game-card" data-id="4" data-correct="yes">
      <div class="game-card-label"><span class="emoji">⚡</span><b>H⁺ 离子</b></div>
      <div class="game-opts">
        <button class="game-opt-btn" onclick="gamePick(this,'yes')">✅ 存在</button>
        <button class="game-opt-btn" onclick="gamePick(this,'no')">❌ 不存在</button>
      </div>
    </div>
    <div class="game-card" data-id="5" data-correct="yes">
      <div class="game-card-label"><span class="emoji">⚡</span><b>ClO⁻ 离子</b></div>
      <div class="game-opts">
        <button class="game-opt-btn" onclick="gamePick(this,'yes')">✅ 存在</button>
        <button class="game-opt-btn" onclick="gamePick(this,'no')">❌ 不存在</button>
      </div>
    </div>
    <div class="game-card" data-id="6" data-correct="yes">
      <div class="game-card-label"><span class="emoji">⚡</span><b>OH⁻ 离子</b><br><span style="font-size:13px;color:#999;">水的电离，极少</span></div>
      <div class="game-opts">
        <button class="game-opt-btn" onclick="gamePick(this,'yes')">✅ 存在</button>
        <button class="game-opt-btn" onclick="gamePick(this,'no')">❌ 不存在</button>
      </div>
    </div>
  </div>
  <div id="game-feedback" style="text-align:center; font-size:22px; margin-top:10px;">
    💡 已答 <span id="game-score" style="color:var(--gold); font-weight:bold;">0</span> / 6 题
  </div>
</div>
''')

# ------- 20. 小结 -------
SLIDES.append('''
<div class="slide" data-slide="20">
  <div class="slide-title">本节小结 · 知识网络</div>
  <div class="slide-subtitle">从结构出发，一链到底</div>
  <div style="display:flex; flex-direction:column; align-items:center; gap:18px; margin-top:10px;">
    <div class="chain-box">
      <div class="chain-step step-blue">原子结构<br>2,8,<b>7</b></div>
      <span class="chain-arrow">→</span>
      <div class="chain-step step-gold">强氧化性</div>
      <span class="chain-arrow">→</span>
      <div class="chain-step step-red">Cl₂ 化学性质</div>
    </div>
    <div class="chain-box">
      <div class="chain-step step-green">与金属<br>Na/Fe/Cu</div>
      <span class="chain-arrow">·</span>
      <div class="chain-step step-green">与非金属<br>H₂</div>
      <span class="chain-arrow">·</span>
      <div class="chain-step step-green">与水<br>HCl+HClO</div>
      <span class="chain-arrow">·</span>
      <div class="chain-step step-green">与碱<br>NaOH / Ca(OH)₂</div>
    </div>
    <div class="chain-box">
      <div class="chain-step step-purple">实验室制法<br>MnO₂ + 浓HCl</div>
      <span class="chain-arrow">→</span>
      <div class="chain-step step-purple">发生→除杂→干燥→收集→验满→尾气</div>
    </div>
    <div class="chain-box">
      <div class="chain-step step-red">Cl⁻ 检验</div>
      <span class="chain-arrow">→</span>
      <div class="chain-step step-red">AgNO₃ + 稀HNO₃ → AgCl↓</div>
    </div>
  </div>
  <div class="highlight-box" style="max-width:1000px; margin:25px auto 0;">
    🔑 <b>一句话记住：</b>结构（<span class="keyword keyword-red">最外层 7e⁻</span>）→ 性质（<span class="keyword keyword-gold">强氧化性</span>）→ 制备（<span class="keyword keyword-blue">浓 HCl + MnO₂</span>）→ 检验（<span class="keyword keyword-green">AgNO₃</span>）→ 应用（<span class="keyword keyword-purple">消毒漂白</span>）
  </div>
</div>
''')

# =========================================================
#  WEB-SOURCED MEDIA SLIDES (verified URLs)
#  Images fetched from 百度百科 (bkimg.cdn.bcebos.com) and
#  inlined as base64 data URIs — no hotlink/referer risk,
#  fully self-contained HTML.
# =========================================================
FETCH_DATE = '2026-04-10'

import base64 as _b64
def _img_data(path, mime):
    with open(path, 'rb') as f:
        return f'data:{mime};base64,' + _b64.b64encode(f.read()).decode('ascii')

IMG_CL2_COLOR   = _img_data('/tmp/baike_cl2_na_burn.png', 'image/png')
IMG_CL2_BOTTLE  = _img_data('/tmp/baike_cl2_h2_react.png', 'image/png')
IMG_84_BOTTLE   = _img_data('/tmp/baike_84_small.jpg', 'image/jpeg')
IMG_BLEACH_PWD  = _img_data('/tmp/baike_bleach_pwd.png', 'image/png')

# Insert after 物理性质 (slide 3) → index 4 in list
cl_photo_slide = f'''
<div class="slide" data-slide="X">
  <div class="slide-title">真实世界中的 Cl₂ · 黄绿色气体</div>
  <div class="slide-row">
    <div class="slide-col-svg">
      <div class="media-card" style="width:100%;">
        <span class="media-card-badge">📷 百度百科</span>
        <div class="media-card-title">高浓度氯气的颜色</div>
        <div class="media-card-body">
          <img src="{IMG_CL2_COLOR}" alt="高浓度氯气的黄绿色外观" loading="lazy">
        </div>
        <div class="media-card-caption">实拍：高浓度 Cl₂ 呈典型<span class="keyword keyword-green">黄绿色</span></div>
        <div class="media-card-source">
          <span>来源：<a href="https://baike.baidu.com/item/氯气" target="_blank" rel="noopener">百度百科 · 氯气</a></span>
          <span>{FETCH_DATE}</span>
        </div>
      </div>
    </div>
    <div class="slide-col-svg">
      <div class="media-card" style="width:100%; border-color:var(--green);">
        <span class="media-card-badge" style="background:var(--green);">📷 百度百科</span>
        <div class="media-card-title">实验室中的氯气瓶</div>
        <div class="media-card-body">
          <img src="{IMG_CL2_BOTTLE}" alt="盛有氯气的玻璃瓶" loading="lazy">
        </div>
        <div class="media-card-caption">玻璃瓶内可见淡黄绿色 Cl₂ 气体</div>
        <div class="media-card-source">
          <span>来源：<a href="https://baike.baidu.com/item/氯气" target="_blank" rel="noopener">百度百科 · 氯气</a></span>
          <span>{FETCH_DATE}</span>
        </div>
      </div>
    </div>
  </div>
</div>
'''

# Insert after Na + Cl₂ (slide 6) → bilibili video
na_video_slide = f'''
<div class="slide" data-slide="X">
  <div class="slide-title">🎬 演示视频 · 钠在氯气中燃烧</div>
  <div style="max-width:900px; margin:0 auto; width:100%;">
    <div class="media-card">
      <span class="media-card-badge">🎬 网络视频</span>
      <div class="media-card-title">3-1 钠在氯气中燃烧</div>
      <div class="media-card-body">
        <iframe src="https://player.bilibili.com/player.html?bvid=BV1Yv4y1i7W4&page=1&autoplay=0" allowfullscreen scrolling="no" frameborder="0" sandbox="allow-top-navigation allow-same-origin allow-forms allow-scripts" referrerpolicy="no-referrer"></iframe>
      </div>
      <div class="media-card-caption">课本实验演示：观察<span class="keyword keyword-gold">黄色火焰</span>与<span class="keyword keyword-red">白烟</span>（NaCl 颗粒）</div>
      <div class="media-card-source">
        <span>来源：<a href="https://www.bilibili.com/video/BV1Yv4y1i7W4/" target="_blank" rel="noopener">bilibili · 老沈化学</a></span>
        <span>抓取于 {FETCH_DATE}</span>
      </div>
    </div>
  </div>
</div>
'''

# Insert before 小结 → real-world application (two product photos from Baike)
app_slide = f'''
<div class="slide" data-slide="X">
  <div class="slide-title">真实应用 · 氯化学在生活中</div>
  <div class="slide-row">
    <div class="slide-col-svg">
      <div class="media-card" style="width:100%;">
        <span class="media-card-badge">📷 百度百科</span>
        <div class="media-card-title">84 消毒液</div>
        <div class="media-card-body" style="background:#f5f5f5;">
          <img src="{IMG_84_BOTTLE}" alt="84 消毒液产品瓶" loading="lazy">
        </div>
        <div class="media-card-caption">有效成分 <b>NaClO</b> · 对应反应：Cl₂ + 2NaOH → NaCl + <span class="keyword keyword-red">NaClO</span> + H₂O</div>
        <div class="media-card-source">
          <span>来源：<a href="https://baike.baidu.com/item/84消毒液" target="_blank" rel="noopener">百度百科 · 84消毒液</a></span>
          <span>{FETCH_DATE}</span>
        </div>
      </div>
    </div>
    <div class="slide-col-svg">
      <div class="media-card" style="width:100%; border-color:var(--gold);">
        <span class="media-card-badge" style="background:var(--gold);">📷 百度百科</span>
        <div class="media-card-title">漂白粉（Ca(ClO)₂ + CaCl₂）</div>
        <div class="media-card-body" style="background:#111;">
          <img src="{IMG_BLEACH_PWD}" alt="漂白粉白色粉末样品" loading="lazy">
        </div>
        <div class="media-card-caption">白色粉末 · 有效成分 <b>Ca(ClO)₂</b> · 对应反应：2Cl₂ + 2Ca(OH)₂ → Ca(ClO)₂ + CaCl₂ + 2H₂O</div>
        <div class="media-card-source">
          <span>来源：<a href="https://baike.baidu.com/item/漂白粉" target="_blank" rel="noopener">百度百科 · 漂白粉</a></span>
          <span>{FETCH_DATE}</span>
        </div>
      </div>
    </div>
  </div>
  <div class="highlight-box" style="max-width:1100px; margin:14px auto 0;">
    💡 <b>"84" 的由来</b> · 北京<span class="keyword keyword-blue">地坛医院</span>于 <span class="keyword keyword-red">1984 年</span>研制而得名；最初用于肝炎病毒灭活，如今广泛用于家庭/医院/公共场所消毒。漂白粉遇空气中 CO₂ + H₂O → 释放 <span class="keyword keyword-gold">HClO</span>，凭强氧化性完成漂白与杀菌。
  </div>
</div>
'''

# Splice into SLIDES at correct positions (reverse order so earlier indices stay valid)
SLIDES.insert(20, app_slide)   # before 小结 (was at 20)
SLIDES.insert(7, na_video_slide)  # after Na+Cl₂ (was at 6)
SLIDES.insert(4, cl_photo_slide)  # after 物理性质 (was at 3)

# Renumber data-slide attrs based on final position
import re as _re
for i in range(len(SLIDES)):
    SLIDES[i] = _re.sub(r'data-slide="[^"]*"', f'data-slide="{i}"', SLIDES[i], count=1)

# =========================================================
#  NAV DOTS
# =========================================================
N = len(SLIDES)
dot_titles = [
    '封面','节次','发现史','物理性质','📷Cl₂实拍','原子结构',
    '金属反应总览','Na+Cl₂','🎬Na燃烧','Fe+Cl₂','Cu+Cl₂','H₂+Cl₂',
    'Cl₂+H₂O','氯水对比','Cl₂+碱','实验室制法总览','装置详解',
    'Cl⁻检验','填空练习','选择题','游戏①现象','游戏②氯水',
    '📡真实应用','小结'
]
assert len(dot_titles) == N, f'{len(dot_titles)} vs {N}'
dots_html = '\n  '.join(
    f'<button class="nav-dot{" active" if i==0 else ""}" data-target="{i}" title="{dot_titles[i]}"></button>'
    for i in range(N)
)
nav = nav_tpl.replace('{{NAV_DOTS}}', dots_html).replace('{{N_SLIDES}}', str(N))

# =========================================================
#  Final assembly
# =========================================================
parts = [head]
parts.extend(SLIDES)
parts.append(nav)
parts.append(scripts_js)
parts.append(editor_html)
parts.append('\n</body>\n</html>\n')

final = ''.join(parts)

# Sanity check: exactly one </body> outside of scripts
# We will only care about the final one. Ensure file ends cleanly.
OUT.write_text(final, encoding='utf-8')
print(f'Wrote {OUT} ({len(final):,} bytes, {N} slides)')
