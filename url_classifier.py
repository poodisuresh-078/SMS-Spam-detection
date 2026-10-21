"""
URL Classification & Lexical Feature Extraction Module
Analyzes URL strings without ever visiting, resolving, or executing them.
Extracts 9 lexical and structural features and predicts whether the URL is
Legitimate or Potentially Malicious using a trained Machine Learning model.
"""

import os
import re
import urllib.parse
import joblib
import pandas as pd

# Suspicious keywords commonly found in phishing and malicious URLs
SUSPICIOUS_KEYWORDS = [
    "login", "verify", "update", "banking", "secure", "free",
    "bonus", "ebayisapi", "account", "signin", "wallet", "confirm",
    "security", "password", "support", "claim", "billing", "unusual",
    "suspended", "unlock", "alert", "validation", "service"
]

FEATURE_NAMES = [
    "url_length",
    "num_dots",
    "num_hyphens",
    "num_digits",
    "has_ip",
    "is_https",
    "num_suspicious_chars",
    "has_suspicious_keyword",
    "num_subdomains"
]

IPv4_REGEX = re.compile(r"(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)")


def extract_url_features(raw_url: str) -> dict:
    """
    Extracts 9 lexical and structural features strictly through string parsing.
    NO network, DNS, or socket requests are ever made.
    """
    url = (raw_url or "").strip()
    
    # Prepend scheme if absent for urllib parseability
    parse_target = url
    if not (url.startswith("http://") or url.startswith("https://") or url.startswith("ftp://")):
        parse_target = "http://" + url
        
    try:
        parsed = urllib.parse.urlparse(parse_target)
        hostname = parsed.hostname or ""
        path = parsed.path or ""
        query = parsed.query or ""
    except Exception:
        hostname = ""
        path = ""
        query = ""

    # Feature 1: URL Length
    url_length = len(url)
    
    # Feature 2: Number of Dots
    num_dots = url.count(".")
    
    # Feature 3: Number of Hyphens
    num_hyphens = url.count("-")
    
    # Feature 4: Number of Digits
    num_digits = sum(1 for c in url if c.isdigit())
    
    # Feature 5: Presence of an IP address
    has_ip = 1 if IPv4_REGEX.search(hostname or url) else 0
    
    # Feature 6: HTTPS Usage
    is_https = 1 if url.lower().startswith("https://") else 0
    
    # Feature 7: Suspicious URL characters (@, // in path, ~, %, =, ?, &, _)
    suspicious_chars_count = 0
    suspicious_chars_count += url.count("@")
    suspicious_chars_count += url.count("~")
    suspicious_chars_count += url.count("%")
    suspicious_chars_count += url.count("=")
    suspicious_chars_count += url.count("?")
    suspicious_chars_count += url.count("&")
    suspicious_chars_count += url.count("_")
    # Check for consecutive slashes in path (often used to disguise redirection)
    if "//" in path:
        suspicious_chars_count += path.count("//")
        
    # Feature 8: Presence of Suspicious Keywords
    lower_url = url.lower()
    keyword_count = sum(1 for kw in SUSPICIOUS_KEYWORDS if kw in lower_url)
    
    # Feature 9: Number of Subdomains
    # Count dots in hostname minus 1 (for domain.tld)
    if hostname:
        clean_host = hostname.split(":")[0]  # remove port if present
        parts = clean_host.split(".")
        if len(parts) > 2:
            num_subdomains = len(parts) - 2
        else:
            num_subdomains = 0
    else:
        num_subdomains = max(0, num_dots - 1)
        
    features = {
        "url_length": int(url_length),
        "num_dots": int(num_dots),
        "num_hyphens": int(num_hyphens),
        "num_digits": int(num_digits),
        "has_ip": int(has_ip),
        "is_https": int(is_https),
        "num_suspicious_chars": int(suspicious_chars_count),
        "has_suspicious_keyword": int(keyword_count),
        "num_subdomains": int(num_subdomains)
    }
    return features


class URLClassifier:
    """Classifier wrapper that loads the trained URL model and performs inference."""
    
    def __init__(self, model_path: str = None):
        if model_path is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            model_path = os.path.join(base_dir, "models", "url_model.joblib")
            
        self.model_path = model_path
        self.model = None
        self.metrics = None
        self.is_demo_mode = False
        self.load_model()
        
    def load_model(self):
        """Loads model file from disk or activates fallback demo mode."""
        if os.path.exists(self.model_path):
            try:
                data = joblib.load(self.model_path)
                self.model = data.get("model")
                self.metrics = data.get("metrics", {})
                self.is_demo_mode = False
                print(f"[+] URLClassifier loaded trained model from {self.model_path}")
            except Exception as e:
                print(f"[!] Warning: Failed loading model from {self.model_path}: {e}")
                self.model = None
                self.is_demo_mode = True
        else:
            print(f"[!] Warning: Model file {self.model_path} not found. Running in demonstration mode.")
            self.model = None
            self.is_demo_mode = True

    def predict(self, url: str) -> dict:
        """
        Classifies the submitted URL.
        Returns a rich response dictionary including features, warnings, and confidence.
        """
        if not url or not isinstance(url, str) or len(url.strip()) == 0:
            return {
                "success": False,
                "error": "URL cannot be empty. Please provide a valid URL string.",
                "url": url
            }
            
        clean_url = url.strip()
        if len(clean_url) > 2000:
            return {
                "success": False,
                "error": "URL exceeds maximum permitted length of 2,000 characters.",
                "url": clean_url
            }

        # Extract 9 features
        features = extract_url_features(clean_url)
        feature_df = pd.DataFrame([features])[FEATURE_NAMES]
        
        warnings = []
        if features["has_ip"] == 1:
            warnings.append("Raw IP address detected instead of a registered domain name (high risk).")
        if features["is_https"] == 0:
            warnings.append("Insecure HTTP protocol used (missing SSL/TLS encryption).")
        if features["has_suspicious_keyword"] > 0:
            warnings.append(f"Contains {features['has_suspicious_keyword']} high-risk keywords (e.g. login, verify, account, banking).")
        if features["num_subdomains"] >= 3:
            warnings.append(f"Excessive subdomains ({features['num_subdomains']}) detected, often used to spoof legitimate domains.")
        if features["num_dots"] > 4:
            warnings.append(f"Abnormally high dot count ({features['num_dots']}).")
        if features["num_hyphens"] > 3:
            warnings.append(f"High number of hyphens ({features['num_hyphens']}), typical of typo-squatting domains.")
        if features["url_length"] > 75:
            warnings.append(f"Abnormally long URL ({features['url_length']} characters).")

        # Inference
        if self.model is not None and not self.is_demo_mode:
            try:
                pred_idx = self.model.predict(feature_df)[0]
                proba = self.model.predict_proba(feature_df)[0]
                
                # Classes: 0 -> legitimate, 1 -> malicious
                is_malicious = bool(pred_idx == 1)
                confidence = float(proba[1] if is_malicious else proba[0]) * 100
                label = "Potentially Malicious" if is_malicious else "Legitimate"
            except Exception as e:
                print(f"[!] Model prediction error: {e}")
                is_malicious = len(warnings) >= 2
                confidence = 75.0
                label = "Potentially Malicious" if is_malicious else "Legitimate"
        else:
            # Heuristic demonstration fallback
            # Flag malicious if raw IP, or 2 or more warning signs
            is_malicious = (features["has_ip"] == 1) or (len(warnings) >= 2)
            confidence = 88.0 if is_malicious else 82.5
            label = "Potentially Malicious (Demo Mode)" if is_malicious else "Legitimate (Demo Mode)"

        # Calculate qualitative risk tier
        if is_malicious:
            if features["has_ip"] == 1 or features["has_suspicious_keyword"] >= 2 or len(warnings) >= 3:
                risk_level = "Critical"
            else:
                risk_level = "High"
        else:
            if len(warnings) > 0:
                risk_level = "Moderate"
            else:
                risk_level = "Low"

        return {
            "success": True,
            "url": clean_url,
            "prediction": label,
            "is_malicious": is_malicious,
            "confidence": round(confidence, 2),
            "risk_level": risk_level,
            "features": features,
            "warnings": warnings,
            "is_demo": self.is_demo_mode,
            "disclaimer": (
                "Safety Notice: This classification is based solely on lexical URL features "
                "without visiting or contacting the remote server. Machine learning predictions "
                "are probabilistic and not guaranteed to detect every sophisticated threat. "
                "Always exercise caution before accessing unknown links."
            )
        }

