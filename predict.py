import sys
import os
import joblib
from src.preprocessor import clean_text
from src.heuristics import SpamHeuristicEngine


class SpamClassifier:
    """Hybrid Spam Classifier combining machine learning text vectorization and

    rule-based heuristic scam/phishing analysis (SpamAssassin-style).
    """
    def __init__(self, model_path: str = "models/spam_classifier_pipeline.joblib"):
        if not os.path.exists(model_path):
            raise FileNotFoundError(
                f"Model file '{model_path}' not found. Please run 'train.py' first."
            )
        self.pipeline = joblib.load(model_path)
        self.heuristics = SpamHeuristicEngine()

    def predict(self, raw_text: str) -> dict:
        """Predict whether an email/text is SPAM or HAM.

        Evaluates both the statistical ML pipeline and heuristic scam detectors.
        """
        cleaned = clean_text(raw_text)

        # ML model prediction & probability
        ml_pred_label = self.pipeline.predict([cleaned])[0]
        if hasattr(self.pipeline, "predict_proba"):
            probs = self.pipeline.predict_proba([cleaned])[0]
            ham_prob = float(probs[0])
            spam_prob = float(probs[1])
        else:
            ham_prob = 1.0 if ml_pred_label == 0 else 0.0
            spam_prob = 1.0 if ml_pred_label == 1 else 0.0

        # Heuristic analysis
        heuristic_res = self.heuristics.evaluate(raw_text)
        scam_heuristic_flag = heuristic_res["is_spam_suspicious"]

        # Hybrid decision: either ML identifies spam OR strong heuristic scam rules trigger
        if ml_pred_label == 1 or scam_heuristic_flag:
            final_label = "SPAM"
            # If triggered by heuristics, elevate confidence accordingly
            if scam_heuristic_flag and spam_prob < 0.85:
                confidence = max(0.95, spam_prob)
                spam_prob = confidence
                ham_prob = 1.0 - confidence
            else:
                confidence = spam_prob
        else:
            final_label = "HAM"
            confidence = ham_prob

        return {
            "prediction": final_label,
            "confidence": confidence,
            "spam_probability": spam_prob,
            "ham_probability": ham_prob,
            "heuristic_score": heuristic_res["score"],
            "triggered_rules": heuristic_res["triggered_rules"],
            "cleaned_text": cleaned
        }


def main():
    try:
        classifier = SpamClassifier()
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)

    # CLI direct argument mode
    if len(sys.argv) > 1:
        text = " ".join(sys.argv[1:])
        result = classifier.predict(text)
        print("=" * 65)
        print(f"Input:        {text}")
        print(f"Result:       [{result['prediction']}]")
        print(f"Confidence:   {result['confidence'] * 100:.2f}%")
        print(f"Probabilities: Ham: {result['ham_probability']*100:.2f}% | Spam: {result['spam_probability']*100:.2f}%")
        if result["triggered_rules"]:
            print("Detected Indicators:")
            for rule in result["triggered_rules"]:
                print(f"  - {rule}")
        print("=" * 65)
        return

    # Interactive console REPL
    print("=" * 65)
    print("       Email Spam Classifier - Interactive Console")
    print(" Type or paste an email message below. Type 'exit' to quit.")
    print("=" * 65)

    while True:
        try:
            user_input = input("\nEnter email/message: ").strip()
            if not user_input:
                continue
            if user_input.lower() in ("exit", "quit", "q"):
                print("Exiting classifier.")
                break

            res = classifier.predict(user_input)
            status_symbol = "[SPAM] 🚨" if res["prediction"] == "SPAM" else "[HAM]  ✅"
            print(f"--> Prediction:   {status_symbol}")
            print(f"--> Confidence:   {res['confidence'] * 100:.2f}%")
            print(f"    Details:      Ham: {res['ham_probability']*100:.1f}% | Spam: {res['spam_probability']*100:.1f}%")
            if res["triggered_rules"]:
                print("    Indicators:")
                for rule in res["triggered_rules"]:
                    print(f"      * {rule}")
        except (KeyboardInterrupt, EOFError):
            print("\nExiting.")
            break


if __name__ == "__main__":
    main()
