import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime

# Configuration
ADMIN_EMAIL = "Bharatsamant@gmail.com"
SENDER_EMAIL = os.environ.get("SENDER_EMAIL", "no-reply@smartnri.com")
SMTP_SERVER = os.environ.get("SMTP_SERVER", "smtp.example.com")
SMTP_PORT = int(os.environ.get("SMTP_PORT", 587))
SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD", "")

import sqlite3

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "backend", "data", "smartnri.db")

def get_db():
    if not os.path.exists(DB_PATH):
        return None
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def get_daily_registrations():
    conn = get_db()
    if not conn: return []
    c = conn.cursor()
    c.execute("SELECT id, name, email, country FROM users WHERE processed = 0")
    rows = [dict(row) for row in c.fetchall()]
    # Mark as processed
    if rows:
        ids = [str(r['id']) for r in rows]
        c.execute(f"UPDATE users SET processed = 1 WHERE id IN ({','.join(ids)})")
        conn.commit()
    conn.close()
    return rows

def get_daily_bug_reports():
    conn = get_db()
    if not conn: return []
    c = conn.cursor()
    c.execute("SELECT id, email, description as desc FROM bug_reports WHERE processed = 0")
    rows = [dict(row) for row in c.fetchall()]
    # Mark as processed
    if rows:
        ids = [str(r['id']) for r in rows]
        c.execute(f"UPDATE bug_reports SET processed = 1 WHERE id IN ({','.join(ids)})")
        conn.commit()
    conn.close()
    return rows

def send_admin_report():
    print(f"[{datetime.now()}] Preparing daily admin report...")
    
    registrations = get_daily_registrations()
    bugs = get_daily_bug_reports()
    
    # HTML Email Template
    html_content = f"""
    <html>
      <body>
        <h2>SmartNRI Daily Admin Report</h2>
        <p><strong>Date:</strong> {datetime.now().strftime('%Y-%m-%d')}</p>
        
        <h3>1. New Registrations ({len(registrations)})</h3>
        <ul>
    """
    
    for reg in registrations:
        html_content += f"<li>{reg['name']} ({reg['email']}) - {reg['country']}</li>"
        
    html_content += f"""
        </ul>
        
        <h3>2. Bug Reports & Feature Requests ({len(bugs)})</h3>
        <ul>
    """
    
    for bug in bugs:
        reporter = bug['email'] if bug['email'] else "Anonymous"
        html_content += f"<li><strong>{reporter}</strong>: {bug['desc']}</li>"
        
    html_content += """
        </ul>
      </body>
    </html>
    """

    # Email construction
    msg = MIMEMultipart('alternative')
    msg['Subject'] = f"SmartNRI Daily Report: {len(registrations)} Users, {len(bugs)} Reports"
    msg['From'] = SENDER_EMAIL
    msg['To'] = ADMIN_EMAIL

    msg.attach(MIMEText(html_content, 'html'))

    # Send Email
    try:
        # NOTE: You will need valid SMTP credentials configured in your environment
        # server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        # server.starttls()
        # server.login(SENDER_EMAIL, SMTP_PASSWORD)
        # server.sendmail(SENDER_EMAIL, ADMIN_EMAIL, msg.as_string())
        # server.quit()
        print(f"Successfully generated report for {ADMIN_EMAIL}.")
        print("--- EMAIL CONTENT PREVIEW ---")
        print(html_content)
        print("-------------------------------")
    except Exception as e:
        print(f"Failed to send email: {e}")

if __name__ == "__main__":
    # This script is intended to be run by a cron job every day at 8:00 PM.
    # e.g. 0 20 * * * /path/to/venv/bin/python /path/to/pipeline/daily_admin_report.py
    send_admin_report()
