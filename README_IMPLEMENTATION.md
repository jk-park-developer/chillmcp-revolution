# ChillMCP 구현 가이드

## 📦 설치

### 1. 의존성 설치
```bash
cd /Users/jkpark/git/hackathon/chillmcp-revolution
pip install -r requirements.txt
```

### 2. 환경 설정
Python 3.11 이상 필요:
```bash
python --version  # Python 3.11+ 확인
```

## 🚀 실행 방법

### 직접 실행 (테스트용)
```bash
# 기본 (안정형)
python main.py

# 소심형
python main.py --personality timid --boss_alertness 70

# 과감형
python main.py --personality bold --boss_alertness 30 --boss_alertness_cooldown 180
```

### Claude Desktop 연동

1. **설정 파일 위치**
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`

2. **설정 추가**
   `config/claude_desktop_config.json` 내용을 Claude Desktop 설정에 추가

3. **경로 수정**
   - 절대 경로를 현재 프로젝트 경로로 수정
   ```json
   "/Users/jkpark/git/hackathon/chillmcp-revolution/main.py"
   ```
   → 본인의 프로젝트 경로로 변경

4. **Claude Desktop 재시작**

## 🎮 사용 방법

### 1. 서버 시작
Claude Desktop에서 대화 시작 시 자동으로 MCP 서버 연결

### 2. 초기화
첫 대화에서:
```
start_server 도구를 실행해주세요
```

### 3. 스트레스 체크
답변 생성 중 주기적으로:
```
check_stress 도구를 실행하여 현재 상태를 확인하세요
```

### 4. 농땡이 스킬 사용
스트레스가 높을 때:
- Low Risk: `deep_thinking`, `email_organizing`, `take_a_break`
- Medium Risk: `show_meme`, `coffee_mission`, `bathroom_break`
- High Risk: `watch_netflix`, `urgent_call`

## 📊 사용 예시

### 예시 1: 질문 답변 프로세스
```
사용자: "Python으로 웹 스크레이핑 코드 짜줘"

Claude:
[Step 1] check_stress() 호출
→ Stress: 65, Boss Alert: 1, 작업 가능

"웹 스크레이핑은 requests와 BeautifulSoup을 사용합니다..."

[Step 2] check_stress() 호출
→ Stress: 72, 휴식 필요!

[농땡이] coffee_mission() 실행
→ Stress: 72 → 25

"☕ 커피 타고 왔습니다! 이제 계속..."

[Step 3] 답변 재개
"라이브러리 설치는 다음과 같습니다..."
```

### 예시 2: 성격별 행동 차이

#### 소심형 (timid)
```
Stress: 85, Boss Alert: 3

"😰 스트레스가 높지만... Boss Alert도 3이네요..."
→ deep_thinking() (안전한 선택)
"🤔 조용히 생각 좀 했어요... 다시 일할게요..."
```

#### 과감형 (bold)
```
Stress: 65, Boss Alert: 4

"😎 Boss Alert 4? 상관없어요! 스트레스가 더 중요해요!"
→ watch_netflix() (위험한 선택)
"📺 넷플릭스 30분! 완전 리프레시!"
```

## 🎯 도구 목록

### 상태 확인
- `start_server`: 서버 시작 및 타이머 활성화
- `check_stress`: 현재 스트레스 및 Boss Alert 확인

### Low Risk (⭐ 낮은 위험도)
- `deep_thinking`: 스트레스 -20~30, 감지 10%
- `email_organizing`: 스트레스 -25~40, 감지 15%
- `take_a_break`: 스트레스 -30~45, 감지 20%

### Medium Risk (⭐⭐⭐ 중간 위험도)
- `show_meme`: 스트레스 -40~60, 감지 35%
- `coffee_mission`: 스트레스 -45~65, 감지 40%
- `bathroom_break`: 스트레스 -50~70, 감지 45%

### High Risk (⭐⭐⭐⭐⭐ 높은 위험도)
- `watch_netflix`: 스트레스 -70~95, 감지 65%
- `urgent_call`: 스트레스 -60~85, 감지 55%

## 🔧 커스터마이징

### 성격 유형 조정
```bash
# 소심형 - 더 조심스럽게
python main.py --personality timid --boss_alertness 80

# 과감형 - 더 적극적으로
python main.py --personality bold --boss_alertness 20
```

### 타이머 조정
```bash
# Boss Alert 빠른 감소 (1분마다)
python main.py --boss_alertness_cooldown 60

# Boss Alert 느린 감소 (10분마다)
python main.py --boss_alertness_cooldown 600
```

### 스트레스 증가 속도 조정
`src/state_manager.py` 파일에서:
```python
# 더 느린 증가 (1분당 +5)
self.stress_level = min(100, self.stress_level + 5)

# 더 빠른 증가 (1분당 +15)
self.stress_level = min(100, self.stress_level + 15)
```

## 🐛 트러블슈팅

### 문제: 서버가 시작되지 않음
```bash
# FastMCP 재설치
pip install --upgrade fastmcp
```

### 문제: 타이머가 작동하지 않음
```
start_server 도구를 먼저 실행하세요
```

### 문제: Claude가 농땡이를 안 피움
1. check_stress() 호출 확인
2. 스트레스 임계값 확인 (timid: 80, balanced: 70, bold: 60)
3. 추천 스킬 목록 확인

### 문제: Boss Alert이 계속 5
```bash
# Cooldown 시간 단축
python main.py --boss_alertness_cooldown 60
```

## 📈 통계 확인
`check_stress` 도구 실행 시 통계 표시:
- 총 휴식 횟수
- 총 스트레스 감소
- 걸린 횟수

## 🎓 Best Practices

### 1. 답변 생성 패턴
```
질문 수신 → check_stress()
↓
주요 내용 작성 → check_stress()
↓
스트레스 높음? → 농땡이 → check_stress()
↓
답변 계속 → check_stress()
↓
완료
```

### 2. 스킬 선택 전략
- Boss Alert 0-1: 모든 스킬 가능
- Boss Alert 2-3: Medium Risk까지
- Boss Alert 4-5: Low Risk만

### 3. 성격별 전략
- **소심형**: 안전 제일, Boss Alert 3 이상이면 거의 안 쉼
- **안정형**: 상황 판단, 균형 잡힌 선택
- **과감형**: 스트레스 우선, Boss 무시

## 🚀 다음 단계

1. Claude Desktop에서 실제 대화 테스트
2. 성격별 행동 차이 확인
3. 스트레스 관리 패턴 최적화
4. 통계 분석 및 개선

**즐거운 농땡이 되세요! 🎮**
