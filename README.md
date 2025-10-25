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
        "--personality",
        "balanced",
        "--boss_alertness",
        "50"
        "--boss_alertness_cooldown",
        "300"
      ]
    }
  }
}
```

## 🧪 테스트 방법

### 통합 테스트 실행

```bash
# 가상환경이 활성화된 상태에서
python test_chillmcp.py
```

테스트 항목:
1. StateManager 초기화 테스트
2. 휴식 필요 여부 판단 테스트
3. 추천 스킬 테스트
4. 농땡이 실행 테스트
5. Boss Alert 5 패널티 테스트
6. 통계 추적 테스트

### 기타 테스트 파일

```bash
# 응답 파싱 테스트
python test_response_parsing.py

# 서버 수동 테스트
python test_server_manually.py

# 대화형 테스트
python interactive_test.py
```

## 📁 프로젝트 구조

```
chillmcp-revolution/
├── main.py                      # 메인 서버 실행 파일
├── requirements.txt             # Python 의존성
├── src/
│   ├── __init__.py
│   ├── state_manager.py         # 상태 관리 핵심 로직
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── check_stress.py      # 스트레스 체크 도구
│   │   ├── low_risk.py          # Low Risk 스킬들
│   │   ├── medium_risk.py       # Medium Risk 스킬들
│   │   └── high_risk.py         # High Risk 스킬들
│   └── utils/
│       └── __init__.py
├── test_chillmcp.py             # 통합 테스트
├── test_response_parsing.py     # 응답 파싱 테스트
├── test_server_manually.py      # 수동 서버 테스트
└── interactive_test.py          # 대화형 테스트
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
