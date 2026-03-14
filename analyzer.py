import json
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL = "llama-3.1-8b-instant"

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
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Analyze this email for phishing indicators:\n\n{email_text}"}
            ],
            temperature=0.1,
            max_tokens=1000
        )

        raw_output = response.choices[0].message.content.strip()

        if raw_output.startswith("```"):
            raw_output = raw_output.split("```")[1]
            if raw_output.startswith("json"):
                raw_output = raw_output[4:]
        raw_output = raw_output.strip()

        result = json.loads(raw_output)
        return {"success": True, "data": result}

    except json.JSONDecodeError:
        return {
            "success": False,
            "error": "Model returned invalid JSON. Please try again."
        }
    except Exception as e:
        return {"success": False, "error": str(e)}