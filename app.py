import streamlit as st
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
        "app_subtitle": "학술 연구 전략 컨설팅 | 3-Engine 하이브리드 | APA 자동생성",
        "login": "로그인", "signup": "회원가입", "logout": "로그아웃",
        "username": "아이디", "password": "비밀번호", "email": "이메일",
        "password_confirm": "비밀번호 확인", "login_button": "로그인", "signup_button": "회원가입",
        "test_account": "🧪 테스트 계정 보기", "free_plan": "🆓 FREE 플랜", "pro_plan": "💎 PRO 회원",
        "remaining": "남은 횟수", "unlimited": "무제한", "upgrade": "💎 PRO 업그레이드",
        # 탭 이름
        "contemplate_tab": "🧠 사유의 방", "master_tab": "🎓 거장과의 대화",
        "gap_tab": "🌱 Gap-Mining", "method_tab": "⚖️ 방법론", "draft_tab": "📝 드래프트",
        "polish_tab": "✍️ 윤문", "diagnosis_tab": "🔬 최종 진단", "submit_tab": "🏁 투고",
        "references_tab": "📚 참고문헌", "storage_tab": "💾 저장소",
        # 사유의 방
        "contemplate_title": "🧠 사유의 방",
        "contemplate_desc": "💭 비정형적 공상 → 실증적 연구 설계 전환 | Gemini Bridge Logic",
        "contemplate_input": "자유롭게 떠오르는 생각, 사회 이슈, 공상을 입력하세요",
        "contemplate_placeholder": "예: 요즘 카페에서 노트북 하는 사람이 많아졌는데, 이게 생산성에 영향을 줄까?\n예: SNS에서 본 뉴스만 보는 사람들이 점점 극단적이 되는 것 같다\n예: AI가 그림을 그리면 그건 예술일까?",
        "contemplate_button": "🧠 연구 설계로 전환",
        "contemplate_depth": "사유 깊이",
        "depth_spark": "🔥 스파크 (빠른 변환)",
        "depth_explore": "🔭 탐색 (변수 확장)",
        "depth_architect": "🏗️ 설계 (완전 프레임워크)",
        # 거장과의 대화
        "master_title": "🎓 거장과의 대화",
        "master_desc": "📖 거장의 인식론으로 당신의 연구 문제를 재해석 | Perplexity 실시간 검증",
        "master_input": "거장에게 질문할 연구 문제를 입력하세요",
        "master_placeholder": "예: 디지털 플랫폼이 노동시장 불평등을 심화시키는가?\n예: 양자컴퓨팅이 암호체계에 미치는 영향은?\n예: 생성AI 시대의 저작권은 어떻게 재정의되어야 하는가?",
        "master_button": "🎓 거장에게 질문",
        "master_select": "거장 선택",
        "master_category": "분야",
        "cat_social": "🏛️ 사회과학",
        "cat_engineer": "⚙️ 공학·자연과학",
        "cat_art": "🎨 예술·인문학",
        # 기존 기능
        "gap_title": "🌱 Gap-Mining", "gap_desc": "연구 독창성 검증 + 공백 발견 + 연구질문 개선",
        "method_title": "⚖️ 방법론 검증", "method_desc": "심사위원 공격 예상 + 방어 전략",
        "draft_title": "📝 드래프트 작성 (PRO)", "draft_desc": "Claude AI 학술적 초안 작성",
        "polish_title": "✍️ 윤문/교정 (PRO)", "polish_desc": "Claude AI 학술적 표현 윤문",
        "diagnosis_title": "🔬 최종 논문 진단 (PRO)", "diagnosis_desc": "3-Engine 하이브리드: Perplexity + Gemini + Claude",
        "submit_title": "🏁 투고 전략", "submit_desc": "저널 추천 + Abstract 개선",
        "references_title": "📚 APA 참고문헌", "references_desc": "Perplexity 기반 최신 논문 + APA 7판",
        # 공통
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
        "app_subtitle": "Academic Research Strategy | 3-Engine Hybrid | APA Generator",
        "login": "Login", "signup": "Sign Up", "logout": "Logout",
        "username": "Username", "password": "Password", "email": "Email",
        "password_confirm": "Confirm Password", "login_button": "Login", "signup_button": "Sign Up",
        "test_account": "🧪 View Test Account", "free_plan": "🆓 FREE Plan", "pro_plan": "💎 PRO Member",
        "remaining": "Remaining", "unlimited": "Unlimited", "upgrade": "💎 Upgrade to PRO",
        "contemplate_tab": "🧠 Contemplation", "master_tab": "🎓 Master Dialogue",
        "gap_tab": "🌱 Gap-Mining", "method_tab": "⚖️ Methodology", "draft_tab": "📝 Draft",
        "polish_tab": "✍️ Polish", "diagnosis_tab": "🔬 Diagnosis", "submit_tab": "🏁 Submission",
        "references_tab": "📚 References", "storage_tab": "💾 Storage",
        "contemplate_title": "🧠 Contemplation Room",
        "contemplate_desc": "💭 Raw ideas → Empirical research design | Gemini Bridge Logic",
        "contemplate_input": "Enter your raw thoughts, social issues, or daydreams",
        "contemplate_placeholder": "e.g., More people work at cafes now—does ambient noise boost productivity?\ne.g., People only read news that confirms their views—echo chambers?\ne.g., If AI paints, is it art?",
        "contemplate_button": "🧠 Transform to Research Design",
        "contemplate_depth": "Depth Level",
        "depth_spark": "🔥 Spark (Quick)",
        "depth_explore": "🔭 Explore (Variable Expansion)",
        "depth_architect": "🏗️ Architect (Full Framework)",
        "master_title": "🎓 Master Dialogue",
        "master_desc": "📖 Reinterpret your research through a master's epistemology | Perplexity-verified",
        "master_input": "Enter a research question for the master",
        "master_placeholder": "e.g., Do digital platforms deepen labor inequality?\ne.g., How will quantum computing affect cryptography?\ne.g., How should copyright be redefined in the generative AI era?",
        "master_button": "🎓 Ask the Master",
        "master_select": "Select Master",
        "master_category": "Field",
        "cat_social": "🏛️ Social Science",
        "cat_engineer": "⚙️ Engineering & Science",
        "cat_art": "🎨 Arts & Humanities",
        "gap_title": "🌱 Gap-Mining", "gap_desc": "Verify Originality + Find Gaps + Improve RQ",
        "method_title": "⚖️ Methodology Validation", "method_desc": "Anticipate Reviewer Attacks + Defense",
        "draft_title": "📝 Draft Writing (PRO)", "draft_desc": "Claude AI writes academic drafts",
        "polish_title": "✍️ Polishing (PRO)", "polish_desc": "Claude AI polishes to academic style",
        "diagnosis_title": "🔬 Final Diagnosis (PRO)", "diagnosis_desc": "3-Engine Hybrid: Perplexity + Gemini + Claude",
        "submit_title": "🏁 Submission Strategy", "submit_desc": "Journal Recommendations + Abstract",
        "references_title": "📚 APA References", "references_desc": "Latest Papers via Perplexity + APA 7th",
        "file_upload": "📄 Upload File", "analyze_button": "🔍 Analyze", "validate_button": "🧪 Validate",
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

def T(key):
    lang = st.session_state.get("language", "ko")
    return LANGUAGES.get(lang, LANGUAGES["ko"]).get(key, key)

if "language" not in st.session_state:
    st.session_state.language = "ko"

# ============================================
# 🔒 API (st.secrets)
# ============================================
try:
    PPLX_API_KEY = st.secrets["api_keys"]["PPLX_API_KEY"]
    GEMINI_API_KEY = st.secrets["api_keys"]["GEMINI_API_KEY"]
    CLAUDE_API_KEY = st.secrets["api_keys"]["CLAUDE_API_KEY"]
except Exception:
    st.error("⚠️ API 키가 설정되지 않았습니다!")
    st.markdown("""
### Streamlit Cloud → Settings → Secrets
```toml
[api_keys]
PPLX_API_KEY = "pplx-..."
GEMINI_API_KEY = "AIzaSy..."
CLAUDE_API_KEY = "sk-ant-api03-..."
```
    """)
    st.stop()

GEMINI_MODEL = "gemini-2.0-flash"
CLAUDE_MODEL = "claude-sonnet-4-5-20250929"

pplx = openai.OpenAI(api_key=PPLX_API_KEY, base_url="https://api.perplexity.ai")
genai.configure(api_key=GEMINI_API_KEY)
gemini = genai.GenerativeModel(GEMINI_MODEL)
claude = anthropic.Anthropic(api_key=CLAUDE_API_KEY)

# ============================================
# 거장 데이터베이스
# ============================================
MASTERS = {
    "social": {
        "Foucault": {"name_ko": "미셸 푸코", "frame": "power-knowledge nexus, discourse analysis, genealogy of institutions",
                     "lens": "Analyze how power structures and institutional discourses shape the phenomenon. Identify whose knowledge is privileged and what is marginalized."},
        "Bourdieu": {"name_ko": "피에르 부르디외", "frame": "habitus, cultural capital, field theory, symbolic violence",
                     "lens": "Examine the role of cultural capital, habitus reproduction, and field dynamics. Identify symbolic violence mechanisms."},
        "Weber": {"name_ko": "막스 베버", "frame": "ideal types, rationalization, verstehen, bureaucracy, legitimacy",
                  "lens": "Construct ideal types for comparison. Analyze rationalization processes and legitimacy structures through interpretive understanding."},
        "Habermas": {"name_ko": "위르겐 하버마스", "frame": "communicative action, public sphere, lifeworld vs system",
                     "lens": "Evaluate communicative rationality vs strategic action. Assess public sphere conditions and system colonization of lifeworld."},
        "Giddens": {"name_ko": "앤서니 기든스", "frame": "structuration theory, duality of structure, reflexive modernity",
                    "lens": "Apply the duality of structure—how agents reproduce and transform structures through practice. Examine reflexive modernization."}
    },
    "engineer": {
        "Einstein": {"name_ko": "알베르트 아인슈타인", "frame": "thought experiments, relativity of reference frames, invariance principles",
                     "lens": "Strip the problem to its invariant core. Design thought experiments that isolate variables. Seek the simplest formulation that preserves all observable constraints."},
        "Feynman": {"name_ko": "리처드 파인만", "frame": "first-principles reasoning, path integrals, simplification through analogy",
                    "lens": "Decompose to first principles. If you cannot explain it simply, it is not understood. Map the problem space using multiple representational frames."},
        "Turing": {"name_ko": "앨런 튜링", "frame": "computability, formal systems, machine intelligence, halting problem",
                   "lens": "Define the problem as a formal system. Identify what is computable vs undecidable. Design the minimal machine that solves the stated task."},
        "Shannon": {"name_ko": "클로드 섀넌", "frame": "information theory, entropy, channel capacity, signal vs noise",
                    "lens": "Quantify information content and noise. Identify channel constraints. Optimize signal transmission within theoretical bounds."},
        "Curie": {"name_ko": "마리 퀴리", "frame": "empirical rigor, measurement precision, systematic experimentation",
                  "lens": "Design experiments with maximum measurement precision. Control for confounds systematically. Let data speak before theory."}
    },
    "art": {
        "Bach": {"name_ko": "요한 세바스찬 바흐", "frame": "counterpoint, fugal structure, mathematical harmony, thematic transformation",
                 "lens": "Identify the core theme and develop it through systematic variation. Layer multiple independent voices that create emergent harmony."},
        "DaVinci": {"name_ko": "레오나르도 다 빈치", "frame": "interdisciplinary synthesis, observation-based design, sfumato thinking",
                    "lens": "Cross-pollinate between domains. Begin with meticulous observation. Embrace ambiguity (sfumato) as a generative force rather than a problem."},
        "Wittgenstein": {"name_ko": "루트비히 비트겐슈타인", "frame": "language games, family resemblance, limits of language, showing vs saying",
                         "lens": "Examine the language game in which the problem exists. Identify what can be said clearly and what can only be shown. Map family resemblances."},
        "Arendt": {"name_ko": "한나 아렌트", "frame": "vita activa, banality of evil, public space, natality, plurality",
                   "lens": "Distinguish labor/work/action. Examine how plurality is maintained or destroyed. Assess whether the phenomenon creates or forecloses public space."},
        "Barthes": {"name_ko": "롤랑 바르트", "frame": "mythology, death of the author, readerly vs writerly texts, punctum/studium",
                    "lens": "Decode the mythology embedded in the phenomenon. Identify what punctum disrupts the studium. Analyze the gap between authorial intent and reader production."}
    }
}

# ============================================
# Protocol-Task-Constraint 프롬프트 빌더
# ============================================
def build_prompt(protocol, task, constraint, payload, context=""):
    """고밀도 명령어 구조: Protocol → Task → Constraint"""
    parts = [
        f"[PROTOCOL] {protocol}",
        f"[CONTEXT] {context}" if context else "",
        f"[INPUT] {payload}",
        f"[TASK] {task}",
        f"[CONSTRAINT] {constraint}"
    ]
    return "\n\n".join(p for p in parts if p)


# ============================================
# 사유의 방 (Gemini)
# ============================================
def contemplate(raw_idea, depth="explore", lang="ko"):
    depth_configs = {
        "spark": {
            "task": "Extract 2 testable variables and 1 research question from this raw idea. Output: Variables → Hypothesis → RQ.",
            "constraint": "Max 300 tokens. No preamble. Direct output only."
        },
        "explore": {
            "task": "Transform this raw idea into empirical research design: (1) Extract IV/DV/Moderator/Mediator, (2) Map to theoretical framework, (3) Generate 3 hypotheses ranked by testability, (4) Suggest methodology.",
            "constraint": "Max 800 tokens. Use structured headers. Cite framework names without explanation."
        },
        "architect": {
            "task": "Full research architecture: (1) Conceptual model with all variable relationships, (2) Theoretical grounding with 2+ frameworks, (3) 3 hypotheses with operational definitions, (4) Mixed-methods design with sampling strategy, (5) Expected contribution to field, (6) Potential limitations and mitigation.",
            "constraint": "Max 1500 tokens. Publication-ready structure. Include visual model description in text form."
        }
    }
    cfg = depth_configs.get(depth, depth_configs["explore"])

    if lang == "ko":
        protocol = "학술 연구 설계 전환 엔진. 비정형 사고를 실증 가능한 연구 프레임워크로 변환한다."
        constraint_suffix = " 한국어로 출력. 학술 용어는 영문 병기."
    else:
        protocol = "Academic research design transformation engine. Convert unstructured ideation into testable research frameworks."
        constraint_suffix = " Output in English."

    prompt = build_prompt(
        protocol=protocol,
        task=cfg["task"],
        constraint=cfg["constraint"] + constraint_suffix,
        payload=raw_idea
    )
    try:
        result = gemini.generate_content(prompt)
        return result.text
    except Exception as e:
        return f"❌ Gemini Error: {str(e)}"


# ============================================
# 거장과의 대화 (Perplexity)
# ============================================
def master_dialogue(question, master_key, category, lang="ko"):
    master = MASTERS[category][master_key]
    master_name = master["name_ko"] if lang == "ko" else master_key

    if lang == "ko":
        protocol = f"인식론 시뮬레이션 엔진. {master_name}의 학문적 사고 체계를 복제하여 연구 문제에 적용한다."
        task = f"""이 연구 문제를 {master_name}의 인식론으로 재해석하라:
(1) {master_name}의 핵심 프레임워크({master['frame']}) 적용
(2) 이 관점에서 도출되는 연구질문 재구성
(3) 방법론적 함의
(4) 이 관점의 한계와 보완점
(5) 최신 학술 동향에서 이 프레임워크의 현재 적용 사례"""
        constraint = "최신 학술 논문 기반으로 실증적 근거 포함. 한국어 출력. 핵심 개념은 원어 병기. Max 1200 tokens."
    else:
        protocol = f"Epistemology simulation engine. Replicate {master_key}'s intellectual framework and apply to research problem."
        task = f"""Reinterpret this research problem through {master_key}'s epistemology:
(1) Apply core framework: {master['frame']}
(2) Reconstructed research question from this lens
(3) Methodological implications
(4) Limitations of this perspective and complementary approaches
(5) Current academic applications of this framework with recent citations"""
        constraint = "Include empirical evidence from recent academic literature. English output. Max 1200 tokens."

    lens_instruction = f"[EPISTEMOLOGICAL LENS] {master['lens']}"

    prompt = build_prompt(
        protocol=protocol,
        task=task,
        constraint=constraint,
        payload=question,
        context=lens_instruction
    )
    try:
        response = pplx.chat.completions.create(
            model="sonar-pro",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ Perplexity Error: {str(e)}"


# ============================================
# 고도화된 기존 기능 (Protocol-Task-Constraint)
# ============================================
def analyze_with_ai(payload, mode):
    if not payload.strip():
        return T("error_empty")
    lang = st.session_state.language
    try:
        # Phase 1: Perplexity 학술 검색
        search_q = f"Recent academic research: {payload[:500]}" if lang == "en" else f"학술 연구 최신 동향: {payload[:500]}"
        p_resp = pplx.chat.completions.create(
            model="sonar-pro",
            messages=[{"role": "user", "content": search_q}]
        )
        context = p_resp.choices[0].message.content

        # Phase 2: Gemini 분석 (Protocol-Task-Constraint)
        prompts = {
            "gap": {
                "protocol": "Research gap identification engine." if lang == "en" else "연구 공백 식별 엔진.",
                "task": "Identify: (1) 3 specific research gaps with evidence, (2) Improved research question addressing largest gap, (3) Impact Score 0-100 with justification." if lang == "en" else "식별: (1) 근거 기반 연구 공백 3개, (2) 최대 공백 해소 연구질문, (3) Impact Score 0-100 근거 포함.",
                "constraint": f"Base analysis on: {context[:1000]}. {'English output.' if lang == 'en' else '한국어 출력.'} Max 800 tokens."
            },
            "method": {
                "protocol": "Methodology stress-test engine." if lang == "en" else "방법론 스트레스 테스트 엔진.",
                "task": "Execute: (1) 3 methodological vulnerabilities ranked by severity, (2) Reviewer attack vectors per vulnerability, (3) Defense strategy per attack, (4) Robustness Score 0-100." if lang == "en" else "실행: (1) 심각도순 방법론 취약점 3개, (2) 취약점별 심사위원 공격 벡터, (3) 공격별 방어 전략, (4) 견고성 점수 0-100.",
                "constraint": f"Base analysis on: {context[:1000]}. {'English output.' if lang == 'en' else '한국어 출력.'} Max 800 tokens."
            },
            "submit": {
                "protocol": "Journal-fit optimization engine." if lang == "en" else "저널 적합성 최적화 엔진.",
                "task": "Deliver: (1) 3 target journals with fit-score, scope match rationale, recent similar publications, (2) Abstract rewrite optimized for top journal, (3) Submission timing recommendation." if lang == "en" else "제공: (1) 적합도 점수 포함 타겟 저널 3곳 + 유사 게재논문, (2) 1순위 저널 최적화 Abstract 재작성, (3) 투고 타이밍 권고.",
                "constraint": f"Base analysis on: {context[:1000]}. {'English output.' if lang == 'en' else '한국어 출력.'} Max 800 tokens."
            },
            "references": {
                "protocol": "APA 7th citation generator with verification." if lang == "en" else "APA 7판 참고문헌 생성 엔진.",
                "task": "Generate 5-10 references: (1) APA 7th format strictly, (2) Relevance score per reference, (3) Categorize as foundational/methodological/recent." if lang == "en" else "5-10개 참고문헌 생성: (1) APA 7판 엄격 준수, (2) 관련성 점수, (3) 기초/방법론/최신으로 분류.",
                "constraint": f"Base analysis on: {context[:1000]}. {'English output.' if lang == 'en' else '한국어 출력.'} Max 1000 tokens."
            }
        }
        cfg = prompts.get(mode, prompts["gap"])
        prompt = build_prompt(
            protocol=cfg["protocol"],
            task=cfg["task"],
            constraint=cfg["constraint"],
            payload=payload
        )
        result = gemini.generate_content(prompt)
        return result.text
    except Exception as e:
        return f"❌ Error: {str(e)}"


def draft_with_claude(topic, section_type, lang="ko"):
    section_tasks = {
        "intro": "Write Introduction: (1) Research context with field positioning, (2) Gap identification from literature, (3) Purpose statement, (4) Significance, (5) RQ/Hypotheses.",
        "method": "Write Methods: (1) Research design with justification, (2) Participants/sampling with power analysis rationale, (3) Instruments with validity evidence, (4) Procedure, (5) Analysis plan.",
        "discussion": "Write Discussion: (1) Key findings interpretation, (2) Theoretical implications with framework integration, (3) Practical implications, (4) Limitations with mitigation, (5) Future research agenda."
    }
    task = section_tasks.get(section_type, section_tasks["intro"])
    lang_c = "한국어 출력. 학술 용어 영문 병기." if lang == "ko" else "English output."

    prompt = build_prompt(
        protocol="Academic manuscript drafting engine. Publication-ready quality.",
        task=task,
        constraint=f"500-800 words. Formal academic register. {lang_c}",
        payload=topic
    )
    try:
        msg = claude.messages.create(
            model=CLAUDE_MODEL, max_tokens=2000, temperature=0.7,
            messages=[{"role": "user", "content": prompt}]
        )
        return msg.content[0].text
    except Exception as e:
        return f"❌ Claude Error: {str(e)}"


def polish_with_claude(text, lang="ko"):
    lang_c = "한국어 출력." if lang == "ko" else "English output."
    prompt = build_prompt(
        protocol="Academic prose refinement engine.",
        task="Refine: (1) Elevate register to publication standard, (2) Tighten syntax and eliminate redundancy, (3) Insert precise terminology, (4) Output Before/After comparison, (5) Score: Academic Rigor / Clarity / Conciseness each 0-100.",
        constraint=f"Preserve original argument structure. {lang_c} Max 1200 tokens.",
        payload=text
    )
    try:
        msg = claude.messages.create(
            model=CLAUDE_MODEL, max_tokens=2500, temperature=0.3,
            messages=[{"role": "user", "content": prompt}]
        )
        return msg.content[0].text
    except Exception as e:
        return f"❌ Claude Error: {str(e)}"


def hybrid_diagnosis(paper_text, lang="ko"):
    lang_c = "한국어 출력." if lang == "ko" else "English output."
    try:
        # Phase 1: Perplexity
        p1_prompt = build_prompt(
            protocol="Academic literature positioning engine.",
            task="Analyze: (1) Current field trajectory 2023-2026, (2) Key competing/complementary works, (3) Reference adequacy assessment, (4) Gap this paper addresses, (5) Positioning within field.",
            constraint=f"Max 500 tokens. {lang_c}",
            payload=paper_text[:1500]
        )
        p1 = pplx.chat.completions.create(model="sonar-pro", messages=[{"role": "user", "content": p1_prompt}])
        perplexity_out = p1.choices[0].message.content

        # Phase 2: Gemini
        p2_prompt = build_prompt(
            protocol="Research value assessment engine.",
            task="Evaluate: (1) Originality X/100 with evidence, (2) Theoretical + Practical contribution, (3) Impact prediction (citation potential, field influence), (4) Gap fulfillment X/100.",
            constraint=f"Max 600 tokens. {lang_c}",
            payload=paper_text[:2000],
            context=f"[LITERATURE ANALYSIS] {perplexity_out}"
        )
        gemini_out = gemini.generate_content(p2_prompt).text

        # Phase 3: Claude
        p3_prompt = build_prompt(
            protocol="Manuscript quality audit engine.",
            task="Audit: (1) Logic & Flow X/100 with specific weak points, (2) Writing Quality X/100, (3) Structure completeness per IMRAD section, (4) Top 3 revision priorities with concrete action items.",
            constraint=f"Max 800 tokens. {lang_c}",
            payload=paper_text[:3000],
            context=f"[LITERATURE] {perplexity_out[:500]}\n[VALUE] {gemini_out[:500]}"
        )
        c_msg = claude.messages.create(
            model=CLAUDE_MODEL, max_tokens=2500, temperature=0.3,
            messages=[{"role": "user", "content": p3_prompt}]
        )
        claude_out = c_msg.content[0].text

        divider = "\n\n---\n\n"
        if lang == "ko":
            return f"# 🔬 최종 논문 진단 보고서{divider}## 📊 Phase 1: 학술 DB 분석 (Perplexity)\n\n{perplexity_out}{divider}## 💎 Phase 2: 가치 평가 (Gemini)\n\n{gemini_out}{divider}## 🤖 Phase 3: 원고 품질 감사 (Claude)\n\n{claude_out}{divider}*Powered by Perplexity + Gemini + Claude*"
        else:
            return f"# 🔬 Final Diagnosis Report{divider}## 📊 Phase 1: Literature Analysis (Perplexity)\n\n{perplexity_out}{divider}## 💎 Phase 2: Value Assessment (Gemini)\n\n{gemini_out}{divider}## 🤖 Phase 3: Manuscript Audit (Claude)\n\n{claude_out}{divider}*Powered by Perplexity + Gemini + Claude*"
    except Exception as e:
        return f"❌ Hybrid Diagnosis Error: {str(e)}"


# ============================================
# 사용자 시스템
# ============================================
USER_DB_FILE = "users_db.json"

def hash_pw(pw): return hashlib.sha256(pw.encode()).hexdigest()
def verify_pw(inp, stored): return hash_pw(inp) == stored
def load_users():
    try:
        with open(USER_DB_FILE, 'r', encoding='utf-8') as f: return json.load(f)
    except: return {}
def save_users(users):
    with open(USER_DB_FILE, 'w', encoding='utf-8') as f: json.dump(users, f, indent=2, ensure_ascii=False)
    try: os.chmod(USER_DB_FILE, 0o600)
    except: pass

def init_accounts():
    users = load_users()
    ch = False
    for uname, tier in [("test_free", "free"), ("test_pro", "pro")]:
        if uname not in users:
            users[uname] = {"password": hash_pw("Test1234!"), "email": f"{tier}@test.com", "tier": tier,
                            "usage_count": 0, "week_start": datetime.now().isoformat(), "created_at": datetime.now().isoformat()}
            ch = True
    if ch: save_users(users)
init_accounts()

def check_reset(ud):
    try: return datetime.now() - datetime.fromisoformat(ud.get("week_start", datetime.now().isoformat())) > timedelta(days=7)
    except: return True

def update_usage(un):
    users = load_users()
    if un in users:
        if check_reset(users[un]):
            users[un]["usage_count"] = 0
            users[un]["week_start"] = datetime.now().isoformat()
        users[un]["usage_count"] += 1
        save_users(users)

def remaining_uses(un):
    users = load_users()
    if un in users:
        if check_reset(users[un]): return 10
        return max(0, 10 - users[un].get("usage_count", 0))
    return 0

def check_limit():
    if st.session_state.user_tier == "pro": return True
    r = remaining_uses(st.session_state.username)
    if r <= 0:
        st.error(T("error_limit"))
        st.warning(f"💎 {T('upgrade')}")
        return False
    return True

def extract_text(file):
    if not file: return ""
    try:
        if file.name.endswith('.pdf'):
            return "".join(p.extract_text() or "" for p in PyPDF2.PdfReader(file).pages)[:3000]
        if file.name.endswith('.docx'):
            return "\n".join(p.text.strip() for p in docx.Document(file).paragraphs)[:3000]
        return file.read().decode('utf-8', errors='ignore')[:3000]
    except Exception as e: return f"Error: {e}"

# ============================================
# 세션 초기화
# ============================================
for k, v in [("logged_in", False), ("username", None), ("user_tier", "free"),
             ("sessions", {"contemplate": {}, "master": {}, "gap": {}, "method": {}, "draft": {}, "polish": {}, "diagnosis": {}, "submit": {}, "references": {}})]:
    if k not in st.session_state:
        st.session_state[k] = v

# ============================================
# 언어 선택
# ============================================
_, col_lang = st.columns([5, 1])
with col_lang:
    cur = st.session_state.get("language", "ko")
    sel = st.selectbox("🌐", list(LANGUAGES.keys()), format_func=lambda x: f"{LANGUAGES[x]['flag']} {LANGUAGES[x]['name']}",
                       index=list(LANGUAGES.keys()).index(cur), label_visibility="collapsed")
    if sel != cur:
        st.session_state.language = sel
        st.rerun()
st.markdown("---")

# ============================================
# 로그인
# ============================================
if not st.session_state.logged_in:
    st.markdown(f"<h1 style='text-align:center'>{T('app_title')}</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center;color:#888'>{T('app_subtitle')}</p>", unsafe_allow_html=True)
    st.markdown("---")
    _, cc, _ = st.columns([1, 2, 1])
    with cc:
        t1, t2 = st.tabs([T("login"), T("signup")])
        with t1:
            st.markdown(f"### {T('login')}")
            with st.expander(T("test_account")):
                st.info("**FREE**: test_free / Test1234!\n**PRO**: test_pro / Test1234!")
            lu = st.text_input(T("username"), key="lu")
            lp = st.text_input(T("password"), type="password", key="lp")
            if st.button(T("login_button"), type="primary", use_container_width=True):
                users = load_users()
                if lu in users and verify_pw(lp, users[lu]["password"]):
                    st.session_state.logged_in = True
                    st.session_state.username = lu
                    st.session_state.user_tier = users[lu].get("tier", "free")
                    st.success(f"✅ {T('welcome')}, {lu}!")
                    st.balloons(); st.rerun()
                else: st.error(T("invalid_cred"))
        with t2:
            st.markdown(f"### {T('signup')}")
            su = st.text_input(T("username"), key="su")
            se = st.text_input(T("email"), key="se")
            sp = st.text_input(T("password"), type="password", key="sp")
            spc = st.text_input(T("password_confirm"), type="password", key="spc")
            if st.button(T("signup_button"), type="primary", use_container_width=True):
                users = load_users()
                if len(su) < 4: st.error("❌ 4자 이상")
                elif su in users: st.error("❌ 이미 존재")
                elif sp != spc: st.error("❌ 비밀번호 불일치")
                elif len(sp) < 6: st.error("❌ 6자 이상")
                else:
                    users[su] = {"password": hash_pw(sp), "email": se, "tier": "free", "usage_count": 0,
                                 "week_start": datetime.now().isoformat(), "created_at": datetime.now().isoformat()}
                    save_users(users); st.success("✅ 가입 완료! 로그인하세요.")
        st.markdown("---"); st.caption(T("security"))
    st.stop()

# ============================================
# 사이드바
# ============================================
with st.sidebar:
    st.markdown(f"## {T('app_title')}")
    st.success(f"👤 **{st.session_state.username}**")
    if st.session_state.user_tier == "free":
        r = remaining_uses(st.session_state.username)
        st.warning(T("free_plan")); st.progress(r / 10)
        st.caption(f"{T('remaining')}: **{r}/10**"); st.caption(T("weekly_reset"))
        if st.button(T("upgrade"), use_container_width=True): st.info("💎 PRO coming soon!")
    else:
        st.success(T("pro_plan")); st.caption(f"✅ {T('unlimited')}")
    st.divider()
    if st.button(T("logout"), use_container_width=True):
        st.session_state.logged_in = False; st.session_state.username = None; st.session_state.user_tier = "free"; st.rerun()
    st.divider(); st.caption(T("security")); st.divider()
    st.caption("🔧 Engine Status")
    st.caption("✅ Perplexity: sonar-pro")
    st.caption(f"✅ Gemini: {GEMINI_MODEL}")
    st.caption(f"✅ Claude: {CLAUDE_MODEL}")

# ============================================
# 메인 앱
# ============================================
st.title(T("app_title"))
st.markdown(T("app_subtitle"))
st.markdown("---")

tabs = st.tabs([
    T("contemplate_tab"), T("master_tab"),
    T("gap_tab"), T("method_tab"), T("draft_tab"), T("polish_tab"),
    T("diagnosis_tab"), T("submit_tab"), T("references_tab"), T("storage_tab")
])

# ── 🧠 사유의 방 ──
with tabs[0]:
    st.header(T("contemplate_title"))
    st.info(T("contemplate_desc"))
    raw_idea = st.text_area(T("contemplate_input"), height=180, placeholder=T("contemplate_placeholder"), key="contemplate_text")
    c1, c2 = st.columns(2)
    with c1:
        depth = st.selectbox(T("contemplate_depth"),
            ["spark", "explore", "architect"],
            format_func=lambda x: {"spark": T("depth_spark"), "explore": T("depth_explore"), "architect": T("depth_architect")}[x])
    with c2:
        con_lang = st.selectbox("Language", ["ko", "en"], format_func=lambda x: "한국어" if x == "ko" else "English", key="con_lang")
    if st.button(T("contemplate_button"), type="primary", use_container_width=True):
        if not check_limit(): st.stop()
        if raw_idea.strip():
            with st.spinner(T("analyzing")):
                result = contemplate(raw_idea, depth, con_lang)
                st.session_state.sessions["contemplate"] = {"result": result}
                update_usage(st.session_state.username); st.rerun()
        else: st.error(T("error_empty"))
    data = st.session_state.sessions.get("contemplate")
    if data:
        st.markdown(f"### 📊 {T('result')}")
        st.markdown(data['result'])
        st.download_button(T("download"), data['result'], "contemplation.txt")

# ── 🎓 거장과의 대화 ──
with tabs[1]:
    st.header(T("master_title"))
    st.info(T("master_desc"))
    cat = st.selectbox(T("master_category"), ["social", "engineer", "art"],
        format_func=lambda x: {"social": T("cat_social"), "engineer": T("cat_engineer"), "art": T("cat_art")}[x])
    lang_now = st.session_state.language
    master_options = list(MASTERS[cat].keys())
    master_labels = [f"{MASTERS[cat][m]['name_ko']} ({m})" if lang_now == "ko" else m for m in master_options]
    master_key = st.selectbox(T("master_select"), master_options, format_func=lambda x: f"{MASTERS[cat][x]['name_ko']} ({x})" if lang_now == "ko" else x)
    question = st.text_area(T("master_input"), height=150, placeholder=T("master_placeholder"), key="master_text")
    m_lang = st.selectbox("Language", ["ko", "en"], format_func=lambda x: "한국어" if x == "ko" else "English", key="m_lang")
    if st.button(T("master_button"), type="primary", use_container_width=True):
        if not check_limit(): st.stop()
        if question.strip():
            master_display = MASTERS[cat][master_key]['name_ko'] if m_lang == "ko" else master_key
            with st.spinner(f"🎓 {master_display} 사유 중..." if m_lang == "ko" else f"🎓 {master_display} is thinking..."):
                result = master_dialogue(question, master_key, cat, m_lang)
                st.session_state.sessions["master"] = {"result": result, "master": master_display}
                update_usage(st.session_state.username); st.rerun()
        else: st.error(T("error_empty"))
    data = st.session_state.sessions.get("master")
    if data:
        st.markdown(f"### 🎓 {data.get('master', '')}의 답변")
        st.markdown(data['result'])
        st.download_button(T("download"), data['result'], "master_dialogue.txt")

# ── 🌱 Gap-Mining ──
with tabs[2]:
    st.header(T("gap_title")); st.info(T("gap_desc"))
    c1, c2 = st.columns([1, 3])
    fg = c1.file_uploader(T("file_upload"), type=['pdf','docx','txt'], key="f1")
    tg = c2.text_area("💡", height=150, placeholder=T("placeholder_idea"), key="t1")
    if st.button(T("analyze_button"), type="primary", use_container_width=True):
        if not check_limit(): st.stop()
        payload = extract_text(fg) or tg
        if payload.strip():
            with st.spinner(T("analyzing")):
                r = analyze_with_ai(payload, "gap")
                st.session_state.sessions["gap"] = {"result": r}; update_usage(st.session_state.username); st.rerun()
        else: st.error(T("error_empty"))
    d = st.session_state.sessions.get("gap")
    if d:
        st.markdown(f"### 📊 {T('result')}"); st.markdown(d['result'])
        st.download_button(T("download"), d['result'], "gap_analysis.txt")
        fq = st.chat_input(T("ask_more"))
        if fq:
            with st.chat_message("user"): st.write(fq)
            with st.spinner("..."):
                a = gemini.generate_content(f"{d['result']}\n\n{fq}").text
            with st.chat_message("assistant"): st.markdown(a)

# ── ⚖️ 방법론 ──
with tabs[3]:
    st.header(T("method_title")); st.info(T("method_desc"))
    c1, c2 = st.columns([1, 3])
    fm = c1.file_uploader(T("file_upload"), type=['pdf','docx','txt'], key="f2")
    tm = c2.text_area("📊", height=150, placeholder=T("placeholder_method"), key="t2")
    if st.button(T("validate_button"), type="primary", use_container_width=True):
        if not check_limit(): st.stop()
        payload = extract_text(fm) or tm
        if payload.strip():
            with st.spinner(T("analyzing")):
                r = analyze_with_ai(payload, "method")
                st.session_state.sessions["method"] = {"result": r}; update_usage(st.session_state.username); st.rerun()
        else: st.error(T("error_empty"))
    d = st.session_state.sessions.get("method")
    if d:
        st.markdown(f"### 📊 {T('result')}"); st.markdown(d['result'])
        st.download_button(T("download"), d['result'], "method_validation.txt")

# ── 📝 드래프트 ──
with tabs[4]:
    st.header(T("draft_title"))
    if st.session_state.user_tier != "pro":
        st.warning(T("pro_only"))
        if st.button(T("upgrade"), use_container_width=True, key="du"): st.info("💎 PRO coming soon!")
        st.stop()
    st.info(T("draft_desc"))
    dt = st.text_area(T("draft_topic"), height=150, placeholder=T("placeholder_idea"), key="di")
    c1, c2 = st.columns(2)
    with c1: sec = st.selectbox(T("section_select"), ["intro", "method", "discussion"],
                format_func=lambda x: {"intro": "Introduction", "method": "Methods", "discussion": "Discussion"}[x])
    with c2: dl = st.selectbox("Language", ["ko", "en"], format_func=lambda x: "한국어" if x == "ko" else "English", key="dl")
    if st.button(T("generate_draft"), type="primary", use_container_width=True):
        if not check_limit(): st.stop()
        if dt.strip():
            with st.spinner(T("analyzing")):
                r = draft_with_claude(dt, sec, dl)
                st.session_state.sessions["draft"] = {"result": r}; update_usage(st.session_state.username); st.rerun()
        else: st.error(T("error_empty"))
    d = st.session_state.sessions.get("draft")
    if d:
        st.markdown(f"### 📄 {T('result')}"); st.markdown(d['result'])
        st.download_button(T("download"), d['result'], "draft.txt")

# ── ✍️ 윤문 ──
with tabs[5]:
    st.header(T("polish_title"))
    if st.session_state.user_tier != "pro":
        st.warning(T("pro_only"))
        if st.button(T("upgrade"), use_container_width=True, key="pu"): st.info("💎 PRO coming soon!")
        st.stop()
    st.info(T("polish_desc"))
    pt = st.text_area(T("polish_input"), height=200, placeholder="학술적으로 다듬을 텍스트...", key="pi")
    pl = st.selectbox("Language", ["ko", "en"], format_func=lambda x: "한국어 윤문" if x == "ko" else "English Polishing", key="pl")
    if st.button(T("start_polish"), type="primary", use_container_width=True):
        if not check_limit(): st.stop()
        if pt.strip():
            with st.spinner(T("analyzing")):
                r = polish_with_claude(pt, pl)
                st.session_state.sessions["polish"] = {"result": r}; update_usage(st.session_state.username); st.rerun()
        else: st.error(T("error_empty"))
    d = st.session_state.sessions.get("polish")
    if d:
        st.markdown(f"### ✨ {T('result')}"); st.markdown(d['result'])
        c1, c2 = st.columns(2)
        with c1: st.download_button(T("download"), d['result'], "polished.txt")
        with c2:
            if st.button(T("repolish")): st.session_state.sessions["polish"] = {}; st.rerun()

# ── 🔬 최종 진단 ──
with tabs[6]:
    st.header(T("diagnosis_title"))
    if st.session_state.user_tier != "pro":
        st.warning(T("pro_only"))
        if st.button(T("upgrade"), use_container_width=True, key="dgu"): st.info("💎 PRO coming soon!")
        st.stop()
    st.info(T("diagnosis_desc"))
    c1, c2 = st.columns([1, 3])
    fd = c1.file_uploader(T("file_upload"), type=['pdf','docx','txt'], key="df")
    td = c2.text_area(T("full_paper"), height=250, placeholder="완성된 논문...", key="dti")
    ddl = st.selectbox("Language", ["ko", "en"], format_func=lambda x: "한국어" if x == "ko" else "English", key="ddl")
    if st.button("🔬 3-Engine 하이브리드 진단", type="primary", use_container_width=True):
        if not check_limit(): st.stop()
        payload = extract_text(fd) or td
        if payload.strip():
            pb = st.progress(0); s = st.empty()
            s.info("🔍 Phase 1/3: Perplexity..."); pb.progress(10)
            with st.spinner("3-Engine 분석 중..."):
                r = hybrid_diagnosis(payload, ddl)
                s.success("✅ 완료!"); pb.progress(100)
                st.session_state.sessions["diagnosis"] = {"result": r}; update_usage(st.session_state.username); st.rerun()
        else: st.error(T("error_empty"))
    d = st.session_state.sessions.get("diagnosis")
    if d:
        st.markdown("### 📋 진단 결과"); st.markdown(d['result'])
        c1, c2, c3 = st.columns(3)
        with c1: st.download_button("💾 리포트", d['result'], "diagnosis.txt")
        with c2: st.download_button("📧 이메일용", d['result'], "diagnosis_email.txt")
        with c3:
            if st.button("🔄 재진단"): st.session_state.sessions["diagnosis"] = {}; st.rerun()

# ── 🏁 투고 ──
with tabs[7]:
    st.header(T("submit_title")); st.info(T("submit_desc"))
    c1, c2 = st.columns([1, 3])
    fs = c1.file_uploader(T("file_upload"), type=['pdf','docx','txt'], key="f3")
    ts = c2.text_area("✍️", height=150, placeholder=T("placeholder_abstract"), key="t3")
    if st.button(T("strategy_button"), type="primary", use_container_width=True):
        if not check_limit(): st.stop()
        payload = extract_text(fs) or ts
        if payload.strip():
            with st.spinner(T("analyzing")):
                r = analyze_with_ai(payload, "submit")
                st.session_state.sessions["submit"] = {"result": r}; update_usage(st.session_state.username); st.rerun()
        else: st.error(T("error_empty"))
    d = st.session_state.sessions.get("submit")
    if d:
        st.markdown(f"### 📊 {T('result')}"); st.markdown(d['result'])
        st.download_button(T("download"), d['result'], "submission_strategy.txt")

# ── 📚 참고문헌 ──
with tabs[8]:
    st.header(T("references_title")); st.info(T("references_desc"))
    rt = st.text_input("🔍", placeholder=T("placeholder_topic"))
    if st.button(T("search_button"), type="primary", use_container_width=True):
        if not check_limit(): st.stop()
        if rt.strip():
            with st.spinner(T("analyzing")):
                r = analyze_with_ai(rt, "references")
                st.session_state.sessions["references"] = {"result": r}; update_usage(st.session_state.username); st.rerun()
        else: st.error(T("error_empty"))
    d = st.session_state.sessions.get("references")
    if d:
        st.markdown(f"### 📚 {T('result')}"); st.markdown(d['result'])
        st.download_button(T("download"), d['result'], "references.txt")

# ── 💾 저장소 ──
with tabs[9]:
    st.header(f"💾 {T('storage_tab')}")
    has = False
    for name in ["contemplate", "master", "gap", "method", "draft", "polish", "diagnosis", "submit", "references"]:
        d = st.session_state.sessions.get(name)
        if d and d.get("result"):
            has = True
            with st.expander(f"📂 {name.upper()}"):
                st.text_area(T("result"), d["result"][:500] + "..." if len(d["result"]) > 500 else d["result"],
                             height=150, disabled=True, key=f"s_{name}")
    if not has: st.info("No saved sessions yet.")
    else:
        bj = json.dumps(st.session_state.sessions, ensure_ascii=False, indent=2)
        st.download_button(f"💾 {T('download')} All (JSON)", bj, "strategist_backup.json", use_container_width=True)

st.markdown("---")
st.caption(f"*{T('app_title')} | 2026 | Powered by Perplexity + Gemini + Claude*")
st.caption(f"✅ sonar-pro + {GEMINI_MODEL} + {CLAUDE_MODEL}")
