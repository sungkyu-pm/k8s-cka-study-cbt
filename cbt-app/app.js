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
    this.selectedExamSet = 'mock1';

    this.initDOMElements();
    this.bindEvents();
  }

  initDOMElements() {
    // 화면들
    this.startScreen = document.getElementById('start-screen');
    this.examScreen = document.getElementById('exam-screen');
    this.resultScreen = document.getElementById('result-screen');

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

  async startExamFromSettings() {
    const examSetRadio = document.querySelector('input[name="examSet"]:checked');
    const examModeRadio = document.querySelector('input[name="examMode"]:checked');

    this.selectedExamSet = examSetRadio ? examSetRadio.value : 'mock1';
    this.mode = examModeRadio ? examModeRadio.value : 'study';

    // 문제 데이터 로드
    let questionList = [];

    // 1차: 로컬 서버 API 시도
    try {
      const res = await fetch(`/api/questions?set=${this.selectedExamSet}`);
      if (res.ok) {
        const json = await res.json();
        questionList = json.questions;
      }
    } catch (e) {
      // 오프라인 폴백
    }

    // 2차: window.EXAM_DATA 폴백
    if (!questionList || questionList.length === 0) {
      if (window.EXAM_DATA && window.EXAM_DATA[this.selectedExamSet]) {
        questionList = window.EXAM_DATA[this.selectedExamSet];
      }
    }

    if (!questionList || questionList.length === 0) {
      alert('문제 데이터를 불러오지 못했습니다.');
      return;
    }

    this.questions = [...questionList];
    this.currentIndex = 0;
    this.userAnswers = {};
    this.flaggedQuestions = new Set();
    this.checkedQuestions = new Set();
    this.koreanVisible = (this.mode === 'study');

    this.updateModeUI();

    // 타이머 설정 (실전 모드: 120분, 학습 모드: 카운트업)
    clearInterval(this.timerInterval);
    if (this.mode === 'exam') {
      this.totalSeconds = 120 * 60; // 120분 (CKA 공식)
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
    const passed = (scorePct >= 66); // CKA 공식 합격 기준: 66% 이상

    // 결과 렌더링
    this.passFailBadge.className = `result-badge ${passed ? 'pass' : 'fail'}`;
    this.passFailBadge.textContent = passed ? '🎉 PASS (합격)' : '⚠️ FAIL (재응시 필요)';

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
