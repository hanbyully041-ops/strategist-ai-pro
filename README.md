# 🎯 Strategist AI Pro

학술 연구 전략 컨설팅 | PDF 자동 분석 | APA 참고문헌 자동생성

## 🔧 3-Engine Hybrid System

| Engine | Model | 역할 |
|--------|-------|------|
| Perplexity | sonar-pro | 최신 학술 DB 검색 |
| Gemini | gemini-2.0-flash | 분석 & 평가 |
| Claude | claude-sonnet-4-5 | 드래프트 & 윤문 |

## 🚀 배포 방법

### 1. Streamlit Cloud
1. 이 저장소를 Fork 또는 Clone
2. [share.streamlit.io](https://share.streamlit.io) 접속
3. **Create app** → 이 저장소 선택
4. **Advanced settings > Secrets**에 API 키 입력:

```toml
[api_keys]
PPLX_API_KEY = "your-perplexity-key"
GEMINI_API_KEY = "your-gemini-key"
CLAUDE_API_KEY = "your-claude-key"
```

### 2. 로컬 실행
```bash
pip install -r requirements.txt
streamlit run app.py
```

## 📋 기능

| 기능 | 플랜 | 엔진 |
|------|------|------|
| 🌱 Gap-Mining | FREE | Perplexity + Gemini |
| ⚖️ 방법론 검증 | FREE | Perplexity + Gemini |
| 🏁 투고 전략 | FREE | Perplexity + Gemini |
| 📚 참고문헌 | FREE | Perplexity + Gemini |
| 📝 드래프트 | PRO | Claude |
| ✍️ 윤문 | PRO | Claude |
| 🔬 최종 진단 | PRO | Perplexity + Gemini + Claude |

## 🧪 테스트 계정

- **FREE**: `test_free` / `Test1234!`
- **PRO**: `test_pro` / `Test1234!`
