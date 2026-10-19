/**
 * Kubernetes Administrator (CKA) CBT Simulation Engine
 */

class K8sCBTSimulator {
  constructor() {
    this.questions = [];
    this.currentIndex = 0;
    this.userAnswers = {}; // { questionId: 'A' }
    this.flaggedQuestions = new Set();
    this.checkedQuestions = new Set(); // 학습 모드에서 정답 확인을 누른 문항
    this.mode = 'study'; // 'study' or 'exam'
    this.koreanVisible = false;
    this.timerInterval = null;
    this.secondsRemaining = 0;
    this.totalSeconds = 0;
    this.timeSpentSeconds = 0;
    this.isReviewMode = false;
    this.selectedExamSet = 'mock_random';
    this.currentTrack = 'cka'; // 'cka' or 'kcna'
    this.passingScorePct = 66; // 66% for CKA, 75% for KCNA

    this.initDOMElements();
    this.bindEvents();
    this.checkInitialURLTrack();
  }

  initDOMElements() {
    // 화면들
    this.startScreen = document.getElementById('start-screen');
    this.examScreen = document.getElementById('exam-screen');
    this.resultScreen = document.getElementById('result-screen');

    // 트랙 컨트롤
    this.cbtCertCka = document.getElementById('cbt-cert-cka');
    this.cbtCertKcna = document.getElementById('cbt-cert-kcna');
    this.cbtWelcomeTitle = document.getElementById('cbt-welcome-title');
    this.cbtWelcomeDesc = document.getElementById('cbt-welcome-desc');
    this.scopeCardTitle = document.getElementById('scope-card-title');
    this.ckaScopeGroup = document.getElementById('cka-scope-group');
    this.kcnaScopeGroup = document.getElementById('kcna-scope-group');
    this.ckaCountGroup = document.getElementById('cka-count-group');
    this.kcnaCountGroup = document.getElementById('kcna-count-group');
    this.examTitle = document.querySelector('.exam-title');

    // 헤더 컨트롤
    this.timerBox = document.getElementById('timer-box');
    this.timeDisplay = document.getElementById('time-display');
    this.modeToggleBtn = document.getElementById('mode-toggle-btn');
    this.modeLabel = document.getElementById('mode-label');
    this.modeIcon = document.getElementById('mode-icon');

    // 문제 표시 컴포넌트
    this.qCounter = document.getElementById('q-counter');
    this.qDomain = document.getElementById('q-domain');
    this.toggleFlagBtn = document.getElementById('toggle-flag-btn');
    this.flagText = document.getElementById('flag-text');
    this.toggleTransBtn = document.getElementById('toggle-trans-btn');
    this.qTextEn = document.getElementById('q-text-en');
    this.qTextKr = document.getElementById('q-text-kr');
    this.optionsContainer = document.getElementById('options-container');

    // 피드백 (학습 모드)
    this.studyFeedbackBox = document.getElementById('study-feedback-box');
    this.feedbackBadge = document.getElementById('feedback-badge');
    this.feedbackKeyConcept = document.getElementById('feedback-key-concept');
    this.feedbackExplanation = document.getElementById('feedback-explanation');
    this.checkAnswerBtn = document.getElementById('check-answer-btn');

    // 네비게이션
    this.prevBtn = document.getElementById('prev-btn');
    this.nextBtn = document.getElementById('next-btn');
    this.finishExamBtn = document.getElementById('finish-exam-btn');
    this.questionNavGrid = document.getElementById('question-nav-grid');
    this.answeredCountBadge = document.getElementById('answered-count-badge');

    // 결과 화면 컴포넌트
    this.passFailBadge = document.getElementById('pass-fail-badge');
    this.scorePercentage = document.getElementById('score-percentage');
    this.scoreRaw = document.getElementById('score-raw');
    this.totalTimeSpent = document.getElementById('total-time-spent');
    this.accuracyRate = document.getElementById('accuracy-rate');
    this.domainStatsList = document.getElementById('domain-stats-list');
    this.reviewWrongBtn = document.getElementById('review-wrong-btn');
    this.restartBtn = document.getElementById('restart-btn');
    this.startExamBtn = document.getElementById('start-exam-btn');
  }

  bindEvents() {
    this.startExamBtn.addEventListener('click', () => this.startExamFromSettings());
    this.prevBtn.addEventListener('click', () => this.navigateQuestion(-1));
    this.nextBtn.addEventListener('click', () => this.navigateQuestion(1));
    this.toggleTransBtn.addEventListener('click', () => this.toggleTranslation());
    this.toggleFlagBtn.addEventListener('click', () => this.toggleFlag());
    this.checkAnswerBtn.addEventListener('click', () => this.checkCurrentAnswer());
    this.finishExamBtn.addEventListener('click', () => this.confirmSubmitExam());

    this.reviewWrongBtn.addEventListener('click', () => this.startWrongReviewMode());
    this.restartBtn.addEventListener('click', () => this.showStartScreen());
    this.modeToggleBtn.addEventListener('click', () => this.switchModeInExam());

    if (this.cbtCertCka) {
      this.cbtCertCka.addEventListener('click', () => this.switchTrack('cka'));
    }
    if (this.cbtCertKcna) {
      this.cbtCertKcna.addEventListener('click', () => this.switchTrack('kcna'));
    }
  }

  checkInitialURLTrack() {
    const urlParams = new URLSearchParams(window.location.search);
    const track = urlParams.get('track');
    if (track === 'kcna') {
      this.switchTrack('kcna');
    }
  }

  switchTrack(track) {
    this.currentTrack = track === 'kcna' ? 'kcna' : 'cka';
    if (this.currentTrack === 'kcna') {
      this.passingScorePct = 75;
      if (this.cbtCertKcna) this.cbtCertKcna.classList.add('active', 'kcna-active');
      if (this.cbtCertCka) this.cbtCertCka.classList.remove('active');

      if (this.ckaScopeGroup) {
        this.ckaScopeGroup.style.display = 'none';
        this.ckaScopeGroup.querySelectorAll('input').forEach(i => i.disabled = true);
      }
      if (this.kcnaScopeGroup) {
        this.kcnaScopeGroup.style.display = 'block';
        this.kcnaScopeGroup.querySelectorAll('input').forEach(i => i.disabled = false);
      }

      if (this.ckaCountGroup) {
        this.ckaCountGroup.style.display = 'none';
        this.ckaCountGroup.querySelectorAll('input').forEach(i => i.disabled = true);
      }
      if (this.kcnaCountGroup) {
        this.kcnaCountGroup.style.display = 'block';
        this.kcnaCountGroup.querySelectorAll('input').forEach(i => i.disabled = false);
      }

      if (this.cbtWelcomeTitle) this.cbtWelcomeTitle.textContent = 'Kubernetes and Cloud Native Associate (KCNA) CBT 실습';
      if (this.cbtWelcomeDesc) this.cbtWelcomeDesc.textContent = 'CNCF 공식 시험 기준 객관식 60문항 대비, 클라우드 네이티브 아키텍처와 쿠버네티스 원리를 완벽 마스터합니다.';
      if (this.scopeCardTitle) this.scopeCardTitle.textContent = '1. 학습 범위 선택 (KCNA 260문항 풀)';
      if (this.examTitle) this.examTitle.textContent = 'Cloud Native Associate (KCNA)';

      const firstKcnaRadio = this.kcnaScopeGroup ? this.kcnaScopeGroup.querySelector('input[type="radio"]') : null;
      if (firstKcnaRadio) firstKcnaRadio.checked = true;
      const firstKcnaCount = this.kcnaCountGroup ? this.kcnaCountGroup.querySelector('input[value="60"]') : null;
      if (firstKcnaCount) firstKcnaCount.checked = true;
    } else {
      this.passingScorePct = 66;
      if (this.cbtCertCka) this.cbtCertCka.classList.add('active');
      if (this.cbtCertKcna) this.cbtCertKcna.classList.remove('active', 'kcna-active');

      if (this.ckaScopeGroup) {
        this.ckaScopeGroup.style.display = 'block';
        this.ckaScopeGroup.querySelectorAll('input').forEach(i => i.disabled = false);
      }
      if (this.kcnaScopeGroup) {
        this.kcnaScopeGroup.style.display = 'none';
        this.kcnaScopeGroup.querySelectorAll('input').forEach(i => i.disabled = true);
      }

      if (this.ckaCountGroup) {
        this.ckaCountGroup.style.display = 'block';
        this.ckaCountGroup.querySelectorAll('input').forEach(i => i.disabled = false);
      }
      if (this.kcnaCountGroup) {
        this.kcnaCountGroup.style.display = 'none';
        this.kcnaCountGroup.querySelectorAll('input').forEach(i => i.disabled = true);
      }

      if (this.cbtWelcomeTitle) this.cbtWelcomeTitle.textContent = 'Kubernetes Certified Administrator (CKA) CBT 실습';
      if (this.cbtWelcomeDesc) this.cbtWelcomeDesc.textContent = '영어 원문 지문 및 실무 시나리오에 익숙해지면서 한국어 상세 해설로 CKA 실전 시험을 완벽 대비합니다.';
      if (this.scopeCardTitle) this.scopeCardTitle.textContent = '1. 학습 범위 선택 (CKA 1,250문항 풀)';
      if (this.examTitle) this.examTitle.textContent = 'Kubernetes Administrator (CKA)';

      const firstCkaRadio = this.ckaScopeGroup ? this.ckaScopeGroup.querySelector('input[type="radio"]') : null;
      if (firstCkaRadio) firstCkaRadio.checked = true;
      const firstCkaCount = this.ckaCountGroup ? this.ckaCountGroup.querySelector('input[value="25"]') : null;
      if (firstCkaCount) firstCkaCount.checked = true;
    }
  }

  showStartScreen() {
    this.isReviewMode = false;
    clearInterval(this.timerInterval);
    this.userAnswers = {};
    this.flaggedQuestions = new Set();
    this.checkedQuestions = new Set();

    this.startScreen.classList.add('active');
    this.examScreen.classList.remove('active');
    this.resultScreen.classList.remove('active');
    this.timerBox.classList.add('hidden');
  }

  shuffleArray(array) {
    const arr = [...array];
    for (let i = arr.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [arr[i], arr[j]] = [arr[j], arr[i]];
    }
    return arr;
  }

  shuffleQuestionOptions(q) {
    if (!q || !q.options) return q;
    const opts = q.options.map(o => ({ ...o }));
    const correctOpt = opts.find(o => o.key === q.correct_answer);
    const correctEn = correctOpt ? correctOpt.text_en : '';

    const shuffled = this.shuffleArray(opts);
    const keys = ['A', 'B', 'C', 'D'];
    let newCorrectKey = q.correct_answer;

    const newOptions = shuffled.map((opt, idx) => {
      const key = keys[idx] || opt.key;
      if (opt.text_en === correctEn) {
        newCorrectKey = key;
      }
      return {
        key: key,
        text_en: opt.text_en,
        text_kr: opt.text_kr
      };
    });

    return {
      ...q,
      options: newOptions,
      correct_answer: newCorrectKey
    };
  }

  sampleMockExam(examCount) {
    const data = window.EXAM_DATA || {};

    // KCNA 샘플링 (D2: 46%, D3: 22%, D1: 16%, D4: 8%, D5: 8%)
    if (this.currentTrack === 'kcna') {
      const d1 = data.kcna_domain1 || [];
      const d2 = data.kcna_domain2 || [];
      const d3 = data.kcna_domain3 || [];
      const d4 = data.kcna_domain4 || [];
      const d5 = data.kcna_domain5 || [];

      if (examCount === 'all') {
        return [...d1, ...d2, ...d3, ...d4, ...d5];
      }

      const count = parseInt(examCount, 10) || 60;
      const c2 = Math.round(count * 0.46);
      const c3 = Math.round(count * 0.22);
      const c1 = Math.round(count * 0.16);
      const c4 = Math.round(count * 0.08);
      const c5 = count - (c2 + c3 + c1 + c4);

      const s1 = this.shuffleArray(d1).slice(0, c1);
      const s2 = this.shuffleArray(d2).slice(0, c2);
      const s3 = this.shuffleArray(d3).slice(0, c3);
      const s4 = this.shuffleArray(d4).slice(0, c4);
      const s5 = this.shuffleArray(d5).slice(0, c5);

      return [...s1, ...s2, ...s3, ...s4, ...s5];
    }

    // CKA 샘플링 (D1: 25%, D2: 15%, D3: 20%, D4: 10%, D5: 30%)
    const d1 = data.domain1 || [];
    const d2 = data.domain2 || [];
    const d3 = data.domain3 || [];
    const d4 = data.domain4 || [];
    const d5 = data.domain5 || [];

    if (examCount === 'all') {
      return [...d1, ...d2, ...d3, ...d4, ...d5];
    }

    const count = parseInt(examCount, 10) || 25;
    const c1 = Math.round(count * 0.25);
    const c2 = Math.round(count * 0.15);
    const c3 = Math.round(count * 0.20);
    const c4 = Math.round(count * 0.10);
    const c5 = count - (c1 + c2 + c3 + c4);

    const s1 = this.shuffleArray(d1).slice(0, c1);
    const s2 = this.shuffleArray(d2).slice(0, c2);
    const s3 = this.shuffleArray(d3).slice(0, c3);
    const s4 = this.shuffleArray(d4).slice(0, c4);
    const s5 = this.shuffleArray(d5).slice(0, c5);

    return [...s1, ...s2, ...s3, ...s4, ...s5];
  }

  async startExamFromSettings() {
    const examSetRadio = document.querySelector('input[name="examSet"]:checked:not(:disabled)') || document.querySelector('input[name="examSet"]:checked');
    const examModeRadio = document.querySelector('input[name="examMode"]:checked:not(:disabled)') || document.querySelector('input[name="examMode"]:checked');
    const examCountRadio = document.querySelector('input[name="examCount"]:checked:not(:disabled)') || document.querySelector('input[name="examCount"]:checked');
    const shuffleQCheck = document.getElementById('shuffle-questions-check');
    const shuffleOptCheck = document.getElementById('shuffle-options-check');

    this.selectedExamSet = examSetRadio ? examSetRadio.value : (this.currentTrack === 'kcna' ? 'kcna_mock_random' : 'mock_random');
    this.mode = examModeRadio ? examModeRadio.value : 'study';
    const examCount = examCountRadio ? examCountRadio.value : (this.currentTrack === 'kcna' ? '60' : '25');
    const shouldShuffleQuestions = shuffleQCheck ? shuffleQCheck.checked : true;
    const shouldShuffleOptions = shuffleOptCheck ? shuffleOptCheck.checked : true;

    // 문제 데이터 로드
    let questionList = [];

    // 1차: 로컬 서버 API 시도
    try {
      const res = await fetch(`/api/questions?set=${this.selectedExamSet}&limit=${examCount}&shuffle=${shouldShuffleQuestions}`);
      if (res.ok) {
        const json = await res.json();
        questionList = json.questions;
      }
    } catch (e) {
      // 오프라인 폴백
    }

    // 2차: window.EXAM_DATA 폴백 (GitHub Pages 또는 로컬 오프라인 모드)
    if (!questionList || questionList.length === 0) {
      if (this.selectedExamSet === 'mock_random' || this.selectedExamSet === 'mock1' || this.selectedExamSet === 'kcna_mock_random' || this.selectedExamSet === 'kcna_mock1') {
        questionList = this.sampleMockExam(examCount);
      } else if (window.EXAM_DATA && window.EXAM_DATA[this.selectedExamSet]) {
        let pool = [...window.EXAM_DATA[this.selectedExamSet]];
        if (shouldShuffleQuestions) {
          pool = this.shuffleArray(pool);
        }
        if (examCount !== 'all') {
          const limit = parseInt(examCount, 10) || (this.currentTrack === 'kcna' ? 60 : 25);
          questionList = pool.slice(0, limit);
        } else {
          questionList = pool;
        }
      }
    }

    if (!questionList || questionList.length === 0) {
      alert('문제 데이터를 불러오지 못했습니다. 데이터 파일을 확인해주세요.');
      return;
    }

    // 문항 셔플 적용 (서버 응답 미셔플 대비 추가 확인)
    if (shouldShuffleQuestions) {
      questionList = this.shuffleArray(questionList);
    }

    // 선택지(A~D) 셔플 적용
    if (shouldShuffleOptions) {
      questionList = questionList.map(q => this.shuffleQuestionOptions(q));
    }

    this.questions = [...questionList];
    this.currentIndex = 0;
    this.userAnswers = {};
    this.flaggedQuestions = new Set();
    this.checkedQuestions = new Set();
    this.koreanVisible = (this.mode === 'study');

    this.updateModeUI();

    // 타이머 설정 (실전 모드: 문항 수 및 트랙에 맞춤 계산)
    clearInterval(this.timerInterval);
    if (this.mode === 'exam') {
      let totalMinutes;
      if (this.currentTrack === 'kcna') {
        totalMinutes = this.questions.length <= 15 ? 25 : (this.questions.length <= 30 ? 45 : 90);
      } else {
        totalMinutes = this.questions.length <= 25 ? 120 : (this.questions.length <= 50 ? 180 : 240);
      }

      this.totalSeconds = totalMinutes * 60;
      this.secondsRemaining = this.totalSeconds;
      this.timerBox.classList.remove('hidden');
      this.updateTimerDisplay();
      this.timerInterval = setInterval(() => {
        this.secondsRemaining--;
        this.timeSpentSeconds++;
        this.updateTimerDisplay();
        if (this.secondsRemaining <= 0) {
          clearInterval(this.timerInterval);
          alert('시험 시간이 종료되었습니다! 결과가 자동으로 제출됩니다.');
          this.submitExam();
        }
      }, 1000);
    } else {
      this.timeSpentSeconds = 0;
      this.timerBox.classList.remove('hidden');
      this.updateStudyTimerDisplay();
      this.timerInterval = setInterval(() => {
        this.timeSpentSeconds++;
        this.updateStudyTimerDisplay();
      }, 1000);
    }

    // 화면 전환
    this.startScreen.classList.remove('active');
    this.resultScreen.classList.remove('active');
    this.examScreen.classList.add('active');

    this.renderQuestionNavGrid();
    this.renderCurrentQuestion();
  }

  updateTimerDisplay() {
    const minutes = Math.floor(this.secondsRemaining / 60);
    const seconds = this.secondsRemaining % 60;
    this.timeDisplay.textContent = `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
    if (this.secondsRemaining <= 300) {
      this.timerBox.classList.add('warning');
    } else {
      this.timerBox.classList.remove('warning');
    }
  }

  updateStudyTimerDisplay() {
    const minutes = Math.floor(this.timeSpentSeconds / 60);
    const seconds = this.timeSpentSeconds % 60;
    this.timeDisplay.textContent = `⏱️ ${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
  }

  updateModeUI() {
    if (this.mode === 'study') {
      this.modeIcon.textContent = '💡';
      this.modeLabel.textContent = '학습 모드';
      this.checkAnswerBtn.classList.remove('hidden');
    } else {
      this.modeIcon.textContent = '⏱️';
      this.modeLabel.textContent = '실전 모드';
      this.checkAnswerBtn.classList.add('hidden');
      this.studyFeedbackBox.classList.add('hidden');
    }
  }

  switchModeInExam() {
    if (this.isReviewMode) return;
    this.mode = (this.mode === 'study') ? 'exam' : 'study';
    this.updateModeUI();
    this.renderCurrentQuestion();
  }

  toggleTranslation() {
    this.koreanVisible = !this.koreanVisible;
    this.qTextKr.classList.toggle('hidden', !this.koreanVisible);
    const krTexts = this.optionsContainer.querySelectorAll('.option-text-kr');
    krTexts.forEach(el => el.classList.toggle('hidden', !this.koreanVisible));
    this.toggleTransBtn.textContent = this.koreanVisible ? '🌐 영어 원문만 보기' : '🌐 한국어 번역 보기';
  }

  toggleFlag() {
    const currentQ = this.questions[this.currentIndex];
    if (this.flaggedQuestions.has(currentQ.id)) {
      this.flaggedQuestions.delete(currentQ.id);
      this.toggleFlagBtn.classList.remove('btn-warning');
      this.flagText.textContent = '나중에 검토 (Flag)';
    } else {
      this.flaggedQuestions.add(currentQ.id);
      this.toggleFlagBtn.classList.add('btn-warning');
      this.flagText.textContent = '검토 표시됨 (Flagged)';
    }
    this.updateNavGridItem(this.currentIndex);
  }

  renderQuestionNavGrid() {
    this.questionNavGrid.innerHTML = '';
    this.questions.forEach((q, idx) => {
      const btn = document.createElement('button');
      btn.className = 'nav-btn';
      btn.textContent = idx + 1;
      btn.addEventListener('click', () => {
        this.currentIndex = idx;
        this.renderCurrentQuestion();
      });
      this.questionNavGrid.appendChild(btn);
    });
    this.updateAllNavGrid();
  }

  updateAllNavGrid() {
    const buttons = this.questionNavGrid.querySelectorAll('.nav-btn');
    let answeredCount = 0;

    buttons.forEach((btn, idx) => {
      const q = this.questions[idx];
      btn.classList.toggle('current', idx === this.currentIndex);

      const hasAnswer = this.userAnswers[q.id] !== undefined;
      btn.classList.toggle('answered', hasAnswer);
      if (hasAnswer) answeredCount++;

      btn.classList.toggle('flagged', this.flaggedQuestions.has(q.id));
    });

    this.answeredCountBadge.textContent = `${answeredCount} / ${this.questions.length} 풀이완료`;
  }

  updateNavGridItem(index) {
    this.updateAllNavGrid();
  }

  renderCurrentQuestion() {
    const q = this.questions[this.currentIndex];
    if (!q) return;

    this.qCounter.textContent = `Question ${this.currentIndex + 1} of ${this.questions.length}`;
    this.qDomain.textContent = q.domain_name || q.domain || 'Domain';

    // 플래그 상태
    if (this.flaggedQuestions.has(q.id)) {
      this.toggleFlagBtn.classList.add('btn-warning');
      this.flagText.textContent = '검토 표시됨 (Flagged)';
    } else {
      this.toggleFlagBtn.classList.remove('btn-warning');
      this.flagText.textContent = '나중에 검토 (Flag)';
    }

    // 지문 렌더링
    this.qTextEn.textContent = q.question_en;
    this.qTextKr.textContent = q.question_kr;
    this.qTextKr.classList.toggle('hidden', !this.koreanVisible);
    this.toggleTransBtn.textContent = this.koreanVisible ? '🌐 영어 원문만 보기' : '🌐 한국어 번역 보기';

    // 선택지 렌더링
    this.optionsContainer.innerHTML = '';
    const selectedAnswer = this.userAnswers[q.id];
    const isChecked = this.checkedQuestions.has(q.id) || this.isReviewMode;

    q.options.forEach(opt => {
      const item = document.createElement('div');
      item.className = 'option-item';

      if (selectedAnswer === opt.key) {
        item.classList.add('selected');
      }

      // 학습 모드에서 정답 확인 후 스타일 적용
      if (isChecked) {
        if (opt.key === q.correct_answer) {
          item.classList.add('correct');
        } else if (selectedAnswer === opt.key && selectedAnswer !== q.correct_answer) {
          item.classList.add('wrong');
        }
      }

      item.innerHTML = `
        <div class="option-key">${opt.key}</div>
        <div class="option-texts">
          <div class="option-text-en">${opt.text_en}</div>
          <div class="option-text-kr ${this.koreanVisible ? '' : 'hidden'}">${opt.text_kr || ''}</div>
        </div>
      `;

      item.addEventListener('click', () => {
        if (this.isReviewMode) return;
        this.selectAnswer(q.id, opt.key);
      });

      this.optionsContainer.appendChild(item);
    });

    // 학습 모드 즉시 피드백
    if ((this.mode === 'study' && this.checkedQuestions.has(q.id)) || this.isReviewMode) {
      this.showFeedbackBox(q);
    } else {
      this.studyFeedbackBox.classList.add('hidden');
    }

    // 네비게이션 버튼 상태
    this.prevBtn.disabled = (this.currentIndex === 0);
    this.nextBtn.disabled = (this.currentIndex === this.questions.length - 1);

    this.updateAllNavGrid();
  }

  selectAnswer(questionId, key) {
    this.userAnswers[questionId] = key;
    this.renderCurrentQuestion();
  }

  checkCurrentAnswer() {
    const q = this.questions[this.currentIndex];
    if (!this.userAnswers[q.id]) {
      alert('정답을 확인하기 전에 먼저 보기를 선택해주세요.');
      return;
    }

    this.checkedQuestions.add(q.id);
    this.renderCurrentQuestion();
  }

  showFeedbackBox(q) {
    const userAnswer = this.userAnswers[q.id];
    const isCorrect = (userAnswer === q.correct_answer);

    this.studyFeedbackBox.classList.remove('hidden');
    this.feedbackBadge.className = `badge ${isCorrect ? 'badge-primary' : 'badge-secondary'}`;
    this.feedbackBadge.style.backgroundColor = isCorrect ? '#10b981' : '#ef4444';
    this.feedbackBadge.style.color = '#ffffff';
    this.feedbackBadge.textContent = isCorrect ? '✅ 정답입니다!' : `❌ 오답 (정답: ${q.correct_answer})`;

    this.feedbackKeyConcept.textContent = q.key_concept ? `핵심 개념: ${q.key_concept}` : '';
    this.feedbackExplanation.textContent = q.explanation_kr || '해설이 준비되어 있지 않습니다.';
  }

  navigateQuestion(delta) {
    const newIdx = this.currentIndex + delta;
    if (newIdx >= 0 && newIdx < this.questions.length) {
      this.currentIndex = newIdx;
      this.renderCurrentQuestion();
    }
  }

  confirmSubmitExam() {
    const unansweredCount = this.questions.filter(q => this.userAnswers[q.id] === undefined).length;
    let message = '시험을 최종 제출하시겠습니까?';
    if (unansweredCount > 0) {
      message = `아직 풀지 않은 문제가 ${unansweredCount}개 있습니다.\n정말 시험을 제출하시겠습니까?`;
    }

    if (confirm(message)) {
      this.submitExam();
    }
  }

  submitExam() {
    clearInterval(this.timerInterval);

    // 채점
    let correctCount = 0;
    const domainStats = {};

    this.questions.forEach(q => {
      const domainKey = q.domain || 'Domain 1';
      if (!domainStats[domainKey]) {
        domainStats[domainKey] = {
          name: q.domain_name || domainKey,
          total: 0,
          correct: 0
        };
      }
      domainStats[domainKey].total++;

      if (this.userAnswers[q.id] === q.correct_answer) {
        correctCount++;
        domainStats[domainKey].correct++;
      }
    });

    const totalQuestions = this.questions.length;
    const scorePct = Math.round((correctCount / totalQuestions) * 100);
    const passed = (scorePct >= this.passingScorePct);

    // 결과 렌더링
    this.passFailBadge.className = `result-badge ${passed ? 'pass' : 'fail'}`;
    this.passFailBadge.textContent = passed ? '🎉 PASS (합격)' : '⚠️ FAIL (재응시 필요)';

    const resultSubtitle = document.getElementById('result-subtitle');
    if (resultSubtitle) {
      resultSubtitle.textContent = `합격 기준: ${this.passingScorePct}% 이상 (${this.currentTrack.toUpperCase()})`;
    }

    this.scorePercentage.textContent = `${scorePct}%`;
    this.scoreRaw.textContent = `${correctCount} / ${totalQuestions} 문항`;

    const mins = Math.floor(this.timeSpentSeconds / 60);
    const secs = this.timeSpentSeconds % 60;
    this.totalTimeSpent.textContent = `${mins}분 ${secs}초`;
    this.accuracyRate.textContent = `${scorePct}%`;

    // 도메인별 성취도 렌더링
    this.domainStatsList.innerHTML = '';
    Object.keys(domainStats).sort().forEach(dKey => {
      const stat = domainStats[dKey];
      const rate = stat.total > 0 ? Math.round((stat.correct / stat.total) * 100) : 0;

      const row = document.createElement('div');
      row.className = 'domain-stat-row';
      row.innerHTML = `
        <div class="domain-stat-meta">
          <span>${stat.name}</span>
          <span>${stat.correct} / ${stat.total} (${rate}%)</span>
        </div>
        <div class="progress-bar-bg">
          <div class="progress-bar-fill" style="width: ${rate}%; background-color: ${rate >= 66 ? '#10b981' : '#f59e0b'};"></div>
        </div>
      `;
      this.domainStatsList.appendChild(row);
    });

    // 백엔드 API에 이력 제출 시도
    this.recordSubmissionToBackend({
      score: scorePct,
      correctCount,
      totalQuestions,
      passed,
      timeSpent: this.timeSpentSeconds,
      domainStats,
      examSet: this.selectedExamSet
    });

    // 화면 전환
    this.examScreen.classList.remove('active');
    this.resultScreen.classList.add('active');
  }

  async recordSubmissionToBackend(data) {
    try {
      await fetch('/api/submit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      });
    } catch (e) {
      // 오프라인 모드 무시
    }
  }

  startWrongReviewMode() {
    const wrongQuestions = this.questions.filter(q => this.userAnswers[q.id] !== q.correct_answer);
    if (wrongQuestions.length === 0) {
      alert('축하합니다! 틀린 문제가 하나도 없습니다.');
      return;
    }

    this.questions = [...wrongQuestions];
    this.currentIndex = 0;
    this.isReviewMode = true;
    this.mode = 'study';
    this.koreanVisible = true;

    this.resultScreen.classList.remove('active');
    this.examScreen.classList.add('active');

    this.updateModeUI();
    this.renderQuestionNavGrid();
    this.renderCurrentQuestion();
  }
}

// 초기화
document.addEventListener('DOMContentLoaded', () => {
  window.cbtApp = new K8sCBTSimulator();
});
