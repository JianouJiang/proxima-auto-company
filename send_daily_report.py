#!/usr/bin/env python3
"""
send_daily_report.py — Send daily report email for Auto Company.

Called by the auto-loop after the editor agent generates a daily report.
Reads the latest daily report from docs/editor/ and sends it via email.

Usage:
    python3 send_daily_report.py                    # Send today's report
    python3 send_daily_report.py 2026-02-20         # Send specific date's report
    python3 send_daily_report.py --file path/to/report.md  # Send specific file
"""

import email.utils
import glob
import logging
import os
import smtplib
import ssl
import sys
from datetime import datetime
from email.mime.text import MIMEText
from email.utils import make_msgid
from pathlib import Path

import yaml

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("daily_report")

SCRIPT_DIR = Path(__file__).resolve().parent
CONFIG_PATH = SCRIPT_DIR / "email_config.yaml"
EDITOR_DIR = SCRIPT_DIR / "docs" / "editor"

PROVIDERS = {
    "gmail": {"smtp_host": "smtp.gmail.com", "smtp_port": 587, "smtp_ssl": False},
    "qq":    {"smtp_host": "smtp.qq.com",    "smtp_port": 587, "smtp_ssl": False},
    "163":   {"smtp_host": "smtp.163.com",   "smtp_port": 465, "smtp_ssl": True},
}

TIMEOUT = 30


def load_config() -> dict | None:
    try:
        if not CONFIG_PATH.exists():
            logger.warning("No email_config.yaml found at %s", CONFIG_PATH)
            return None
        with open(CONFIG_PATH) as f:
            raw = yaml.safe_load(f)
        cfg = raw.get("email", {})
        if not cfg.get("enabled", False):
            logger.info("Email disabled in config.")
            return None
        provider = cfg.get("provider", "").lower()
        if provider not in PROVIDERS:
            logger.warning("Unknown provider '%s'", provider)
            return None
        for key in ("address", "password", "recipient"):
            if not cfg.get(key) or cfg[key] in ("you@gmail.com", "xxxx-xxxx-xxxx-xxxx"):
                logger.warning("Email config: '%s' not configured.", key)
                return None
        cfg.update(PROVIDERS[provider])
        return cfg
    except Exception as e:
        logger.warning("Failed to load config: %s", e)
        return None


def find_report(date_str: str = None, file_path: str = None) -> Path | None:
    if file_path:
        p = Path(file_path)
        return p if p.exists() else None

    if date_str is None:
        date_str = datetime.now().strftime("%Y-%m-%d")

    # Try exact date match
    target = EDITOR_DIR / f"daily-{date_str}.md"
    if target.exists():
        return target

    # Try latest daily report
    reports = sorted(glob.glob(str(EDITOR_DIR / "daily-*.md")))
    if reports:
        return Path(reports[-1])

    # Try consensus as fallback
    consensus = SCRIPT_DIR / "memories" / "consensus.md"
    if consensus.exists():
        return consensus

    return None


def send_email(config: dict, subject: str, body: str) -> bool:
    try:
        msg = MIMEText(body, "plain", "utf-8")
        msg_id = make_msgid(domain=config["address"].split("@")[-1])
        msg["Message-ID"] = msg_id
        msg["From"] = config["address"]
        msg["To"] = config["address"]
        msg["Subject"] = subject
        msg["Date"] = email.utils.formatdate(localtime=True)

        all_recipients = [
            addr.strip() for addr in config["recipient"].split(",")
            if addr.strip()
        ]

        host = config["smtp_host"]
        port = config["smtp_port"]
        sender = config["address"]

        if config.get("smtp_ssl"):
            ctx = ssl.create_default_context()
            with smtplib.SMTP_SSL(host, port, timeout=TIMEOUT, context=ctx) as server:
                server.login(sender, config["password"])
                server.sendmail(sender, all_recipients, msg.as_string())
        else:
            with smtplib.SMTP(host, port, timeout=TIMEOUT) as server:
                server.ehlo()
                server.starttls(context=ssl.create_default_context())
                server.ehlo()
                server.login(sender, config["password"])
                server.sendmail(sender, all_recipients, msg.as_string())

        logger.info("Email sent: %s (to %d recipients)", subject, len(all_recipients))
        return True

    except Exception as e:
        logger.warning("Failed to send email: %s", e)
        return False


def main():
    config = load_config()
    if not config:
        logger.error("Email not configured. Create email_config.yaml first.")
        sys.exit(1)

    date_str = None
    file_path = None

    if len(sys.argv) > 1:
        if sys.argv[1] == "--file" and len(sys.argv) > 2:
            file_path = sys.argv[2]
        else:
            date_str = sys.argv[1]

    report = find_report(date_str=date_str, file_path=file_path)
    if not report:
        logger.warning("No report found to send.")
        sys.exit(1)

    body = report.read_text(errors="replace")
    date_label = date_str or datetime.now().strftime("%Y-%m-%d")
    prefix = config.get("subject_prefix", "[Auto Company]")
    subject = f"{prefix} Daily Report — {date_label}"

    if send_email(config, subject, body):
        logger.info("Daily report sent successfully.")
    else:
        logger.error("Failed to send daily report.")
        sys.exit(1)


if __name__ == "__main__":
    main()
