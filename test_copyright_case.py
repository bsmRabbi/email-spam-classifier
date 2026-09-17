from predict import SpamClassifier

c = SpamClassifier()

msg = (
    "Hello,I am a professional photographer and the legal owner of the copyrighted images used on your website "
    "without my explicit permission or license.This unauthorized use constitutes a direct violation of intellectual "
    "property laws. I have documented the infringing pages and compiled them into a formal legal complaint.To avoid "
    "immediate legal action and a formal lawsuit for statutory damages, I demand that you review the infringing material "
    "and remove it from your servers immediately. You can view the specific list of copyrighted assets and the legal notice "
    "in the cloud repository link below:[👉 View Copyright Infringement Notice Document (PDF)]If the material is not removed "
    "within 48 hours, my attorney will proceed with filing a formal Digital Millennium Copyright Act (DMCA) takedown "
    "notice and pursuing financial damages.Sincerely,Alex RiveraRivera Photography Studios"
)

res = c.predict(msg)
print("\n" + "=" * 70)
print("Input Preview: [Copyright / DMCA Takedown Notice Phishing]")
print(f"Result:       [{res['prediction']}]")
print(f"Confidence:   {res['confidence'] * 100:.2f}%")
print(f"Probabilities: Ham: {res['ham_probability']*100:.2f}% | Spam: {res['spam_probability']*100:.2f}%")
print(f"Heuristic Score: {res['heuristic_score']}")
print("Triggered Indicators:")
for rule in res['triggered_rules']:
    print(f"  * {rule}")
print("=" * 70 + "\n")
