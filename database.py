"""
SQLite Database Layer for Scan History
Stores scan timestamps, types (SMS or URL), inputs, predictions,
threat classifications, confidence scores, and feature metadata.
Includes stats aggregation and secure history management.
"""

import os
import sqlite3
import json
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_DB_PATH = os.path.join(BASE_DIR, "scan_history.db")


def get_db_connection(db_path=None):
    """Returns a SQLite connection with dict-like row access."""
    path = db_path or DEFAULT_DB_PATH
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(db_path=None):
    """Initializes the SQLite database and creates the scans table."""
    conn = get_db_connection(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS scans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            scan_type TEXT NOT NULL,
            input_content TEXT NOT NULL,
            prediction TEXT NOT NULL,
            is_threat INTEGER NOT NULL,
            confidence REAL NOT NULL,
            risk_level TEXT,
            details_json TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_scan_type ON scans (scan_type);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_created_at ON scans (created_at);")
    conn.commit()
    conn.close()
    print(f"[+] Initialized SQLite database at {db_path or DEFAULT_DB_PATH}")


def add_scan(scan_type: str, input_content: str, prediction: str,
             is_threat: bool, confidence: float, risk_level: str = None,
             details: dict = None, db_path=None) -> int:
    """Inserts a new scan event into the database."""
    conn = get_db_connection(db_path)
    cursor = conn.cursor()
    
    details_str = json.dumps(details) if details else None
    threat_int = 1 if is_threat else 0
    
    cursor.execute("""
        INSERT INTO scans (scan_type, input_content, prediction, is_threat, confidence, risk_level, details_json, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        scan_type,
        input_content,
        prediction,
        threat_int,
        float(confidence),
        risk_level or ("High" if is_threat else "Low"),
        details_str,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))
    
    scan_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return scan_id


def get_all_scans(limit: int = 100, scan_type: str = None, search_query: str = None, db_path=None) -> list:
    """Retrieves scans with optional type and content search filtering."""
    conn = get_db_connection(db_path)
    cursor = conn.cursor()
    
    query = "SELECT * FROM scans"
    params = []
    conditions = []
    
    if scan_type and scan_type.upper() in ["SMS", "URL"]:
        conditions.append("scan_type = ?")
        params.append(scan_type.upper())
        
    if search_query and search_query.strip():
        conditions.append("(input_content LIKE ? OR prediction LIKE ?)")
        wildcard = f"%{search_query.strip()}%"
        params.extend([wildcard, wildcard])
        
    if conditions:
        query += " WHERE " + " AND ".join(conditions)
        
    query += " ORDER BY id DESC LIMIT ?"
    params.append(limit)
    
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    
    results = []
    for row in rows:
        item = dict(row)
        if item.get("details_json"):
            try:
                item["details"] = json.loads(item["details_json"])
            except Exception:
                item["details"] = {}
        else:
            item["details"] = {}
        results.append(item)
        
    return results


def get_stats(db_path=None) -> dict:
    """Computes comprehensive dashboard metrics across all historical scans."""
    conn = get_db_connection(db_path)
    cursor = conn.cursor()
    
    # Total counts
    cursor.execute("SELECT COUNT(*) FROM scans")
    total_scans = cursor.fetchone()[0]
    
    # SMS stats
    cursor.execute("SELECT COUNT(*) FROM scans WHERE scan_type = 'SMS'")
    total_sms = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM scans WHERE scan_type = 'SMS' AND is_threat = 1")
    sms_spam = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM scans WHERE scan_type = 'SMS' AND is_threat = 0")
    sms_ham = cursor.fetchone()[0]
    
    # URL stats
    cursor.execute("SELECT COUNT(*) FROM scans WHERE scan_type = 'URL'")
    total_urls = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM scans WHERE scan_type = 'URL' AND is_threat = 1")
    url_malicious = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM scans WHERE scan_type = 'URL' AND is_threat = 0")
    url_legitimate = cursor.fetchone()[0]
    
    # Threat totals
    cursor.execute("SELECT COUNT(*) FROM scans WHERE is_threat = 1")
    total_threats = cursor.fetchone()[0]
    
    total_safe = total_scans - total_threats
    
    conn.close()
    
    return {
        "total_scans": total_scans,
        "total_sms": total_sms,
        "sms_spam": sms_spam,
        "sms_ham": sms_ham,
        "sms_spam_rate": round((sms_spam / total_sms * 100), 1) if total_sms > 0 else 0.0,
        "total_urls": total_urls,
        "url_malicious": url_malicious,
        "url_legitimate": url_legitimate,
        "url_malicious_rate": round((url_malicious / total_urls * 100), 1) if total_urls > 0 else 0.0,
        "total_threats": total_threats,
        "total_safe": total_safe
    }


def clear_all_scans(db_path=None) -> bool:
    """Safely deletes all records from the scans table."""
    conn = get_db_connection(db_path)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM scans;")
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='scans';")
    conn.commit()
    conn.close()
    return True


def delete_scan(scan_id: int, db_path=None) -> bool:
    """Deletes a single scan by ID."""
    conn = get_db_connection(db_path)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM scans WHERE id = ?", (scan_id,))
    deleted = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return deleted


if __name__ == "__main__":
    init_db()
    print("Database test run completed.")

