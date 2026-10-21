"""
SMS Spam Detection & Text Analysis Module
Processes raw SMS messages, applies NLP text preprocessing,
and predicts whether an SMS is Ham (Legitimate) or Spam using a trained Machine Learning model.
"""

import os
import re
import joblib

SPAM_TRIGGER_WORDS = [
    "urgent", "congratulations", "winner", "won", "claim", "free", "prize",
    "gift card", "reward", "lottery", "cash", "deposit", "refund", "credit",
    "loan", "approved", "suspended", "locked", "expire", "unauthorized",
    "verify", "verification", "security alert", "password", "pin", "ssn",
    "wire transfer", "bitcoin", "crypto", "viagra", "dating", "singles",
    "limited time", "act now", "immediate", "customs fee", "dispute", "bonus"
]

PHONE_REGEX = re.compile(r"(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}")
URL_IN_TEXT_REGEX = re.compile(r"https?://[^\s]+|www\.[^\s]+|[a-zA-Z0-9-]+\.(?:xyz|top|cc|ru|buzz|info|club|biz)")


class SMSDetector:
    """Classifier wrapper that loads the trained SMS spam model and performs NLP inference."""
    
    def __init__(self, model_path: str = None):
        if model_path is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            model_path = os.path.join(base_dir, "models", "sms_model.joblib")
            
        self.model_path = model_path
        self.pipeline = None
        self.metrics = None
        self.is_demo_mode = False
        self.load_model()
        
    def load_model(self):
        """Loads trained pipeline from disk or activates fallback demo mode."""
        if os.path.exists(self.model_path):
            try:
                data = joblib.load(self.model_path)
                self.pipeline = data.get("pipeline")
                self.metrics = data.get("metrics", {})
                self.is_demo_mode = False
                print(f"[+] SMSDetector loaded trained model from {self.model_path}")
            except Exception as e:
                print(f"[!] Warning: Failed loading SMS model from {self.model_path}: {e}")
                self.pipeline = None
                self.is_demo_mode = True
        else:
            print(f"[!] Warning: SMS model file {self.model_path} not found. Running in demonstration mode.")
            self.pipeline = None
            self.is_demo_mode = True

    def analyze_text(self, text: str) -> dict:
        """Extracts NLP metadata and identifies potential spam indicators."""
        clean_text = text.strip()
        lower_text = clean_text.lower()
        
        words = clean_text.split()
        char_count = len(clean_text)
        word_count = len(words)
        
        # Detect spam trigger keywords
        found_triggers = []
        for kw in SPAM_TRIGGER_WORDS:
            if kw in lower_text and kw not in found_triggers:
                found_triggers.append(kw)
                
        # Detect embedded URLs or phones
        has_url = bool(URL_IN_TEXT_REGEX.search(clean_text))
        has_phone = bool(PHONE_REGEX.search(clean_text))
        
        # Calculate capital letter percentage (common in aggressive spam)
        uppercase_count = sum(1 for c in clean_text if c.isupper())
        capital_ratio = (uppercase_count / char_count * 100) if char_count > 0 else 0
        
        return {
            "char_count": char_count,
            "word_count": word_count,
            "found_triggers": found_triggers,
            "has_url": has_url,
            "has_phone": has_phone,
            "capital_ratio": round(capital_ratio, 1)
        }

    def predict(self, text: str) -> dict:
        """
        Classifies an SMS message as Ham or Spam.
        Returns a rich response dictionary with confidence, metrics, and text analysis.
        """
        if not text or not isinstance(text, str) or len(text.strip()) == 0:
            return {
                "success": False,
                "error": "SMS text cannot be empty. Please enter a valid message.",
                "message": text
            }
            
        clean_text = text.strip()
        if len(clean_text) > 1500:
            return {
                "success": False,
                "error": "SMS exceeds standard maximum character limit of 1,500 characters.",
                "message": clean_text
            }
            
        analysis = self.analyze_text(clean_text)
        
        if self.pipeline is not None and not self.is_demo_mode:
            try:
                pred_idx = self.pipeline.predict([clean_text])[0]
                proba = self.pipeline.predict_proba([clean_text])[0]
                
                # Class 0: Ham, Class 1: Spam
                is_spam = bool(pred_idx == 1)
                confidence = float(proba[1] if is_spam else proba[0]) * 100
                label = "Spam" if is_spam else "Ham (Legitimate)"
            except Exception as e:
                print(f"[!] Model prediction error: {e}")
                is_spam = len(analysis["found_triggers"]) >= 2 or (analysis["has_url"] and len(analysis["found_triggers"]) >= 1)
                confidence = 80.0
                label = "Spam" if is_spam else "Ham (Legitimate)"
        else:
            # Fallback heuristic mode
            is_spam = len(analysis["found_triggers"]) >= 2 or (analysis["has_url"] and len(analysis["found_triggers"]) >= 1)
            confidence = 85.0 if is_spam else 90.0
            label = "Spam (Demo Mode)" if is_spam else "Ham (Demo Mode)"
            
        # Explanatory warnings
        reasons = []
        if is_spam:
            if analysis["found_triggers"]:
                reasons.append(f"Identified {len(analysis['found_triggers'])} high-frequency spam keywords: {', '.join(analysis['found_triggers'][:4])}")
            if analysis["has_url"]:
                reasons.append("Contains an embedded hyperlink (often used to direct victims to phishing pages).")
            if analysis["capital_ratio"] > 25:
                reasons.append(f"Excessive capitalization ({analysis['capital_ratio']}%), typical of urgent promotional spam.")
        else:
            reasons.append("Conversational syntax and absence of aggressive promotional or phishing markers.")

        return {
            "success": True,
            "message": clean_text,
            "prediction": label,
            "is_spam": is_spam,
            "confidence": round(confidence, 2),
            "analysis": analysis,
            "reasons": reasons,
            "is_demo": self.is_demo_mode
        }

