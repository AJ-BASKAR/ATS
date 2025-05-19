# 🔧 Prevent torch.classes error with Streamlit file watcher
import os
os.environ["STREAMLIT_FILE_WATCHER_TYPE"] = "none"

# 🚀 Imports
import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from PIL import Image
import hashlib
import base64
import html
from PyPDF2 import PdfReader  # Install with: pip install PyPDF2
from docx import Document




# --- PAGE CONFIGURATION ---
st.set_page_config(page_title= "ATS Tool", page_icon="🗃️", layout="wide")


st.markdown("""
    <style>
    .glow {
        font-size: 60px;
        font-weight: bold;
        color: white;
        text-align: center;
        margin-top: 20px;
        animation: glow 1.5s ease-in-out infinite alternate;
    }

    @keyframes glow {
        from {
            text-shadow: 0 0 10px #00ffff, 0 0 20px #00ffff, 0 0 30px #00ffff;
        }
        to {
            text-shadow: 0 0 20px #ff00ff, 0 0 30px #ff00ff, 0 0 40px #ff00ff;
        }
    }

    body {
        background-color: #0f0f0f;
        color: white;
    }
    </style>

    <div class="glow"> 📄 AI-Powered ATS Tool</div>
""", unsafe_allow_html=True)

# --- IMAGE ENCODING FUNCTION ---
def get_image_base64(img_path):
    if os.path.exists(img_path):
        with open(img_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode()
    else:
        st.warning(f"⚠️ Image not found at path: {img_path}")
        return None

# --- BACKGROUND IMAGE FUNCTION ---
def add_bg_from_local(img_path):
    if os.path.exists(img_path):
        with open(img_path, "rb") as img_file:
            encoded = base64.b64encode(img_file.read()).decode()
        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: url("data:image/jpg;base64,{encoded}");
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                background-attachment: fixed;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )
    else:
        st.warning(f"⚠️ Background image not found at path: {img_path}")
        # Fallback background color
        st.markdown(
            """
            <style>
            .stApp {
                background-color: #f0f2f6;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

# --- PATHS ---
logo_path = "AJ_LOGO.jpg"
background_path = "background3.jpg"

# --- LOAD IMAGES ---
image_base64 = get_image_base64(logo_path)
add_bg_from_local(background_path)

# --- SIDEBAR LOGO ---
if image_base64:
    st.sidebar.markdown(f"""
        <style>
        .round-logo {{
            border-radius: 50%;
            width: 150px;
            height: 150px;
            object-fit: cover;
            display: block;
            margin-left: auto;
            margin-right: auto;
            margin-top: 20px;
        }}
        </style>
        <img src="data:image/jpeg;base64,{image_base64}" class="round-logo" />
    """, unsafe_allow_html=True)

# --- SIDEBAR BANNER ---
st.sidebar.markdown("""
    <div style="
        background: linear-gradient(135deg, #667eea, #764ba2);
        padding: 20px;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-top: 20px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.2);
    ">
        <h2 style="margin-bottom: 10px;">🚀 AJ BASKAR's ATS</h2>
        <p style="font-size: 16px; color: #e0e0e0;">
            AI-powered resume matcher for smarter hiring decisions
        </p>
        <hr style="border: 0.5px solid #ddd; margin: 10px 0;">
        <p style="font-size: 14px;">Created ❤️ by  <b> AJ BASKAR 🦄</b></p>
    </div>
""", unsafe_allow_html=True)

# --- CUSTOM STYLES ---
st.markdown("""
    <style>
    .score-card {
        background: linear-gradient(135deg, #667eea, #764ba2);
        border-radius: 15px;
        padding: 20px;
        color: white;
        margin-bottom: 20px;
        animation: gradient 3s ease infinite;
        background-size: 400% 400%;
    }

    @keyframes gradient {
        0% {background-position: 0% 50%;}
        50% {background-position: 100% 50%;}
        100% {background-position: 0% 50%;}
    }

    .match-tag {
        font-size: 18px;
        font-weight: bold;
        padding: 5px 10px;
        border-radius: 5px;
        display: inline-block;
        margin-bottom: 10px;
    }

    .high { background-color: #28a745; }   /* Green */
    .medium { background-color: #ffc107; } /* Yellow */
    .low { background-color: #dc3545; }    /* Red */

    .view-details {
        background-color: rgba(255,255,255,0.1);
        padding: 10px;
        border-radius: 10px;
        margin-top: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# --- PROCESS RESUME FUNCTION ---

def process_resume(uploaded_file):
    try:
        pdf = PdfReader(uploaded_file)
        text = ""
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        return text.lower().strip()
    except Exception as e:
        raise ValueError(f"Could not process PDF file: {e}")

# --- SIMILARITY FUNCTION ---
def match_resume_with_job(resume_text, job_description):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([job_description, resume_text])
    similarity_score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()[0]
    return round(similarity_score * 100, 2)

# --- DUPLICATE DETECTION FUNCTION ---
def get_text_hash(text):
    return hashlib.md5(text.encode()).hexdigest()

# --- MAIN UI ---
st.title("🗃️ ATS Tool")
st.subheader("Upload Multiple Resumes & Match with Job Description")

uploaded_files = st.file_uploader("📎 Upload Resumes (PDF format only)", type="pdf", accept_multiple_files=True)
job_description = st.text_area("📝 Enter Job Description")

# Checkbox to enable top resume filtering
enable_top_n = st.checkbox("✅ Show only top matching resumes")

if enable_top_n:
    top_n = st.slider("How many top resumes do you want to display?", 1, 10, 5)
else:
    top_n = None

# --- MATCH SCORE LOGIC ---
if st.button("🔍 Predict Match Scores"):
    if uploaded_files and job_description.strip():
        st.subheader("📌 Resume Match Scores")

        seen_hashes = set()
        results = []

        for file in uploaded_files:
            try:
                cleaned_resume_text = process_resume(file)
                text_hash = get_text_hash(cleaned_resume_text)

                if text_hash in seen_hashes:
                    continue
                seen_hashes.add(text_hash)

                score = match_resume_with_job(cleaned_resume_text, job_description)
                results.append((file.name, score, cleaned_resume_text))

            except Exception as e:
                st.error(f"❌ Error processing {file.name}: {e}")

        if not results:
            st.warning("⚠️ All resumes appear to be duplicates or could not be processed.")
        else:
            results.sort(key=lambda x: x[1], reverse=True)
            st.success(f"✅ {len(results)} unique resume(s) evaluated.")

            display_count = top_n if top_n else len(results)
            for idx, (name, score, text) in enumerate(results[:display_count]):
                score_class = "high" if score >= 75 else "medium" if score >= 50 else "low"
                top_label = "🏆 Top Match — " if idx == 0 else ""

                safe_text = html.escape(text).replace('\n', '<br>')

                st.markdown(f"""
                    <div class="score-card">
                        <div class="match-tag {score_class}">🎯 {top_label}Match Score: {score}%</div>
                        <h4>📄 {name}</h4>
                        <details class="view-details">
                            <summary style='cursor: pointer;'>🔍 View Resume Details</summary>
                            <div style="margin-top:10px;">{safe_text}</div>
                        </details>
                    </div>
                """, unsafe_allow_html=True)
    else:
        st.warning("⚠️ Please upload at least one resume and enter a job description to get match scores.")
