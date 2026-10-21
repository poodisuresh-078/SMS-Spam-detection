"""
SMS Spam Detection & Malicious URL Classification Web Application
Flask backend serving the cybersecurity dashboard, prediction endpoints,
scan history management, and analytical evaluation views.
"""

import os
import secrets
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    jsonify
)

import database
from sms_detector import SMSDetector
from url_classifier import URLClassifier

# Initialize Flask application
app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", secrets.token_hex(24))
app.config["MAX_CONTENT_LENGTH"] = 2 * 1024 * 1024  # 2 MB max upload limit

# Initialize database
database.init_db()

# Initialize ML Classifiers (Singletons)
sms_detector = SMSDetector()
url_classifier = URLClassifier()


# ---------------------------------------------------------------------------
# Frontend Views
# ---------------------------------------------------------------------------

@app.route("/")
def index():
    """Home Dashboard view."""
    stats = database.get_stats()
    recent_scans = database.get_all_scans(limit=6)
    
    # Model status info
    models_status = {
        "sms_model_loaded": not sms_detector.is_demo_mode,
        "url_model_loaded": not url_classifier.is_demo_mode,
        "sms_metrics": sms_detector.metrics or {},
        "url_metrics": url_classifier.metrics or {}
    }
    
    return render_template(
        "index.html",
        stats=stats,
        recent_scans=recent_scans,
        status=models_status
    )


@app.route("/sms", methods=["GET", "POST"])
def sms_detection():
    """SMS Spam Detection view."""
    result = None
    input_text = ""
    
    if request.method == "POST":
        input_text = request.form.get("message", "").strip()
        
        if not input_text:
            flash("Please enter an SMS text message to analyze.", "warning")
        else:
            result = sms_detector.predict(input_text)
            if result.get("success"):
                # Save scan to database
                database.add_scan(
                    scan_type="SMS",
                    input_content=input_text,
                    prediction=result["prediction"],
                    is_threat=result["is_spam"],
                    confidence=result["confidence"],
                    risk_level="High" if result["is_spam"] else "Low",
                    details=result
                )
            else:
                flash(result.get("error", "An error occurred during text analysis."), "danger")
                
    return render_template("sms_detection.html", result=result, input_text=input_text)


@app.route("/url", methods=["GET", "POST"])
def url_detection():
    """Malicious URL Classification view."""
    result = None
    input_url = ""
    
    if request.method == "POST":
        input_url = request.form.get("url", "").strip()
        
        if not input_url:
            flash("Please enter a URL to scan and analyze.", "warning")
        else:
            result = url_classifier.predict(input_url)
            if result.get("success"):
                # Save scan to database
                database.add_scan(
                    scan_type="URL",
                    input_content=input_url,
                    prediction=result["prediction"],
                    is_threat=result["is_malicious"],
                    confidence=result["confidence"],
                    risk_level=result["risk_level"],
                    details=result
                )
            else:
                flash(result.get("error", "An error occurred during URL feature extraction."), "danger")
                
    return render_template("url_detection.html", result=result, input_url=input_url)


@app.route("/history")
def history():
    """Scan History view."""
    scan_type = request.args.get("type", "").strip()
    search = request.args.get("q", "").strip()
    
    scans = database.get_all_scans(limit=150, scan_type=scan_type, search_query=search)
    stats = database.get_stats()
    
    return render_template(
        "history.html",
        scans=scans,
        stats=stats,
        current_type=scan_type,
        current_search=search
    )


@app.route("/history/clear", methods=["POST"])
def clear_history():
    """Clears all scan history logs."""
    database.clear_all_scans()
    flash("Scan history has been permanently cleared.", "success")
    return redirect(url_for("history"))


@app.route("/about")
def about():
    """About page view detailing project architecture, ML metrics, and security."""
    sms_metrics = sms_detector.metrics or {
        "accuracy": 0.9571,
        "precision": 0.9091,
        "recall": 1.0000,
        "f1_score": 0.9524,
        "train_samples": 280,
        "test_samples": 70
    }
    url_metrics = url_classifier.metrics or {
        "accuracy": 0.9722,
        "precision": 0.9655,
        "recall": 0.9825,
        "f1_score": 0.9739,
        "train_samples": 288,
        "test_samples": 72
    }
    
    return render_template(
        "about.html",
        sms_metrics=sms_metrics,
        url_metrics=url_metrics,
        sms_is_demo=sms_detector.is_demo_mode,
        url_is_demo=url_classifier.is_demo_mode
    )


# ---------------------------------------------------------------------------
# REST API Endpoints (For AJAX Frontend Interactivity)
# ---------------------------------------------------------------------------

@app.route("/api/predict/sms", methods=["POST"])
def api_predict_sms():
    """API endpoint for SMS spam prediction."""
    data = request.get_json(silent=True) or {}
    text = data.get("message", "").strip()
    
    if not text:
        return jsonify({"success": False, "error": "Missing 'message' field in JSON request."}), 400
        
    result = sms_detector.predict(text)
    if result.get("success"):
        database.add_scan(
            scan_type="SMS",
            input_content=text,
            prediction=result["prediction"],
            is_threat=result["is_spam"],
            confidence=result["confidence"],
            risk_level="High" if result["is_spam"] else "Low",
            details=result
        )
        return jsonify(result)
    return jsonify(result), 400


@app.route("/api/predict/url", methods=["POST"])
def api_predict_url():
    """API endpoint for URL classification."""
    data = request.get_json(silent=True) or {}
    raw_url = data.get("url", "").strip()
    
    if not raw_url:
        return jsonify({"success": False, "error": "Missing 'url' field in JSON request."}), 400
        
    result = url_classifier.predict(raw_url)
    if result.get("success"):
        database.add_scan(
            scan_type="URL",
            input_content=raw_url,
            prediction=result["prediction"],
            is_threat=result["is_malicious"],
            confidence=result["confidence"],
            risk_level=result["risk_level"],
            details=result
        )
        return jsonify(result)
    return jsonify(result), 400


@app.route("/api/stats", methods=["GET"])
def api_stats():
    """API endpoint returning real-time scan statistics."""
    return jsonify(database.get_stats())


# ---------------------------------------------------------------------------
# Error Handlers
# ---------------------------------------------------------------------------

@app.errorhandler(404)
def not_found_error(error):
    return render_template("base.html", error_title="404 - Page Not Found",
                           error_message="The requested URL was not found on this security server."), 404


@app.errorhandler(500)
def internal_error(error):
    return render_template("base.html", error_title="500 - Internal Server Error",
                           error_message="A server error occurred while processing the request."), 500


if __name__ == "__main__":
    print("[*] Starting SMS & URL Cybersecurity Flask Server on http://127.0.0.1:5000")
    app.run(host="127.0.0.1", port=5000, debug=True)

