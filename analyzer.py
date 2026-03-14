import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.2:1b"

SYSTEM_PROMPT = """You are a cybersecurity analyst specializing in phishing detection.
Analyze the email provided and return ONLY a valid JSON object — no explanation, no markdown, no extra text.

The JSON must have exactly these keys:
{
  "phishing_score": <integer 0-100>,
  "verdict": "<Safe | Suspicious | Phishing>",
  "phishing_type": "<one of: Credential Harvesting | CEO/BEC Fraud | Invoice Scam | Delivery Notification Scam | Lottery/Prize Scam | Tech Support Scam | Generic Spam | Not Phishing>",
  "red_flags": [<list of strings describing each red flag found>],
  "urgency_language": <true | false>,
  "suspicious_links": <true | false>,
  "sender_spoofing_risk": "<Low | Medium | High>",
  "triggered_sentences": [<list of exact short quotes from the email that triggered red flags>],
  "summary": "<2-3 sentence plain English explanation of your verdict>"
}

Phishing type guide:
- Credential Harvesting: asks for login, password, card details, SSN
- CEO/BEC Fraud: impersonates executive, requests urgent wire transfer or gift cards
- Invoice Scam: fake invoice or payment request from unknown vendor
- Delivery Notification Scam: fake package delivery, asks to pay fee or verify address
- Lottery/Prize Scam: claims user won something, asks for personal info or fee
- Tech Support Scam: fake Microsoft/Apple alert, asks to call number or install software
- Generic Spam: unsolicited promotional or irrelevant bulk email
- Not Phishing: legitimate email with no malicious indicators

Scoring guide:
- 0-30: Likely safe
- 31-60: Suspicious, needs review
- 61-100: Almost certainly phishing
"""

def analyze_email(email_text: str) -> dict:
    """
    Send email text to local Llama model via Ollama and return threat analysis.
    """
    prompt = f"Analyze this email for phishing indicators:\n\n{email_text}"

    payload = {
        "model": MODEL,
        "prompt": prompt,
        "system": SYSTEM_PROMPT,
        "stream": False,
        "options": {
            "temperature": 0.1,
            "top_p": 0.9
        }
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=60)
        response.raise_for_status()

        raw_output = response.json().get("response", "")

        # Strip markdown code fences if model adds them
        clean = raw_output.strip()
        if clean.startswith("```"):
            clean = clean.split("```")[1]
            if clean.startswith("json"):
                clean = clean[4:]
        clean = clean.strip()

        result = json.loads(clean)
        return {"success": True, "data": result}

    except requests.exceptions.ConnectionError:
        return {
            "success": False,
            "error": "Cannot connect to Ollama. Make sure it is running: run 'ollama serve' in a terminal."
        }
    except requests.exceptions.Timeout:
        return {
            "success": False,
            "error": "Ollama took too long to respond. Try a shorter email or restart Ollama."
        }
    except json.JSONDecodeError:
        return {
            "success": False,
            "error": "Model returned invalid JSON. Try again — this is rare with Llama 3.1."
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def get_score_color(score: int) -> str:
    if score <= 30:
        return "green"
    elif score <= 60:
        return "orange"
    else:
        return "red"