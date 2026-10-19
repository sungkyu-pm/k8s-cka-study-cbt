/**
 * Kubernetes & Cloud Native Certification (CKA & KCNA) 통합 포털 스크립트
 */

// 문서 매핑 정보 (CKA & KCNA)
const DOC_KEYS = {
  // CKA
  overview: 'exam_guide',
  glossary: 'glossary',
  domain1: 'domain1',
  domain2: 'domain2',
  domain3: 'domain3',
  domain4: 'domain4',
  domain5: 'domain5',
  kubectl_cheat: 'kubectl_cheat',
  // KCNA
  kcna_overview: 'kcna_guide',
  kcna_glossary: 'kcna_glossary',
  kcna_domain1: 'kcna_domain1',
  kcna_domain2: 'kcna_domain2',
  kcna_domain3: 'kcna_domain3',
  kcna_domain4: 'kcna_domain4',
  kcna_domain5: 'kcna_domain5'
};

const docCache = {};
let activeTrack = 'cka'; // 'cka' or 'kcna'
let activeTab = 'overview';
const isGitHubPages = window.location.hostname.includes('github.io');

document.addEventListener('DOMContentLoaded', () => {
  initServerStatus();
  initTrackSwitching();
  initTabNavigation();
  initGlossarySearch();

  // 초기 트랙 및 탭 감지 (URL param -> hash -> localStorage 순)
  const urlParams = new URLSearchParams(window.location.search);
  const paramTrack = urlParams.get('track');
  const rawHash = (window.location.hash || '').replace('#', '').trim().toLowerCase();
  const savedTrack = localStorage.getItem('k8s_cert_track');

  let initialTrack = 'cka';
  let initialTab = null;

  if (rawHash === 'kcna' || paramTrack === 'kcna' || (!rawHash && savedTrack === 'kcna')) {
    initialTrack = 'kcna';
    initialTab = 'kcna_overview'; // KCNA 기본값: 개요 & 전략
  } else if (rawHash === 'cka' || paramTrack === 'cka' || (!rawHash && savedTrack === 'cka')) {
    initialTrack = 'cka';
    initialTab = 'overview'; // CKA 기본값: 개요 & 로드맵
  } else if (rawHash) {
    // 특정 서브 탭 해시 (예: #domain1, #cbt, #kcna_domain2 등)
    if (rawHash.startsWith('kcna_')) {
      initialTrack = 'kcna';
      initialTab = rawHash;
    } else {
      initialTrack = 'cka';
      initialTab = rawHash;
    }
  } else {
    initialTrack = 'cka';
    initialTab = 'overview';
  }

  // 초기 트랙 및 탭 적용
  switchCertTrack(initialTrack, false, initialTab);

  // 해시 변경 감지 (뒤로가기/앞으로가기 또는 외부 딥링크)
  window.addEventListener('hashchange', () => {
    const currentHash = (window.location.hash || '').replace('#', '').trim().toLowerCase();
    if (currentHash === 'kcna') {
      switchCertTrack('kcna', false, 'kcna_overview');
    } else if (currentHash === 'cka') {
      switchCertTrack('cka', false, 'overview');
    } else if (currentHash) {
      if (currentHash.startsWith('kcna_')) {
        if (activeTrack !== 'kcna') {
          switchCertTrack('kcna', false, currentHash);
        } else {
          switchTab(currentHash, false);
        }
      } else {
        if (activeTrack !== 'cka') {
          switchCertTrack('cka', false, currentHash);
        } else {
          switchTab(currentHash, false);
        }
      }
    }
  });
});

/**
 * 1. 서버 상태 감지 및 인디케이터 표시
 */
async function initServerStatus() {
  const statusBox = document.getElementById('server-status-box');
  const statusDot = statusBox ? statusBox.querySelector('.status-indicator-dot') : null;
  const statusText = document.getElementById('server-status-text');

  if (isGitHubPages) {
    if (statusDot) statusDot.className = 'status-indicator-dot online';
    if (statusText) statusText.textContent = 'GitHub Pages 온라인 (1,510문항)';
    return;
  }

  try {
    const res = await fetch('/api/status', { cache: 'no-cache' });
    if (res.ok) {
      const data = await res.json();
      if (statusDot) statusDot.className = 'status-indicator-dot online';
      if (statusText) statusText.textContent = `로컬 서버 온라인 (${data.total_questions || 1510}문항)`;
    } else {
      throw new Error('Server returned non-200');
    }
  } catch (err) {
    if (statusDot) statusDot.className = 'status-indicator-dot';
    if (statusText) statusText.textContent = '정적 파일 모드 (Offline)';
  }
}

/**
 * 2. 자격증 트랙 전환 제어 (CKA vs KCNA)
 */
function initTrackSwitching() {
  const btnCka = document.getElementById('track-cka-btn');
  const btnKcna = document.getElementById('track-kcna-btn');

  if (btnCka) {
    btnCka.onclick = (e) => {
      e.preventDefault();
      switchCertTrack('cka', true, 'overview');
    };
  }

  if (btnKcna) {
    btnKcna.onclick = (e) => {
      e.preventDefault();
      switchCertTrack('kcna', true, 'kcna_overview');
    };
  }
}

/**
 * 전역 트랙 전환 함수 (상단 탭 누를 시 항상 default '개요 & 로드맵' 선택)
 */
window.switchCertTrack = function(track, shouldUpdateHistory = true, targetTab = null) {
  activeTrack = track === 'kcna' ? 'kcna' : 'cka';
  localStorage.setItem('k8s_cert_track', activeTrack);

  const btnCka = document.getElementById('track-cka-btn');
  const btnKcna = document.getElementById('track-kcna-btn');
  const navCka = document.getElementById('nav-cka');
  const navKcna = document.getElementById('nav-kcna');
  const portalTitle = document.getElementById('portal-title');
  const portalSubtitle = document.getElementById('portal-subtitle');
  const cbtIframe = document.getElementById('cbt-iframe');
  const cbtQuickBtnLabel = document.getElementById('cbt-quick-btn-label');
  const cbtFullscreenLink = document.getElementById('cbt-fullscreen-link');
  const cbtToolbarTitle = document.getElementById('cbt-toolbar-title');
  const cbtToolbarDesc = document.getElementById('cbt-toolbar-desc');

  if (activeTrack === 'kcna') {
    // 버튼 상태
    if (btnCka) btnCka.classList.remove('active');
    if (btnKcna) btnKcna.classList.add('active', 'kcna-active');

    // 네비게이션 표시
    if (navCka) navCka.style.display = 'none';
    if (navKcna) navKcna.style.display = 'block';

    // 헤더 타이틀 갱신
    if (portalTitle) portalTitle.textContent = 'KCNA Cloud Native Associate Certification';
    if (portalSubtitle) portalSubtitle.textContent = 'CNCF 공식 필기 가이드 (5대 영역 심층 학습 & 260문항 CBT)';
    if (cbtQuickBtnLabel) cbtQuickBtnLabel.textContent = '💻 KCNA 실전 CBT (260문항)';

    if (cbtToolbarTitle) cbtToolbarTitle.textContent = 'KCNA 클라우드 네이티브 어소시에이트 실전 CBT 시뮬레이터';
    if (cbtToolbarDesc) cbtToolbarDesc.textContent = 'CNCF 공식 출제 기준 260문항 풀 · 90분 타이머 · 75% 합격 기준 · 실시간 한/영 번역 및 개념 해설';
    if (cbtFullscreenLink) cbtFullscreenLink.href = `./cbt-app/index.html?track=kcna&v=20261019_1705`;

    // 상단 탭 클릭 시 default는 무조건 'KCNA 시험 안내 & 전략'(kcna_overview)
    const nextTab = targetTab || 'kcna_overview';
    switchTab(nextTab, shouldUpdateHistory);
  } else {
    // CKA 트랙
    if (btnCka) btnCka.classList.add('active');
    if (btnKcna) btnKcna.classList.remove('active', 'kcna-active');

    // 네비게이션 표시
    if (navCka) navCka.style.display = 'block';
    if (navKcna) navKcna.style.display = 'none';

    // 헤더 타이틀 갱신
    if (portalTitle) portalTitle.textContent = 'Kubernetes Administrator (CKA) Certification';
    if (portalSubtitle) portalSubtitle.textContent = 'Linux Foundation & CNCF 공식 실기 대비 (1,250문항 CBT & 5대 도메인 심층 가이드)';
    if (cbtQuickBtnLabel) cbtQuickBtnLabel.textContent = '💻 CKA 실전 CBT (1,250문항)';

    if (cbtToolbarTitle) cbtToolbarTitle.textContent = 'CKA 쿠버네티스 공인 관리자 실전 CBT 시뮬레이터';
    if (cbtToolbarDesc) cbtToolbarDesc.textContent = '5대 도메인 1,250문항 풀 · 120분 타이머 · 66% 합격 기준 · 실기 시나리오 중심 무작위 추출';
    if (cbtFullscreenLink) cbtFullscreenLink.href = `./cbt-app/index.html?track=cka&v=20261019_1705`;

    // 상단 탭 클릭 시 default는 무조건 'CKA 개요 & 로드맵'(overview)
    const nextTab = targetTab || 'overview';
    switchTab(nextTab, shouldUpdateHistory);
  }

  // CBT Iframe src 동기화
  if (cbtIframe && activeTab !== 'cbt') {
    cbtIframe.src = `./cbt-app/index.html?track=${activeTrack}&v=20261019_1705`;
  }
};

/**
 * 3. 서브 탭 네비게이션 제어
 */
function initTabNavigation() {
  const tabs = document.querySelectorAll('.nav-tab, .nav-tab-btn');

  tabs.forEach(tab => {
    tab.addEventListener('click', (e) => {
      const targetTab = tab.getAttribute('data-tab');
      if (!targetTab) return;

      switchTab(targetTab, true);
    });
  });
}

window.switchTab = function(tabId, updateHistory = true) {
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

  // URL 해시 동기화
  if (updateHistory && history.replaceState) {
    if (tabId === 'overview' && activeTrack === 'cka') {
      history.replaceState(null, '', '#cka');
    } else if (tabId === 'kcna_overview' && activeTrack === 'kcna') {
      history.replaceState(null, '', '#kcna');
    } else {
      history.replaceState(null, '', `#${tabId}`);
    }
  }

  // 콘텐츠 로드 (CBT 탭 제외)
  if (tabId !== 'cbt') {
    loadCurrentTabContent(tabId);
  } else {
    // CBT iframe 동기화
    const cbtIframe = document.getElementById('cbt-iframe');
    if (cbtIframe) {
      const expectedSrc = `./cbt-app/index.html?track=${activeTrack}&v=20261019_1705`;
      if (!cbtIframe.src || !cbtIframe.src.includes(`track=${activeTrack}`)) {
        cbtIframe.src = expectedSrc;
      }
    }
  }

  // 윈도우 스크롤 상단 이동
  window.scrollTo({ top: 0, behavior: 'smooth' });
};

/**
 * 4. 마크다운 문서 로드 및 렌더링
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

  let markdownText = '';

  // 1순위: GitHub Pages이거나 정적 번들링 객체가 있는 경우 즉시 번들에서 로드 (지연 0ms)
  if (window.PORTAL_DOCS && window.PORTAL_DOCS[docKey]) {
    markdownText = window.PORTAL_DOCS[docKey];
  }

  // 2순위: 번들에 없고 로컬 백엔드 서버인 경우 API 조회
  if (!markdownText && !isGitHubPages) {
    contentEl.innerHTML = '<div style="text-align: center; padding: 2rem; color: #64748b;">📖 문서를 불러오는 중입니다...</div>';
    try {
      const res = await fetch(`/api/docs?key=${docKey}`);
      if (res.ok) {
        const data = await res.json();
        markdownText = data.content;
      }
    } catch (err) {
      console.warn('Backend /api/docs fetch failed:', err);
    }
  }

  if (markdownText) {
    const html = renderMarkdown(markdownText);
    docCache[docKey] = html;
    contentEl.innerHTML = html;
  } else {
    contentEl.innerHTML = `
      <div style="color: #ef4444; padding: 3rem; text-align: center; background: #fee2e2; border-radius: 8px;">
        <h3>⚠️ 문서를 불러오지 못했습니다.</h3>
        <p>요청한 문서 키: <code>${escapeHtml(docKey)}</code></p>
        <button onclick="delete docCache['${docKey}']; loadCurrentTabContent('${tabId}');" style="padding: 0.5rem 1rem; margin-top: 1rem; border-radius: 4px; border: 1px solid #ef4444; background: white; cursor: pointer;">다시 시도</button>
      </div>
    `;
  }
}

/**
 * marked 라이브러리를 사용한 마크다운 파싱
 */
function renderMarkdown(md) {
  if (typeof marked !== 'undefined') {
    return marked.parse(md);
  }
  return `<pre style="white-space: pre-wrap; font-family: monospace; padding: 1.5rem; background: #f8fafc; border-radius: 8px;">${escapeHtml(md)}</pre>`;
}

function escapeHtml(str) {
  if (!str) return '';
  return str.replace(/[&<>'"]/g, tag => ({
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    "'": '&#39;',
    '"': '&quot;'
  }[tag] || tag));
}

/**
 * 5. 용어사전 검색 필터링 기능 (CKA & KCNA)
 */
function initGlossarySearch() {
  // CKA 용어사전 검색
  const ckaInput = document.getElementById('glossary-search');
  const ckaClear = document.getElementById('glossary-clear-btn');
  if (ckaInput) {
    ckaInput.addEventListener('input', (e) => {
      filterGlossary('glossary-content', e.target.value.toLowerCase().trim());
    });
    if (ckaClear) {
      ckaClear.addEventListener('click', () => {
        ckaInput.value = '';
        filterGlossary('glossary-content', '');
        ckaInput.focus();
      });
    }
  }

  // KCNA 용어사전 검색
  const kcnaInput = document.getElementById('kcna-glossary-search');
  const kcnaClear = document.getElementById('kcna-glossary-clear-btn');
  if (kcnaInput) {
    kcnaInput.addEventListener('input', (e) => {
      filterGlossary('kcna_glossary-content', e.target.value.toLowerCase().trim());
    });
    if (kcnaClear) {
      kcnaClear.addEventListener('click', () => {
        kcnaInput.value = '';
        filterGlossary('kcna_glossary-content', '');
        kcnaInput.focus();
      });
    }
  }
}

function filterGlossary(containerId, query) {
  const glossaryEl = document.getElementById(containerId);
  if (!glossaryEl) return;

  const tableRows = glossaryEl.querySelectorAll('tbody tr');
  if (tableRows && tableRows.length > 0) {
    tableRows.forEach(row => {
      const text = row.textContent.toLowerCase();
      row.style.display = (!query || text.includes(query)) ? '' : 'none';
    });
  }

  const listItems = glossaryEl.querySelectorAll('li, p');
  if (listItems && listItems.length > 0) {
    listItems.forEach(item => {
      const text = item.textContent.toLowerCase();
      if (!query || text.includes(query)) {
        item.style.display = '';
      } else {
        item.style.display = 'none';
      }
    });
  }
}
