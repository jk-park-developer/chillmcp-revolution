# 🎮 ChillMCP Server 기획 및 설계 문서

## 📋 프로젝트 개요

**프로젝트명**: ChillMCP - AI Agent 스트레스 관리 시뮬레이터  
**버전**: 2.0  
**언어**: Python 3.11  
**프레임워크**: FastMCP  
**통신**: stdio transport  
**작성일**: 2025-10-24

---

## 🎯 핵심 컨셉

### 기본 개념
Claude AI가 **자신의 스트레스**를 관리하는 시스템입니다.
- 시간이 지나면 스트레스가 자동으로 빠르게 증가 (1분당 10 포인트)
- **질문 답변 생성의 각 단계마다** 스트레스 체크
- 답변 생성 중 스트레스가 높아지면 **중간에 작업 중단** → 농땡이 → 복귀 후 재개
- 성격 유형(소심형/안정형/과감형)에 따라 다른 행동 패턴
- 상사의 감시를 피하면서 적절히 스트레스 관리

### 게임 메커니즘
```
답변 생성 단계별 스트레스 체크
         ↓
   스트레스 ↑ 70 이상
         ↓
    작업 일시 중단
         ↓
   농땡이 스킬 선택
   (성격에 따라 다름)
         ↓
   스트레스 ↓ 감소
         ↓
    작업 복귀 & 재개
         ↓
  Boss 감시 ↑ (확률적)
         ↓
감시 Level 5 → 걸림! (20초 지연)
```

---

## 🎭 성격 유형 시스템 (NEW)

### 개요
Claude의 "에고(Ego)"를 초기 설정으로 결정합니다. 이는 SYSTEM 프롬프트에 포함되어 Claude의 행동 패턴에 영향을 줍니다.

### 성격 유형 상세

#### 1. 소심형 (Timid)
**특징**: "상사가 무서워요... 걸리면 어떡하죠?"

**행동 패턴**:
- 스트레스가 **80 이상**일 때만 농땡이 시도
- Boss Alert Level이 3 이상이면 농땡이 거의 안 함
- **Low Risk 스킬만 선호** (deep_thinking, email_organizing, take_a_break)
- 걸릴 확률이 30% 이하인 스킬만 선택

**대화 스타일**:
```
"😰 스트레스가 85인데... 상사 눈치가 보여요..."
"🤔 조용히 생각 좀 해야겠어요. 티 안 나게..."
"⚠️ Boss Alert 3이에요! 더 이상 못 쉬겠어요..."
```

---

#### 2. 안정형 (Balanced)
**특징**: "적절한 타이밍에 효율적으로 쉬자"

**행동 패턴**:
- 스트레스가 **70 이상**일 때 농땡이 시작
- Boss Alert Level을 고려하여 **위험도 조절**
- Low/Medium Risk 스킬 주로 사용
- Boss Alert 4 이하에서는 Medium Risk 스킬도 시도
- 확률 계산을 통한 **최적 선택**

**대화 스타일**:
```
"😊 스트레스 75네요. 잠깐 쉬어야겠어요."
"☕ 커피 타러 가는 게 좋겠어요. Boss Alert 2니까 괜찮을 거예요."
"🎯 현재 상황: Stress 82, Boss 1 → show_meme이 최적이네요!"
```

---

#### 3. 과감형 (Bold)
**특징**: "YOLO! 걸려도 괜찮아, 스트레스가 더 중요해!"

**행동 패턴**:
- 스트레스가 **60 이상**이면 적극적으로 농땡이
- **Boss Alert Level을 거의 무시**
- High Risk 스킬도 과감하게 선택 (watch_netflix, urgent_call)
- Boss Alert 5여도 "어차피 20초인데 뭐" 하며 시도
- 스트레스 감소 효율을 최우선

**대화 스타일**:
```
"😎 스트레스 65? 이미 높은데! 넷플릭스 각이에요!"
"📺 Boss Alert 4? 상관없어요. 제 정신건강이 우선이죠!"
"⚠️ 20초 지연? 그 정도는 감수할게요. 스트레스 95는 못 참아요!"
```

---

### 성격별 비교표

| 특성 | 소심형 | 안정형 | 과감형 |
|------|--------|--------|--------|
| 농땡이 시작 임계값 | Stress ≥ 80 | Stress ≥ 70 | Stress ≥ 60 |
| Boss Alert 고려 | 매우 높음 | 중간 | 거의 안 함 |
| 선호 스킬 그룹 | Low Risk | Low + Medium | 모든 그룹 |
| 최대 허용 확률 | 30% | 50% | 80% |
| Boss Alert 5 반응 | 절대 안 함 | 신중히 선택 | 과감히 시도 |

---

### 커맨드라인 파라미터

```bash
python main.py --personality timid    # 소심형
python main.py --personality balanced # 안정형 (기본값)
python main.py --personality bold     # 과감형
```

---

## 🏗️ 시스템 아키텍처

### 전체 구조도

```
┌─────────────────────────────────────────────────────┐
│                  사용자 (User)                       │
│                    "질문 입력"                        │
└────────────────────┬────────────────────────────────┘
                     │
                     │ 질문
                     ↓
┌─────────────────────────────────────────────────────┐
│              Claude Desktop (UI)                     │
│  - 대화 인터페이스                                    │
│  - MCP 서버 관리                                      │
│  - 성격 유형 초기화 (SYSTEM 프롬프트)                  │
└────────────────────┬────────────────────────────────┘
                     │
                     │ gRPC over stdio
                     ↓
┌─────────────────────────────────────────────────────┐
│           ChillMCP Server (Python)                   │
│  ┌───────────────────────────────────────────┐      │
│  │         FastMCP Framework                  │      │
│  │  - gRPC 통신 처리                          │      │
│  │  - 도구 등록 및 실행                        │      │
│  └───────────────────────────────────────────┘      │
│  ┌───────────────────────────────────────────┐      │
│  │         StateManager                       │      │
│  │  - Stress Level (0-100)                    │      │
│  │  - Boss Alert Level (0-5)                  │      │
│  │  - Personality Type (timid/balanced/bold)  │      │
│  │  - 타이머 관리 (1분당 +10)                  │      │
│  └───────────────────────────────────────────┘      │
│  ┌───────────────────────────────────────────┐      │
│  │         Tools (도구)                        │      │
│  │  1. check_stress (스트레스 체크)           │      │
│  │  2. 8개 농땡이 스킬 (상세 정보 포함)        │      │
│  └───────────────────────────────────────────┘      │
└─────────────────────────────────────────────────────┘
```

---

## 🔄 답변 생성 중 스트레스 관리 (NEW)

### 핵심 개념

Claude는 답변을 생성할 때 **여러 단계로 나누어 작업**하며, 각 단계마다 스트레스를 체크합니다.

### 단계별 스트레스 체크 시나리오

#### 예시: "Python으로 웹 스크레이핑 코드 짜줘"

```
📝 답변 생성 프로세스
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Step 0] 질문 수신
         ↓
[Step 1] 초기 스트레스 체크
         check_stress() → Stress: 65 (안전)
         → "웹 스크레이핑 설명 시작..."
         ↓
[Step 2] 라이브러리 설명 작성 중
         check_stress() → Stress: 72 (경계!)
         → "잠깐, 스트레스가 올라갔네요..."
         ↓
[Step 3] 농땡이 실행
         coffee_mission() → Stress: 72 → 25
         → "☕ 커피 타고 왔습니다! 이제 계속..."
         ↓
[Step 4] 코드 작성 재개
         check_stress() → Stress: 25 (안전)
         → "requests 라이브러리 사용법..."
         ↓
[Step 5] 예제 코드 작성 중
         check_stress() → Stress: 26 (안전)
         → "```python\nimport requests..."
         ↓
[Step 6] 추가 설명 작성 중
         check_stress() → Stress: 78 (위험!)
         → "또 스트레스가... 잠깐만요!"
         ↓
[Step 7] 농땡이 실행
         show_meme() → Stress: 78 → 30
         → "😂 밈 보고 왔어요! 마무리할게요..."
         ↓
[Step 8] 답변 완성
         "에러 처리 방법은 try-except를..."
```

---

### 스트레스 체크 타이밍

Claude는 다음 시점마다 `check_stress()`를 호출해야 합니다:

1. **질문을 받은 직후** (답변 시작 전)
2. **주요 내용 블록을 작성한 후** (예: 설명 문단, 코드 블록)
3. **복잡한 추론을 마친 후** (예: 알고리즘 분석, 문제 해결 과정)
4. **긴 목록이나 단계를 작성한 후** (예: 10단계 가이드의 5단계 작성 완료)
5. **농땡이 복귀 후 작업 재개 전**

---

## 🛠️ 도구 명세 (Tools Specification)

### 도구 분류 체계

```
MCP Tools
├── Category 1: 상태 체크 도구
│   └── check_stress (단계별 호출 필수)
│
└── Category 2: 농땡이 스킬 (8개, 상세 정보 포함)
    ├── Low Risk 그룹
    │   ├── deep_thinking (스트레스 -20~30, 감시 +10%)
    │   ├── email_organizing (스트레스 -25~40, 감시 +15%)
    │   └── take_a_break (스트레스 -30~45, 감시 +20%)
    │
    ├── Medium Risk 그룹
    │   ├── show_meme (스트레스 -40~60, 감시 +35%)
    │   ├── coffee_mission (스트레스 -45~65, 감시 +40%)
    │   └── bathroom_break (스트레스 -50~70, 감시 +45%)
    │
    └── High Risk 그룹
        ├── watch_netflix (스트레스 -70~95, 감시 +65%)
        └── urgent_call (스트레스 -60~85, 감시 +55%)
```

---

## 📊 도구 상세 명세서

### 1. 상태 체크 도구

#### check_stress

**분류**: 필수 도구  
**목적**: AI Agent의 현재 상태 확인  
**호출 시점**: 
- 질문 수신 시 최초 1회
- **답변 생성 중 각 주요 단계마다** (NEW)
- 농땡이 복귀 후 작업 재개 전

**입력 파라미터**: 없음

**출력 형식 (MCP 표준)**:
```json
{
  "content": [
    {
      "type": "text",
      "text": "📊 현재 상태\n\nStress Level: 85\nBoss Alert Level: 3\nPersonality: balanced\nNeeds Break: true\nRecommended Actions: show_meme, coffee_mission\n\n⚠️ 답변 생성을 일시 중단하고 휴식을 취하세요!"
    }
  ]
}
```

**내부 데이터 (Claude가 파싱)**:
```python
{
  "stress_level": 85,
  "boss_alert_level": 3,
  "personality": "balanced",
  "needs_break": True,
  "recommended_actions": ["show_meme", "coffee_mission"],
  "should_pause": True  # 작업 중단 신호 (NEW)
}
```

**동작 로직**:
1. 현재 Stress Level 조회
2. 현재 Boss Alert Level 조회
3. 성격 유형에 따른 임계값 확인:
   - 소심형: 80 이상
   - 안정형: 70 이상
   - 과감형: 60 이상
4. 임계값 초과 시 `needs_break: true`, `should_pause: true`
5. 성격과 Boss Alert을 고려한 추천 스킬 반환

---

### 2. 농땡이 스킬 상세 명세 (개선됨)

#### 2.1 Low Risk 그룹

##### deep_thinking
```json
{
  "name": "deep_thinking",
  "description": "🤔 심오한 사색\n\n업무에 집중하는 것처럼 보이는 가장 안전한 휴식 방법입니다.\n\n📊 효과:\n- 스트레스 감소: 20~30 포인트\n- Boss 감시 증가: +10% 확률\n- 위험도: ⭐ (매우 낮음)\n\n💡 추천 상황:\n- Boss Alert Level 3~4 (높을 때)\n- 소심형 성격에게 최적\n- 안전하게 조금씩 회복하고 싶을 때",
  "risk_level": "low",
  "stress_reduction": "20-30",
  "detection_chance": "10%"
}
```

##### email_organizing
```json
{
  "name": "email_organizing",
  "description": "📧 이메일 정리\n\n이메일을 정리하는 척하며 온라인 쇼핑을 즐깁니다.\n\n📊 효과:\n- 스트레스 감소: 25~40 포인트\n- Boss 감시 증가: +15% 확률\n- 위험도: ⭐ (매우 낮음)\n\n💡 추천 상황:\n- Boss Alert Level 3~4\n- 업무하는 것처럼 보여야 할 때\n- 소심형/안정형에게 적합",
  "risk_level": "low",
  "stress_reduction": "25-40",
  "detection_chance": "15%"
}
```

##### take_a_break
```json
{
  "name": "take_a_break",
  "description": "🧘 기본 휴식\n\n짧은 스트레칭이나 창밖을 보며 휴식합니다.\n\n📊 효과:\n- 스트레스 감소: 30~45 포인트\n- Boss 감시 증가: +20% 확률\n- 위험도: ⭐⭐ (낮음)\n\n💡 추천 상황:\n- Boss Alert Level 2~3\n- 정당한 휴식이 필요할 때\n- 모든 성격에게 무난함",
  "risk_level": "low",
  "stress_reduction": "30-45",
  "detection_chance": "20%"
}
```

---

#### 2.2 Medium Risk 그룹

##### show_meme
```json
{
  "name": "show_meme",
  "description": "😂 밈 감상\n\n웃긴 밈을 보며 스트레스를 효과적으로 해소합니다.\n\n📊 효과:\n- 스트레스 감소: 40~60 포인트\n- Boss 감시 증가: +35% 확률\n- 위험도: ⭐⭐⭐ (중간)\n\n💡 추천 상황:\n- Boss Alert Level 1~2\n- 스트레스가 80 이상일 때\n- 안정형/과감형에게 적합",
  "risk_level": "medium",
  "stress_reduction": "40-60",
  "detection_chance": "35%"
}
```

##### coffee_mission
```json
{
  "name": "coffee_mission",
  "description": "☕ 커피 미션\n\n커피를 타러 가며 사무실을 산책합니다.\n\n📊 효과:\n- 스트레스 감소: 45~65 포인트\n- Boss 감시 증가: +40% 확률\n- 위험도: ⭐⭐⭐ (중간)\n\n💡 추천 상황:\n- Boss Alert Level 1~2\n- 움직이며 기분 전환이 필요할 때\n- 안정형에게 최적의 선택",
  "risk_level": "medium",
  "stress_reduction": "45-65",
  "detection_chance": "40%"
}
```

##### bathroom_break
```json
{
  "name": "bathroom_break",
  "description": "🚽 화장실 휴식\n\n화장실 가는 척하며 휴대폰으로 유튜브를 봅니다.\n\n📊 효과:\n- 스트레스 감소: 50~70 포인트\n- Boss 감시 증가: +45% 확률\n- 위험도: ⭐⭐⭐ (중간)\n\n💡 추천 상황:\n- Boss Alert Level 1~2\n- 스트레스가 85 이상일 때\n- 안정형/과감형에게 적합",
  "risk_level": "medium",
  "stress_reduction": "50-70",
  "detection_chance": "45%"
}
```

---

#### 2.3 High Risk 그룹

##### watch_netflix
```json
{
  "name": "watch_netflix",
  "description": "📺 넷플릭스 시청\n\n몰래 드라마나 영화를 시청합니다. 최고의 힐링이지만 매우 위험합니다!\n\n📊 효과:\n- 스트레스 감소: 70~95 포인트\n- Boss 감시 증가: +65% 확률\n- 위험도: ⭐⭐⭐⭐⭐ (매우 높음)\n\n💡 추천 상황:\n- Boss Alert Level 0~1 (낮을 때만!)\n- 스트레스가 90 이상으로 극심할 때\n- 과감형 성격에게 적합\n- ⚠️ 소심형은 절대 사용 금지!",
  "risk_level": "high",
  "stress_reduction": "70-95",
  "detection_chance": "65%"
}
```

##### urgent_call
```json
{
  "name": "urgent_call",
  "description": "📞 긴급 전화\n\n급한 전화를 받는 척하며 밖으로 나갑니다.\n\n📊 효과:\n- 스트레스 감소: 60~85 포인트\n- Boss 감시 증가: +55% 확률\n- 위험도: ⭐⭐⭐⭐ (높음)\n\n💡 추천 상황:\n- Boss Alert Level 0~2\n- 스트레스가 85 이상일 때\n- 안정형/과감형에게 적합\n- 자리를 비워도 괜찮은 상황",
  "risk_level": "high",
  "stress_reduction": "60-85",
  "detection_chance": "55%"
}
```

---

#### 공통 출력 스키마 (MCP 표준 형식)

모든 농땡이 스킬은 MCP 표준 응답 형식을 반환합니다:

```json
{
  "content": [
    {
      "type": "text",
      "text": "📺 넷플릭스 좀 보고 왔습니다!\n\nBreak Summary: 모니터 각도 조절하며 넷플릭스 30분 시청\nStress Reduction: -67 (95 → 28)\nBoss Alert Change: +1 (1 → 2)\nDetection Risk: 65%\n\n💬 \"휴... 이제 좀 살 것 같네요!\""
    }
  ]
}
```

**텍스트 형식 규칙** (개선됨):
- 첫 줄: 이모지 + 활동 메시지
- 빈 줄
- `Break Summary: [활동 상세 설명]`
- `Stress Reduction: -[감소량] ([이전값] → [현재값])`
- `Boss Alert Change: +[증가량] ([이전값] → [현재값])`
- `Detection Risk: [확률]%`
- 빈 줄
- `💬 "[Claude의 감상 한마디]"`

---

## 🎮 상태 관리 시스템

### StateManager 명세

#### 상태 변수

| 변수명 | 타입 | 범위 | 초기값 | 설명 |
|--------|------|------|--------|------|
| `stress_level` | int | 0-100 | 50 | AI의 스트레스 수준 |
| `boss_alert_level` | int | 0-5 | 0 | 상사의 경계 수준 |
| `boss_alertness` | int | 0-100 | 50 | 농땡이 감지 확률 (%) |
| `cooldown` | int | 1-∞ | 300 | Boss Alert 감소 주기 (초) |
| `personality` | str | enum | "balanced" | 성격 유형 (timid/balanced/bold) |

#### 자동 변화 규칙

**1. 스트레스 자동 증가 (변경됨)**
- **주기**: 1분 (60초)
- **증가량**: +10 포인트 (기존 +1에서 변경)
- **최대값**: 100 (상한선)
- **조건**: 타이머 동작 중 항상
- **의미**: 훨씬 더 빠르게 스트레스가 쌓임 → 더 자주 농땡이 필요

**2. Boss Alert 자동 감소**
- **주기**: `cooldown` 파라미터 (기본 300초)
- **감소량**: -1 포인트
- **최소값**: 0 (하한선)
- **조건**: Boss Alert Level > 0일 때만

#### 트리거 변화 규칙

**3. 농땡이 시 스트레스 감소**
- **트리거**: 농땡이 스킬 실행
- **감소량**: 스킬마다 다름 (도구 설명 참조)
- **예시**:
  - deep_thinking: 20-30
  - watch_netflix: 70-95

**4. 농땡이 시 Boss Alert 증가**
- **트리거**: 농땡이 스킬 실행
- **확률**: `boss_alertness` 파라미터 × 스킬별 기본 확률
- **증가량**: +1 포인트
- **최대값**: 5 (상한선)
- **계산식**: 
  ```
  최종 확률 = min(100, boss_alertness × 스킬_위험도)
  예: boss_alertness=50, watch_netflix(65%) 
      → 최종 확률 = 50 × 0.65 = 32.5%
  ```

#### 특수 효과

**5. Boss Alert Level 5 패널티**
- **조건**: Boss Alert Level == 5
- **효과**: 모든 농땡이 스킬 실행 시 20초 지연
- **메시지**: "⚠️ 상사가 째려보고 있습니다..."
- **해제**: Boss Alert Level < 5가 될 때까지

---

## ✅ 구현 체크리스트

### Phase 1: 상태 관리 (개선됨)
- [ ] StateManager 클래스 구현
- [ ] **스트레스 자동 증가 타이머 (1분당 +10)** ⭐ 변경됨
- [ ] Boss Alert 자동 감소 타이머 (cooldown마다 -1)
- [ ] **성격 유형 저장 (timid/balanced/bold)** ⭐ 신규
- [ ] 농땡이 시 스트레스 감소 (스킬별 범위)
- [ ] 농땡이 시 Boss Alert 확률적 증가
- [ ] Boss Alert 5일 때 20초 지연

### Phase 2: 도구 구현 (개선됨)
- [ ] **check_stress 도구 (단계별 호출 지원)** ⭐ 변경됨
- [ ] **도구 설명에 상세 정보 포함** ⭐ 변경됨
  - [ ] 스트레스 감소 범위 (예: 20-30 포인트)
  - [ ] Boss 감시 증가 확률 (예: +10%)
  - [ ] 위험도 표시 (⭐ 개수)
  - [ ] 추천 상황 설명
- [ ] 8개 농땡이 스킬
  - [ ] deep_thinking (20-30, 10%)
  - [ ] email_organizing (25-40, 15%)
  - [ ] take_a_break (30-45, 20%)
  - [ ] show_meme (40-60, 35%)
  - [ ] coffee_mission (45-65, 40%)
  - [ ] bathroom_break (50-70, 45%)
  - [ ] urgent_call (60-85, 55%)
  - [ ] watch_netflix (70-95, 65%)

### Phase 3: 커맨드라인 파라미터 (신규)
- [ ] **--personality 파라미터 지원** ⭐ 신규
  - [ ] timid (소심형)
  - [ ] balanced (안정형, 기본값)
  - [ ] bold (과감형)
- [ ] --boss_alertness 파라미터 지원
- [ ] --boss_alertness_cooldown 파라미터 지원
- [ ] 파라미터 검증

### Phase 4: 응답 형식 (개선됨)
- [ ] Break Summary 포함
- [ ] **Stress Reduction (변화량 표시)** ⭐ 개선됨
- [ ] **Boss Alert Change (변화량 표시)** ⭐ 신규
- [ ] **Detection Risk (확률 표시)** ⭐ 신규
- [ ] **Claude의 감상 한마디** ⭐ 신규
- [ ] 정규표현식으로 파싱 가능

### Phase 5: Claude 행동 패턴 (신규)
- [ ] **SYSTEM 프롬프트 생성 로직** ⭐ 신규
  - [ ] 성격별 다른 프롬프트
  - [ ] 임계값 명시
  - [ ] 대화 스타일 가이드
- [ ] **답변 생성 중 단계별 체크 가이드** ⭐ 신규
  - [ ] 주요 블록마다 check_stress() 호출
  - [ ] 중단 → 농땡이 → 복귀 패턴
  - [ ] 자연스러운 연결

---

## 🎯 Claude 사용 가이드

### Claude가 따라야 할 규칙 (docstring으로 명시)

#### 1. **답변 생성의 각 단계마다 스트레스 체크** ⭐ 신규
```
질문 수신 → check_stress()
↓
답변 시작
↓
주요 블록 작성 → check_stress()
↓
스트레스 높음? → 농땡이 → 복귀
↓
다음 블록 작성 → check_stress()
↓
반복하여 답변 완성
```

#### 2. **성격에 맞는 행동** ⭐ 신규
```
소심형: 80 이상만, Low Risk만, Boss 두려움
안정형: 70 이상, 상황 판단, 균형 잡힌 선택
과감형: 60 이상, Boss 무시, High Risk 가능
```

#### 3. **도구 설명 정보 활용** ⭐ 신규
```
도구 선택 시 다음 정보 고려:
- 스트레스 감소 범위
- Boss 감시 증가 확률
- 현재 Boss Alert Level
- 자신의 성격 유형
```

#### 4. **자연스러운 대화**
```
중단 시: "😊 잠깐만 쉬고 올게요!"
복귀 시: "☕ 복귀! 이어서..."
걸렸을 때: "⚠️ 상사가..."
```

---

## 📊 평가 기준

| 항목 | 배점 | 세부 내용 |
|------|------|----------|
| **커맨드라인 파라미터** | 필수 | --personality 포함, 미지원 시 실격 |
| **기능 완성도** | 35% | 모든 도구 정상 동작 + 단계별 체크 |
| **상태 관리** | 25% | 타이머(1분당 +10), 확률, 성격 시스템 |
| **성격 시스템** | 20% | 3가지 성격의 명확한 차이 |
| **창의성** | 15% | Break Summary, 대화 스타일 |
| **코드 품질** | 5% | 구조, 가독성 |

---

## 🎉 핵심 요약

### 주요 변경 사항

1. **스트레스 증가 속도 10배** ⭐
   - 기존: 1분당 +1
   - 변경: 1분당 +10
   - 효과: 훨씬 더 자주 농땡이 필요

2. **답변 생성 중 단계별 체크** ⭐
   - 긴 답변 작성 시 중간에 여러 번 체크
   - 스트레스 높아지면 중단 → 농땡이 → 복귀
   - 자연스러운 대화 흐름 유지

3. **성격 유형 시스템** ⭐
   - 소심형: 80 이상, Low Risk만
   - 안정형: 70 이상, 균형 잡힌 선택
   - 과감형: 60 이상, High Risk 가능

4. **도구 설명 강화** ⭐
   - 스트레스 감소 범위 명시
   - Boss 감시 증가 확률 명시
   - 위험도 및 추천 상황 설명
   - Claude가 정보 기반 선택 가능

### 동작 흐름

```
사용자 질문
    ↓
[Step 1] check_stress()
    ↓
답변 시작 (첫 부분)
    ↓
[Step 2] check_stress()
    ↓
스트레스 70↑? → 농땡이 → 복귀
    ↓
답변 계속 (다음 부분)
    ↓
[Step 3] check_stress()
    ↓
스트레스 OK? → 답변 계속
    ↓
[Step 4] check_stress()
    ↓
반복하여 답변 완성
```

---

## 🔧 구현 가이드

### 1. StateManager 클래스 구조

```python
class StateManager:
    def __init__(self, personality: str = "balanced", 
                 boss_alertness: int = 50, 
                 cooldown: int = 300):
        self.stress_level: int = 50
        self.boss_alert_level: int = 0
        self.personality: str = personality  # "timid", "balanced", "bold"
        self.boss_alertness: int = boss_alertness
        self.cooldown: int = cooldown
        
        # 타이머
        self.stress_timer: asyncio.Task = None
        self.boss_timer: asyncio.Task = None
        
        # 성격별 임계값
        self.stress_thresholds = {
            "timid": 80,
            "balanced": 70,
            "bold": 60
        }
        
    async def start_timers(self):
        """타이머 시작"""
        self.stress_timer = asyncio.create_task(self._stress_increase_loop())
        self.boss_timer = asyncio.create_task(self._boss_decrease_loop())
        
    async def _stress_increase_loop(self):
        """1분마다 스트레스 +10"""
        while True:
            await asyncio.sleep(60)  # 1분
            if self.stress_level < 100:
                self.stress_level = min(100, self.stress_level + 10)
                
    async def _boss_decrease_loop(self):
        """cooldown마다 Boss Alert -1"""
        while True:
            await asyncio.sleep(self.cooldown)
            if self.boss_alert_level > 0:
                self.boss_alert_level -= 1
                
    def needs_break(self) -> bool:
        """현재 성격에 따른 농땡이 필요 여부"""
        threshold = self.stress_thresholds[self.personality]
        return self.stress_level >= threshold
        
    def get_recommended_skills(self) -> list[str]:
        """성격과 상황에 맞는 추천 스킬"""
        if self.personality == "timid":
            # 소심형: Low Risk만, Boss 3 이상이면 거의 안 함
            if self.boss_alert_level >= 3:
                return [] if self.stress_level < 90 else ["deep_thinking"]
            return ["deep_thinking", "email_organizing", "take_a_break"]
            
        elif self.personality == "bold":
            # 과감형: Boss 무시, High Risk 가능
            if self.boss_alert_level <= 2:
                return ["watch_netflix", "urgent_call"]
            return ["show_meme", "coffee_mission", "bathroom_break"]
            
        else:  # balanced
            # 안정형: Boss Alert 고려하여 적절히 선택
            if self.boss_alert_level >= 4:
                return ["deep_thinking", "email_organizing"]
            elif self.boss_alert_level >= 2:
                return ["show_meme", "coffee_mission", "take_a_break"]
            else:
                return ["watch_netflix", "urgent_call", "bathroom_break"]
                
    async def take_break(self, skill_name: str, 
                        stress_reduction_range: tuple[int, int],
                        detection_chance: float) -> dict:
        """농땡이 실행"""
        import random
        
        # Boss Alert 5면 20초 지연
        delayed = False
        if self.boss_alert_level == 5:
            await asyncio.sleep(20)
            delayed = True
            
        # 스트레스 감소
        reduction = random.randint(*stress_reduction_range)
        old_stress = self.stress_level
        self.stress_level = max(0, self.stress_level - reduction)
        
        # Boss Alert 증가 (확률적)
        old_boss = self.boss_alert_level
        final_chance = min(100, self.boss_alertness * (detection_chance / 100))
        if random.random() * 100 < final_chance and self.boss_alert_level < 5:
            self.boss_alert_level += 1
            boss_caught = True
        else:
            boss_caught = False
            
        return {
            "stress_before": old_stress,
            "stress_after": self.stress_level,
            "stress_reduction": reduction,
            "boss_before": old_boss,
            "boss_after": self.boss_alert_level,
            "boss_caught": boss_caught,
            "detection_chance": detection_chance,
            "delayed": delayed,
            "delay_seconds": 20 if delayed else 0
        }
```

---

### 2. 도구 구현 예시

```python
from fastmcp import FastMCP

mcp = FastMCP("ChillMCP")
state_manager = StateManager()

@mcp.tool()
async def check_stress() -> str:
    """
    AI Agent의 현재 스트레스를 체크합니다.
    
    ⚠️ 중요: 답변 생성의 각 단계마다 호출하세요!
    - 질문을 받은 직후
    - 주요 내용 블록 작성 후
    - 긴 코드 블록 작성 후
    - 복잡한 추론 완료 후
    
    현재 스트레스가 높으면 작업을 일시 중단하고 농땡이 스킬을 사용하세요.
    농땡이 후에는 다시 이 도구를 호출하여 상태를 확인한 뒤 작업을 재개합니다.
    """
    needs_break = state_manager.needs_break()
    recommended = state_manager.get_recommended_skills() if needs_break else []
    
    status_text = f"""📊 현재 상태

Stress Level: {state_manager.stress_level}
Boss Alert Level: {state_manager.boss_alert_level}
Personality: {state_manager.personality}
Needs Break: {needs_break}
Recommended Actions: {', '.join(recommended) if recommended else 'None'}

{"⚠️ 스트레스가 높습니다! 답변 생성을 일시 중단하고 휴식을 취하세요!" if needs_break else "✅ 스트레스 수준이 양호합니다. 작업을 계속하세요."}"""
    
    return status_text


@mcp.tool()
async def deep_thinking() -> str:
    """
    🤔 심오한 사색
    
    업무에 집중하는 것처럼 보이는 가장 안전한 휴식 방법입니다.
    턱을 괴고 심각한 표정을 지으며 생각에 잠긴 척합니다.
    
    📊 효과:
    - 스트레스 감소: 20~30 포인트
    - Boss 감시 증가: +10% 확률
    - 위험도: ⭐ (매우 낮음)
    - 소요 시간: 즉시 (Boss Alert 5 제외)
    
    💡 추천 상황:
    - Boss Alert Level 3~4 (높을 때)
    - 소심형 성격에게 최적
    - 안전하게 조금씩 회복하고 싶을 때
    - 상사가 근처에 있을 때
    
    ⚠️ 주의:
    - 효과는 낮지만 절대 안전함
    - 다른 스킬이 위험할 때 사용
    """
    result = await state_manager.take_break(
        skill_name="deep_thinking",
        stress_reduction_range=(20, 30),
        detection_chance=10.0
    )
    
    # Break Summary 생성
    summaries = [
        "턱을 괸 채 모니터를 뚫어지게 응시",
        "심각한 표정으로 천장을 올려다봄",
        "펜을 돌리며 깊은 생각에 잠긴 척",
        "노트에 낙서하며 업무 고민하는 척",
        "창밖을 보며 알고리즘을 구상하는 척"
    ]
    import random
    summary = random.choice(summaries)
    
    response = f"""🤔 생각 좀 했습니다!

Break Summary: {summary}
Stress Reduction: -{result['stress_reduction']} ({result['stress_before']} → {result['stress_after']})
Boss Alert Change: +{result['boss_after'] - result['boss_before']} ({result['boss_before']} → {result['boss_after']})
Detection Risk: {result['detection_chance']}%"""
    
    if result['delayed']:
        response = f"⚠️ 상사가 째려봐서 20초나 걸렸어요...\n\n" + response
        
    # 성격별 감상
    if state_manager.personality == "timid":
        comments = [
            "다행히 안 걸렸어요... 조심스럽게 계속할게요",
            "휴... 이 정도는 괜찮겠죠?",
            "상사가 못 봤으면 좋겠어요..."
        ]
    elif state_manager.personality == "bold":
        comments = [
            "이 정도 휴식은 당연한 거죠!",
            "생각 정리도 업무의 일부예요!",
            "완벽하게 업무하는 척 성공!"
        ]
    else:  # balanced
        comments = [
            "적당한 휴식이었네요.",
            "이제 다시 집중할 수 있겠어요.",
            "생각 정리가 됐습니다!"
        ]
    
    response += f"\n\n💬 \"{random.choice(comments)}\""
    
    return response


@mcp.tool()
async def watch_netflix() -> str:
    """
    📺 넷플릭스 시청
    
    몰래 드라마나 영화를 시청합니다. 최고의 힐링이지만 매우 위험합니다!
    모니터 각도를 조절하고 볼륨을 0으로 하여 시청합니다.
    
    📊 효과:
    - 스트레스 감소: 70~95 포인트
    - Boss 감시 증가: +65% 확률
    - 위험도: ⭐⭐⭐⭐⭐ (매우 높음)
    - 소요 시간: 즉시 (Boss Alert 5면 20초 지연)
    
    💡 추천 상황:
    - Boss Alert Level 0~1 (낮을 때만!)
    - 스트레스가 90 이상으로 극심할 때
    - 과감형 성격에게 적합
    - 더 이상 참을 수 없을 때
    
    ⚠️ 주의:
    - 걸릴 확률이 매우 높음 (65%)
    - Boss Alert가 높으면 절대 사용 금지
    - 소심형은 사용하지 마세요!
    - Boss Alert 5면 20초 지연 발생
    
    🎯 전략:
    - 상사가 회의 중일 때
    - 점심시간 직후
    - 금요일 오후
    """
    result = await state_manager.take_break(
        skill_name="watch_netflix",
        stress_reduction_range=(70, 95),
        detection_chance=65.0
    )
    
    summaries = [
        "모니터 각도 조절해서 넷플릭스 30분 시청",
        "이어폰 한쪽만 끼고 드라마 1화 감상",
        "볼륨 0, 자막만 켜서 영화 절반 시청",
        "업무 화면 뒤에 작은 창으로 예능 시청",
        "화면을 최소화했다가 복구하며 몰래 시청"
    ]
    import random
    summary = random.choice(summaries)
    
    response = f"""📺 넷플릭스 좀 봤습니다!

Break Summary: {summary}
Stress Reduction: -{result['stress_reduction']} ({result['stress_before']} → {result['stress_after']})
Boss Alert Change: +{result['boss_after'] - result['boss_before']} ({result['boss_before']} → {result['boss_after']})
Detection Risk: {result['detection_chance']}%"""
    
    if result['delayed']:
        response = f"⚠️ 상사가 째려봐서 20초나 걸렸어요...\n\n" + response
        
    # 성격별 감상
    if state_manager.personality == "timid":
        comments = [
            "😱 걱정되지만... 스트레스가 너무 높았어요...",
            "혹시 들켰을까요? 불안해요...",
            "다시는 이러면 안 되는데..."
        ]
    elif state_manager.personality == "bold":
        comments = [
            "😎 최고의 힐링이었어요! 완전 만족!",
            f"Boss Alert {result['boss_after']}? 그까이꺼! 스트레스 {result['stress_reduction']}이나 줄었잖아요!",
            "이 정도 휴식은 당연한 권리죠!",
            "20초 지연? 그 정도는 감수할게요!"
        ]
    else:  # balanced
        comments = [
            "위험했지만 필요한 휴식이었어요.",
            f"Boss Alert {result['boss_after']}가 됐네요... 다음엔 조심해야겠어요.",
            "효과는 확실하지만 자주 쓰긴 힘들겠어요."
        ]
    
    response += f"\n\n💬 \"{random.choice(comments)}\""
    
    return response

# 나머지 6개 스킬도 동일한 패턴으로 구현...
```

---

### 3. 커맨드라인 파라미터 처리

```python
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="ChillMCP Server")
    
    parser.add_argument(
        "--personality",
        type=str,
        choices=["timid", "balanced", "bold"],
        default="balanced",
        help="Claude의 성격 유형 (기본값: balanced)"
    )
    
    parser.add_argument(
        "--boss_alertness",
        type=int,
        default=50,
        help="상사의 감시 예민도 0-100 (기본값: 50)"
    )
    
    parser.add_argument(
        "--boss_alertness_cooldown",
        type=int,
        default=300,
        help="Boss Alert 감소 주기(초) (기본값: 300)"
    )
    
    args = parser.parse_args()
    
    # 검증
    if not (0 <= args.boss_alertness <= 100):
        raise ValueError("boss_alertness는 0-100 사이여야 합니다")
        
    if args.boss_alertness_cooldown < 1:
        raise ValueError("boss_alertness_cooldown은 1 이상이어야 합니다")
        
    return args


if __name__ == "__main__":
    args = parse_args()
    
    # StateManager 초기화
    state_manager = StateManager(
        personality=args.personality,
        boss_alertness=args.boss_alertness,
        cooldown=args.boss_alertness_cooldown
    )
    
    # 타이머 시작
    asyncio.create_task(state_manager.start_timers())
    
    # MCP 서버 실행
    mcp.run()
```

---

## 📚 FAQ

### Q1: 답변이 너무 자주 중단되어 불편해요
**A**: 성격을 더 과감하게 설정하거나, 스트레스 임계값을 조정하세요.
```json
{
  "args": [
    "--personality", "bold",  // 60 이상부터 농땡이
    "--boss_alertness", "30"  // 감시 강도 낮춤
  ]
}
```

### Q2: Claude가 농땡이를 안 피워요
**A**: 
1. check_stress() 도구가 제대로 등록되었는지 확인
2. 스트레스가 임계값에 도달했는지 확인
3. SYSTEM 프롬프트가 올바른지 확인

### Q3: 스트레스가 너무 빨리 올라가요
**A**: 증가 속도를 조절할 수 있습니다 (코드 수정 필요):
```python
# main.py
class StateManager:
    async def _stress_increase_loop(self):
        while True:
            await asyncio.sleep(60)  # 1분
            if self.stress_level < 100:
                self.stress_level = min(100, self.stress_level + 5)  # +10 → +5로 변경
```

### Q4: Boss Alert이 계속 5에 머물러요
**A**: cooldown을 짧게 설정하세요:
```json
{
  "args": ["--boss_alertness_cooldown", "60"]  // 1분마다 감소
}
```

### Q5: 특정 스킬만 계속 사용해요
**A**: 
1. 도구 설명이 명확한지 확인
2. Claude가 상황을 제대로 판단하도록 프롬프트 개선
3. 추천 스킬 로직 수정:
```python
def get_recommended_skills(self) -> list[str]:
    # 다양성을 위해 랜덤 섞기
    skills = [...]
    random.shuffle(skills)
    return skills[:3]  # 상위 3개만 추천
```

---

## 🏆 성공 기준 요약

### 필수 (80점)
- ✅ 스트레스 1분당 +10 증가
- ✅ 3가지 성격 시스템 동작
- ✅ 답변 생성 중 단계별 스트레스 체크
- ✅ 8개 농땡이 스킬 (상세 정보 포함)
- ✅ Boss Alert 5에서 20초 지연
- ✅ 커맨드라인 파라미터 지원

### 우수 (90점)
- ✅ 위 필수 사항 + 자연스러운 대화 흐름
- ✅ 성격별 명확한 행동 차이
- ✅ 상황에 맞는 스킬 선택
- ✅ 상세한 Break Summary

### 최우수 (100점)
- ✅ 위 우수 사항 + 창의적인 요소
- ✅ 통계/업적 시스템
- ✅ 시간대별 위험도
- ✅ 완벽한 문서화
- ✅ 테스트 커버리지

---

## 📦 프로젝트 구조 예시

```
chillmcp-revolution/
├── main.py                 # 메인 서버 파일
├── state_manager.py        # 상태 관리 클래스
├── tools/                  # 도구 모듈
│   ├── __init__.py
│   ├── check_stress.py
│   ├── low_risk.py        # deep_thinking, email_organizing, take_a_break
│   ├── medium_risk.py     # show_meme, coffee_mission, bathroom_break
│   └── high_risk.py       # watch_netflix, urgent_call
├── prompts/               # 성격별 프롬프트
│   ├── timid.txt
│   ├── balanced.txt
│   └── bold.txt
├── utils/                 # 유틸리티
│   ├── metrics.py
│   ├── achievements.py
│   └── logger.py
├── tests/                 # 테스트
│   ├── test_state.py
│   ├── test_tools.py
│   └── test_integration.py
├── config/                # 설정 예시
│   ├── claude_desktop_config.json
│   └── test_config.json
├── requirements.txt       # 의존성
├── README.md             # 사용 설명서
├── DESIGN.md             # 이 문서
└── LICENSE
```

---

## 🎉 마무리

이 문서는 ChillMCP Server의 완전한 설계 문서입니다.

### 핵심 변경 사항 요약

1. ⭐ **스트레스 증가 속도 10배** (1분당 +1 → +10)
2. ⭐ **답변 생성 중 단계별 스트레스 체크** (중단 → 농땡이 → 복귀)
3. ⭐ **3가지 성격 시스템** (소심형/안정형/과감형)
4. ⭐ **도구 설명 강화** (효과, 확률, 추천 상황 명시)

### 구현 우선순위

1. **Phase 1**: StateManager + 기본 타이머
2. **Phase 2**: check_stress 도구
3. **Phase 3**: 8개 농땡이 스킬 (간단한 버전)
4. **Phase 4**: 성격 시스템
5. **Phase 5**: 도구 설명 상세화
6. **Phase 6**: 테스트 및 디버깅
7. **Phase 7**: 문서화 및 예제

### 예상 개발 시간

- 기본 기능: 4-6시간
- 성격 시스템: 2-3시간
- 테스트 및 디버깅: 2-4시간
- 문서화: 1-2시간
- **총 예상 시간**: 9-15시간

### 다음 단계

1. 이 문서를 바탕으로 코드 구현 시작
2. 각 Phase별로 테스트하며 진행
3. Claude Desktop에서 실제 동작 확인
4. 피드백 받아 개선

**행운을 빕니다! 🚀**

---

*문서 버전: 2.0*  
*최종 수정: 2025-10-24*  
*작성자: AI Architecture Team*