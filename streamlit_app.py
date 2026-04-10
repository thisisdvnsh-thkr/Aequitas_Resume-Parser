import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pdfminer.high_level
import docx2txt
import re
import io

# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title="Aequitas | AI Resume Auditor",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== THEME TOGGLE ====================
if 'theme' not in st.session_state:
    st.session_state.theme = 'dark'

def toggle_theme():
    st.session_state.theme = 'light' if st.session_state.theme == 'dark' else 'dark'

# ==================== CUSTOM CSS ====================
def load_css():
    theme = st.session_state.theme
    
    if theme == 'dark':
        bg_color = "#0e1117"
        card_bg = "rgba(28, 31, 40, 0.7)"
        text_color = "#ffffff"
        secondary_text = "#b4b4b4"
        accent_color = "#00d4ff"
        border_color = "rgba(255, 255, 255, 0.1)"
        shadow = "0 8px 32px 0 rgba(0, 0, 0, 0.37)"
    else:
        bg_color = "#ffffff"
        card_bg = "rgba(255, 255, 255, 0.7)"
        text_color = "#1f1f1f"
        secondary_text = "#5f5f5f"
        accent_color = "#0066cc"
        border_color = "rgba(0, 0, 0, 0.1)"
        shadow = "0 8px 32px 0 rgba(31, 38, 135, 0.15)"
    
    css = f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {{
        font-family: 'Inter', sans-serif;
    }}
    
    .stApp {{
        background: {bg_color};
        background-image: 
            radial-gradient(at 0% 0%, rgba(0, 212, 255, 0.1) 0px, transparent 50%),
            radial-gradient(at 100% 100%, rgba(138, 43, 226, 0.1) 0px, transparent 50%);
    }}
    
    /* Glassmorphism Cards */
    .glass-card {{
        background: {card_bg};
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border-radius: 20px;
        border: 1px solid {border_color};
        padding: 2rem;
        box-shadow: {shadow};
        margin-bottom: 2rem;
        transition: all 0.3s ease;
    }}
    
    .glass-card:hover {{
        transform: translateY(-5px);
        box-shadow: 0 12px 40px 0 rgba(0, 212, 255, 0.2);
    }}
    
    /* Header Styling */
    .main-header {{
        text-align: center;
        padding: 3rem 0;
        background: linear-gradient(135deg, {accent_color}, #8a2be2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3.5rem;
        font-weight: 700;
        letter-spacing: -2px;
        margin-bottom: 1rem;
    }}
    
    .sub-header {{
        text-align: center;
        color: {secondary_text};
        font-size: 1.2rem;
        font-weight: 400;
        margin-bottom: 3rem;
    }}
    
    /* Feature Cards */
    .feature-box {{
        background: {card_bg};
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 1.5rem;
        border: 1px solid {border_color};
        margin: 1rem 0;
        display: flex;
        align-items: center;
        gap: 1rem;
        transition: all 0.3s ease;
    }}
    
    .feature-box:hover {{
        border-color: {accent_color};
        transform: translateX(10px);
    }}
    
    .feature-icon {{
        font-size: 2rem;
        min-width: 50px;
    }}
    
    /* Upload Section */
    .upload-section {{
        background: {card_bg};
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2rem;
        border: 2px dashed {border_color};
        text-align: center;
        transition: all 0.3s ease;
    }}
    
    .upload-section:hover {{
        border-color: {accent_color};
    }}
    
    /* Results Card */
    .result-card {{
        background: linear-gradient(135deg, {accent_color}22, #8a2be233);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2rem;
        border: 1px solid {accent_color}44;
        margin: 2rem 0;
    }}
    
    .match-score {{
        font-size: 4rem;
        font-weight: 700;
        background: linear-gradient(135deg, {accent_color}, #8a2be2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin: 1rem 0;
    }}
    
    /* Skill Pills */
    .skill-pill {{
        display: inline-block;
        background: {accent_color}33;
        color: {accent_color};
        padding: 0.5rem 1rem;
        border-radius: 20px;
        margin: 0.5rem;
        font-size: 0.9rem;
        font-weight: 500;
        border: 1px solid {accent_color}66;
    }}
    
    /* Sidebar */
    .css-1d391kg {{
        background: {card_bg};
        backdrop-filter: blur(10px);
    }}
    
    /* Theme Toggle Button */
    .theme-toggle {{
        position: fixed;
        bottom: 20px;
        right: 20px;
        background: {card_bg};
        backdrop-filter: blur(10px);
        border: 1px solid {border_color};
        border-radius: 50px;
        padding: 10px 20px;
        cursor: pointer;
        box-shadow: {shadow};
        z-index: 9999;
        display: flex;
        align-items: center;
        gap: 10px;
        font-size: 1.2rem;
        transition: all 0.3s ease;
    }}
    
    .theme-toggle:hover {{
        transform: scale(1.1);
        border-color: {accent_color};
    }}
    
    /* Footer */
    .footer {{
        text-align: center;
        padding: 2rem;
        color: {secondary_text};
        font-size: 0.9rem;
        margin-top: 4rem;
    }}
    
    /* Progress Bar */
    .stProgress > div > div > div {{
        background: linear-gradient(90deg, {accent_color}, #8a2be2);
    }}
    
    /* Buttons */
    .stButton>button {{
        background: linear-gradient(135deg, {accent_color}, #8a2be2);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }}
    
    .stButton>button:hover {{
        transform: scale(1.05);
        box-shadow: 0 5px 20px {accent_color}66;
    }}
    
    /* File Uploader */
    .stFileUploader {{
        background: {card_bg};
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 1rem;
    }}
    
    /* Hide Streamlit Branding */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# ==================== TEXT EXTRACTION ====================
def extract_text_from_pdf(file):
    try:
        return pdfminer.high_level.extract_text(io.BytesIO(file.read()))
    except:
        return ""

def extract_text_from_docx(file):
    try:
        return docx2txt.process(io.BytesIO(file.read()))
    except:
        return ""

def extract_text(file):
    if file.type == "application/pdf":
        return extract_text_from_pdf(file)
    elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        return extract_text_from_docx(file)
    else:
        return ""

# ==================== SKILL EXTRACTION ====================
def extract_skills(text):
    common_skills = [
        'Python', 'Java', 'C++', 'JavaScript', 'SQL', 'R', 'Machine Learning',
        'Deep Learning', 'NLP', 'Data Science', 'TensorFlow', 'PyTorch', 'Keras',
        'Scikit-learn', 'Pandas', 'NumPy', 'Matplotlib', 'Power BI', 'Tableau',
        'Excel', 'AWS', 'Azure', 'GCP', 'Docker', 'Kubernetes', 'Git', 'CI/CD',
        'Agile', 'Scrum', 'REST API', 'Flask', 'Django', 'React', 'Node.js',
        'MongoDB', 'PostgreSQL', 'MySQL', 'Data Analysis', 'Statistics',
        'Computer Vision', 'Time Series', 'A/B Testing', 'ETL', 'Big Data'
    ]
    
    found_skills = []
    text_lower = text.lower()
    
    for skill in common_skills:
        if skill.lower() in text_lower:
            found_skills.append(skill)
    
    return found_skills

# ==================== MATCHING LOGIC ====================
def calculate_match(resume_text, jd_text):
    vectorizer = TfidfVectorizer(stop_words='english')
    vectors = vectorizer.fit_transform([resume_text, jd_text])
    similarity = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
    return round(similarity * 100, 2)

# ==================== MAIN APP ====================
def main():
    load_css()
    
    # Header
    st.markdown('<h1 class="main-header">⚖️ Aequitas: AI Resume Auditor</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Intelligent & Fair Resume Screening System</p>', unsafe_allow_html=True)
    
    # Features Section
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-box">
            <div class="feature-icon">🎯</div>
            <div>
                <strong>Instant Match Calculation</strong><br>
                <small>Get precise resume-JD alignment scores</small>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-box">
            <div class="feature-icon">🔍</div>
            <div>
                <strong>Fair & Unbiased Screening</strong><br>
                <small>AI-powered objective evaluation</small>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-box">
            <div class="feature-icon">📊</div>
            <div>
                <strong>Detailed Skill Gap Analysis</strong><br>
                <small>Identify missing qualifications</small>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Upload Section
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### 📄 Upload Documents")
    
    col_resume, col_jd = st.columns(2)
    
    with col_resume:
        st.markdown("**Candidate Resume**")
        resume_file = st.file_uploader(
            "Upload Resume (PDF/DOCX)",
            type=['pdf', 'docx'],
            key='resume',
            help="Maximum file size: 5MB"
        )
    
    with col_jd:
        st.markdown("**Job Description**")
        jd_file = st.file_uploader(
            "Upload Job Description (PDF/DOCX)",
            type=['pdf', 'docx'],
            key='jd',
            help="Maximum file size: 5MB"
        )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Analysis Section
    if resume_file and jd_file:
        # File size validation (5MB limit)
        if resume_file.size > 5 * 1024 * 1024:
            st.error("❌ Resume file size exceeds 5MB limit")
            return
        if jd_file.size > 5 * 1024 * 1024:
            st.error("❌ Job Description file size exceeds 5MB limit")
            return
        
        with st.spinner("🔄 Analyzing documents..."):
            resume_text = extract_text(resume_file)
            jd_text = extract_text(jd_file)
            
            if not resume_text or not jd_text:
                st.error("❌ Failed to extract text from one or both documents")
                return
            
            match_score = calculate_match(resume_text, jd_text)
            resume_skills = extract_skills(resume_text)
            jd_skills = extract_skills(jd_text)
            missing_skills = list(set(jd_skills) - set(resume_skills))
        
        # Results
        st.markdown('<div class="result-card">', unsafe_allow_html=True)
        
        st.markdown("### 🎯 Match Results")
        st.markdown(f'<div class="match-score">{match_score}%</div>', unsafe_allow_html=True)
        st.markdown('<p style="text-align: center; font-size: 1.2rem; opacity: 0.8;">Resume-JD Compatibility</p>', unsafe_allow_html=True)
        
        st.progress(match_score / 100)
        
        if match_score >= 75:
            st.success("✅ **Strong Match** - Candidate is highly qualified for this role")
        elif match_score >= 50:
            st.warning("⚠️ **Moderate Match** - Candidate meets some requirements")
        else:
            st.error("❌ **Weak Match** - Significant skill gaps detected")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Skills Analysis
        col_found, col_missing = st.columns(2)
        
        with col_found:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("### ✅ Skills Found")
            if resume_skills:
                skills_html = "".join([f'<span class="skill-pill">{skill}</span>' for skill in resume_skills])
                st.markdown(skills_html, unsafe_allow_html=True)
            else:
                st.info("No common skills detected")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col_missing:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("### ❌ Missing Skills")
            if missing_skills:
                skills_html = "".join([f'<span class="skill-pill">{skill}</span>' for skill in missing_skills])
                st.markdown(skills_html, unsafe_allow_html=True)
            else:
                st.success("No skill gaps identified!")
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 📋 Control Panel")
        
        st.markdown("---")
        
        st.markdown("**Created By**")
        st.markdown("• Devansh Thakur")
        st.markdown("• Arpit Upadhyay")
        
        st.markdown("---")
        
        st.markdown("**Version:** v1.0 | Final Year Project")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Theme Toggle (Footer Button)
    theme_icon = "🌙" if st.session_state.theme == 'light' else "☀️"
    theme_text = "Dark Mode" if st.session_state.theme == 'light' else "Light Mode"
    
    st.markdown(f"""
    <div class="theme-toggle" onclick="document.querySelector('button[kind=primary]').click()">
        {theme_icon} {theme_text}
    </div>
    """, unsafe_allow_html=True)
    
    # Hidden button for theme toggle
    if st.button("Toggle Theme", key="theme_btn", type="primary"):
        toggle_theme()
        st.rerun()
    
    # Footer
    st.markdown("""
    <div class="footer">
        <p>Aequitas © 2024 | Built with Streamlit & Python</p>
        <p style="font-size: 0.8rem; opacity: 0.6;">Powered by TF-IDF & Cosine Similarity</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
