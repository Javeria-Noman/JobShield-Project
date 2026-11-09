#An AI-driven Streamlit application for real-time online job scam and fraudulent listing detection.

** Overview**

Fake job postings cause financial loss, phishing, and identity theft. Job Shielder analyzes a job description (or a job link / email text) and classifies it as Legitimate, Suspicious, or Scam. If the model cannot decide confidently, it returns Uncertain instead of guessing.

The app gives users an instant safety score, a color-coded risk level, and a summary of red flags before they apply or share personal details.

✨ Features
Instant Job Analysis: paste a job description, URL (LinkedIn or other job platforms), or email text
Visual Risk Score: safety gauge with color-coded levels (Safe, Caution, High Risk)
Red-Flag Extraction: highlights suspicious phrases such as "No experience needed - $5000/week" or payment requests
Live SOAP API integration for real-time checks
Uncertain result when confidence is low
Interactive Streamlit dashboard
🧠 How It Works
User Input → NLP Preprocessing → ML Classification (SVM) → Risk Output
User Input: job description / URL / email text via the Streamlit UI
NLP Preprocessing: text cleaning, tokenization, stop-word removal, TF-IDF vectorization
ML Classification: supervised model predicts legitimate vs. fraudulent patterns
Risk Output: safety score gauge, threat level tag, and red-flag summary

The prediction is also exposed through a SOAP API, so other applications can send a job description and get the verdict in real time.

🔌 API (SOAP)

The project uses a SOAP (Simple Object Access Protocol) web service for live job verification. The client sends an XML request containing the job text or link, and the service replies with an XML response containing the verdict.

Request (example):

xml
<?xml version="1.0" encoding="UTF-8"?>
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
  <soapenv:Body>
    <CheckJob>
      <jobText>Earn $5000 weekly from home. No experience needed. Pay registration fee.</jobText>
    </CheckJob>
  </soapenv:Body>
</soapenv:Envelope>

Response (example):

xml
<?xml version="1.0" encoding="UTF-8"?>
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
  <soapenv:Body>
    <CheckJobResponse>
      <prediction>Scam</prediction>
      <confidence>0.93</confidence>
    </CheckJobResponse>
  </soapenv:Body>
</soapenv:Envelope>

Possible prediction values: Legitimate, Suspicious, Scam, Uncertain.

Update the endpoint, operation name, and field names above to match your actual WSDL.

🚦 Risk Levels
Level	Category	Indicators
1	Legitimate	Verified company domain, detailed role requirements, realistic pay, standard contact channels
2	Suspicious / Caution	Generic email domains (Gmail/Yahoo), vague description, inflated salary, missing company profile links
3	Confirmed Scam	Upfront processing fees, requests for sensitive financial info, instant unverified offers via messaging apps

**Model Performance**
Metric	Score
Accuracy	96.5%
Precision	94.2%
F1-Score	95.1%

⚙️ Challenges & Solutions
Challenge	Solution
Imbalanced dataset (legitimate posts far outnumber fake ones)	SMOTE and adjusted class weighting during training
Scammers keep changing their phrasing	TF-IDF n-grams and context-aware feature extraction
🛠️ Tech Stack
Language: Python 3.x
Frontend: Streamlit
API: SOAP (XML web service)
ML & NLP: scikit-learn (SVM), NLTK, pandas, NumPy

📂 Project Structure
job-shielder/
│
├── data/            # Dataset

├── model/             # Saved model & TF-IDF vectorizer (.pkl)

├── notebooks/         # Training & experiments

├── app.py             # Streamlit app

├── requirements.txt

└── README.md

** Installation & Setup**
bash
git clone https://github.com/<javeria-noman>/job-shielder.git
cd job-shielder

python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

pip install -r requirements.txt
streamlit run app.py
💻 Usage
Open the app in your browser (default: http://localhost:8501)
Paste the job description, a job link, or email text
Click analyze
View the verdict, safety score, and red flags
⚠️ Limitations
Predictions are based on text patterns, so well-written scams can slip through
Some platforms (e.g., LinkedIn) may block scraping or require login
Results are a guide, not a guarantee. Always verify the company independently
🔮 Future Work
LLM Integration: transformer models for deeper analysis of sophisticated scam copy
Browser Extension: Chrome extension to auto-verify postings on LinkedIn and Indeed
Domain URL Checker: WHOIS domain-age lookup to flag newly registered scam sites
👥 Team
Sidra Sultan
Noor-ul-Aien
Sadaf Ahmed
An AI-driven Streamlit application for real-time online job scam and fraudulent listing detection.

📌 Overview

Fake job postings cause financial loss, phishing, and identity theft. Job Shielder analyzes a job description (or a job link / email text) and classifies it as Legitimate, Suspicious, or Scam. If the model cannot decide confidently, it returns Uncertain instead of guessing.

The app gives users an instant safety score, a color-coded risk level, and a summary of red flags before they apply or share personal details.

✨ Features
Instant Job Analysis: paste a job description, URL (LinkedIn or other job platforms), or email text
Visual Risk Score: safety gauge with color-coded levels (Safe, Caution, High Risk)
Red-Flag Extraction: highlights suspicious phrases such as "No experience needed - $5000/week" or payment requests
Live SOAP API integration for real-time checks
Uncertain result when confidence is low
Interactive Streamlit dashboard
🧠 How It Works
User Input → NLP Preprocessing → ML Classification (SVM) → Risk Output
User Input: job description / URL / email text via the Streamlit UI
NLP Preprocessing: text cleaning, tokenization, stop-word removal, TF-IDF vectorization
ML Classification: supervised model predicts legitimate vs. fraudulent patterns
Risk Output: safety score gauge, threat level tag, and red-flag summary

The prediction is also exposed through a SOAP API, so other applications can send a job description and get the verdict in real time.

🔌 API (SOAP)

The project uses a SOAP (Simple Object Access Protocol) web service for live job verification. The client sends an XML request containing the job text or link, and the service replies with an XML response containing the verdict.

Request (example):

xml
<?xml version="1.0" encoding="UTF-8"?>
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
  <soapenv:Body>
    <CheckJob>
      <jobText>Earn $5000 weekly from home. No experience needed. Pay registration fee.</jobText>
    </CheckJob>
  </soapenv:Body>
</soapenv:Envelope>

Response (example):

xml
<?xml version="1.0" encoding="UTF-8"?>
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
  <soapenv:Body>
    <CheckJobResponse>
      <prediction>Scam</prediction>
      <confidence>0.93</confidence>
    </CheckJobResponse>
  </soapenv:Body>
</soapenv:Envelope>

Possible prediction values: Legitimate, Suspicious, Scam, Uncertain.

Update the endpoint, operation name, and field names above to match your actual WSDL.

🚦 Risk Levels
Level	Category	Indicators
1	Legitimate	Verified company domain, detailed role requirements, realistic pay, standard contact channels
2	Suspicious / Caution	Generic email domains (Gmail/Yahoo), vague description, inflated salary, missing company profile links
3	Confirmed Scam	Upfront processing fees, requests for sensitive financial info, instant unverified offers via messaging apps
📊 Model Performance
Metric	Score
Accuracy	96.5%
Precision	94.2%
F1-Score	95.1%
⚙️ Challenges & Solutions
Challenge	Solution
Imbalanced dataset (legitimate posts far outnumber fake ones)	SMOTE and adjusted class weighting during training
Scammers keep changing their phrasing	TF-IDF n-grams and context-aware feature extraction
🛠️ Tech Stack
Language: Python 3.x
Frontend: Streamlit
API: SOAP (XML web service)
ML & NLP: scikit-learn (SVM), NLTK, pandas, NumPy
📂 Project Structure
job-shielder/
│
├── data/              # Dataset
├── model/             # Saved model & TF-IDF vectorizer (.pkl)
├── notebooks/         # Training & experiments
├── app.py             # Streamlit app
├── requirements.txt
└── README.md
🚀 Installation & Setup
bash
git clone https://github.com/<your-username>/job-shielder.git
cd job-shielder

python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

pip install -r requirements.txt
streamlit run app.py
💻 Usage
Open the app in your browser (default: http://localhost:8501)
Paste the job description, a job link, or email text
Click analyze
View the verdict, safety score, and red flags
⚠️ Limitations
Predictions are based on text patterns, so well-written scams can slip through
Some platforms (e.g., LinkedIn) may block scraping or require login
Results are a guide, not a guarantee. Always verify the company independently
🔮 Future Work
LLM Integration: transformer models for deeper analysis of sophisticated scam copy
Browser Extension: Chrome extension to auto-verify postings on LinkedIn and Indeed
Domain URL Checker: WHOIS domain-age lookup to flag newly registered scam sites
👥 Team
Javeria Noman
Sidra Sultan
Noor-ul-Aien
Sadaf Ahmed
Rida Khan
