"""
AI Regulatory Compliance Copilot - Enhanced Streamlit UI
Copy this file to your VS Code project to replace app.py
"""

import streamlit as st
import pandas as pd

from preprocessing import extract_text, split_into_clauses
from embeddings import generate_embeddings
from similarity import build_index, search_similar
from classifier import classify_compliance, calculate_risk
from rag_generator import configure_gemini, generate_explanation


# Page configuration
st.set_page_config(
    page_title="ComplianceAI — Regulatory Copilot",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# CUSTOM CSS — Premium Dark UI
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Inter:wght@300;400;500;600&display=swap');

/* ── Global ── */
.stApp {
    background: linear-gradient(180deg, #0a0f1e 0%, #0f172a 50%, #0a0f1e 100%);
    color: #e2e8f0;
    font-family: 'Inter', sans-serif;
}

h1, h2, h3, h4, h5, h6, .hero-title, .sidebar-title {
    font-family: 'Space Grotesk', sans-serif !important;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #070b16 0%, #0c1222 100%);
    border-right: 1px solid rgba(56, 97, 251, 0.1);
}

[data-testid="stSidebar"] * {
    color: #94a3b8 !important;
}

.sidebar-title {
    color: #f1f5f9 !important;
    font-size: 22px;
    font-weight: 700;
    letter-spacing: -0.5px;
}

.sidebar-badge {
    display: inline-block;
    background: rgba(56, 97, 251, 0.15);
    color: #60a5fa !important;
    padding: 2px 10px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 600;
    margin-top: 4px;
}

/* ── Hero ── */
.hero-container {
    text-align: center;
    padding: 100px 20px 80px;
    position: relative;
}

.hero-container::before {
    content: '';
    position: absolute;
    top: 0; left: 50%;
    transform: translateX(-50%);
    width: 600px; height: 400px;
    background: radial-gradient(ellipse, rgba(56, 97, 251, 0.12) 0%, transparent 70%);
    pointer-events: none;
}

.hero-icon {
    width: 80px; height: 80px;
    background: rgba(56, 97, 251, 0.1);
    border: 1px solid rgba(56, 97, 251, 0.2);
    border-radius: 20px;
    display: flex; align-items: center; justify-content: center;
    margin: 0 auto 30px;
    font-size: 36px;
    box-shadow: 0 0 40px -10px rgba(56, 97, 251, 0.3);
}

.hero-title {
    font-size: 52px;
    font-weight: 700;
    letter-spacing: -1.5px;
    line-height: 1.1;
    margin-bottom: 20px;
}

.hero-title .gradient {
    background: linear-gradient(135deg, #3b82f6, #8b5cf6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-title .white {
    color: #f1f5f9;
}

.hero-subtitle {
    color: #64748b;
    font-size: 17px;
    line-height: 1.7;
    max-width: 520px;
    margin: 0 auto;
}

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #3b82f6, #6366f1) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 14px 36px !important;
    font-size: 15px !important;
    font-weight: 600 !important;
    font-family: 'Space Grotesk', sans-serif !important;
    letter-spacing: -0.3px;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 20px -4px rgba(56, 97, 251, 0.4) !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 30px -4px rgba(56, 97, 251, 0.5) !important;
}

/* ── Cards ── */
.glass-card {
    background: rgba(15, 23, 42, 0.6);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(56, 97, 251, 0.08);
    border-radius: 16px;
    padding: 28px;
    transition: all 0.3s ease;
}

.glass-card:hover {
    border-color: rgba(56, 97, 251, 0.2);
}

/* ── Metric Cards ── */
.metric-card {
    background: rgba(15, 23, 42, 0.6);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 16px;
    padding: 28px;
    text-align: center;
    transition: all 0.3s ease;
}

.metric-card:hover {
    border-color: rgba(56, 97, 251, 0.15);
    transform: translateY(-2px);
}

.metric-value {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 2.8rem;
    font-weight: 700;
    letter-spacing: -1px;
}

.metric-label {
    color: #64748b;
    font-size: 0.85rem;
    margin-top: 6px;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

/* ── Status Badges ── */
.status-badge {
    padding: 5px 14px;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 600;
    display: inline-block;
}

.status-compliant {
    background: rgba(22, 163, 74, 0.15);
    color: #4ade80;
    border: 1px solid rgba(22, 163, 74, 0.2);
}

.status-partial {
    background: rgba(234, 179, 8, 0.15);
    color: #facc15;
    border: 1px solid rgba(234, 179, 8, 0.2);
}

.status-not {
    background: rgba(239, 68, 68, 0.15);
    color: #f87171;
    border: 1px solid rgba(239, 68, 68, 0.2);
}

/* ── Upload Section ── */
.upload-card {
    background: rgba(15, 23, 42, 0.5);
    border: 2px dashed rgba(56, 97, 251, 0.15);
    border-radius: 16px;
    padding: 30px;
    text-align: center;
    transition: all 0.3s ease;
}

.upload-card:hover {
    border-color: rgba(56, 97, 251, 0.35);
    background: rgba(15, 23, 42, 0.7);
}

/* ── File uploader ── */
[data-testid="stFileUploader"] {
    background: transparent !important;
}

[data-testid="stFileUploader"] section {
    background: rgba(15, 23, 42, 0.4) !important;
    border: 2px dashed rgba(56, 97, 251, 0.15) !important;
    border-radius: 12px !important;
    padding: 20px !important;
}

/* ── Slider ── */
.stSlider > div > div {
    background: rgba(56, 97, 251, 0.2) !important;
}

/* ── Expander ── */
.streamlit-expanderHeader {
    background: rgba(15, 23, 42, 0.5) !important;
    border: 1px solid rgba(255, 255, 255, 0.05) !important;
    border-radius: 12px !important;
    font-family: 'Space Grotesk', sans-serif !important;
}

/* ── Feature cards ── */
.feature-card {
    background: rgba(15, 23, 42, 0.5);
    backdrop-filter: blur(16px);
    border: 1px solid rgba(255, 255, 255, 0.04);
    border-radius: 16px;
    padding: 24px;
    text-align: center;
    transition: all 0.3s ease;
}

.feature-card:hover {
    border-color: rgba(56, 97, 251, 0.2);
}

.feature-icon {
    width: 48px; height: 48px;
    background: rgba(56, 97, 251, 0.1);
    border-radius: 12px;
    display: flex; align-items: center; justify-content: center;
    margin: 0 auto 14px;
    font-size: 22px;
}

.feature-title {
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 600;
    font-size: 15px;
    color: #e2e8f0;
    margin-bottom: 6px;
}

.feature-desc {
    color: #64748b;
    font-size: 13px;
    line-height: 1.5;
}

/* ── Dividers ── */
hr {
    border-color: rgba(255, 255, 255, 0.05) !important;
}

/* ── Info/Success/Warning boxes ── */
.stAlert {
    background: rgba(15, 23, 42, 0.5) !important;
    border: 1px solid rgba(255, 255, 255, 0.05) !important;
    border-radius: 12px !important;
    color: #94a3b8 !important;
}

/* ── Select box ── */
.stSelectbox > div > div {
    background: rgba(15, 23, 42, 0.6) !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
}

/* ── Section header ── */
.section-header {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 26px;
    font-weight: 700;
    color: #f1f5f9;
    letter-spacing: -0.5px;
    margin-bottom: 8px;
}

.section-subtitle {
    color: #64748b;
    font-size: 15px;
    margin-bottom: 24px;
}

/* ── Footer ── */
.footer {
    text-align: center;
    color: #475569;
    padding: 30px 20px;
    font-size: 13px;
    border-top: 1px solid rgba(255, 255, 255, 0.04);
    margin-top: 40px;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────
if 'results' not in st.session_state:
    st.session_state.results = None
if 'page' not in st.session_state:
    st.session_state.page = "🏠 Dashboard"


# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding: 10px 0 20px;'>
        <div style='display:flex; align-items:center; gap:12px;'>
            <div style='width:40px;height:40px;background:rgba(56,97,251,0.15);border-radius:12px;
                 display:flex;align-items:center;justify-content:center;font-size:20px;'>🛡️</div>
            <div>
                <div class='sidebar-title'>ComplianceAI</div>
                <div class='sidebar-badge'>Regulatory Copilot</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    page = st.radio(
        "Navigation",
        ["🏠 Dashboard", "📊 New Analysis", "📈 Results"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.markdown("""
    <div style='padding:12px;background:rgba(15,23,42,0.5);border-radius:10px;
         border:1px solid rgba(255,255,255,0.04);'>
        <div style='font-size:11px;color:#475569;'>v1.0.0 — Hackathon Prototype</div>
        <div style='font-size:10px;color:#334155;margin-top:3px;'>SentenceTransformers + FAISS</div>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# DASHBOARD PAGE
# ─────────────────────────────────────────────
if page == "🏠 Dashboard":
    st.markdown("""
    <div class='hero-container'>
        <div class='hero-icon'>🛡️</div>
        <div class='hero-title'>
            <span class='gradient'>AI-Powered</span><br>
            <span class='white'>Compliance Copilot</span>
        </div>
        <div class='hero-subtitle'>
            Upload regulatory circulars and internal policies to get
            clause-level gap analysis with AI-powered explanations
            and risk scoring.
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([3, 2, 3])
    with col2:
        if st.button("Start New Analysis →", use_container_width=True):
            st.session_state.page = "📊 New Analysis"
            st.rerun()

    # Feature cards
    st.markdown("<br>", unsafe_allow_html=True)
    
    f1, f2, f3 = st.columns(3)
    with f1:
        st.markdown("""
        <div class='feature-card'>
            <div class='feature-icon'>🔍</div>
            <div class='feature-title'>PDF Parsing</div>
            <div class='feature-desc'>Extract and split regulatory & policy documents into clauses</div>
        </div>
        """, unsafe_allow_html=True)
    with f2:
        st.markdown("""
        <div class='feature-card'>
            <div class='feature-icon'>🧠</div>
            <div class='feature-title'>Semantic Matching</div>
            <div class='feature-desc'>FAISS + SentenceTransformers for clause-level similarity</div>
        </div>
        """, unsafe_allow_html=True)
    with f3:
        st.markdown("""
        <div class='feature-card'>
            <div class='feature-icon'>📊</div>
            <div class='feature-title'>Gap Analysis</div>
            <div class='feature-desc'>Compliance scoring with AI-powered explanations via Gemini</div>
        </div>
        """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# NEW ANALYSIS PAGE
# ─────────────────────────────────────────────
elif page == "📊 New Analysis":
    st.markdown("""
    <div class='section-header'>📊 New Compliance Analysis</div>
    <div class='section-subtitle'>Upload your documents to begin clause-level comparison</div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class='glass-card' style='margin-bottom:16px;'>
            <div style='display:flex;align-items:center;gap:10px;margin-bottom:14px;'>
                <div style='width:36px;height:36px;background:rgba(56,97,251,0.1);border-radius:10px;
                     display:flex;align-items:center;justify-content:center;'>📜</div>
                <div>
                    <div style='font-family:Space Grotesk;font-weight:600;color:#e2e8f0;font-size:15px;'>
                        Regulatory Document</div>
                    <div style='font-size:12px;color:#64748b;'>Upload circular or regulation PDF</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        reg_doc = st.file_uploader("Upload Regulatory PDF", type=["pdf"], key="reg", label_visibility="collapsed")

    with col2:
        st.markdown("""
        <div class='glass-card' style='margin-bottom:16px;'>
            <div style='display:flex;align-items:center;gap:10px;margin-bottom:14px;'>
                <div style='width:36px;height:36px;background:rgba(56,97,251,0.1);border-radius:10px;
                     display:flex;align-items:center;justify-content:center;'>📄</div>
                <div>
                    <div style='font-family:Space Grotesk;font-weight:600;color:#e2e8f0;font-size:15px;'>
                        Internal Policy</div>
                    <div style='font-size:12px;color:#64748b;'>Upload your internal policy PDF</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        policy_doc = st.file_uploader("Upload Policy PDF", type=["pdf"], key="policy", label_visibility="collapsed")

    # Settings
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style='display:flex;align-items:center;gap:8px;margin-bottom:16px;'>
        <span style='color:#3b82f6;'>⚙️</span>
        <span style='font-family:Space Grotesk;font-weight:600;color:#e2e8f0;'>Analysis Settings</span>
    </div>
    """, unsafe_allow_html=True)

    threshold = st.slider("Similarity Threshold", 0.0, 1.0, 0.75,
                          help="Adjust the minimum similarity score for compliance")

    col1, col2 = st.columns([1, 1])
    with col1:
        use_ai = st.toggle("✨ AI Explanations (Gemini)", value=False)
        gemini_key = None
        if use_ai:
            gemini_key = st.text_input("🔑 Gemini API Key", type="password")

    st.markdown("---")

    if reg_doc and policy_doc:
        if st.button("⚡ Run Analysis", type="primary", use_container_width=True):
            with st.spinner("Processing documents..."):
                reg_text = extract_text(reg_doc)
                policy_text = extract_text(policy_doc)
                
                reg_clauses = split_into_clauses(reg_text)
                policy_clauses = split_into_clauses(policy_text)
                
                reg_embeddings = generate_embeddings(reg_clauses)
                policy_embeddings = generate_embeddings(policy_clauses)
                
                index = build_index(policy_embeddings)
                distances, indices = search_similar(index, reg_embeddings)
                
                results = []
                for i, reg_clause in enumerate(reg_clauses):
                    distance = distances[i][0]
                    similarity_score = 1 / (1 + distance)
                    
                    if similarity_score > threshold:
                        status = "Compliant"
                    elif similarity_score > (threshold - 0.2):
                        status = "Partial"
                    else:
                        status = "Missing"
                    
                    policy_clause = policy_clauses[indices[i][0]]
                    
                    if status == "Missing":
                        risk = "High"
                    elif status == "Partial":
                        risk = "Medium"
                    else:
                        risk = "Low"
                    
                    explanation = ""
                    if use_ai and gemini_key and status != "Compliant":
                        try:
                            configure_gemini(gemini_key)
                            explanation = generate_explanation(reg_clause, policy_clause)
                        except:
                            explanation = "AI explanation unavailable"
                    
                    results.append({
                        "Clause": f"Clause {i+1}",
                        "Regulatory Text": reg_clause[:200] + "..." if len(reg_clause) > 200 else reg_clause,
                        "Policy Match": policy_clause[:200] + "..." if len(policy_clause) > 200 else policy_clause,
                        "Similarity": round(similarity_score, 2),
                        "Status": status,
                        "Risk": risk,
                        "Full Reg": reg_clause,
                        "Full Policy": policy_clause,
                        "Explanation": explanation
                    })
                
                st.session_state.results = results
                st.session_state.analyzed = True
            
            st.success("✅ Analysis complete!")
            st.rerun()
    else:
        st.info("📎 Upload both documents to begin analysis")


# ─────────────────────────────────────────────
# RESULTS PAGE
# ─────────────────────────────────────────────
elif page == "📈 Results":
    st.markdown("""
    <div class='section-header'>📈 Analysis Results</div>
    <div class='section-subtitle'>Clause-level compliance comparison</div>
    """, unsafe_allow_html=True)

    if st.session_state.results is None:
        st.info("No analysis results yet. Run a new analysis first.")
        if st.button("→ Go to New Analysis"):
            st.session_state.page = "📊 New Analysis"
            st.rerun()
    else:
        results = st.session_state.results
        df = pd.DataFrame(results)
        
        total = len(results)
        compliant = len(df[df["Status"] == "Compliant"])
        partial = len(df[df["Status"] == "Partial"])
        missing = len(df[df["Status"] == "Missing"])
        risk_score = missing * 2 + partial * 1

        # Metrics row
        c1, c2, c3, c4, c5 = st.columns(5)
        
        with c1:
            st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-value' style='color:#e2e8f0;'>{total}</div>
                <div class='metric-label'>Total Clauses</div>
            </div>""", unsafe_allow_html=True)
        with c2:
            st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-value' style='color:#4ade80;'>{compliant}</div>
                <div class='metric-label'>Compliant</div>
            </div>""", unsafe_allow_html=True)
        with c3:
            st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-value' style='color:#facc15;'>{partial}</div>
                <div class='metric-label'>Partial</div>
            </div>""", unsafe_allow_html=True)
        with c4:
            st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-value' style='color:#f87171;'>{missing}</div>
                <div class='metric-label'>Missing</div>
            </div>""", unsafe_allow_html=True)
        with c5:
            st.markdown(f"""
            <div class='metric-card' style='border-color:rgba(239,68,68,0.15);'>
                <div class='metric-value' style='color:#f87171;'>{risk_score}</div>
                <div class='metric-label'>Risk Score</div>
            </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Filter
        filter_status = st.selectbox("Filter by Status", ["All", "Compliant", "Partial", "Missing"])
        
        if filter_status != "All":
            display_df = df[df["Status"] == filter_status]
        else:
            display_df = df

        # Clause cards
        for idx, row in display_df.iterrows():
            status_class = {
                "Compliant": "status-compliant",
                "Partial": "status-partial",
                "Missing": "status-not"
            }.get(row["Status"], "")

            risk_badge = ""
            if row["Risk"] == "High":
                risk_badge = "<span class='status-badge status-not' style='margin-left:8px;'>High Risk</span>"

            with st.expander(f"🔹 {row['Clause']} — {row['Status']} ({row['Similarity']:.0%})"):
                col_r, col_p = st.columns(2)
                
                with col_r:
                    st.markdown("**📜 Regulatory Requirement**")
                    st.info(row["Full Reg"])
                
                with col_p:
                    st.markdown("**📄 Current Policy**")
                    st.info(row["Full Policy"])
                
                col_s, col_risk = st.columns(2)
                
                with col_s:
                    st.metric("Similarity Score", f"{row['Similarity']:.0%}")
                
                with col_risk:
                    risk_color = {"Low": "normal", "Medium": "off", "High": "inverse"}
                    st.metric("Risk Level", row["Risk"],
                              delta_color=risk_color.get(row["Risk"], "off"))
                
                if row.get("Explanation"):
                    st.markdown("---")
                    st.markdown("**✨ AI Analysis:**")
                    st.success(row["Explanation"])

        # Export
        st.markdown("---")
        csv = display_df[["Clause", "Regulatory Text", "Policy Match", "Similarity", "Status", "Risk"]].to_csv(index=False)
        
        st.download_button(
            "📥 Download Results CSV",
            csv,
            "compliance_results.csv",
            "text/csv",
            use_container_width=True
        )


# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown("""
<div class='footer'>
    🛡️ AI Regulatory Compliance Copilot &nbsp;·&nbsp; SentenceTransformers + FAISS + Gemini
</div>
""", unsafe_allow_html=True)
