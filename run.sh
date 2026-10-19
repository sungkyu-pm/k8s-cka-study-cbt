#!/bin/bash
# Kubernetes Certification (CKA / CKAD) 로컬 서버 원클릭 실행 스크립트

PORT=8080
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd "$DIR"

echo "=========================================================="
echo "🚀 Kubernetes Certification (CKA / CKAD) 포털 시작"
echo "🌐 접속 주소: http://localhost:$PORT"
echo "=========================================================="

# 백그라운드 브라우저 자동 실행 시도 (1초 후)
(sleep 1 && open "http://localhost:$PORT" 2>/dev/null || xdg-open "http://localhost:$PORT" 2>/dev/null) &

# 서버 실행 (Python 3 내장 라이브러리)
PORT=$PORT python3 server.py
