# AI Phishing Email Detector

🌐 **Live Demo:** https://phishing-detector-production-4409.up.railway.app
🐙 **GitHub:** https://github.com/HarshAsolkar/phishing-detector

An AI-powered phishing email detector built as a SOC analyst portfolio project. Paste any suspicious email and get a full threat report in seconds — powered by Llama 3.1 via Groq API and VirusTotal.

---

## What it does

Paste any suspicious email and get an instant structured threat report:

- **Phishing score** (0–100) with a Safe / Suspicious / Phishing verdict
- **Attack type classification** — Credential Harvesting, CEO/BEC Fraud, Invoice Scam, Delivery Notification Scam, Lottery/Prize Scam, Tech Support Scam
- **Red flags list** — specific issues detected in the email
- **Triggered sentences** — exact sentences from the email that raised suspicion
- **VirusTotal URL scan** — every link checked against 90+ antivirus engines
- **PDF incident report** — one-click download, ready for SOC ticket documentation
- **Urgency language detection** — pressure tactics commonly used in phishing
- **Sender spoofing risk** — Low / Medium / High assessment
- **Plain English summary** — what an analyst would conclude

---

## Tech stack

| Component | Tool |
|---|---|
| LLM | Llama 3.1 8B (via Groq API) |
| Backend | Python 3.10+ / Flask |
| Frontend | HTML / CSS / Vanilla JS |
| URL Scanning | VirusTotal API |
| PDF Export | jsPDF |
| Deployment | Railway |

---

## Live Demo

Try it here — no installation needed:
**https://phishing-detector-production-4409.up.railway.app**

Click **Load sample phishing email** to test immediately.

---

## Local Setup

### 1. Clone this repo

```bash
git clone https://github.com/HarshAsolkar/phishing-detector.git
cd phishing-detector
```

### 2. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 3. Create a `.env` file

```
GROQ_API_KEY=your_groq_api_key_here
VIRUSTOTAL_API_KEY=your_virustotal_api_key_here
```

Get your free Groq API key at: https://console.groq.com
Get your free VirusTotal API key at: https://virustotal.com

### 4. Run the app

```bash
python app.py
```

Open your browser at: **http://localhost:5000**

---

## Usage

1. Paste a suspicious email (headers + body) into the text area
2. Click **Analyze Email**
3. Wait 5–6 seconds for the AI to process
4. Review the full threat report
5. Click **Download Incident Report** to export as PDF

---

## Sample test emails

The `sample_emails/` folder contains:
- `phishing_1.txt` — classic PayPal impersonation phishing
- `legit_1.txt` — legitimate GitHub notification

---

## Why this project

Phishing detection is one of the most common tasks in a Tier 1 SOC analyst role. This project demonstrates:

- Practical LLM integration into a security workflow
- Prompt engineering for structured threat analysis output
- Attack type classification using AI reasoning
- Live URL reputation checking via VirusTotal
- Production-ready deployment on Railway
- PDF report generation for SOC ticket documentation

---

## Project structure

```
phishing-detector/
├── app.py              # Flask server and API routes
├── analyzer.py         # Groq API integration and prompt logic
├── url_checker.py      # VirusTotal URL scanning
├── requirements.txt
├── Procfile            # Railway deployment config
├── README.md
├── templates/
│   └── index.html      # Frontend UI
└── sample_emails/
    ├── phishing_1.txt
    └── legit_1.txt
```

---

## Built by

Harsh Asolkar — Final year BSc Computer Science, Kirti M Doongursee College, Mumbai University 
Interests: Cybersecurity, SOC Analysis, AI-powered security tools
LinkedIn: https://www.linkedin.com/in/harshasolkar

---

## License

MIT License — feel free to fork and extend.
