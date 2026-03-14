import re
import requests
import base64
import os
from dotenv import load_dotenv

load_dotenv()

VIRUSTOTAL_API_KEY = os.getenv("VIRUSTOTAL_API_KEY")
VT_BASE_URL = "https://www.virustotal.com/api/v3"


def extract_urls(text: str) -> list:
    """Extract all URLs from email text."""
    pattern = r'https?://[^\s<>"\')\]]+'
    urls = re.findall(pattern, text)
    return list(set(urls))  # remove duplicates


def check_url(url: str) -> dict:
    """Check a single URL against VirusTotal."""
    if not VIRUSTOTAL_API_KEY:
        return {"url": url, "error": "No VirusTotal API key found in .env file."}

    try:
        # VirusTotal requires URL to be base64 encoded
        url_id = base64.urlsafe_b64encode(url.encode()).decode().strip("=")

        headers = {"x-apikey": VIRUSTOTAL_API_KEY}
        response = requests.get(
            f"{VT_BASE_URL}/urls/{url_id}",
            headers=headers,
            timeout=15
        )

        if response.status_code == 404:
            # URL not in VT database yet, submit it for analysis
            submit = requests.post(
                f"{VT_BASE_URL}/urls",
                headers=headers,
                data={"url": url},
                timeout=15
            )
            if submit.status_code == 200:
                return {
                    "url": url,
                    "status": "submitted",
                    "message": "URL submitted to VirusTotal for first-time analysis. Check again in a minute.",
                    "malicious": 0,
                    "total_engines": 0,
                    "verdict": "Unknown"
                }
            else:
                return {"url": url, "error": "Could not submit URL to VirusTotal."}

        if response.status_code != 200:
            return {"url": url, "error": f"VirusTotal returned status {response.status_code}"}

        data = response.json()
        stats = data.get("data", {}).get("attributes", {}).get("last_analysis_stats", {})

        malicious = stats.get("malicious", 0)
        suspicious = stats.get("suspicious", 0)
        total = sum(stats.values())
        flagged = malicious + suspicious

        if malicious >= 5:
            verdict = "Malicious"
        elif flagged > 0:
            verdict = "Suspicious"
        else:
            verdict = "Clean"

        return {
            "url": url,
            "malicious": malicious,
            "suspicious": suspicious,
            "flagged": flagged,
            "total_engines": total,
            "verdict": verdict,
            "vt_link": f"https://www.virustotal.com/gui/url/{url_id}"
        }

    except requests.exceptions.Timeout:
        return {"url": url, "error": "VirusTotal request timed out."}
    except Exception as e:
        return {"url": url, "error": str(e)}


def check_all_urls(email_text: str) -> list:
    """Extract and check all URLs found in the email."""
    urls = extract_urls(email_text)
    if not urls:
        return []
    results = []
    for url in urls[:5]:  # limit to 5 URLs to stay within free tier
        result = check_url(url)
        results.append(result)
    return results