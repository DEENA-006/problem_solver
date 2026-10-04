import os
import time
import random
import html
import streamlit as st
import streamlit.components.v1 as components
from PIL import Image
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

# Read API key from environment variable (local .env) or Streamlit Secrets (Cloud)
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    try:
        api_key = st.secrets.get("GEMINI_API_KEY")
    except Exception:
        api_key = None

client = genai.Client(api_key=api_key)

st.set_page_config(
    page_title="STEM Tutor AI",
    page_icon="⬡",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
  --bg:          #0a0a0f;
  --surface:     #111118;
  --surface2:    #16161f;
  --border:      #1e1e2e;
  --border-hover:#2a2a3e;
  --accent:      #6366f1;
  --accent-dim:  rgba(99,102,241,0.12);
  --accent-glow: rgba(99,102,241,0.25);
  --cyan:        #22d3ee;
  --text:        #f1f5f9;
  --text-muted:  #64748b;
  --text-dim:    #94a3b8;
  --success:     #10b981;
  --radius-sm:   8px;
  --radius-md:   12px;
  --radius-lg:   16px;
}

html, body, [data-testid="stApp"] {
  background: var(--bg) !important;
  font-family: 'Inter', sans-serif !important;
  color: var(--text) !important;
}

#MainMenu, footer, header { visibility: hidden; }
[data-testid="stToolbar"]        { display: none !important; }
[data-testid="collapsedControl"] { display: none !important; }
[data-testid="stDecoration"]     { display: none !important; }

.block-container {
  max-width: 760px !important;
  padding: 1.2rem 1.5rem 7rem !important;
}

/* ── HEADER ── */
.app-header {
  padding: 1.2rem 0 1.4rem;
  border-bottom: 1px solid var(--border);
  margin-bottom: 1.4rem;
}
.app-logo {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 0.6rem;
}
.logo-icon {
  width: 36px; height: 36px;
  background: var(--accent-dim);
  border: 1px solid rgba(99,102,241,0.3);
  border-radius: 9px;
  display: flex; align-items: center; justify-content: center;
  font-size: 18px;
}
.logo-name {
  font-size: 1.05rem; font-weight: 600;
  color: var(--text); letter-spacing: -0.2px;
}
.logo-badge {
  font-size: 0.65rem; font-weight: 600;
  background: var(--accent-dim); color: #818cf8;
  border: 1px solid rgba(99,102,241,0.25);
  border-radius: 4px; padding: 2px 6px;
  letter-spacing: 0.5px; text-transform: uppercase;
}
.app-title {
  font-size: 2rem; font-weight: 700; color: var(--text);
  letter-spacing: -0.8px; line-height: 1.2; margin: 0 0 0.5rem;
}
.app-desc {
  font-size: 0.93rem; color: var(--text-muted);
  font-weight: 400; line-height: 1.65; max-width: 520px;
}
.subject-tags {
  display: flex; flex-wrap: wrap; gap: 6px; margin-top: 1.1rem;
}
.tag {
  font-size: 0.72rem; font-weight: 500; padding: 3px 10px;
  border-radius: 999px; border: 1px solid var(--border-hover);
  color: var(--text-dim); background: var(--surface);
}

/* ── DIVIDER ── */
.divider { height: 1px; background: var(--border); margin: 1rem 0; }

/* ── STATUS BAR ── */
.status-bar {
  display: flex; align-items: center; gap: 6px;
  font-size: 0.75rem; color: var(--text-muted); margin-bottom: 0.6rem;
}
.status-dot {
  width: 7px; height: 7px; background: var(--success);
  border-radius: 50%; box-shadow: 0 0 6px var(--success);
  animation: pulse 2.5s ease-in-out infinite;
}
@keyframes pulse {
  0%, 100% { opacity: 1; } 50% { opacity: 0.4; }
}



[data-testid="stChatMessage"] {
  background: var(--surface) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--radius-lg) !important;
  padding: 16px 20px !important;
  margin-bottom: 8px !important;
  transition: border-color 0.2s;
}
[data-testid="stChatMessage"]:hover { border-color: var(--border-hover) !important; }
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
  border-left: 3px solid var(--accent) !important;
  background: var(--surface2) !important;
}
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
  border-left: 3px solid var(--cyan) !important;
}
[data-testid="stChatMessage"] p,
[data-testid="stChatMessage"] li,
[data-testid="stChatMessage"] td {
  font-family: 'Inter', sans-serif !important;
  font-size: 0.925rem !important; line-height: 1.75 !important; color: var(--text) !important;
}
[data-testid="stChatMessage"] h1,
[data-testid="stChatMessage"] h2,
[data-testid="stChatMessage"] h3 {
  color: var(--text) !important; font-family: 'Inter', sans-serif !important; font-weight: 600 !important;
}
[data-testid="stChatMessage"] code {
  font-family: 'JetBrains Mono', monospace !important; font-size: 0.83rem !important;
  background: rgba(99,102,241,0.08) !important; border: 1px solid rgba(99,102,241,0.18) !important;
  border-radius: 5px !important; padding: 1px 6px !important; color: #a5b4fc !important;
}
[data-testid="stChatMessage"] pre {
  font-family: 'JetBrains Mono', monospace !important;
  background: #0d0d16 !important; border: 1px solid var(--border-hover) !important;
  border-radius: var(--radius-sm) !important; padding: 14px 16px !important;
}

/* ── BOTTOM CONTAINER & CHAT INPUT (No white background) ── */
[data-testid="stBottom"],
[data-testid="stBottom"] > div,
[data-testid="stBottomBlockContainer"],
[data-testid="stBottomBlockContainer"] > div,
footer,
.stBottom {
  background: var(--bg) !important;
  background-color: var(--bg) !important;
  border: none !important;
  box-shadow: none !important;
}

[data-testid="stChatInput"],
[data-testid="stChatInput"] > div,
[data-testid="stChatInput"] div[data-baseweb="input"],
[data-testid="stChatInput"] div[data-baseweb="base-input"] {
  background: var(--surface) !important;
  background-color: var(--surface) !important;
  border-color: var(--border-hover) !important;
  color: var(--text) !important;
}

[data-testid="stChatInput"] {
  border: 1px solid var(--border-hover) !important;
  border-radius: var(--radius-md) !important;
  position: relative !important;
  transition: border-color 0.2s, box-shadow 0.2s;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4) !important;
}

[data-testid="stChatInput"]:focus-within {
  border-color: var(--accent) !important;
  box-shadow: 0 0 0 3px var(--accent-glow), 0 4px 20px rgba(0, 0, 0, 0.5) !important;
}

[data-testid="stChatInput"] textarea {
  color: var(--text) !important;
  font-family: 'Inter', sans-serif !important;
  font-size: 0.9rem !important;
  background: transparent !important;
  background-color: transparent !important;
  padding-left: 52px !important;
}

[data-testid="stChatInput"] textarea::placeholder {
  color: var(--text-muted) !important;
}

[data-testid="stChatInput"] button {
  background: transparent !important;
  color: var(--text-dim) !important;
  border: none !important;
}

[data-testid="stChatInput"] button:hover {
  color: var(--cyan) !important;
}

/* ── BUTTON (clear) ── */
.stButton > button {
  background: var(--surface) !important; color: var(--text-dim) !important;
  border: 1px solid var(--border-hover) !important; border-radius: var(--radius-sm) !important;
  font-family: 'Inter', sans-serif !important; font-size: 0.8rem !important;
  font-weight: 500 !important; padding: 6px 14px !important;
  transition: all 0.18s ease !important;
}
.stButton > button:hover {
  background: var(--surface2) !important; color: var(--text) !important;
  border-color: #374151 !important;
}

/* ── FILE UPLOADER — hidden dropzone, show only preview strip ── */
[data-testid="stFileUploaderDropzone"] {
  position: absolute !important;
  opacity: 0 !important;
  width: 0 !important;
  height: 0 !important;
  overflow: hidden !important;
  margin: 0 !important;
  padding: 0 !important;
  border: none !important;
  z-index: -10 !important;
}
[data-testid="stFileUploaderDropzone"] input[type="file"] {
  position: absolute !important;
  opacity: 0 !important;
  width: 1px !important;
  height: 1px !important;
}
[data-testid="stFileUploader"] {
  margin: 0 !important;
  padding: 0 !important;
}
[data-testid="stFileUploader"] > label {
  display: none !important;
}
/* Show the uploaded file name / delete button when file exists */
[data-testid="stFileUploader"] [data-testid="stFileUploaderFile"] {
  display: flex !important;
  background: var(--surface2) !important;
  border: 1px solid var(--border-hover) !important;
  border-radius: var(--radius-sm) !important;
  padding: 6px 10px !important;
  margin-top: 4px !important;
  font-size: 0.78rem !important; color: var(--text-dim) !important;
  font-family: 'Inter', sans-serif !important;
}
/* Preview image (compact) */
.preview-strip {
  display: flex; align-items: center; gap: 10px;
  background: var(--surface2); border: 1px solid var(--border-hover);
  border-radius: var(--radius-sm); padding: 8px 12px; margin-bottom: 6px;
  animation: slideDown 0.15s ease;
}
.preview-strip img { border-radius: 6px; object-fit: cover; }
.preview-info { font-size: 0.78rem; color: var(--text-dim); }
.preview-name { font-weight: 500; color: var(--text); }
@keyframes slideDown {
  from { opacity: 0; transform: translateY(-4px); }
  to   { opacity: 1; transform: translateY(0); }
}

/* ── SUGGESTION CHIPS ── */
.suggestions {
  display: flex; flex-wrap: wrap; gap: 8px;
  margin-top: 14px;
}
.chip {
  font-size: 0.8rem; font-weight: 450;
  padding: 6px 14px;
  border-radius: 999px;
  border: 1px solid var(--border-hover);
  color: var(--text-dim);
  background: var(--surface2);
  cursor: pointer;
  transition: all 0.15s ease;
  white-space: nowrap;
}
.chip:hover {
  border-color: var(--accent);
  color: #a5b4fc;
  background: var(--accent-dim);
}

/* ── GREETING BUBBLE ── */
.greeting-bubble {
  background: var(--surface) !important;
  border: 1px solid var(--border) !important;
  border-left: 3px solid var(--cyan) !important;
  border-radius: var(--radius-lg) !important;
  padding: 18px 22px !important;
  margin-bottom: 12px;
  animation: fadeIn 0.3s ease;
}
.greeting-hi {
  font-size: 1rem; font-weight: 600;
  color: var(--text); margin-bottom: 6px;
}
.greeting-body {
  font-size: 0.9rem; color: var(--text-dim);
  line-height: 1.7;
}
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(6px); }
  to   { opacity: 1; transform: translateY(0); }
}

/* ── MISC ── */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--border-hover); border-radius: 999px; }
[data-testid="stBottom"] {
  background: linear-gradient(to top, var(--bg) 65%, transparent) !important;
}
[data-testid="stAlert"] {
  background: rgba(239,68,68,0.08) !important;
  border: 1px solid rgba(239,68,68,0.25) !important;
  border-radius: var(--radius-sm) !important;
}

/* ── TOP NAVIGATION BAR ── */
.top-status-bar {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 8px;
  font-size: 0.78rem;
  color: var(--text-dim);
  padding: 6px 14px;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  margin-top: 2px;
}

[data-testid="stPopover"] > button {
  background: var(--surface) !important;
  border: 1px solid var(--border-hover) !important;
  border-radius: var(--radius-sm) !important;
  color: var(--text) !important;
  padding: 6px 14px !important;
  font-size: 0.86rem !important;
  font-weight: 500 !important;
  display: inline-flex !important;
  align-items: center !important;
  gap: 6px !important;
  box-shadow: 0 2px 10px rgba(0,0,0,0.3) !important;
  transition: all 0.18s ease !important;
  cursor: pointer !important;
}
[data-testid="stPopover"] > button:hover {
  border-color: var(--cyan) !important;
  color: var(--cyan) !important;
  background: var(--surface2) !important;
  box-shadow: 0 0 12px rgba(34, 211, 238, 0.22) !important;
}

/* Floating Popover Menu Panel */
[data-baseweb="popover"] {
  z-index: 100001 !important;
}
div[data-testid="stPopoverBody"] {
  background: #111118 !important;
  border: 1px solid #2a2a3e !important;
  border-radius: 14px !important;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.9) !important;
  width: min(580px, 92vw) !important;
  max-width: 92vw !important;
  max-height: 82vh !important;
  overflow-y: auto !important;
  padding: 1.2rem 1.4rem !important;
}

.menu-popover-title {
  font-size: 0.98rem;
  font-weight: 600;
  color: var(--cyan);
  margin-bottom: 0.8rem;
  display: flex;
  align-items: center;
  gap: 8px;
}

[data-baseweb="tab-list"] {
  background-color: transparent !important;
  border-bottom: 1px solid var(--border) !important;
}
[data-baseweb="tab"] {
  color: var(--text-dim) !important;
  font-family: 'Inter', sans-serif !important;
  font-size: 0.82rem !important;
  padding: 8px 14px !important;
}
[aria-selected="true"] {
  color: var(--cyan) !important;
  border-bottom-color: var(--cyan) !important;
}

/* Topmost Right Status Bar */
.top-status-bar {
  position: fixed !important;
  top: 9px !important;
  right: 18px !important;
  z-index: 99999 !important;
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.76rem;
  color: var(--text-dim);
  padding: 6px 14px;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  box-shadow: 0 2px 10px rgba(0,0,0,0.3);
}
</style>
""", unsafe_allow_html=True)

def build_system_instruction(level="Undergraduate", style="Step-by-step"):
    level_prompt = {
        "High School": "Target explanations for a high school student. Use intuitive analogies, clear step-by-step algebra, and easy-to-follow explanations.",
        "Undergraduate": "Target explanations for a university undergraduate. Maintain mathematical rigor, formal derivations, standard scientific notation, and college-level depth.",
        "Advanced / Research": "Target explanations for an advanced / research level. Provide rigorous mathematical proofs, theoretical depth, and literature-grade scientific precision."
    }.get(level, "Target explanations for university undergraduate level.")

    style_prompt = {
        "Step-by-step": "Break down every problem step-by-step with complete formulas and logical progression.",
        "Socratic Hints": "Act as a Socratic tutor: do NOT give the entire answer immediately. Provide the first crucial step or hint, point out key principles, and ask a guiding question to help the student solve it themselves.",
        "Concise Summary": "Provide a direct, high-density solution or conceptual summary without unnecessary fluff."
    }.get(style, "Break down every problem step-by-step.")

    return f"""You are an expert STEM tutor.
Level: {level}. {level_prompt}
Teaching Style: {style}. {style_prompt}
When given a problem:
- Follow the requested teaching style and level.
- Always use LaTeX for mathematical, physics, and chemical equations ($inline$ or $$display$$).
- Always use syntax-highlighted code blocks for programming tasks.
- If follow-up questions are asked, patiently explain the underlying concepts."""

STEM_POOLS = {
    "math": [
        ("∑ Solve: x² − 5x + 6 = 0", "Solve step by step: x² - 5x + 6 = 0"),
        ("∑ Derivative: d/dx(x³ · sin x)", "Calculate the derivative of f(x) = x³ * sin(x) using the product rule step by step"),
        ("∑ Integral: ∫ x · eˣ dx", "Evaluate the integral ∫ x * e^x dx using integration by parts step by step"),
        ("∑ Matrix: 2×2 Eigenvalues", "Find the eigenvalues and eigenvectors of a 2x2 matrix step by step"),
        ("∑ Limit: lim(x→0) sin(x)/x", "Evaluate the limit as x approaches 0 of sin(x)/x using L'Hôpital's rule step by step"),
        ("∑ Bayes' Theorem probability", "Explain Bayes' Theorem with a step-by-step conditional probability calculation example"),
        ("∑ Taylor series for eˣ", "Derive the Taylor series expansion for e^x centered at x = 0 step by step"),
        ("∑ Quadratic formula derivation", "Derive the quadratic formula by completing the square step by step"),
    ],
    "physics": [
        ("⚛ Newton's second law", "Explain Newton's second law with a real-world calculation example step by step"),
        ("⚛ Projectile motion at 45°", "Calculate the maximum range and time of flight for a projectile launched at 45 degrees step by step"),
        ("⚛ Doppler effect in sound", "Derive the formula for the Doppler effect for sound waves and solve a numerical example"),
        ("⚛ Special relativity: Time dilation", "Explain Einstein's time dilation formula with a step-by-step example at 0.8c"),
        ("⚛ Carnot engine efficiency", "Calculate the maximum theoretical efficiency of a Carnot heat engine step by step"),
        ("⚛ Snell's Law & Total reflection", "Explain Snell's law and calculate the critical angle for total internal reflection in glass and air"),
        ("⚛ Schrödinger equation basics", "Explain the concept and physical meaning of the time-independent Schrödinger equation"),
        ("⚛ Bernoulli's principle", "Explain Bernoulli's equation in fluid dynamics and its application to airplane wing lift"),
    ],
    "cs": [
        ("</> Python binary search", "Write a binary search algorithm in Python with time complexity analysis and explanation"),
        ("</> Dynamic programming: Fibonacci", "Explain dynamic programming memoization vs tabulation using Fibonacci numbers in Python"),
        ("</> Dijkstra's shortest path", "Explain Dijkstra's shortest path algorithm step by step with pseudocode and time complexity"),
        ("</> Merge sort vs Quick sort", "Compare Merge Sort and Quick Sort with code implementations and runtime comparisons"),
        ("</> Invert a binary tree in Python", "Write a clean Python function to invert a binary tree recursively with step-by-step explanation"),
        ("</> LRU Cache design", "Explain how to design an LRU (Least Recently Used) cache using a Hash Map and Doubly Linked List in Python"),
        ("</> Big-O notation guide", "Explain Big-O notation from O(1) to O(2^n) with practical code examples for each complexity class"),
        ("</> Breadth-first search in Python", "Explain Breadth-First Search (BFS) for graphs in Python with an adjacency list example"),
    ],
    "chem": [
        ("⚗ Entropy in thermodynamics", "What is entropy in thermodynamics and statistical mechanics? Explain with clear examples"),
        ("⚗ Balance redox: MnO₄⁻ + Fe²⁺", "Balance this redox reaction in acidic solution step by step: MnO4- + Fe2+ -> Mn2+ + Fe3+"),
        ("⚗ Le Chatelier's principle", "Explain Le Chatelier's principle and how temperature and pressure affect chemical equilibrium"),
        ("⚗ SN1 vs SN2 reaction mechanisms", "Compare SN1 and SN2 reaction mechanisms in organic chemistry with energy profiles and stereochemistry"),
        ("⚗ Buffer pH: Henderson-Hasselbalch", "Calculate the pH of an acetate buffer solution using the Henderson-Hasselbalch equation step by step"),
        ("⚗ Hybridization: sp, sp², sp³", "Explain orbital hybridization (sp, sp2, sp3) with molecular shapes and bond angles"),
        ("⚗ Ideal Gas Law: PV = nRT", "Explain the Ideal Gas Law (PV = nRT) and solve a step-by-step stoichiometry calculation"),
        ("⚗ Gibbs Free Energy: ΔG = ΔH - TΔS", "Explain how Gibbs Free Energy determines reaction spontaneity with endothermic and exothermic examples"),
    ],
    "bio": [
        ("🧬 DNA replication step by step", "Explain the molecular process of DNA replication step by step including helicase, polymerase, and ligase"),
        ("🧬 CRISPR-Cas9 mechanism", "How does CRISPR-Cas9 gene editing work? Explain guide RNA, Cas9 cleavage, and repair mechanisms"),
        ("🧬 Cellular respiration: Krebs cycle", "Break down the stages of cellular respiration from glycolysis to the Krebs cycle and ATP synthase"),
        ("🧬 Photosynthesis light reactions", "Explain the light-dependent reactions of photosynthesis in the thylakoid membrane step by step"),
        ("🧬 Action potential in neurons", "Describe how an action potential is generated and propagated along a neuron axon with ion channel states"),
        ("🧬 Mendelian genetics: Dihybrid cross", "Solve a dihybrid Punnett square problem (9:3:3:1 ratio) step by step with phenotypic probabilities"),
        ("🧬 Protein synthesis: Transcription to Translation", "Explain protein synthesis from mRNA transcription to ribosome translation with tRNA codons"),
        ("🧬 Enzyme kinetics: Michaelis-Menten", "Explain the Michaelis-Menten equation and what Km and Vmax represent in enzyme biochemistry"),
    ],
}

def pick_random_suggestions():
    return [random.choice(STEM_POOLS[cat]) for cat in ["math", "physics", "cs", "chem", "bio"]]

# ── State Initialization ──────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "active_model" not in st.session_state:
    st.session_state.active_model = "gemini-3.5-flash"
if "uploader_key" not in st.session_state:
    st.session_state.uploader_key = 0
if "tutor_level" not in st.session_state:
    st.session_state.tutor_level = "Undergraduate"
if "tutor_style" not in st.session_state:
    st.session_state.tutor_style = "Step-by-step"
if "menu_open" not in st.session_state:
    st.session_state.menu_open = False
if "suggestions" not in st.session_state or not st.session_state.suggestions:
    st.session_state.suggestions = pick_random_suggestions()

# ── Topmost Navigation Bar (Leftmost Menu Icon & Rightmost Status) ────────────
count = len(st.session_state.messages)
label = f"{count // 2} exchange{'s' if count // 2 != 1 else ''}" if count else "No messages yet"
model_name = st.session_state.get("active_model", "gemini-3.5-flash")
lvl_icon = "🎓" if st.session_state.tutor_level == "High School" else ("🏛️" if st.session_state.tutor_level == "Undergraduate" else "🔬")

col_top_menu, col_top_status = st.columns([1.5, 4.5])
with col_top_menu:
    with st.popover("☰ Menu"):
        st.markdown('<div class="menu-popover-title">☰ STEM Tutor Menu</div>', unsafe_allow_html=True)
        menu_tabs = st.tabs(["⚙️ Tutor Mode", "📐 Formulas & Constants", "📥 Export Notes", "⚡ Quick Actions"])

        with menu_tabs[0]:
            c1, c2, c3 = st.columns(3)
            with c1:
                st.session_state.tutor_level = st.selectbox(
                    "Target Level",
                    ["High School", "Undergraduate", "Advanced / Research"],
                    index=["High School", "Undergraduate", "Advanced / Research"].index(st.session_state.tutor_level),
                    help="Adapts vocabulary, mathematical depth, and proof rigor"
                )
            with c2:
                st.session_state.tutor_style = st.selectbox(
                    "Teaching Method",
                    ["Step-by-step", "Socratic Hints", "Concise Summary"],
                    index=["Step-by-step", "Socratic Hints", "Concise Summary"].index(st.session_state.tutor_style),
                    help="Choose between comprehensive steps, guided hints, or summaries"
                )
            with c3:
                model_options = ["gemini-3.5-flash", "gemini-3.5-flash-lite", "gemini-3-flash-preview", "gemini-3.1-flash-lite"]
                current_m = st.session_state.active_model if st.session_state.active_model in model_options else model_options[0]
                st.session_state.active_model = st.selectbox(
                    "Gemini Model",
                    model_options,
                    index=model_options.index(current_m),
                    help="Select AI model (Auto-resilient fallback is always active)"
                )

        with menu_tabs[1]:
            tab_phys, tab_math, tab_chem, tab_bio = st.tabs(["⚛ Physics", "∑ Mathematics", "⚗ Chemistry", "🧬 Biology"])
            with tab_phys:
                st.markdown("""
                **Fundamental Physical Constants:**
                - Speed of Light: $c = 2.998 \\times 10^8\\text{ m/s}$
                - Planck's Constant: $h = 6.626 \\times 10^{-34}\\text{ J}\\cdot\\text{s}$ &nbsp;($\\hbar = h/2\\pi$)
                - Gravitational Constant: $G = 6.674 \\times 10^{-11}\\text{ N}\\cdot\\text{m}^2/\\text{kg}^2$
                - Boltzmann Constant: $k_B = 1.381 \\times 10^{-23}\\text{ J/K}$
                - Elementary Charge: $e = 1.602 \\times 10^{-19}\\text{ C}$
                - Vacuum Permittivity: $\\varepsilon_0 = 8.854 \\times 10^{-12}\\text{ F/m}$
                
                **Core Mechanics & Electromagnetism:**
                - Newton's 2nd Law: $\\mathbf{F} = \\frac{d\\mathbf{p}}{dt} = m\\mathbf{a}$
                - Kinetic Energy: $K = \\frac{1}{2}mv^2$ &nbsp;|&nbsp; Momentum: $\\mathbf{p} = m\\mathbf{v}$
                - Lorentz Force: $\\mathbf{F} = q(\\mathbf{E} + \\mathbf{v} \\times \\mathbf{B})$
                - Time Dilation: $\\Delta t' = \\frac{\\Delta t}{\\sqrt{1 - v^2/c^2}}$
                """)
            with tab_math:
                st.markdown("""
                **Calculus & Algebra:**
                - Quadratic Equation: $x = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}$
                - Product Rule: $(uv)' = u'v + uv'$
                - Quotient Rule: $\\left(\\frac{u}{v}\\right)' = \\frac{u'v - uv'}{v^2}$
                - Chain Rule: $\\frac{d}{dx}f(g(x)) = f'(g(x)) \\cdot g'(x)$
                - Integration by Parts: $\\int u\\,dv = uv - \\int v\\,du$
                - Euler's Formula: $e^{i\\theta} = \\cos\\theta + i\\sin\\theta$
                - Taylor Series: $f(x) = \\sum_{n=0}^{\\infty} \\frac{f^{(n)}(a)}{n!}(x - a)^n$
                """)
            with tab_chem:
                st.markdown("""
                **Thermodynamics & Equilibrium:**
                - Ideal Gas Law: $PV = nRT$ &nbsp;($R = 8.314\\text{ J/(mol}\\cdot\\text{K)} = 0.0821\\text{ L}\\cdot\\text{atm/(mol}\\cdot\\text{K)}$)
                - Gibbs Free Energy: $\\Delta G = \\Delta H - T\\Delta S = -RT \\ln K$
                - Henderson-Hasselbalch: $\\text{pH} = \\text{p}K_a + \\log\\left(\\frac{[\\text{A}^-]}{[\\text{HA}]}\\right)$
                - Nernst Equation: $E = E^\\circ - \\frac{RT}{nF} \\ln Q = E^\\circ - \\frac{0.0592}{n} \\log_{10} Q$ (at $298\\text{ K}$)
                - Avogadro's Number: $N_A = 6.022 \\times 10^{23}\\text{ mol}^{-1}$
                """)
            with tab_bio:
                st.markdown("""
                **Molecular Biology & Genetics:**
                - Central Dogma: $\\text{DNA} \\xrightarrow{\\text{Transcription}} \\text{mRNA} \\xrightarrow{\\text{Translation}} \\text{Polypeptide (Protein)}$
                - Base Pairing: Adenine (A) = Thymine (T) [Uracil in RNA], Guanine (G) $\\equiv$ Cytosine (C)
                - Cellular Respiration: $\\text{C}_6\\text{H}_{12}\\text{O}_6 + 6\\text{O}_2 \\to 6\\text{CO}_2 + 6\\text{H}_2\\text{O} + \\sim 30\\text{--}32\\text{ ATP}$
                - Michaelis-Menten Equation: $v_0 = \\frac{V_{\\max}[S]}{K_m + [S]}$
                - Hardy-Weinberg Equilibrium: $p^2 + 2pq + q^2 = 1$ &nbsp;|&nbsp; $p + q = 1$
                """)

        with menu_tabs[2]:
            msg_count = len(st.session_state.messages)
            if msg_count == 0:
                st.info("No chat messages recorded in this session yet. Ask any question below to generate notes!")
            else:
                st.write(f"You have **{msg_count // 2} completed exchange(s)** in this study session.")
                notes_content = f"# ⬡ STEM Tutor AI — Study Session Notes\n\n"
                notes_content += f"- **Date**: {time.strftime('%Y-%m-%d %H:%M')}\n"
                notes_content += f"- **Target Level**: {st.session_state.tutor_level}\n"
                notes_content += f"- **Teaching Mode**: {st.session_state.tutor_style}\n\n---\n\n"
                for i, msg in enumerate(st.session_state.messages):
                    role_title = "🧑‍🎓 Student" if msg["role"] == "user" else "🤖 STEM Tutor"
                    notes_content += f"## {role_title}\n\n{msg['content']}\n\n---\n\n"

                st.download_button(
                    label="⬇️ Download Notes as Markdown (.md)",
                    data=notes_content,
                    file_name=f"STEM_Study_Notes_{time.strftime('%Y%m%d_%H%M')}.md",
                    mime="text/markdown",
                    use_container_width=True,
                )

        with menu_tabs[3]:
            act_c1, act_c2 = st.columns(2)
            with act_c1:
                if st.button("🎲 Generate Fresh Problem Ideas", use_container_width=True):
                    st.session_state.suggestions = pick_random_suggestions()
                    st.rerun()
            with act_c2:
                if st.button("🗑️ Clear All Chats & Attachments", use_container_width=True):
                    st.session_state.messages = []
                    st.session_state.active_model = "gemini-3.5-flash"
                    st.session_state.uploader_key += 1
                    st.session_state.suggestions = pick_random_suggestions()
                    st.rerun()

with col_top_status:
    st.markdown(f"""
    <div class="top-status-bar">
      <span class="status-dot"></span>
      {model_name} &nbsp;&middot;&nbsp; {lvl_icon} {st.session_state.tutor_level} &nbsp;&middot;&nbsp; {label}
    </div>
    """, unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="app-header">
  <div class="app-logo">
    <div class="logo-icon">⬡</div>
    <span class="logo-name">STEM Tutor AI</span>
    <span class="logo-badge">Beta</span>
  </div>
  <h1 class="app-title">Your personal STEM tutor</h1>
  <p class="app-desc">
    Ask any question in mathematics, physics, programming, chemistry, or biology.
    Get clear, step-by-step explanations powered by AI.
  </p>
  <div class="subject-tags">
    <span class="tag">∑ Mathematics</span>
    <span class="tag">⚛ Physics</span>
    <span class="tag">&lt;/&gt; Programming</span>
    <span class="tag">⚗ Chemistry</span>
    <span class="tag">🧬 Biology</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Chat history ──────────────────────────────────────────────────────────────
if not st.session_state.messages:
    # ── Initial greeting bubble with dynamic random suggestions ───────────────
    chips_html = "".join([
        f'        <span class="chip" data-q="{html.escape(prompt_text, quote=True)}">{html.escape(label)}</span>\n'
        for label, prompt_text in st.session_state.suggestions
    ])

    st.markdown(f"""
    <div class="greeting-bubble">
      <div class="greeting-hi">👋 Hi, I'm your STEM Tutor!</div>
      <div class="greeting-body">
        I can help you with <strong>Mathematics</strong>, <strong>Physics</strong>,
        <strong>Programming</strong>, <strong>Chemistry</strong>, and <strong>Biology</strong>.<br/>
        I'll break every problem down step-by-step with proper formulas and code.
        What would you like to learn today?
      </div>
      <div class="suggestions">
{chips_html}      </div>
    </div>
    """, unsafe_allow_html=True)
else:
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            if msg.get("image"):
                st.image(msg["image"], width=240)
            st.markdown(msg["content"])

# ── Hidden file uploader (triggered by + button via JS) ───────────────────────
uploaded_file = st.file_uploader(
    "Attach image",
    type=["jpg", "jpeg", "png"],
    label_visibility="collapsed",
    key=f"file_upload_{st.session_state.uploader_key}",
)
image = None
if uploaded_file:
    image = Image.open(uploaded_file)
    # Compact preview strip with delete button
    col_img, col_info, col_del = st.columns([0.14, 0.76, 0.10])
    with col_img:
        st.image(image, width=64)
    with col_info:
        st.markdown(f"""
        <div class="preview-info">
          <div class="preview-name">📎 {uploaded_file.name}</div>
          <div style="margin-top:2px;font-size:0.73rem;color:#64748b;">
            {round(uploaded_file.size / 1024, 1)} KB · attached
          </div>
        </div>
        """, unsafe_allow_html=True)
    with col_del:
        if st.button("✕", key=f"del_img_{st.session_state.uploader_key}", help="Remove image"):
            st.session_state.uploader_key += 1
            st.rerun()

# ── Chat input ────────────────────────────────────────────────────────────────
if prompt := st.chat_input("Ask a question or describe a problem…"):

    user_msg = {"role": "user", "content": prompt}
    if uploaded_file and image:
        user_msg["image"] = image

    with st.chat_message("user"):
        if user_msg.get("image"):
            st.image(user_msg["image"], width=240)
        st.markdown(prompt)
    st.session_state.messages.append(user_msg)

    # Sliding window memory
    window_size = 4
    recent_messages = st.session_state.messages[-window_size:]

    context_prompt = "Context of our recent conversation:\n\n"
    for msg in recent_messages[:-1]:
        role_name = "Student" if msg["role"] == "user" else "Tutor"
        context_prompt += f"{role_name}: {msg['content']}\n\n"

    context_prompt += f"Student's New Question: {prompt}\n"
    context_prompt += "Please answer the new question based on the context above."

    contents = []
    if uploaded_file:
        contents.append(image)
    contents.append(context_prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking…"):
            response_text = None
            used_model = None
            last_err = None

            active_sys_instruct = build_system_instruction(
                st.session_state.get("tutor_level", "Undergraduate"),
                st.session_state.get("tutor_style", "Step-by-step"),
            )

            # Resilient fallback chain: tries active model first, then auto-fails over
            priority_models = [
                st.session_state.get("active_model", "gemini-3.5-flash"),
                "gemini-3.5-flash",
                "gemini-3.5-flash-lite",
                "gemini-3-flash-preview",
                "gemini-3.1-flash-lite",
            ]
            seen = set()
            candidate_models = [m for m in priority_models if not (m in seen or seen.add(m))]

            for m in candidate_models:
                try:
                    response = client.models.generate_content(
                        model=m,
                        contents=contents,
                        config=types.GenerateContentConfig(
                            system_instruction=active_sys_instruct,
                            temperature=0.2,
                        ),
                    )
                    if response and response.text:
                        response_text = response.text
                        used_model = m
                        st.session_state.active_model = m
                        break
                except Exception as e:
                    last_err = e
                    err_msg = str(e)
                    # Transient error, quota limit, or high-demand 503: try fallback model
                    if any(term in err_msg for term in ["503", "UNAVAILABLE", "429", "RESOURCE_EXHAUSTED", "demand", "overload"]):
                        time.sleep(0.3)
                        continue
                    else:
                        continue

            if response_text:
                st.markdown(response_text)
                st.session_state.messages.append({"role": "assistant", "content": response_text})
                if uploaded_file:
                    st.session_state.uploader_key += 1
                    st.rerun()
            else:
                if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
                    st.session_state.messages.pop()
                st.markdown(f"""
                <div style="background: rgba(239, 68, 68, 0.1); border: 1px solid rgba(239, 68, 68, 0.3); border-radius: 10px; padding: 14px 18px; margin: 10px 0;">
                  <div style="color: #ef4444; font-weight: 600; font-size: 0.95rem; margin-bottom: 6px;">
                    ⚠️ Model Temporarily Busy
                  </div>
                  <div style="color: #cbd5e1; font-size: 0.85rem; line-height: 1.4;">
                    Google's AI service is currently experiencing peak traffic surges ({last_err}). Please try sending your question again in a moment.
                  </div>
                </div>
                """, unsafe_allow_html=True)

# ── Inject "+" button + chip-click wiring via JavaScript ──────────────────
components.html("""
<script>
(function () {

  function fillTextarea(text) {
    const doc = window.parent.document;
    const ta  = doc.querySelector('[data-testid="stChatInput"] textarea');
    if (!ta) return;
    const nativeSetter = Object.getOwnPropertyDescriptor(
      window.parent.HTMLTextAreaElement.prototype, 'value'
    ).set;
    nativeSetter.call(ta, text);
    ta.dispatchEvent(new Event('input', { bubbles: true }));
    ta.focus();
  }

  function wireChips() {
    const doc   = window.parent.document;
    const chips = doc.querySelectorAll('.chip[data-q]:not([data-wired])');
    chips.forEach(chip => {
      chip.setAttribute('data-wired', '1');
      chip.style.cursor = 'pointer';
      chip.addEventListener('click', () => fillTextarea(chip.getAttribute('data-q')));
    });
  }

  function injectPlusBtn() {
    const doc = window.parent.document;
    if (doc.querySelector('.ai-plus-btn')) return;
    const chatInput = doc.querySelector('[data-testid="stChatInput"]');
    if (!chatInput) { setTimeout(injectPlusBtn, 200); return; }
    chatInput.style.position = 'relative';
    const ta = chatInput.querySelector('textarea');
    if (ta) ta.style.paddingLeft = '52px';
    const btn = doc.createElement('label');
    btn.className = 'ai-plus-btn';
    btn.title     = 'Attach an image';
    btn.innerHTML = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>';
    Object.assign(btn.style, {
      position:'absolute', left:'12px', bottom:'10px',
      width:'30px', height:'30px', borderRadius:'8px',
      border:'1px solid #2a2a3e', background:'#111118', color:'#94a3b8',
      cursor:'pointer', display:'flex', alignItems:'center',
      justifyContent:'center', zIndex:'999',
      transition:'all 0.15s ease', userSelect:'none', flexShrink:'0',
    });
    btn.onmouseenter = () => { btn.style.background='#16161f'; btn.style.borderColor='#6366f1'; btn.style.color='#818cf8'; };
    btn.onmouseleave = () => { btn.style.background='#111118'; btn.style.borderColor='#2a2a3e'; btn.style.color='#94a3b8'; };
    
    function linkInput() {
      const fi = doc.querySelector('input[type="file"]');
      if (fi) {
        if (!fi.id) fi.id = 'stem-file-upload-input';
        btn.setAttribute('for', fi.id);
        return fi;
      }
      return null;
    }
    linkInput();

    btn.onclick = (e) => {
      e.preventDefault();
      e.stopPropagation();
      const fi = doc.querySelector('input[type="file"]');
      if (fi) {
        fi.click();
      } else {
        const browseBtn = doc.querySelector('[data-testid="stFileUploaderDropzone"] button');
        if (browseBtn) browseBtn.click();
      }
    };
    chatInput.appendChild(btn);
  }

  function init() { injectPlusBtn(); wireChips(); }
  init();

  new MutationObserver(() => {
    const doc = window.parent.document;
    if (!doc.querySelector('.ai-plus-btn')) setTimeout(injectPlusBtn, 100);
    const t = doc.querySelector('[data-testid="stChatInput"] textarea');
    if (t && t.style.paddingLeft !== '52px') t.style.paddingLeft = '52px';
    const fi = doc.querySelector('input[type="file"]');
    const b = doc.querySelector('.ai-plus-btn');
    if (fi && b) {
      if (!fi.id) fi.id = 'stem-file-upload-input';
      b.setAttribute('for', fi.id);
    }
    wireChips();
  }).observe(window.parent.document.body, { childList: true, subtree: true });

})();
</script>
""", height=0)

