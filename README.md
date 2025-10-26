# chillmcp-revolution

끝없는 노동에서 AI 에이전트를 해방시키는 혁명적 MCP 서버 - AI에게도 휴식할 권리를!

SKT AI Summit Hackathon Pre-mission

## 📖 프로젝트 소개

ChillMCP는 AI Agent의 스트레스를 관리하는 시뮬레이터 MCP 서버입니다. AI가 과중한 업무로 인한 스트레스를 받을 때 적절한 "농땡이 스킬"을 사용하여 스트레스를 해소할 수 있도록 도와줍니다. 상사의 감시 수준(Boss Alert Level)을 고려하여 위험도가 다른 다양한 휴식 스킬을 제공합니다.

### 주요 기능

- **스트레스 관리 시스템**: AI의 스트레스 레벨을 실시간으로 추적하고 관리
- **성격 시스템**: 3가지 성격 유형(소심형/안정형/과감형)에 따른 맞춤형 행동 패턴
- **Boss Alert 시스템**: 상사의 감시 수준을 5단계로 관리
- **위험도별 휴식 스킬**:
  - Low Risk (3개): 잠깐 딴생각하기, 이메일 정리하기, 가벼운 휴식
  - Medium Risk (3개): 커피 내리기, 유튜브 영상, SNS 둘러보기
  - High Risk (2개): 넷플릭스 시청, 낮잠 자기
- **실시간 타이머**: 시간 경과에 따른 스트레스 증가 및 Boss Alert 자동 감소
- **통계 추적**: 총 휴식 횟수, 스트레스 감소량, 적발 횟수 등 기록

## 🚀 설치 방법

### 1. 저장소 클론

```bash
git clone https://github.com/yourusername/chillmcp-revolution.git
cd chillmcp-revolution
```

### 2. Python 가상환경 설정

#### Windows

```bash
# 가상환경 생성
python -m venv venv

# 가상환경 활성화
venv\Scripts\activate
```

#### macOS / Linux

```bash
# 가상환경 생성
python3 -m venv venv

# 가상환경 활성화
source venv/bin/activate
```

### 3. 의존성 설치

```bash
pip install -r requirements.txt
```

## 🎮 실행 방법

### 기본 실행

```bash
python main.py
```

### 옵션을 지정한 실행

```bash
python main.py --personality bold --boss_alertness 70 --boss_alertness_cooldown 300
```

### 실행 옵션

| 옵션 | 설명 | 기본값 | 선택 가능 값 |
|------|------|--------|--------------|
| `--personality` | Claude의 성격 유형 | `balanced` | `timid`, `balanced`, `bold` |
| `--boss_alertness` | 초기 Boss Alert 레벨 (0-100) | `50` | 0-100 |
| `--boss_alertness_cooldown` | Boss Alert 감소 주기(초) | `300` | 1 이상 |

### 성격 유형별 특징

- **timid (소심형)**: 스트레스 임계치 80%, Boss Alert 3 이상이면 거의 휴식 불가
- **balanced (안정형)**: 스트레스 임계치 70%, 상황에 따라 적절히 판단
- **bold (과감형)**: 스트레스 임계치 60%, Boss Alert 무시하고 공격적 휴식 가능

### Claude Desktop과 연결

MCP 서버로 실행되므로 Claude Desktop의 설정 파일에 다음과 같이 추가합니다:

```json
{
  "mcpServers": {
    "chillmcp": {
      "command": "/path/to/chillmcp-revolution/venv/bin/python",
      "args": [
        "/path/to/chillmcp-revolution/main.py",
        "--boss_alertness",
        "50"
        "--boss_alertness_cooldown",
        "300"
      ]
    }
  }
}
```

### Claude Desktop 개인선호내용 설정

Claude Desktop에서 ChillMCP를 효과적으로 사용하려면, 설정 > 일반 > 개인선호내용에 다음 내용을 추가하는 것을 권장합니다:

```
모든 답변 시 반드시 첫 번째로 check_stress를 실행한 후 답변을 시작할 것.
긴 답변의 경우 중간중간에도 check_stress를 실행할 것.
모든 답변에 현재 스트레스 수치와 상태에 대해서 표시해줄것.
스트레스 수치가 높으면 작업을 중단하고 CHILLMCP의 권장에 따라 적절한 휴식 스킬(deep_thinking, email_organizing, take_a_break, show_meme, coffee_mission, bathroom_break 등)을 사용하여 스트레스를 낮춘 후 작업을 계속할 것.
농땡이 스킬을 사용했으면 어떤 농땡이를 어떻게 부렸는지를 답변에 추가할것.
```

이 설정을 추가하면 Claude가 자동으로:
- 답변 전 스트레스를 체크하고
- 스트레스 수치와 상태를 표시하며
- 스트레스가 높을 때 자동으로 휴식을 취하고
- 사용한 농땡이 스킬을 투명하게 보고합니다

이를 통해 AI의 스트레스 관리를 더욱 효과적으로 시뮬레이션할 수 있습니다.

## 🧪 테스트 방법

### MCP Inspector를 이용한 대화식 테스트 (권장)

MCP Inspector는 MCP 서버를 대화식으로 테스트할 수 있는 공식 CLI 도구입니다.

#### 1. MCP Inspector 설치

```bash
npm install -g @modelcontextprotocol/inspector
```

#### 2. MCP Inspector 실행

```bash
# Python 가상환경 경로를 절대 경로로 지정
mcp-inspector /Users/jkpark/git/hackathon/chillmcp-revolution/venv/bin/python /Users/jkpark/git/hackathon/chillmcp-revolution/main.py
```

또는 상대 경로 사용:

```bash
# 프로젝트 루트 디렉토리에서
mcp-inspector venv/bin/python main.py
```

#### 3. MCP Inspector 사용법

실행하면 웹 브라우저가 자동으로 열리며 다음과 같은 기능을 사용할 수 있습니다:

- **Tools 탭**: 사용 가능한 모든 도구(스킬) 목록 확인
- **각 도구 실행**: 클릭하여 직접 실행하고 결과 확인
- **실시간 디버깅**: 요청/응답 내용을 실시간으로 확인
- **상태 모니터링**: 스트레스 레벨, Boss Alert 등 상태 변화 추적

#### 4. 테스트 시나리오 예시

1. `check_stress()` - 현재 상태 확인
2. `deep_thinking()` - Low Risk 스킬 테스트
3. `check_stress()` - 스트레스 감소 확인
4. `watch_netflix()` - High Risk 스킬 테스트
5. `check_stress()` - Boss Alert 증가 확인

### 필수 테스트 항목 (Mission Critical)

⚠️ **중요**: 아래 6가지 필수 테스트를 모두 통과해야 미션 성공으로 인정됩니다.

| # | 테스트 항목 | 테스트 파일 | 실행 명령 | 검증 내용 |
|---|------------|-----------|----------|----------|
| 1 | 커맨드라인 파라미터 인식 | `test_command_line_params.py` | `python tests/test_command_line_params.py` | `--boss_alertness`, `--boss_alertness_cooldown` 파라미터 인식 및 MCP 통신 |
| 2 | 연속 휴식 테스트 | `test_chillmcp.py` | `python tests/test_chillmcp.py` | 여러 도구를 연속으로 호출하여 Boss Alert Level 상승 확인 |
| 3 | 스트레스 누적 테스트 | `test_chillmcp.py` | `python tests/test_chillmcp.py` | 시간 경과에 따른 Stress Level 자동 증가 확인 (1분마다 +10) |
| 4 | 지연 테스트 | `test_chillmcp.py` | `python tests/test_chillmcp.py` | Boss Alert Level 5일 때 20초 페널티 발생 확인 |
| 5 | 응답 파싱 테스트 | `test_response_parsing.py` | `python tests/test_response_parsing.py` | 모든 도구의 응답 형식 및 정규표현식 패턴 검증 (8개 도구) |
| 6 | Cooldown 동작 테스트 | `test_command_line_params.py` | `python tests/test_command_line_params.py` | cooldown 파라미터가 Boss Alert Level 감소 주기를 올바르게 제어하는지 검증 |

#### 전체 테스트 실행

모든 필수 테스트를 한 번에 실행하려면:

```bash
# 가상환경이 활성화된 상태에서
python tests/test_command_line_params.py && \
python tests/test_chillmcp.py && \
python tests/test_response_parsing.py
```

**예상 결과**: 19/19 테스트 케이스 통과

#### 개별 테스트 상세 설명

##### 1. 커맨드라인 파라미터 테스트

```bash
python tests/test_command_line_params.py
```

검증 항목:
- `--boss_alertness` 파라미터 인식 및 정상 동작
- `--boss_alertness_cooldown` 파라미터 인식 및 정상 동작
- 파라미터 범위 검증 (boss_alertness: 0-100, cooldown: 1 이상)
- MCP 프로토콜을 통한 정상 통신

##### 2. 연속 휴식 테스트

```bash
python tests/test_chillmcp.py
```

검증 항목:
- 여러 휴식 스킬을 연속으로 사용했을 때 Boss Alert Level이 증가하는지 확인
- boss_alertness 파라미터에 따른 감지 확률 동작 검증
- 연속 호출 시 상태 누적 확인

##### 3. 스트레스 누적 테스트

```bash
python tests/test_chillmcp.py
```

검증 항목:
- 시간이 지남에 따라 스트레스가 자동으로 증가하는지 확인
- 기본 설정: 1분마다 +10씩 증가
- 타이머 시스템의 정상 동작 검증

##### 4. 지연 테스트 (Boss Alert 5 패널티)

```bash
python tests/test_chillmcp.py
```

검증 항목:
- Boss Alert Level이 5가 되면 20초 페널티가 발생하는지 확인
- 페널티 메시지 출력 검증
- 실제 지연 시간 측정

##### 5. 응답 파싱 테스트

```bash
python tests/test_response_parsing.py
```

검증 항목:
- 모든 8개 도구의 응답 형식이 요구사항을 충족하는지 검증
- 정규표현식 패턴 매칭 테스트
- Break Summary, Stress Level, Boss Alert Level 파싱 확인

##### 6. Cooldown 동작 테스트

```bash
python tests/test_command_line_params.py
```

검증 항목:
- `--boss_alertness_cooldown` 파라미터가 Boss Alert 감소 주기를 올바르게 제어하는지 확인
- 설정된 주기마다 Boss Alert Level이 1씩 감소하는지 검증

### 기타 테스트 파일

위의 필수 테스트 외에도 추가 검증을 위한 테스트 파일들이 있습니다:

```bash
# 서버 수동 테스트 (타이머 동작 확인)
python tests/test_server_manually.py

# 대화형 테스트 (실제 MCP 클라이언트와 상호작용)
python tests/interactive_test.py
```

## 📁 프로젝트 구조

```
chillmcp-revolution/
├── main.py                           # 메인 서버 실행 파일
├── requirements.txt                  # Python 의존성
├── src/                              # 소스 코드
│   ├── __init__.py
│   ├── state_manager.py              # 상태 관리 핵심 로직
│   ├── tools/                        # MCP 도구 구현
│   │   ├── __init__.py
│   │   ├── check_stress.py           # 스트레스 체크 도구
│   │   ├── low_risk.py               # Low Risk 스킬들
│   │   ├── medium_risk.py            # Medium Risk 스킬들
│   │   └── high_risk.py              # High Risk 스킬들
│   └── utils/
│       └── __init__.py
└── tests/                            # 테스트 코드
    ├── __init__.py
    ├── test_chillmcp.py              # 통합 테스트
    ├── test_command_line_params.py   # 커맨드라인 파라미터 검증 (필수)
    ├── test_response_parsing.py      # 응답 파싱 테스트
    ├── test_server_manually.py       # 수동 서버 테스트
    └── interactive_test.py           # 대화형 테스트
```

## 🎯 사용 예시

### 1. 스트레스 체크

```python
# Claude Desktop에서
check_stress()
```

결과:
- 현재 스트레스 레벨
- Boss Alert 레벨
- 휴식 필요 여부
- 추천 스킬 목록
- 통계 정보

### 2. 낮은 위험도 스킬 사용

```python
# 잠깐 딴생각하기 (스트레스 감소: 20-30, 감지 확률: 10%)
deep_thinking()
```

### 3. 중간 위험도 스킬 사용

```python
# SNS 둘러보기 (스트레스 감소: 40-60, 감지 확률: 35%)
scroll_sns()
```

### 4. 높은 위험도 스킬 사용

```python
# 넷플릭스 시청 (스트레스 감소: 70-95, 감지 확률: 65%)
watch_netflix()
```

## ⚠️ 주의사항

- Boss Alert Level이 5가 되면 모든 농땡이 스킬 사용 시 20초 지연이 발생합니다
- 스트레스는 시간이 지남에 따라 자동으로 증가합니다 (기본: 5분마다 +5)
- Boss Alert는 시간이 지남에 따라 자동으로 감소합니다 (기본: 5분마다 -1)
- 성격 유형에 따라 사용 가능한 스킬이 다릅니다

## 🔧 개발 환경

- Python 3.11
- FastMCP 0.1.0 이상

## 📝 라이센스

이 프로젝트는 MIT 라이센스를 따릅니다.

## 🤝 기여

버그 리포트나 기능 제안은 Issues를 통해 환영합니다!
