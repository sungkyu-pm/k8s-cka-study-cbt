#!/usr/bin/env python3
"""
Kubernetes Certification (CKA / CKAD / KCNA) Local Backend Server
- Built using only Python 3 standard libraries (No external pip dependencies).
- Serves static assets (HTML/CSS/JS/Docs).
- Provides REST APIs for Questions, Dynamic Docs, Exam History, and Submissions.
"""

import os
import sys
import json
import time
import random
from datetime import datetime
from urllib.parse import urlparse, parse_qs
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler

PORT = int(os.environ.get('PORT', 8080))
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
HISTORY_FILE = os.path.join(DATA_DIR, 'history.json')
QUESTIONS_DIR = os.path.join(BASE_DIR, 'questions')
DOCS_DIR = os.path.join(BASE_DIR, 'docs')

os.makedirs(DATA_DIR, exist_ok=True)
if not os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump([], f, ensure_ascii=False, indent=2)


class K8sExamServerHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=BASE_DIR, **kwargs)

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)

        # API 라우팅
        if path == '/api/status':
            self.handle_api_status()
        elif path == '/api/docs':
            self.handle_api_docs(query)
        elif path == '/api/questions':
            self.handle_api_questions(query)
        elif path == '/api/history':
            self.handle_api_history()
        else:
            if path == '/':
                self.path = '/index.html'
            super().do_GET()

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path == '/api/submit':
            self.handle_api_submit()
        elif path == '/api/questions/add':
            self.handle_api_add_question()
        else:
            self.send_error(404, "Endpoint not found")

    # ==========================
    # API 핸들러들
    # ==========================

    def send_json_response(self, data, status_code=200):
        body = json.dumps(data, ensure_ascii=False).encode('utf-8')
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(body)

    def handle_api_status(self):
        """서버 상태 및 데이터베이스 통계 정보 반환"""
        total_questions = 0
        for i in range(1, 6):
            q_file = os.path.join(QUESTIONS_DIR, f'questions_domain{i}.json')
            if os.path.exists(q_file):
                try:
                    with open(q_file, 'r', encoding='utf-8') as f:
                        total_questions += len(json.load(f))
                except Exception:
                    pass

        exam_count = 0
        if os.path.exists(HISTORY_FILE):
            try:
                with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                    exam_count = len(json.load(f))
            except Exception:
                pass

        self.send_json_response({
            "status": "online",
            "server": "K8S Certification Local Backend",
            "total_questions": total_questions,
            "total_exams_taken": exam_count,
            "port": PORT,
            "time": datetime.now().isoformat()
        })

    def handle_api_docs(self, query):
        """docs 디렉토리의 마크다운 내용 실시간 반환"""
        doc_key = query.get('key', [None])[0]
        doc_mapping = {
            'exam_guide': '00_CKA_EXAM_GUIDE.md',
            'glossary': '01_GLOSSARY_KR_EN.md',
            'domain1': '02_DOMAIN_1_CLUSTER_ARCHITECTURE.md',
            'domain2': '03_DOMAIN_2_WORKLOADS_SCHEDULING.md',
            'domain3': '04_DOMAIN_3_SERVICES_NETWORKING.md',
            'domain4': '05_DOMAIN_4_STORAGE.md',
            'domain5': '06_DOMAIN_5_TROUBLESHOOTING.md',
            'kubectl_cheat': '07_KUBECTL_CHEAT_SHEET.md'
        }

        if not doc_key or doc_key not in doc_mapping:
            self.send_json_response({"error": "Invalid or missing doc key"}, 400)
            return

        file_path = os.path.join(DOCS_DIR, doc_mapping[doc_key])
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            self.send_json_response({"key": doc_key, "content": content})
        else:
            self.send_json_response({"error": f"Doc file not found: {doc_mapping[doc_key]}"}, 404)

    def handle_api_questions(self, query):
        """문제 세트 조회 (mock_random, mock1, 또는 domain1~5)"""
        q_set = query.get('set', ['mock_random'])[0]
        limit = query.get('limit', [None])[0]
        should_shuffle = query.get('shuffle', ['true'])[0].lower() == 'true'

        if q_set in ['mock_random', 'all']:
            # 5개 도메인에서 가중치에 맞춰 랜덤 추출
            domain_pools = {}
            for i in range(1, 6):
                fpath = os.path.join(QUESTIONS_DIR, f'questions_domain{i}.json')
                if os.path.exists(fpath):
                    with open(fpath, 'r', encoding='utf-8') as f:
                        domain_pools[f'domain{i}'] = json.load(f)
                else:
                    domain_pools[f'domain{i}'] = []

            # 목표 문항 수 결정
            try:
                target_count = int(limit) if limit and limit != 'all' else 25
            except ValueError:
                target_count = 25

            if limit == 'all':
                # 전체 문항 반환 (1,250개)
                all_q = []
                for pool in domain_pools.values():
                    all_q.extend(pool)
                if should_shuffle:
                    random.shuffle(all_q)
                self.send_json_response({"set": q_set, "count": len(all_q), "questions": all_q})
                return

            # CKA 공식 비중에 맞춘 샘플링 (D1: 25%, D2: 15%, D3: 20%, D4: 10%, D5: 30%)
            c1 = round(target_count * 0.25)
            c2 = round(target_count * 0.15)
            c3 = round(target_count * 0.20)
            c4 = round(target_count * 0.10)
            c5 = target_count - (c1 + c2 + c3 + c4)

            selected = []
            for d_name, cnt in [('domain1', c1), ('domain2', c2), ('domain3', c3), ('domain4', c4), ('domain5', c5)]:
                pool = domain_pools.get(d_name, [])
                if pool:
                    k = min(cnt, len(pool))
                    selected.extend(random.sample(pool, k))

            if should_shuffle:
                random.shuffle(selected)

            self.send_json_response({"set": q_set, "count": len(selected), "questions": selected})
            return

        file_map = {
            'mock1': 'mock_exam_1.json',
            'domain1': 'questions_domain1.json',
            'domain2': 'questions_domain2.json',
            'domain3': 'questions_domain3.json',
            'domain4': 'questions_domain4.json',
            'domain5': 'questions_domain5.json',
        }

        filename = file_map.get(q_set, 'mock_exam_1.json')
        file_path = os.path.join(QUESTIONS_DIR, filename)

        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                questions = json.load(f)

            if should_shuffle:
                questions = list(questions)
                random.shuffle(questions)

            if limit and limit != 'all':
                try:
                    num_limit = int(limit)
                    questions = questions[:num_limit]
                except ValueError:
                    pass

            self.send_json_response({"set": q_set, "count": len(questions), "questions": questions})
        else:
            self.send_json_response({"error": f"Question set not found: {q_set}"}, 404)

    def handle_api_history(self):
        """과거 시험 응시 기록 반환"""
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                history = json.load(f)
            self.send_json_response(history)
        else:
            self.send_json_response([])

    def handle_api_submit(self):
        """시험 응시 결과 제출 및 통계 누적 기록"""
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            submission = json.loads(post_data.decode('utf-8'))

            submission['timestamp'] = datetime.now().isoformat()
            submission['id'] = f"k8s-exam-{int(time.time())}"

            history = []
            if os.path.exists(HISTORY_FILE):
                try:
                    with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                        history = json.load(f)
                except Exception:
                    history = []

            history.insert(0, submission)
            # 최근 100회 기록 보관
            history = history[:100]

            with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
                json.dump(history, f, ensure_ascii=False, indent=2)

            self.send_json_response({
                "status": "success",
                "message": "Submission recorded successfully",
                "submission_id": submission['id'],
                "total_taken": len(history)
            })
        except Exception as e:
            self.send_json_response({"error": str(e)}, 500)

    def handle_api_add_question(self):
        """새로운 문제 실시간 추가 API"""
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            payload = json.loads(post_data.decode('utf-8'))

            target_domain = payload.get('domain_key', 'domain1')
            filename = f"questions_{target_domain}.json"
            file_path = os.path.join(QUESTIONS_DIR, filename)

            questions = []
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    questions = json.load(f)

            new_q = payload.get('question')
            if not new_q or 'question_en' not in new_q or 'correct_answer' not in new_q:
                self.send_json_response({"error": "Invalid question format"}, 400)
                return

            questions.append(new_q)
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(questions, f, ensure_ascii=False, indent=2)

            self.send_json_response({"status": "success", "total_in_domain": len(questions)})
        except Exception as e:
            self.send_json_response({"error": str(e)}, 500)


def run_server():
    server_address = ('', PORT)
    httpd = ThreadingHTTPServer(server_address, K8sExamServerHandler)
    print("=" * 60)
    print("🚀 Kubernetes Certification (CKA / CKAD) Local Portal Server")
    print(f"📡 Server running at: http://localhost:{PORT}")
    print(f"📂 Base Directory: {BASE_DIR}")
    print("=" * 60)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped gracefully.")
        httpd.server_close()


if __name__ == '__main__':
    run_server()
