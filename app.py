import os
import email
from email import policy
from flask import Flask, render_template, request, jsonify
from predict import SpamClassifier

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024  # 5MB max upload limit

# Initialize classifier
classifier = SpamClassifier()

# Curated samples for one-click testing in the UI
PRESET_SAMPLES = {
    "419_scam": {
        "title": "419 Advance-Fee Wire Transfer",
        "text": """Hello, Greetings to you. Thanks for your quick response. A top VIP in one of the African Countries is in dire need of an entrepreneur or fund manager that can confidently receive and manage the sum of US$5.2 Billion with a reasonable return on investment annually. Please should you find this offer interesting, kindly revert back to me so we can discuss modalities that will perfect the transfer of the funds to any account you may deem safe. To make this happen, a meeting may be arranged where this transaction will be discussed one on one and measures will be streamlined for a successful completion of the transaction where applicable. Note: For your eligibility to handle this significant huge funds, you would have to own a company and operational bank account where the funds shall be transferred into for the investment purposes. Also, You must have a project plan to accommodate and invest the funds. Please feel free to contact me and i would be happy to provide further details. Regards, Mr. William Schneider"""
    },
    "copyright_phishing": {
        "title": "DMCA / Copyright Malware Phishing",
        "text": """Hello, I am a professional photographer and the legal owner of the copyrighted images used on your website without my explicit permission or license. This unauthorized use constitutes a direct violation of intellectual property laws. I have documented the infringing pages and compiled them into a formal legal complaint. To avoid immediate legal action and a formal lawsuit for statutory damages, I demand that you review the infringing material and remove it from your servers immediately. You can view the specific list of copyrighted assets and the legal notice in the cloud repository link below: [👉 View Copyright Infringement Notice Document (PDF)] If the material is not removed within 48 hours, my attorney will proceed with filing a formal Digital Millennium Copyright Act (DMCA) takedown notice and pursuing financial damages. Sincerely, Alex Rivera, Rivera Photography Studios"""
    },
    "fake_invoice": {
        "title": "Geek Squad / Norton Renewal Scam",
        "text": """INVOICE #9842 OVERDUE: Your subscription for Geek Squad BestBuy Protection has been renewed for $499.99 auto-debited from your checking account. If you did not authorize this charge, call our toll-free cancellation department immediately at +1-800-555-0199 for an instant refund within 24 hours."""
    },
    "legit_meeting": {
        "title": "Legitimate Project Sync",
        "text": """Hi team, Please find attached the updated quarterly financial report for review. We will walk through the budget allocations and expense forecasts during tomorrow morning's staff meeting at 10:00 AM. Let me know if you have any questions beforehand. Best regards, Sarah Jenkins"""
    },
    "legit_inquiry": {
        "title": "Legitimate Business Inquiry",
        "text": """Dear John, Thanks for reaching out regarding our consulting services. I would be happy to schedule a 30-minute introductory call next Tuesday or Wednesday afternoon to discuss your company's requirements and see how we can assist. Does 2:00 PM EST work for your calendar? Looking forward to speaking with you. Warm regards, Michael"""
    }
}


def parse_email_content(raw_bytes: bytes, filename: str) -> str:
    """Extract plain text body or content from raw bytes or .eml / .txt files."""
    if filename.lower().endswith(".eml"):
        try:
            msg = email.message_from_bytes(raw_bytes, policy=policy.default)
            subject = msg.get("subject", "")
            sender = msg.get("from", "")
            body = ""
            if msg.is_multipart():
                for part in msg.walk():
                    content_type = part.get_content_type()
                    content_disposition = str(part.get("Content-Disposition"))
                    if content_type == "text/plain" and "attachment" not in content_disposition:
                        payload = part.get_payload(decode=True)
                        if payload:
                            body += payload.decode("utf-8", errors="replace") + "\n"
            else:
                payload = msg.get_payload(decode=True)
                if payload:
                    body = payload.decode("utf-8", errors="replace")
                else:
                    body = str(msg.get_payload())

            combined = f"Subject: {subject}\nFrom: {sender}\n\n{body}".strip()
            return combined if combined else body
        except Exception:
            pass

    # Fallback to direct text decoding
    for enc in ["utf-8", "latin-1", "cp1252", "iso-8859-1"]:
        try:
            return raw_bytes.decode(enc)
        except UnicodeDecodeError:
            continue

    return raw_bytes.decode("utf-8", errors="replace")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/samples", methods=["GET"])
def get_samples():
    return jsonify(PRESET_SAMPLES)


@app.route("/api/classify", methods=["POST"])
def classify():
    content = ""

    # Check for file upload
    if "file" in request.files:
        uploaded_file = request.files["file"]
        if uploaded_file.filename:
            file_bytes = uploaded_file.read()
            content = parse_email_content(file_bytes, uploaded_file.filename)

    # Check for direct JSON body or form text
    if not content:
        if request.is_json:
            data = request.get_json()
            content = data.get("text", "")
        else:
            content = request.form.get("text", "")

    content = content.strip()
    if not content:
        return jsonify({"error": "No email or text content provided for analysis."}), 400

    result = classifier.predict(content)

    # Calculate supplementary readability / content metadata
    word_count = len(content.split())
    char_count = len(content)

    return jsonify({
        "success": True,
        "prediction": result["prediction"],
        "confidence": result["confidence"],
        "spam_probability": result["spam_probability"],
        "ham_probability": result["ham_probability"],
        "heuristic_score": result.get("heuristic_score", 0.0),
        "triggered_rules": result.get("triggered_rules", []),
        "word_count": word_count,
        "char_count": char_count,
        "preview": content[:180] + ("..." if len(content) > 180 else "")
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"Starting Email Spam Classifier Web Interface on http://127.0.0.1:{port}")
    app.run(host="127.0.0.1", port=port, debug=False)
