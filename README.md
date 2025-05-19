🧠 AI-Powered ATS Tool

An AI-driven Applicant Tracking System (ATS) that matches multiple resumes against a given job description using NLP and TF-IDF. 
Built with Streamlit, this tool helps recruiters make smarter hiring decisions quickly and efficiently.

🚀 Features
✅ Upload multiple resumes in PDF format

📝 Match resumes with any custom job description

📊 Get match scores using TF-IDF cosine similarity

🏆 Highlight top matching resumes

🔍 View full resume content (cleaned and normalized)

🧠 Uses Spacy, NLTK, and Sklearn for NLP

🎨 Clean, animated UI with custom styling and background

🔒 Detects and removes duplicate resumes

📸 Screenshot
![image](https://github.com/user-attachments/assets/dafff5dd-e12a-4f97-bb11-c77d88d02794)



🛠 Tech Stack

Frontend: Streamlit

NLP: spaCy, NLTK, TF-IDF (Scikit-learn)

PDF Parsing: pdfplumber, PyPDF2

Similarity Scoring: Cosine Similarity (Sklearn)

Styling: HTML + CSS in Streamlit

📂 Directory Structure
bash
Copy
Edit
├── ATS/
│   ├── app.py              # Main Streamlit App
│   ├── AJ_LOGO.jpg         # Sidebar logo
│   ├── background3.jpg     # Background image
│   ├── requirements.txt    # All Python dependencies
│   └── README.md           # This file
✅ Installation


1. Clone the repository
bash
Copy
Edit
git clone https://github.com/AJ-BASKAR/ATS.git
cd ATS
2. Create virtual environment (optional but recommended)
bash
Copy
Edit
python -m venv venv
venv\Scripts\activate  # For Windows
# or
source venv/bin/activate  # For Linux/macOS
3. Install dependencies
bash
Copy
Edit
pip install -r requirements.txt
▶️ Run the App
bash
Copy
Edit
streamlit run app.py
🔍 How It Works
Upload one or more PDF resumes.

Enter a job description.

Click "Predict Match Scores".

The app will:

Extract and clean text from PDFs

Compare it with the job description using TF-IDF + Cosine Similarity

Display match score and resume preview

📦 Dependencies
text
Copy
Edit
streamlit
pdfplumber
PyPDF2
spacy
nltk
scikit-learn
Pillow
Make sure to run:
python -m nltk.downloader stopwords
python -m spacy download en_core_web_sm

👨‍💻** Author**

AJ BASKAR
🦄 Passionate about AI, ML, and intuitive user experiences.
📧 Connect on LinkedIn (Optional)

📝 License
This project is licensed under the MIT License - see the LICENSE file for details.
