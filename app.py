import os
from flask import Flask, request, jsonify, render_template
from analyzer import analyze_email
from url_checker import check_all_urls

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    email_text = data.get("email", "").strip()

    if not email_text:
        return jsonify({"success": False, "error": "No email text provided."}), 400

    if len(email_text) > 5000:
        return jsonify({"success": False, "error": "Email too long. Keep it under 5000 characters."}), 400

    result = analyze_email(email_text)

    if result["success"]:
        url_results = check_all_urls(email_text)
        result["data"]["url_scan"] = url_results

    return jsonify(result)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)

Save it, then push:
git add .
git commit -m "Fix Railway port binding"
git push