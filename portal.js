/**
 * Kubernetes Certification (CKA / CKAD) 통합 포털 스크립트
 */

document.addEventListener('DOMContentLoaded', () => {
  initServerStatus();
  initTabNavigation();
  initGlossarySearch();
  loadCurrentTabContent('overview');
});

// 문서 매핑 정보
const DOC_KEYS = {
  overview: 'exam_guide',
  glossary: 'glossary',
  domain1: 'domain1',
  domain2: 'domain2',
  domain3: 'domain3',
  domain4: 'domain4',
  domain5: 'domain5',
  kubectl_cheat: 'kubectl_cheat'
};

const docCache = {};
let activeTab = 'overview';

/**
 * 1. 서버 상태 감지 및 인디케이터 표시
 */
async function initServerStatus() {
  const statusBox = document.getElementById('server-status-box');
  const statusDot = statusBox.querySelector('.status-indicator-dot');
  const statusText = document.getElementById('server-status-text');

  try {
    const res = await fetch('/api/status', { cache: 'no-cache' });
    if (res.ok) {
      const data = await res.json();
      statusDot.className = 'status-indicator-dot online';
      statusText.textContent = `로컬 서버 온라인 (문제 ${data.total_questions}문항)`;
    } else {
      throw new Error('Server returned non-200');
    }
  } catch (err) {
    statusDot.className = 'status-indicator-dot';
    statusText.textContent = '정적 파일 모드 (Offline)';
  }
}

/**
 * 2. 탭 네비게이션 바 제어
 */
function initTabNavigation() {
  const tabs = document.querySelectorAll('.nav-tab, .nav-tab-btn');

  tabs.forEach(tab => {
    tab.addEventListener('click', (e) => {
      const targetTab = tab.getAttribute('data-tab');
      if (!targetTab) return;

      switchTab(targetTab);
    });
  });
}

function switchTab(tabId) {
  activeTab = tabId;

  // 탭 버튼 스타일 갱신
  document.querySelectorAll('.nav-tab').forEach(t => {
    t.classList.toggle('active', t.getAttribute('data-tab') === tabId);
  });

  // 탭 패널 표시 갱신
  document.querySelectorAll('.tab-panel').forEach(p => {
    p.classList.remove('active');
  });

  const targetPanel = document.getElementById(`tab-${tabId}`);
  if (targetPanel) {
    targetPanel.classList.add('active');
  }

  // 콘텐츠 로드 (CBT 탭 제외)
  if (tabId !== 'cbt') {
    loadCurrentTabContent(tabId);
  }
}

/**
 * 3. 마크다운 문서 로드 및 렌더링
 */
async function loadCurrentTabContent(tabId) {
  const docKey = DOC_KEYS[tabId];
  if (!docKey) return;

  const contentEl = document.getElementById(`${tabId}-content`);
  if (!contentEl) return;

  // 이미 렌더링되어 있으면 반환
  if (docCache[docKey]) {
    contentEl.innerHTML = docCache[docKey];
    return;
  }

  contentEl.innerHTML = '<div style="text-align: center; padding: 2rem; color: #64748b;">📖 문서를 불러오는 중입니다...</div>';

  let markdownText = '';

  // 1차 시도: 백엔드 API
  try {
    const res = await fetch(`/api/docs?key=${docKey}`);
    if (res.ok) {
      const data = await res.json();
      markdownText = data.content;
    }
  } catch (err) {
    // API 연결 실패 시 아래 폴백으로 진행
  }

  // 2차 시도: 번들링된 PORTAL_DOCS 폴백
  if (!markdownText && window.PORTAL_DOCS && window.PORTAL_DOCS[docKey]) {
    markdownText = window.PORTAL_DOCS[docKey];
  }

  if (markdownText) {
    const html = renderMarkdown(markdownText);
    docCache[docKey] = html;
    contentEl.innerHTML = html;
  } else {
    contentEl.innerHTML = '<div style="color: #ef4444; padding: 2rem;">문서를 불러오지 못했습니다.</div>';
  }
}

/**
 * marked 라이브러리를 사용한 마크다운 파싱
 */
function renderMarkdown(md) {
  if (typeof marked !== 'undefined') {
    return marked.parse(md);
  }
  // 단순 텍스트 폴백
  return `<pre style="white-space: pre-wrap;">${escapeHtml(md)}</pre>`;
}

function escapeHtml(str) {
  return str.replace(/[&<>'"]/g, tag => ({
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    "'": '&#39;',
    '"': '&quot;'
  }[tag] || tag));
}

/**
 * 4. 용어사전 검색 필터링 기능
 */
function initGlossarySearch() {
  const searchInput = document.getElementById('glossary-search');
  const clearBtn = document.getElementById('glossary-clear-btn');
  if (!searchInput) return;

  searchInput.addEventListener('input', (e) => {
    const query = e.target.value.toLowerCase().trim();
    filterGlossary(query);
  });

  if (clearBtn) {
    clearBtn.addEventListener('click', () => {
      searchInput.value = '';
      filterGlossary('');
      searchInput.focus();
    });
  }
}

function filterGlossary(query) {
  const glossaryEl = document.getElementById('glossary-content');
  if (!glossaryEl) return;

  const rows = glossaryEl.querySelectorAll('tbody tr');
  if (!rows || rows.length === 0) return;

  rows.forEach(row => {
    const text = row.textContent.toLowerCase();
    if (!query || text.includes(query)) {
      row.style.display = '';
    } else {
      row.style.display = 'none';
    }
  });
}
