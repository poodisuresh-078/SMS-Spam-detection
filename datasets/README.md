# Dataset Documentation: SMS Spam & Malicious URL Classification

This directory contains the datasets used for training and evaluating the Machine Learning models in this project.

---

## 1. SMS Spam Detection Dataset (`sms_spam.csv`)

### Schema & Format
* **File Name:** `sms_spam.csv`
* **File Type:** Comma-Separated Values (CSV, UTF-8)
* **Required Columns:**
  * `label`: String indicating classification — either `ham` (legitimate) or `spam` (unsolicited / malicious / fraudulent).
  * `message`: Raw text of the SMS communication.

### Example Rows
```csv
label,message
ham,"Hey, are we still meeting for lunch at 12:30 PM today?"
spam,"URGENT: Your bank account has been locked. Verify immediately at http://secure-bank-update.xyz to restore access."
```

### Pre-packaged Sample vs. External Large Datasets
The bundled dataset includes curated, diverse real-world SMS examples covering:
- **Spam categories:** Prize/lottery scams, urgent financial alerts, package tracking fraud, OTP phishing, loan offers, crypto schemes, subscription renewals.
- **Ham categories:** Everyday conversations, project updates, appointment confirmations, university notices, calendar reminders.

### Recommended Public Datasets
You can substitute or expand this file with standard benchmarks:
1. **UCI Machine Learning Repository - SMS Spam Collection:**
   - Link: https://archive.ics.uci.edu/dataset/228/sms+spam+collection
   - Contains 5,574 English SMS messages labeled as ham or spam.
2. **Kaggle SMS Spam Collection Dataset:**
   - Link: https://www.kaggle.com/datasets/uciml/sms-spam-collection-dataset
   - Download the CSV, ensure columns are mapped to `label` and `message`, and replace `datasets/sms_spam.csv`.

---

## 2. Malicious URL Classification Dataset (`urls.csv`)

### Schema & Format
* **File Name:** `urls.csv`
* **File Type:** Comma-Separated Values (CSV, UTF-8)
* **Required Columns:**
  * `url`: The raw URL string.
  * `label`: String indicating classification — either `legitimate` or `malicious`.

### Example Rows
```csv
url,label
https://www.wikipedia.org/wiki/Machine_learning,legitimate
http://192.168.1.100/paypal-login/verification-update.php,malicious
```

### Lexical Features Extracted from URLs
During model preprocessing, URLs are never accessed, pinged, or fetched over the network. Only syntactic and lexical properties are extracted:
1. `url_length`: Total character count.
2. `num_dots`: Count of period characters (`.`).
3. `num_hyphens`: Count of hyphen characters (`-`).
4. `num_digits`: Count of numerical digits (`0-9`).
5. `has_ip`: Binary flag indicating presence of an IPv4 address in the hostname.
6. `is_https`: Binary flag indicating whether HTTPS protocol is used.
7. `num_suspicious_chars`: Count of anomalous characters (`@`, `//`, `~`, `%`, `=`, `?`, `&`).
8. `has_suspicious_keyword`: Presence or count of high-risk phishing keywords (`login`, `verify`, `banking`, `secure`, `ebayisapi`, `signin`, `update`, `wallet`, `claim`, `account`).
9. `num_subdomains`: Depth of subdomains parsed from the domain authority.

### Recommended Public Datasets
1. **ISCX-URL-2016 (University of New Brunswick):**
   - Link: https://www.unb.ca/cic/datasets/url-2016.html
   - Contains over 35,000 legitimate and malicious URLs.
2. **PhishTank:**
   - Link: https://phishtank.org/developer_info.php
   - Real-time verified phishing feeds.
3. **Kaggle Malicious and Benign URLs:**
   - Link: https://www.kaggle.com/datasets/siddharthkumar25/malicious-and-benign-urls
   - Filter down to `url` and `label` columns for direct compatibility.

---

## 3. Dataset Validation & Integrity Rules

Both training scripts (`train_sms_model.py` and `train_url_model.py`) validate the following before execution:
1. The CSV file must exist and contain non-zero rows.
2. The expected column headers (`label`, `message` for SMS; `url`, `label` for URLs) must exist.
3. Missing or null values are dropped automatically.
4. Class distribution is verified so that both classes are represented in train and test splits.
5. If datasets are missing, a demonstration / warning fallback mode is reported rather than generating simulated numbers.

