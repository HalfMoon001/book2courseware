<script>
// ================================================================
//  book2courseware · runtime scripts
//  提供：翻页、填空、选择题反馈
//  任何课件都应原封不动地嵌入这段 <script>
//
//  NOTE on the closure bug we used to have:
//  Previously this file cached `slides`, `current`, and `total` in the IIFE
//  closure. That broke two ways:
//    (1) editor.html later overrides `window.goTo` with a version that
//        re-queries the DOM. The keydown handler below calls `window.goTo`
//        (via bare `goTo`), so navigation worked, but the cached `current`
//        here never updated — so `goTo(current + 1)` kept resolving to
//        `goTo(1)` forever after the first press and the deck got stuck.
//    (2) After undo/redo or add/delete-slide, the DOM gets new .slide nodes
//        but the cached `slides` NodeList still pointed at stale / detached
//        elements, so any subsequent non-editor.html path stopped working.
//  Fix: every lookup (slides list, current index) is re-queried on demand.
//  window.goTo reads `.slide.active` from the DOM; editor.html can still
//  override it freely.
// ================================================================
(function() {
  function allSlides() { return document.querySelectorAll('.slide'); }
  function allDots()   { return document.querySelectorAll('.nav-dot'); }
  function currentIdx() {
    var slides = allSlides();
    for (var i = 0; i < slides.length; i++) if (slides[i].classList.contains('active')) return i;
    return 0;
  }

  window.goTo = function(index) {
    var slides = allSlides();
    var dots = allDots();
    var pageLabel = document.querySelector('.nav-page');
    var total = slides.length;
    if (total === 0) return;
    if (index < 0) index = 0;
    if (index >= total) index = total - 1;
    slides.forEach(function(s, i) { s.classList.toggle('active', i === index); });
    dots.forEach(function(d, i) { d.classList.toggle('active', i === index); });
    if (pageLabel) pageLabel.textContent = (index + 1) + ' / ' + total;
    window.scrollTo(0, 0);
  };

  document.addEventListener('keydown', function(e) {
    // 编辑器激活或在输入框里时，不抢键盘
    if (document.activeElement) {
      var tag = document.activeElement.tagName;
      if (tag === 'INPUT' || tag === 'TEXTAREA' || document.activeElement.getAttribute('contenteditable')) return;
    }
    if (e.key === 'ArrowRight' || e.key === 'PageDown') { e.preventDefault(); window.goTo(currentIdx() + 1); }
    else if (e.key === 'ArrowLeft' || e.key === 'PageUp') { e.preventDefault(); window.goTo(currentIdx() - 1); }
    else if (e.key === 'Home') { e.preventDefault(); window.goTo(0); }
    else if (e.key === 'End')  { e.preventDefault(); window.goTo(allSlides().length - 1); }
    // ArrowUp/Down 交给浏览器原生滚动
  });

  // Delegate dot clicks so it survives rebuildNavDots in editor.html
  document.addEventListener('click', function(e) {
    var dot = e.target.closest && e.target.closest('.nav-dot');
    if (!dot) return;
    var t = dot.getAttribute('data-target');
    if (t != null) window.goTo(parseInt(t, 10));
  });

  // 触屏滑动翻页
  var touchStartX = 0;
  document.addEventListener('touchstart', function(e) { touchStartX = e.changedTouches[0].screenX; }, { passive: true });
  document.addEventListener('touchend', function(e) {
    var diff = touchStartX - e.changedTouches[0].screenX;
    if (Math.abs(diff) > 50) window.goTo(currentIdx() + (diff > 0 ? 1 : -1));
  }, { passive: true });

  // 填空：点击揭示答案 (delegated so restored/added blanks still work)
  document.addEventListener('click', function(e) {
    var blank = e.target.closest && e.target.closest('.blank');
    if (!blank) return;
    if (blank.getAttribute('onclick')) return;
    blank.classList.toggle('revealed');
  });
})();

// ================================================================
//  选择题反馈 · 在 label 的 onclick 里调用 checkAnswer(this, 'correct'|'wrong')
// ================================================================
function checkAnswer(label, type) {
  if (label.dataset.answered) return;
  var card = label.closest('.info-card');
  card.querySelectorAll('label').forEach(function(l) { l.dataset.answered = '1'; });
  if (type === 'correct') {
    label.classList.add('answer-correct');
    label.innerHTML += ' <b style="color:var(--green);">✅ 正确！</b>';
  } else {
    label.classList.add('answer-wrong');
    label.innerHTML += ' <b style="color:var(--red);">❌</b>';
    // 自动高亮正确答案
    card.querySelectorAll('label').forEach(function(l) {
      var click = l.getAttribute('onclick') || '';
      if (click.indexOf('correct') !== -1) l.classList.add('answer-correct');
    });
  }
}

// ================================================================
//  揭示当前页所有填空（给 fill-blank-slide 的 "显示全部答案" 按钮用）
// ================================================================
function revealAllBlanks(btn) {
  btn.closest('.slide').querySelectorAll('.blank').forEach(function(b) {
    b.classList.add('revealed');
  });
}

// ================================================================
//  MINI-GAME · 通用"判断/配对"游戏逻辑
//  用在 judge-game.html / match-game.html 组件上
//
//  HTML 约定：
//    <div class="game-card" data-id="1" data-correct="radio">
//      <div class="game-card-label">...</div>
//      <div class="game-opts">
//        <button class="game-opt-btn" onclick="gamePick(this,'radio')">无线电</button>
//        <button class="game-opt-btn" onclick="gamePick(this,'ir')">红外</button>
//        ...
//      </div>
//    </div>
//    <div id="game-score">0</div>
//    <div id="game-feedback">...</div>
//
//  用 data-correct 标记正确答案，gamePick 会对比并反馈。
// ================================================================
(function(){
  var answered = {};
  var score = 0;
  var total = null;
  window.gamePick = function(btn, pick) {
    var card = btn.closest('.game-card');
    var id = card.getAttribute('data-id');
    if (answered[id]) return;
    answered[id] = true;
    var correct = card.getAttribute('data-correct');
    if (pick === correct) {
      btn.classList.add('game-correct');
      score++;
    } else {
      btn.classList.add('game-wrong');
      // Highlight the correct sibling
      card.querySelectorAll('.game-opt-btn').forEach(function(b) {
        var oc = b.getAttribute('onclick') || '';
        if (oc.indexOf("'" + correct + "'") !== -1) b.classList.add('game-correct');
      });
    }
    var scoreEl = document.getElementById('game-score');
    if (scoreEl) scoreEl.textContent = score;
    if (total === null) {
      total = document.querySelectorAll('.game-card').length;
    }
    if (Object.keys(answered).length === total) {
      var fb = document.getElementById('game-feedback');
      if (fb) fb.innerHTML = '🎉 完成！总得分 <b style="color:var(--gold); font-size:26px;">' + score + ' / ' + total + '</b>';
    }
  };
})();
</script>
