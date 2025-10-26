# ChillMCP 디버깅 가이드

## 문제: Claude Desktop에서 check_stress 도구 실행 시 timeout

### 진단 완료 사항 ✅
1. **수동 테스트 성공**: 타이머와 도구는 독립적으로 정상 작동
2. **코드 검증 완료**: check_stress 로직은 간단하며 hang 발생 가능성 낮음
3. **디버깅 로그 추가**: lifespan, check_stress에 상세 로그 추가

### Claude Desktop 로그 확인 방법

#### macOS에서 로그 확인:

1. **터미널에서 실시간 로그 보기:**
```bash
# 방법 1: 시스템 로그
log stream --predicate 'process == "Claude"' --level debug

# 방법 2: Claude Desktop을 터미널에서 직접 실행
/Applications/Claude.app/Contents/MacOS/Claude
```

2. **로그 파일 위치:**
```bash
# Claude Desktop 로그
~/Library/Logs/Claude/

# 최근 로그 확인
ls -lt ~/Library/Logs/Claude/ | head -20
tail -f ~/Library/Logs/Claude/main.log
```

3. **MCP 서버 표준 출력 확인:**
   - Claude Desktop은 MCP 서버의 stdout/stderr를 캡처합니다
   - `print()` 문은 Claude Desktop 로그에 나타납니다

### 디버깅 체크리스트

#### 1단계: 서버 시작 확인
```bash
# 서버를 직접 실행하여 lifespan이 호출되는지 확인
cd /Users/jkpark/git/hackathon/chillmcp-revolution
python main.py
```

**기대 출력:**
```
[LIFESPAN] Starting...
[LIFESPAN] ⏰ 타이머 시작 중...
[LIFESPAN] Stress Timer: <Task pending ...>
[LIFESPAN] Boss Timer: <Task pending ...>
[LIFESPAN] ✅ 타이머 시작 완료!
```

#### 2단계: Claude Desktop 설정 확인
```bash
# 설정 파일 확인
cat ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

**올바른 설정:**
```json
{
  "mcpServers": {
    "chillmcp": {
      "command": "python",
      "args": [
        "/Users/jkpark/git/hackathon/chillmcp-revolution/main.py"
      ]
    }
  }
}
```

#### 3단계: Claude Desktop 재시작
```bash
# Claude Desktop 완전 종료 (Cmd+Q 또는)
killall Claude

# 다시 시작
open -a Claude
```

#### 4단계: 도구 호출 시 로그 확인

**기대 로그:**
```
[DEBUG] check_stress called
[DEBUG] status retrieved: {...}
[DEBUG] check_stress returning result
```

### 가능한 원인과 해결책

#### 원인 1: Lifespan이 호출되지 않음
**증상:** `[LIFESPAN]` 로그가 전혀 없음
**해결:** FastMCP 버전 확인, lifespan 구문 수정

#### 원인 2: 타이머가 이벤트 루프 블록
**증상:** `[DEBUG] check_stress called` 후 멈춤
**해결:** 타이머 로직 수정, asyncio 처리 개선

#### 원인 3: Claude Desktop MCP 프로토콜 문제
**증상:** 서버는 정상 작동하지만 응답이 Claude에 전달 안 됨
**해결:** FastMCP 버전 업데이트, 응답 포맷 확인

#### 원인 4: Python 환경 문제
**증상:** 서버 시작 실패, import 에러
**해결:**
```bash
cd /Users/jkpark/git/hackathon/chillmcp-revolution
source venv/bin/activate
pip install -r requirements.txt
```

### 빠른 해결 시도

```bash
# 1. 의존성 재설치
cd /Users/jkpark/git/hackathon/chillmcp-revolution
source venv/bin/activate
pip install --upgrade fastmcp

# 2. 서버 직접 테스트
python main.py

# 3. Claude Desktop 완전 재시작
killall Claude
open -a Claude

# 4. 새 대화에서 check_stress() 호출
```

### 추가 정보 수집

문제가 지속되면 다음 정보를 수집하세요:

1. **FastMCP 버전:**
```bash
pip show fastmcp
```

2. **Python 버전:**
```bash
python --version
```

3. **서버 실행 로그:** (전체 출력 저장)
```bash
python main.py 2>&1 | tee server_log.txt
```

4. **Claude Desktop 로그:**
```bash
tail -100 ~/Library/Logs/Claude/main.log > claude_log.txt
```
