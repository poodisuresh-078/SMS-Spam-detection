# 🛡️ SMS Spam Detection & Malicious URL Classification Using Machine Learning

[![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Flask Version](https://img.shields.io/badge/Flask-3.x-lightgrey.svg)](https://flask.palletsprojects.com/)
[![Scikit-Learn](https://img.shields.io/badge/scikit--learn-1.4%2B-orange.svg)](https://scikit-learn.org/)
[![Database](https://img.shields.io/badge/Database-SQLite3-003B57.svg)](https://www.sqlite.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

An enterprise-grade cybersecurity web application that combines **Natural Language Processing (NLP)** and **Lexical Feature Engineering** to detect unsolicited SMS spam messages and classify web links as legitimate or potentially malicious.

---

## 📋 Table of Contents
1. [Project Overview](#-project-overview)
2. [Objectives](#-objectives)
3. [Key Features](#-key-features)
4. [Technologies Used](#-technologies-used)
5. [Machine Learning Architecture](#-machine-learning-architecture)
6. [Project Folder Structure](#-project-folder-structure)
7. [Installation & Setup](#-installation--setup)
8. [Dataset Preparation](#-dataset-preparation)
9. [Model Training Instructions](#-model-training-instructions)
10. [Running the Application](#-running-the-application)
11. [Defensive Security Principles](#-defensive-security-principles)
12. [User Interface & Screenshots](#-user-interface--screenshots)
13. [Future Enhancements](#-future-enhancements)
14. [License](#-license)

---

## 📌 Project Overview
Smishing (SMS phishing) and malicious URL distribution are two of the most prevalent attack vectors in modern social engineering. Fraudulent SMS messages deceive users into clicking counterfeit hyperlinks that harvest bank credentials, compromise accounts, or distribute malware.

This project delivers a dual-engine threat intelligence dashboard built with **Python**, **Flask**, **Scikit-Learn**, and **SQLite**. It offers automated classification, probabilistic confidence ratings, lexical inspection, and real-time audit logging through a modern dark cyber interface.

---

## 🎯 Objectives
* Develop an end-to-end Machine Learning web application deployed on Flask.
* Build an NLP classification pipeline using **TF-IDF vectorization** and **Multinomial Naive Bayes** to classify SMS communications into **Ham** (Legitimate) or **Spam**.
* Design an offline lexical feature extractor evaluating 9 structural attributes to identify **Potentially Malicious** or **Legitimate** URLs.
* Eliminate Server-Side Request Forgery (SSRF) and remote execution vulnerabilities by ensuring URLs are analyzed strictly offline without remote network connections.
* Provide interactive dashboards with threat distribution statistics, audit history in SQLite, and downloadable model evaluation plots.

---

## ✨ Key Features

### 1. Cyber Threat Dashboard
* Real-time metrics counters tracking total SMS analyzed, spam ratio, total URLs scanned, and threat distribution.
* Quick launch cards with status pulse indicators for active machine learning engines.
* Recent scan activity stream displaying threat status, confidence scores, and timestamps.

### 2. SMS Spam & Smishing Detector
* Natural language tokenization and n-gram extraction (unigrams and bigrams).
* High-confidence probabilistic classification (Spam vs. Ham).
* Automated extraction of spam trigger keywords (e.g. *urgent, prize, locked, bank, free*).
* Structural metadata tracking: word count, character count, capital letter ratio, embedded phone numbers, and hyperlinks.
* Preset one-click test samples for rapid demonstration.

### 3. Malicious URL Lexical Classifier
* Extracts **9 structural & lexical features** purely from the URL string:
  1. `url_length`: Total character length.
  2. `num_dots`: Period delimiter count.
  3. `num_hyphens`: Hyphen delimiter count (typo-squatting indicator).
  4. `num_digits`: Numeric character count.
  5. `has_ip`: Detection of raw IPv4 host addresses.
  6. `is_https`: Cryptographic transport scheme check.
  7. `num_suspicious_chars`: Detection of `@`, `//`, `~`, `%`, `=`, `?`, `&`.
  8. `has_suspicious_keyword`: Presence of sensitive terms (`login`, `verify`, `banking`, `secure`, `ebayisapi`, `account`, `wallet`).
  9. `num_subdomains`: Domain hierarchy depth.
* Evaluates qualitative risk tiers: `Low`, `Moderate`, `High`, `Critical`.
* Features breakdown table displaying exact values and threat interpretation.

### 4. Scan History & Audit Logging
* Automated persistence of every scan into an embedded SQLite database.
* Filter logs by channel (`All`, `SMS`, `URL`) and search by keyword.
* Safe purge modal with confirmation dialog to clear historical records.
* Single-click clipboard export of classification reports.

### 5. High-Resolution Visual Analytics
* Matplotlib confusion matrices rendered with custom dark cybersecurity styling.
* Model performance metrics tables featuring Accuracy, Precision, Recall, and F1-score.

---

## 🛠️ Technologies Used

| Domain | Technology / Library | Purpose |
| :--- | :--- | :--- |
| **Backend Framework** | Flask 3.x | Routing, templating, session security, REST API |
| **Programming Language**| Python 3.10+ | Core application logic and feature parsing |
| **Machine Learning** | Scikit-Learn | TF-IDF Vectorizer, Multinomial Naive Bayes, Random Forest |
| **Data Processing** | Pandas & NumPy | Dataset manipulation, feature matrices, CSV parsing |
| **Model Serialization** | Joblib | Persistence of trained models and metadata |
| **Data Visualization** | Matplotlib | High-resolution confusion matrix chart generation |
| **Database** | SQLite3 | Audit trail storage, scan history, metrics calculation |
| **Frontend UI** | HTML5, CSS3, JavaScript | Responsive dark cyber theme with glassmorphism accents |
| **Typography & Icons** | Inter & FontAwesome 6 | Clean cybersecurity dashboard aesthetics |

---

## 🧠 Machine Learning Architecture

```
[Raw SMS Message]
       │
       ▼
[Text Preprocessing & Regex Cleaning]
       │
       ▼
[TF-IDF Vectorizer (1-2 N-grams, Sublinear TF)]
       │
       ▼
[Multinomial Naive Bayes (α = 0.1)] ──────► [Prediction: Spam / Ham (Confidence %)]

───────────────────────────────────────────────────────────────────────────────

[Raw URL String]
       │
       ▼
[Offline Lexical & Syntactic Parser] ──► (Length, Dots, Hyphens, Digits, IP, HTTPS, Special Chars, Keywords, Subdomains)
       │
       ▼
[Feature Vector (9 Dimensions)]
       │
       ▼
[Random Forest Classifier (120 Estimators)] ──► [Prediction: Legitimate / Malicious (Risk Tier)]
```

### SMS Evaluation Benchmark
* **Accuracy:** 95.71%
* **Precision:** 90.91%
* **Recall:** 100.00%
* **F1-Score:** 95.24%

---

## 📁 Project Folder Structure

```
sms-url-detection/
│
├── app.py                     # Flask web server and routing controller
├── train_sms_model.py         # SMS dataset pipeline, evaluation & model trainer
├── train_url_model.py         # URL feature extraction & model trainer
├── sms_detector.py            # SMS inference module & trigger keyword detector
├── url_classifier.py          # URL 9-feature lexical parser & inference module
├── database.py                # SQLite database interface & scan history manager
├── requirements.txt           # Python dependency specifications
├── README.md                  # Comprehensive project documentation
├── .gitignore                 # Version control exclusions
│
├── models/
│   ├── .gitkeep
│   ├── sms_model.joblib       # Serialized SMS Naive Bayes model & pipeline
│   └── url_model.joblib       # Serialized URL Random Forest model & features
│
├── datasets/
│   ├── README.md              # Dataset provenance and replacement guidelines
│   ├── build_datasets.py      # Seed dataset generator script
│   ├── sms_spam.csv           # Curated SMS spam/ham dataset
│   └── urls.csv               # Curated legitimate/malicious URL dataset
│
├── templates/
│   ├── base.html              # Core navigation layout, head, and footer
│   ├── index.html             # System overview dashboard & metrics
│   ├── sms_detection.html     # Interactive SMS spam prediction page
│   ├── url_detection.html     # Malicious URL classifier & 9-feature table
│   ├── history.html           # Historical scan audit log viewer
│   └── about.html             # Architecture, ML metrics & security policy
│
└── static/
    ├── css/
    │   └── style.css          # Custom cybersecurity dark theme styles
    ├── js/
    │   └── script.js          # Client-side reactivity, counters & samples
    └── images/
        ├── sms_confusion_matrix.png
        └── url_confusion_matrix.png
```

---

## 💻 Installation & Setup

### 1. Prerequisites
* Python 3.10 or higher installed.
* Git installed on your system.

### 2. Clone Repository or Open Directory
Open PowerShell or your Windows terminal in VS Code:
```powershell
cd "c:\Users\HP\OneDrive\Desktop\SMS PROJECT"
```

### 3. Create & Activate Virtual Environment (Recommended)
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 4. Install Dependencies
```powershell
pip install -r requirements.txt
```

---

## 📊 Dataset Preparation
The project comes pre-equipped with seed datasets ready for immediate training:
* `datasets/sms_spam.csv`: 350 curated SMS messages (200 Ham, 150 Spam).
* `datasets/urls.csv`: 360 curated URLs (180 Legitimate, 180 Malicious).

To regenerate or customize the starter datasets at any time:
```powershell
python datasets/build_datasets.py
```

*For large-scale academic benchmarks, refer to the [datasets/README.md](datasets/README.md) documentation.*

---

## ⚡ Model Training Instructions

### Train the SMS Spam Model
Runs TF-IDF feature extraction, trains Multinomial Naive Bayes, prints evaluation metrics, and saves the confusion matrix plot:
```powershell
python train_sms_model.py
```

### Train the URL Classification Model
Extracts the 9 lexical features for every URL in `datasets/urls.csv`, trains a Random Forest ensemble, prints classification reports, and saves the confusion matrix plot:
```powershell
python train_url_model.py
```

---

## 🚀 Running the Application

Start the Flask development server:
```powershell
python app.py
```

Open your web browser and navigate to:
```
http://127.0.0.1:5000
```

---

## 🔒 Defensive Security Principles

1. **Zero Remote Execution (Anti-SSRF):**  
   The application never makes HTTP requests, queries DNS records, or downloads remote web assets for submitted URLs. Features are derived strictly via offline lexical string inspection.
2. **Data Minimization:**  
   The application stores only the inquiry text, timestamp, and prediction result in SQLite. No cookies, browser fingerprints, or personal identifying information are stored.
3. **Probabilistic Disclaimer:**  
   Predictions are statistical machine learning estimates. While yielding high accuracy, no AI model can guarantee detection of 100% of zero-day threats or newly registered evasive domains.

---

## 🖥️ User Interface & Views

* **Home Dashboard (`/`):** Real-time analytics counter cards, threat ratio meters, ML pipeline status, and quick-action launcher.
* **SMS Scanner (`/sms`):** Textarea with live character & word counting, quick test presets, trigger word highlights, and confidence gauges.
* **URL Scanner (`/url`):** Lexical parsing engine, 9-feature breakdown table, threat badges, and safety advisories.
* **Audit History (`/history`):** Searchable and filterable SQLite scan history table with permanent clear confirmation.
* **Architecture & Metrics (`/about`):** Detailed technical documentation with embedded confusion matrix plots.

---

## 🔮 Future Enhancements
* **BERT / Transformer Fine-Tuning:** Integrate a lightweight DistilBERT model for contextual SMS classification.
* **Domain Age & WHOIS Integration:** Add optional, rate-limited RDAP/WHOIS age lookups through secure caching proxies.
* **Browser Extension:** Develop a lightweight Chrome/Firefox extension that queries the local Flask REST API.
* **Export Audit Reports:** Enable one-click PDF and CSV audit log downloads.

---

## 📄 License
This project is open-source under the MIT License. Developed for educational, research, and portfolio demonstration purposes.

