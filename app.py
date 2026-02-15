import streamlit as st
import streamlit.components.v1 as components
import openai
import google.generativeai as genai
import anthropic
import PyPDF2
import docx
import json
import hashlib
import os
from datetime import datetime, timedelta

# ============================================
# 페이지 설정
# ============================================
st.set_page_config(
    page_title="🎯 Strategist AI Pro",
    layout="wide",
    page_icon="🎯",
    initial_sidebar_state="expanded"
)

# ============================================
# 다국어 지원 시스템
# ============================================
LANGUAGES = {
    "ko": {
        "name": "한국어", "flag": "🇰🇷",
        "app_title": "🎯 Strategist AI Pro",
        "app_subtitle": "학술 연구 전략 컨설팅 | PDF 자동 분석 | APA 참고문헌 자동생성",
        "login": "로그인", "signup": "회원가입", "logout": "로그아웃",
        "username": "아이디", "password": "비밀번호", "email": "이메일",
        "password_confirm": "비밀번호 확인", "login_button": "로그인", "signup_button": "회원가입",
        "test_account": "🧪 테스트 계정 보기", "free_plan": "🆓 FREE 플랜", "pro_plan": "💎 PRO 회원",
        "remaining": "남은 횟수", "unlimited": "무제한", "upgrade": "💎 PRO 업그레이드",
        "gap_tab": "🌱 Gap-Mining", "method_tab": "⚖️ 방법론", "draft_tab": "📝 드래프트",
        "polish_tab": "✍️ 윤문", "diagnosis_tab": "🔬 최종 진단", "submit_tab": "🏁 투고",
        "references_tab": "📚 참고문헌", "storage_tab": "💾 저장소",
        "gap_title": "🌱 Gap-Mining", "gap_desc": "💡 연구의 독창성 검증 + 공백 발견 + 연구질문 개선",
        "method_title": "⚖️ 방법론 검증", "method_desc": "🛡️ 심사위원 공격 예상 + 방어 전략",
        "draft_title": "📝 드래프트 작성 (PRO)", "draft_desc": "🤖 Claude AI가 학술적 초안을 작성해드립니다",
        "polish_title": "✍️ 윤문/교정 (PRO)", "polish_desc": "🤖 Claude AI가 학술적 표현으로 윤문해드립니다",
        "diagnosis_title": "🔬 최종 논문 진단 (PRO)", "diagnosis_desc": "🔬 3-Engine 하이브리드: Perplexity + Gemini + Claude",
        "submit_title": "🏁 투고 전략", "submit_desc": "📈 저널 추천 + Abstract 개선",
        "references_title": "📚 APA 참고문헌", "references_desc": "📖 Perplexity 기반 최신 논문 + APA 7판 포맷",
        "file_upload": "📄 파일 업로드", "analyze_button": "🔍 분석 시작", "validate_button": "🧪 검증",
        "strategy_button": "📤 전략 생성", "search_button": "📚 참고문헌 찾기", "analyzing": "분석 중...",
        "result": "결과", "download": "💾 저장", "ask_more": "💬 연속 질문", "repolish": "🔄 다시 윤문",
        "placeholder_idea": "연구 아이디어를 입력하세요...", "placeholder_method": "방법론을 입력하세요...",
        "placeholder_abstract": "초록을 입력하세요...", "placeholder_topic": "연구 주제를 입력하세요...",
        "error_empty": "❌ 내용을 입력해주세요.", "error_limit": "❌ 무료 사용 횟수를 모두 사용했습니다!",
        "welcome": "환영합니다", "account_info": "계정 정보", "weekly_reset": "*매주 월요일 0시 리셋*",
        "security": "🔒 보안: SHA256 암호화", "invalid_cred": "❌ 아이디 또는 비밀번호가 틀렸습니다",
        "pro_only": "💎 PRO 전용 기능입니다!", "draft_topic": "연구 주제 및 개요",
        "section_select": "작성할 섹션", "polish_input": "윤문할 텍스트", "full_paper": "완성된 논문",
        "generate_draft": "📝 드래프트 생성", "start_polish": "✍️ 윤문 시작", "diagnose_button": "🔬 진단 시작"
    },
    "en": {
        "name": "English", "flag": "🇺🇸",
        "app_title": "🎯 Strategist AI Pro",
        "app_subtitle": "Academic Research Strategy | Auto PDF Analysis | APA Citation Generator",
        "login": "Login", "signup": "Sign Up", "logout": "Logout",
        "username": "Username", "password": "Password", "email": "Email",
        "password_confirm": "Confirm Password", "login_button": "Login", "signup_button": "Sign Up",
        "test_account": "🧪 View Test Account", "free_plan": "🆓 FREE Plan", "pro_plan": "💎 PRO Member",
        "remaining": "Remaining", "unlimited": "Unlimited", "upgrade": "💎 Upgrade to PRO",
        "gap_tab": "🌱 Gap-Mining", "method_tab": "⚖️ Methodology", "draft_tab": "📝 Draft",
        "polish_tab": "✍️ Polish", "diagnosis_tab": "🔬 Diagnosis", "submit_tab": "🏁 Submission",
        "references_tab": "📚 References", "storage_tab": "💾 Storage",
        "gap_title": "🌱 Gap-Mining", "gap_desc": "💡 Verify Originality + Find Gaps + Improve RQ",
        "method_title": "⚖️ Methodology Validation", "method_desc": "🛡️ Anticipate Reviewer Attacks + Defense",
        "draft_title": "📝 Draft Writing (PRO)", "draft_desc": "🤖 Claude AI writes academic drafts",
        "polish_title": "✍️ Polishing (PRO)", "polish_desc": "🤖 Claude AI polishes to academic style",
        "diagnosis_title": "🔬 Final Diagnosis (PRO)", "diagnosis_desc": "🔬 3-Engine Hybrid: Perplexity + Gemini + Claude",
        "submit_title": "🏁 Submission Strategy", "submit_desc": "📈 Journal Recommendations + Abstract Improvement",
        "references_title": "📚 APA References", "references_desc": "📖 Latest Papers via Perplexity + APA 7th",
        "file_upload": "📄 Upload File", "analyze_button": "🔍 Start Analysis", "validate_button": "🧪 Validate",
        "strategy_button": "📤 Generate Strategy", "search_button": "📚 Find References", "analyzing": "Analyzing...",
        "result": "Result", "download": "💾 Download", "ask_more": "💬 Ask More", "repolish": "🔄 Re-polish",
        "placeholder_idea": "Enter your research idea...", "placeholder_method": "Enter your methodology...",
        "placeholder_abstract": "Enter your abstract...", "placeholder_topic": "Enter research topic...",
        "error_empty": "❌ Please enter content.", "error_limit": "❌ You've used all free analyses!",
        "welcome": "Welcome", "account_info": "Account Info", "weekly_reset": "*Resets every Monday*",
        "security": "🔒 Security: SHA256 Encryption", "invalid_cred": "❌ Invalid credentials",
        "pro_only": "💎 PRO feature only!", "draft_topic": "Research Topic & Overview",
        "section_select": "Section to Write", "polish_input": "Text to Polish", "full_paper": "Full Paper",
        "generate_draft": "📝 Generate Draft", "start_polish": "✍️ Start Polishing", "diagnose_button": "🔬 Diagnose"
    }
}

def get_text(key):
    lang = st.session_state.get("language", "ko")
    return LANGUAGES.get(lang, LANGUAGES["ko"]).get(key, key)

if "language" not in st.session_state:
    st.session_state.language = "ko"

# ============================================
# 🔒 API 설정 (st.secrets 보안 방식)
# Streamlit Cloud > Settings > Secrets 에 키 입력
# ============================================
try:
    PPLX_API_KEY = st.secrets["api_keys"]["PPLX_API_KEY"]
    GEMINI_API_KEY = st.secrets["api_keys"]["GEMINI_API_KEY"]
    CLAUDE_API_KEY = st.secrets["api_keys"]["CLAUDE_API_KEY"]
except Exception:
    st.error("⚠️ API 키가 설정되지 않았습니다!")
    st.markdown("""
### 🔧 Streamlit Cloud Secrets 설정 방법
Dashboard → 앱 선택 → Settings → Secrets에 아래 내용 붙여넣기:
```toml
[api_keys]
PPLX_API_KEY = "your-perplexity-key"
GEMINI_API_KEY = "your-gemini-key"
CLAUDE_API_KEY = "your-claude-key"
```
    """)
    st.stop()

GEMINI_MODEL_NAME = "gemini-2.0-flash"
CLAUDE_MODEL_NAME = "claude-sonnet-4-5-20250929"

pplx_client = openai.OpenAI(api_key=PPLX_API_KEY, base_url="https://api.perplexity.ai")
genai.configure(api_key=GEMINI_API_KEY)
gemini_model = genai.GenerativeModel(GEMINI_MODEL_NAME)
claude_client = anthropic.Anthropic(api_key=CLAUDE_API_KEY)

# ============================================
# 보안 시스템
# ============================================
USER_DB_FILE = "users_db.json"

def secure_file_permissions():
    try:
        if os.path.exists(USER_DB_FILE):
            os.chmod(USER_DB_FILE, 0o600)
    except: pass

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(input_password, stored_hash):
    return hash_password(input_password) == stored_hash

def load_users():
    try:
        with open(USER_DB_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except: return {}

def save_users(users):
    with open(USER_DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(users, f, indent=2, ensure_ascii=False)
    secure_file_permissions()

def init_test_accounts():
    users = load_users()
    changed = False
    if "test_free" not in users:
        users["test_free"] = {
            "password": hash_password("Test1234!"),
            "email": "free@test.com",
            "tier": "free",
            "usage_count": 0,
            "week_start": datetime.now().isoformat(),
            "created_at": datetime.now().isoformat()
        }
        changed = True
    if "test_pro" not in users:
        users["test_pro"] = {
            "password": hash_password("Test1234!"),
            "email": "pro@test.com",
            "tier": "pro",
            "usage_count": 0,
            "week_start": datetime.now().isoformat(),
            "created_at": datetime.now().isoformat()
        }
        changed = True
    if changed:
        save_users(users)

init_test_accounts()

def check_week_reset(user_data):
    try:
        week_start = datetime.fromisoformat(user_data.get("week_start", datetime.now().isoformat()))
        return datetime.now() - week_start > timedelta(days=7)
    except: return True

def update_usage(username):
    users = load_users()
    if username in users:
        if check_week_reset(users[username]):
            users[username]["usage_count"] = 0
            users[username]["week_start"] = datetime.now().isoformat()
        users[username]["usage_count"] += 1
        save_users(users)
        return users[username]["usage_count"]
    return 0

def get_remaining_free_uses(username):
    users = load_users()
    if username in users:
        user = users[username]
        if check_week_reset(user): return 10
        return max(0, 10 - user.get("usage_count", 0))
    return 0

# ============================================
# 세션 상태 초기화
# ============================================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = None
if "user_tier" not in st.session_state:
    st.session_state.user_tier = "free"
if "sessions" not in st.session_state:
    st.session_state.sessions = {"gap": {}, "method": {}, "draft": {}, "polish": {}, "diagnosis": {}, "submit": {}, "references": {}}
if "chat_histories" not in st.session_state:
    st.session_state.chat_histories = {"gap": [], "method": [], "submit": [], "references": []}

# ============================================
# 언어 선택 UI
# ============================================
col_space, col_lang = st.columns([5, 1])
with col_lang:
    current_lang = st.session_state.get("language", "ko")
    selected_lang = st.selectbox(
        "🌐",
        options=list(LANGUAGES.keys()),
        format_func=lambda x: f"{LANGUAGES[x]['flag']} {LANGUAGES[x]['name']}",
        index=list(LANGUAGES.keys()).index(current_lang),
        label_visibility="collapsed"
    )
    if selected_lang != current_lang:
        st.session_state.language = selected_lang
        st.rerun()

st.markdown("---")

# ============================================
# 로그인 페이지
# ============================================
if not st.session_state.logged_in:
    st.markdown(f"<h1 style='text-align: center;'>{get_text('app_title')}</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center; color: #888;'>{get_text('app_subtitle')}</p>", unsafe_allow_html=True)
    st.markdown("---")

    col_left, col_center, col_right = st.columns([1, 2, 1])

    with col_center:
        tab_login, tab_signup = st.tabs([get_text("login"), get_text("signup")])

        with tab_login:
            st.markdown(f"### {get_text('login')}")
            with st.expander(get_text("test_account")):
                st.info("**FREE**: test_free / Test1234!\n**PRO**: test_pro / Test1234!")
            login_username = st.text_input(get_text("username"), key="login_user")
            login_password = st.text_input(get_text("password"), type="password", key="login_pass")
            if st.button(get_text("login_button"), type="primary", use_container_width=True):
                users = load_users()
                if login_username in users and verify_password(login_password, users[login_username]["password"]):
                    st.session_state.logged_in = True
                    st.session_state.username = login_username
                    st.session_state.user_tier = users[login_username].get("tier", "free")
                    st.success(f"✅ {get_text('welcome')}, {login_username}!")
                    st.balloons()
                    st.rerun()
                else:
                    st.error(get_text("invalid_cred"))

        with tab_signup:
            st.markdown(f"### {get_text('signup')}")
            signup_username = st.text_input(get_text("username"), key="signup_user")
            signup_email = st.text_input(get_text("email"), key="signup_email")
            signup_password = st.text_input(get_text("password"), type="password", key="signup_pass")
            signup_password_confirm = st.text_input(get_text("password_confirm"), type="password", key="signup_pass_confirm")
            if st.button(get_text("signup_button"), type="primary", use_container_width=True):
                users = load_users()
                if len(signup_username) < 4:
                    st.error("❌ Username must be at least 4 characters")
                elif signup_username in users:
                    st.error("❌ Username already exists")
                elif signup_password != signup_password_confirm:
                    st.error("❌ Passwords don't match")
                elif len(signup_password) < 6:
                    st.error("❌ Password must be at least 6 characters")
                else:
                    users[signup_username] = {
                        "password": hash_password(signup_password),
                        "email": signup_email,
                        "tier": "free",
                        "usage_count": 0,
                        "week_start": datetime.now().isoformat(),
                        "created_at": datetime.now().isoformat()
                    }
                    save_users(users)
                    st.success("✅ Account created successfully! Please login.")

        st.markdown("---")
        st.caption(get_text("security"))
    st.stop()

# ============================================
# 유틸리티
# ============================================
def extract_text(file):
    if not file: return ""
    try:
        if file.name.endswith('.pdf'):
            reader = PyPDF2.PdfReader(file)
            return "".join(page.extract_text() or "" for page in reader.pages)[:3000]
        if file.name.endswith('.docx'):
            doc = docx.Document(file)
            return "\n".join(p.text.strip() for p in doc.paragraphs)[:3000]
        return file.read().decode('utf-8', errors='ignore')[:3000]
    except Exception as e:
        return f"Error extracting text: {e}"

def analyze_with_ai(payload, mode):
    if not payload.strip():
        return get_text("error_empty")
    try:
        lang = st.session_state.language
        search_prompts = {
            "ko": f"학술 연구 관련 최신 정보: {payload[:500]}",
            "en": f"Latest academic research info: {payload[:500]}"
        }
        p_response = pplx_client.chat.completions.create(
            model="sonar-pro",
            messages=[{"role": "user", "content": search_prompts.get(lang, search_prompts["ko"])}]
        )
        context = p_response.choices[0].message.content
        analysis_prompts = {
            "ko": {
                "gap": f"학술 DB 검색 결과:\n{context}\n\n사용자 연구:\n{payload}\n\n다음을 분석하세요:\n1. 연구 공백 3가지\n2. 개선된 연구질문\n3. Impact Score (0-100)",
                "method": f"학술 DB 검색 결과:\n{context}\n\n방법론:\n{payload}\n\n다음을 분석하세요:\n1. 방법론 약점 3가지\n2. 방어 전략\n3. Impact Score (0-100)",
                "submit": f"학술 DB 검색 결과:\n{context}\n\n논문:\n{payload}\n\n다음을 제공하세요:\n1. 적합한 저널 3곳\n2. Abstract 개선안\n3. Impact Score (0-100)",
                "references": f"학술 DB 검색 결과:\n{context}\n\n주제: {payload}\n\nAPA 7판 형식으로 참고문헌 5-10개를 생성하세요."
            },
            "en": {
                "gap": f"Academic DB results:\n{context}\n\nUser research:\n{payload}\n\nProvide:\n1. 3 Research Gaps\n2. Improved RQ\n3. Impact Score (0-100)",
                "method": f"Academic DB results:\n{context}\n\nMethodology:\n{payload}\n\nProvide:\n1. 3 Weaknesses\n2. Defense Strategy\n3. Impact Score (0-100)",
                "submit": f"Academic DB results:\n{context}\n\nPaper:\n{payload}\n\nProvide:\n1. 3 Journal Recommendations\n2. Abstract Improvement\n3. Impact Score (0-100)",
                "references": f"Academic DB results:\n{context}\n\nTopic: {payload}\n\nGenerate 5-10 references in APA 7th format."
            }
        }
        prompt = analysis_prompts.get(lang, analysis_prompts["ko"]).get(mode, "")
        result = gemini_model.generate_content(prompt)
        return result.text
    except Exception as e:
        return f"❌ Error: {str(e)}"

def draft_with_claude(topic, section_type, lang="ko"):
    prompts = {
        "ko": {
            "intro": f"""당신은 학술 논문 작성 전문가입니다.\n\n다음 주제로 Introduction 초안을 작성하세요:\n{topic}\n\n요구사항:\n- 학술적 톤\n- 명확한 논리 구조\n- 선행연구 필요성 언급\n- 연구 필요성 제시\n- 약 500-800자\n\n출력 형식:\n## Introduction\n\n[본문]""",
            "method": f"""당신은 학술 논문 작성 전문가입니다.\n\n다음 연구에 대한 Methods 섹션 초안을 작성하세요:\n{topic}\n\n요구사항:\n- 연구 설계 명확히\n- 데이터 수집 방법\n- 분석 방법\n- 재현 가능하도록 상세히\n- 약 500-800자\n\n출력 형식:\n## Methods\n\n[본문]""",
            "discussion": f"""당신은 학술 논문 작성 전문가입니다.\n\n다음 연구에 대한 Discussion 초안을 작성하세요:\n{topic}\n\n요구사항:\n- 결과의 의미 해석\n- 선행연구와 비교\n- 한계점 제시\n- 향후 연구 제안\n- 약 500-800자\n\n출력 형식:\n## Discussion\n\n[본문]"""
        },
        "en": {
            "intro": f"""You are an academic writing expert.\n\nWrite an Introduction draft for:\n{topic}\n\nRequirements:\n- Academic tone\n- Clear logical structure\n- 500-800 words\n\nFormat:\n## Introduction\n\n[Content]""",
            "method": f"""You are an academic writing expert.\n\nWrite a Methods section draft for:\n{topic}\n\nRequirements:\n- Clear research design\n- Data collection method\n- 500-800 words\n\nFormat:\n## Methods\n\n[Content]""",
            "discussion": f"""You are an academic writing expert.\n\nWrite a Discussion draft for:\n{topic}\n\nRequirements:\n- Interpret results\n- Compare with prior research\n- 500-800 words\n\nFormat:\n## Discussion\n\n[Content]"""
        }
    }
    prompt = prompts.get(lang, prompts["ko"]).get(section_type, prompts["ko"]["intro"])
    try:
        message = claude_client.messages.create(
            model=CLAUDE_MODEL_NAME, max_tokens=2000, temperature=0.7,
            messages=[{"role": "user", "content": prompt}]
        )
        return message.content[0].text
    except Exception as e:
        return f"❌ Claude API Error: {str(e)}"

def polish_with_claude(text, lang="ko"):
    prompts = {
        "ko": f"""당신은 학술 논문 윤문 전문가입니다.\n\n다음 텍스트를 학술적이고 세련된 표현으로 개선하세요:\n\n원문:\n{text}\n\n요구사항:\n1. 문법은 유지하되 표현을 학술적으로\n2. 어색한 표현 개선\n3. 전문 용어 사용\n4. 문장 구조 개선\n5. Before/After 명확히 구분\n6. 주요 변경사항 설명\n\n출력 형식:\n## 윤문 결과\n[개선된 텍스트]\n\n## 주요 변경사항\n1. [변경]: 이유\n\n## 스타일 평가\n- 학술성: X/100\n- 명확성: X/100\n- 간결성: X/100""",
        "en": f"""You are an academic writing polishing expert.\n\nImprove the following text:\n\nOriginal:\n{text}\n\nRequirements:\n1. Academic expression\n2. Fix awkward phrasing\n3. Use technical terms\n4. Improve structure\n\nOutput:\n## Polished Result\n[Improved text]\n\n## Major Changes\n1. [Change]: Reason\n\n## Style Assessment\n- Academic: X/100\n- Clarity: X/100\n- Conciseness: X/100"""
    }
    prompt = prompts.get(lang, prompts["ko"])
    try:
        message = claude_client.messages.create(
            model=CLAUDE_MODEL_NAME, max_tokens=2500, temperature=0.3,
            messages=[{"role": "user", "content": prompt}]
        )
        return message.content[0].text
    except Exception as e:
        return f"❌ Claude API Error: {str(e)}"

def hybrid_diagnosis(paper_text, lang="ko"):
    try:
        # Phase 1: Perplexity
        pplx_prompt = {
            "ko": f"다음 논문의 주제와 관련된 최신 학술 연구 동향을 분석하세요:\n\n{paper_text[:1500]}\n\n1. 최신 연구 동향 (2023-2026)\n2. 주요 선행 연구 비교\n3. 참고문헌 적정성\n4. 핵심 논의\n5. 학술적 위치\n\n500자 이내로 요약.",
            "en": f"Analyze latest academic trends for this paper:\n\n{paper_text[:1500]}\n\n1. Latest trends (2023-2026)\n2. Prior study comparison\n3. Reference adequacy\n4. Key discussions\n5. Academic positioning\n\nSummarize within 500 words."
        }
        pplx_resp = pplx_client.chat.completions.create(
            model="sonar-pro",
            messages=[{"role": "user", "content": pplx_prompt.get(lang, pplx_prompt["ko"])}]
        )
        perplexity_analysis = pplx_resp.choices[0].message.content

        # Phase 2: Gemini
        gemini_prompt = {
            "ko": f"당신은 학술 심사위원입니다.\n\n논문:\n{paper_text[:2000]}\n\n학술 DB 분석:\n{perplexity_analysis}\n\n평가:\n## 독창성 (X/100)\n## 연구 가치 (X/100)\n## Impact 예측\n## 학술적 공백 충족도 (X/100)\n**총평 (200자)**",
            "en": f"You are an academic reviewer.\n\nPaper:\n{paper_text[:2000]}\n\nAcademic DB:\n{perplexity_analysis}\n\nEvaluate:\n## Originality (X/100)\n## Research Value (X/100)\n## Impact Prediction\n## Gap Fulfillment (X/100)\n**Overall (200 words)**"
        }
        gemini_analysis = gemini_model.generate_content(gemini_prompt.get(lang, gemini_prompt["ko"])).text

        # Phase 3: Claude
        claude_prompt = {
            "ko": f"당신은 학술 논문 편집 전문가입니다.\n\n논문:\n{paper_text[:3000]}\n\nPerplexity 분석:\n{perplexity_analysis[:500]}\n\nGemini 평가:\n{gemini_analysis[:500]}\n\n평가:\n## 논리 전개 (X/100)\n## 문장 품질 (X/100)\n## 구조/형식 (X/100)\n## 개선 우선순위 Top 3",
            "en": f"You are an academic editor.\n\nPaper:\n{paper_text[:3000]}\n\nPerplexity:\n{perplexity_analysis[:500]}\n\nGemini:\n{gemini_analysis[:500]}\n\nEvaluate:\n## Logic & Flow (X/100)\n## Writing Quality (X/100)\n## Structure (X/100)\n## Top 3 Improvements"
        }
        claude_msg = claude_client.messages.create(
            model=CLAUDE_MODEL_NAME, max_tokens=2500, temperature=0.3,
            messages=[{"role": "user", "content": claude_prompt.get(lang, claude_prompt["ko"])}]
        )
        claude_analysis = claude_msg.content[0].text

        report = {
            "ko": f"# 🔬 최종 논문 진단 보고서\n\n## 🎯 3-Engine 하이브리드 분석 결과\n\n---\n\n## 📊 Phase 1: 학술 DB 분석 (Perplexity)\n\n{perplexity_analysis}\n\n---\n\n## 💎 Phase 2: 창의성 & 가치 평가 (Gemini)\n\n{gemini_analysis}\n\n---\n\n## 🤖 Phase 3: 구조 & 문장 분석 (Claude)\n\n{claude_analysis}\n\n---\n\n## 🚨 최종 제출 전 체크리스트\n\n- [ ] 선행 연구 충분히 인용\n- [ ] 연구 공백 명확히 제시\n- [ ] 방법론 재현 가능성\n- [ ] 논리적 일관성\n- [ ] 문장 품질 확인\n- [ ] 구조적 완성도\n\n---\n\n*Powered by Perplexity + Gemini + Claude*",
            "en": f"# 🔬 Final Paper Diagnosis Report\n\n## 🎯 3-Engine Hybrid Analysis\n\n---\n\n## 📊 Phase 1: Academic DB (Perplexity)\n\n{perplexity_analysis}\n\n---\n\n## 💎 Phase 2: Creativity & Value (Gemini)\n\n{gemini_analysis}\n\n---\n\n## 🤖 Phase 3: Structure & Writing (Claude)\n\n{claude_analysis}\n\n---\n\n## 🚨 Pre-Submission Checklist\n\n- [ ] Sufficient citations\n- [ ] Clear research gap\n- [ ] Reproducible methodology\n- [ ] Logical consistency\n- [ ] Writing quality\n- [ ] Structural completeness\n\n---\n\n*Powered by Perplexity + Gemini + Claude*"
        }
        return report.get(lang, report["ko"])
    except Exception as e:
        return f"❌ Hybrid Diagnosis Error: {str(e)}"

def check_usage_limit():
    if st.session_state.user_tier == "pro":
        return True
    remaining = get_remaining_free_uses(st.session_state.username)
    if remaining <= 0:
        st.error(get_text("error_limit"))
        st.warning(f"💎 {get_text('upgrade')}")
        return False
    return True

# ============================================
# 사이드바
# ============================================
with st.sidebar:
    st.markdown(f"## {get_text('app_title')}")
    st.success(f"👤 **{st.session_state.username}**")
    if st.session_state.user_tier == "free":
        remaining = get_remaining_free_uses(st.session_state.username)
        st.warning(get_text("free_plan"))
        st.progress(remaining / 10)
        st.caption(f"{get_text('remaining')}: **{remaining}/10**")
        st.caption(get_text("weekly_reset"))
        if st.button(get_text("upgrade"), use_container_width=True):
            st.info("💎 PRO upgrade coming soon!")
    else:
        st.success(get_text("pro_plan"))
        st.caption(f"✅ {get_text('unlimited')}")
    st.divider()
    if st.button(get_text("logout"), use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.session_state.user_tier = "free"
        st.rerun()
    st.divider()
    st.caption(get_text("security"))
    st.divider()
    st.caption("🔧 Engine Status")
    st.caption("✅ Perplexity: sonar-pro")
    st.caption(f"✅ Gemini: {GEMINI_MODEL_NAME}")
    st.caption(f"✅ Claude: {CLAUDE_MODEL_NAME}")

# ============================================
# 메인 앱
# ============================================
st.title(get_text("app_title"))
st.markdown(get_text("app_subtitle"))
st.markdown("---")

tabs = st.tabs([
    get_text("gap_tab"), get_text("method_tab"), get_text("draft_tab"),
    get_text("polish_tab"), get_text("diagnosis_tab"), get_text("submit_tab"),
    get_text("references_tab"), get_text("storage_tab")
])

# GAP 탭
with tabs[0]:
    st.header(get_text("gap_title"))
    st.info(get_text("gap_desc"))
    col1, col2 = st.columns([1, 3])
    file_gap = col1.file_uploader(get_text("file_upload"), type=['pdf','docx','txt'], key="f1")
    text_gap = col2.text_area("💡", height=150, placeholder=get_text("placeholder_idea"), key="t1")
    if st.button(get_text("analyze_button"), type="primary", use_container_width=True):
        if not check_usage_limit(): st.stop()
        payload = extract_text(file_gap) or text_gap
        if payload.strip():
            with st.spinner(get_text("analyzing")):
                result = analyze_with_ai(payload, "gap")
                st.session_state.sessions["gap"] = {"result": result, "timestamp": datetime.now().isoformat()}
                update_usage(st.session_state.username)
                st.rerun()
        else: st.error(get_text("error_empty"))
    gap_data = st.session_state.sessions.get("gap")
    if gap_data:
        st.markdown(f"### 📊 {get_text('result')}")
        st.markdown(gap_data['result'])
        st.download_button(get_text("download"), gap_data['result'], "gap_analysis.txt")
        follow_q = st.chat_input(get_text("ask_more"))
        if follow_q:
            with st.chat_message("user"): st.write(follow_q)
            with st.spinner("..."):
                answer = gemini_model.generate_content(f"{gap_data['result']}\n\n{follow_q}").text
            with st.chat_message("assistant"): st.markdown(answer)

# 방법론 탭
with tabs[1]:
    st.header(get_text("method_title"))
    st.info(get_text("method_desc"))
    col1, col2 = st.columns([1, 3])
    file_method = col1.file_uploader(get_text("file_upload"), type=['pdf','docx','txt'], key="f2")
    text_method = col2.text_area("📊", height=150, placeholder=get_text("placeholder_method"), key="t2")
    if st.button(get_text("validate_button"), type="primary", use_container_width=True):
        if not check_usage_limit(): st.stop()
        payload = extract_text(file_method) or text_method
        if payload.strip():
            with st.spinner(get_text("analyzing")):
                result = analyze_with_ai(payload, "method")
                st.session_state.sessions["method"] = {"result": result}
                update_usage(st.session_state.username)
                st.rerun()
        else: st.error(get_text("error_empty"))
    method_data = st.session_state.sessions.get("method")
    if method_data:
        st.markdown(f"### 📊 {get_text('result')}")
        st.markdown(method_data['result'])
        st.download_button(get_text("download"), method_data['result'], "method_validation.txt")

# 드래프트 탭
with tabs[2]:
    st.header(get_text("draft_title"))
    if st.session_state.user_tier != "pro":
        st.warning(get_text("pro_only"))
        if st.button(get_text("upgrade"), use_container_width=True, key="draft_upgrade"):
            st.info("💎 PRO upgrade coming soon!")
        st.stop()
    st.info(get_text("draft_desc"))
    draft_topic = st.text_area(get_text("draft_topic"), height=150, placeholder=get_text("placeholder_idea"), key="draft_input")
    col1, col2 = st.columns(2)
    with col1:
        section_type = st.selectbox(get_text("section_select"), ["intro", "method", "discussion"],
            format_func=lambda x: {"intro": "Introduction", "method": "Methods", "discussion": "Discussion"}[x])
    with col2:
        draft_lang = st.selectbox("Language", ["ko", "en"], format_func=lambda x: "한국어" if x == "ko" else "English")
    if st.button(get_text("generate_draft"), type="primary", use_container_width=True):
        if not check_usage_limit(): st.stop()
        if draft_topic.strip():
            with st.spinner(get_text("analyzing")):
                result = draft_with_claude(draft_topic, section_type, draft_lang)
                st.session_state.sessions["draft"] = {"result": result}
                update_usage(st.session_state.username)
                st.rerun()
        else: st.error(get_text("error_empty"))
    draft_data = st.session_state.sessions.get("draft")
    if draft_data:
        st.markdown(f"### 📄 {get_text('result')}")
        st.markdown(draft_data['result'])
        st.download_button(get_text("download"), draft_data['result'], "draft.txt")

# 윤문 탭
with tabs[3]:
    st.header(get_text("polish_title"))
    if st.session_state.user_tier != "pro":
        st.warning(get_text("pro_only"))
        if st.button(get_text("upgrade"), use_container_width=True, key="polish_upgrade"):
            st.info("💎 PRO upgrade coming soon!")
        st.stop()
    st.info(get_text("polish_desc"))
    polish_text = st.text_area(get_text("polish_input"), height=200, placeholder="학술적으로 다듬을 텍스트...", key="polish_input_text")
    polish_lang = st.selectbox("Language", ["ko", "en"], format_func=lambda x: "한국어 윤문" if x == "ko" else "English Polishing", key="polish_lang")
    if st.button(get_text("start_polish"), type="primary", use_container_width=True):
        if not check_usage_limit(): st.stop()
        if polish_text.strip():
            with st.spinner(get_text("analyzing")):
                result = polish_with_claude(polish_text, polish_lang)
                st.session_state.sessions["polish"] = {"result": result}
                update_usage(st.session_state.username)
                st.rerun()
        else: st.error(get_text("error_empty"))
    polish_data = st.session_state.sessions.get("polish")
    if polish_data:
        st.markdown(f"### ✨ {get_text('result')}")
        st.markdown(polish_data['result'])
        col1, col2 = st.columns(2)
        with col1: st.download_button(get_text("download"), polish_data['result'], "polished.txt")
        with col2:
            if st.button(get_text("repolish")):
                st.session_state.sessions["polish"] = {}
                st.rerun()

# 최종 진단 탭
with tabs[4]:
    st.header(get_text("diagnosis_title"))
    if st.session_state.user_tier != "pro":
        st.warning(get_text("pro_only"))
        if st.button(get_text("upgrade"), use_container_width=True, key="diagnosis_upgrade"):
            st.info("💎 PRO upgrade coming soon!")
        st.stop()
    st.info(get_text("diagnosis_desc"))
    with st.expander("📖 3단계 하이브리드 분석 프로세스"):
        st.markdown(f"""
### 🔍 Phase 1: Perplexity (sonar-pro)
최신 연구 동향 · 참고문헌 검증 · 학계 논의 분석

### 💎 Phase 2: Gemini ({GEMINI_MODEL_NAME})
독창성 평가 · 연구 가치 · Impact 예측

### 🤖 Phase 3: Claude ({CLAUDE_MODEL_NAME})
논리 전개 · 문장 품질 · 구조 완성도

→ **최종 통합 리포트 생성**
        """)
    col1, col2 = st.columns([1, 3])
    file_diagnosis = col1.file_uploader(get_text("file_upload"), type=['pdf','docx','txt'], key="diagnosis_file")
    text_diagnosis = col2.text_area(get_text("full_paper"), height=250, placeholder="완성된 논문 전체를 입력하세요...", key="diagnosis_input")
    diagnosis_lang = st.selectbox("Language", ["ko", "en"], format_func=lambda x: "한국어" if x == "ko" else "English", key="diagnosis_lang")
    if st.button("🔬 3-Engine 하이브리드 진단 시작", type="primary", use_container_width=True):
        if not check_usage_limit(): st.stop()
        payload = extract_text(file_diagnosis) or text_diagnosis
        if payload.strip():
            progress_bar = st.progress(0)
            status = st.empty()
            status.info("🔍 Phase 1/3: Perplexity 학술 DB 검색 중...")
            progress_bar.progress(10)
            with st.spinner("3-Engine 분석 중..."):
                result = hybrid_diagnosis(payload, diagnosis_lang)
                status.success("✅ 3-Engine 하이브리드 진단 완료!")
                progress_bar.progress(100)
                st.session_state.sessions["diagnosis"] = {"result": result}
                update_usage(st.session_state.username)
                st.rerun()
        else: st.error(get_text("error_empty"))
    diagnosis_data = st.session_state.sessions.get("diagnosis")
    if diagnosis_data:
        st.markdown("### 📋 3-Engine 하이브리드 진단 결과")
        st.markdown(diagnosis_data['result'])
        col1, col2, col3 = st.columns(3)
        with col1: st.download_button("💾 리포트 저장", diagnosis_data['result'], "hybrid_diagnosis_report.txt")
        with col2: st.download_button("📧 이메일용", diagnosis_data['result'], "diagnosis_email.txt")
        with col3:
            if st.button("🔄 재진단"):
                st.session_state.sessions["diagnosis"] = {}
                st.rerun()

# 투고 탭
with tabs[5]:
    st.header(get_text("submit_title"))
    st.info(get_text("submit_desc"))
    col1, col2 = st.columns([1, 3])
    file_submit = col1.file_uploader(get_text("file_upload"), type=['pdf','docx','txt'], key="f3")
    text_submit = col2.text_area("✍️", height=150, placeholder=get_text("placeholder_abstract"), key="t3")
    if st.button(get_text("strategy_button"), type="primary", use_container_width=True):
        if not check_usage_limit(): st.stop()
        payload = extract_text(file_submit) or text_submit
        if payload.strip():
            with st.spinner(get_text("analyzing")):
                result = analyze_with_ai(payload, "submit")
                st.session_state.sessions["submit"] = {"result": result}
                update_usage(st.session_state.username)
                st.rerun()
        else: st.error(get_text("error_empty"))
    submit_data = st.session_state.sessions.get("submit")
    if submit_data:
        st.markdown(f"### 📊 {get_text('result')}")
        st.markdown(submit_data['result'])
        st.download_button(get_text("download"), submit_data['result'], "submission_strategy.txt")

# 참고문헌 탭
with tabs[6]:
    st.header(get_text("references_title"))
    st.info(get_text("references_desc"))
    ref_topic = st.text_input("🔍", placeholder=get_text("placeholder_topic"))
    if st.button(get_text("search_button"), type="primary", use_container_width=True):
        if not check_usage_limit(): st.stop()
        if ref_topic.strip():
            with st.spinner(get_text("analyzing")):
                result = analyze_with_ai(ref_topic, "references")
                st.session_state.sessions["references"] = {"result": result}
                update_usage(st.session_state.username)
                st.rerun()
        else: st.error(get_text("error_empty"))
    ref_data = st.session_state.sessions.get("references")
    if ref_data:
        st.markdown(f"### 📚 {get_text('result')}")
        st.markdown(ref_data['result'])
        st.download_button(get_text("download"), ref_data['result'], "references.txt")

# 저장소 탭
with tabs[7]:
    st.header(f"💾 {get_text('storage_tab')}")
    has_data = False
    for name in ["gap", "method", "draft", "polish", "diagnosis", "submit", "references"]:
        data = st.session_state.sessions.get(name)
        if data and data.get("result"):
            has_data = True
            with st.expander(f"📂 {name.upper()}"):
                st.text_area(get_text("result"),
                    data["result"][:500] + "..." if len(data["result"]) > 500 else data["result"],
                    height=150, disabled=True, key=f"storage_{name}")
    if not has_data:
        st.info("No saved sessions yet. Start analyzing!")
    else:
        backup_json = json.dumps(st.session_state.sessions, ensure_ascii=False, indent=2)
        st.download_button(f"💾 {get_text('download')} All (JSON)", backup_json, "strategist_backup.json", use_container_width=True)

st.markdown("---")
st.caption(f"*{get_text('app_title')} | 2026 | Powered by Perplexity + Gemini + Claude*")
st.caption(f"✅ Engine: sonar-pro + {GEMINI_MODEL_NAME} + {CLAUDE_MODEL_NAME}")
