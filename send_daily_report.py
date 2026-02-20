#!/usr/bin/env python3
"""
send_daily_report.py — Email system for Auto Company.

Two modes:
  1. Per-round progress email (plain text, fast, after every cycle)
  2. Daily PDF report (professional LaTeX bilingual PDF, once per day)

Usage:
    python3 send_daily_report.py round <cycle_num> <consensus_file>  # Plain text round email
    python3 send_daily_report.py daily [YYYY-MM-DD]                  # Compile & send daily PDF
    python3 send_daily_report.py daily --skip-pdf [YYYY-MM-DD]       # Send daily as plain text
"""

import email.utils
import glob
import json
import logging
import os
import re
import shutil
import smtplib
import ssl
import subprocess
import sys
from datetime import datetime
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import make_msgid
from pathlib import Path

import yaml

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("email_report")

SCRIPT_DIR = Path(__file__).resolve().parent
CONFIG_PATH = SCRIPT_DIR / "email_config.yaml"
EDITOR_DIR = SCRIPT_DIR / "docs" / "editor"
LATEX_DIR = EDITOR_DIR / "latex"
TEMPLATE_PATH = LATEX_DIR / "report_template.tex"
CONSENSUS_PATH = SCRIPT_DIR / "memories" / "consensus.md"

PROVIDERS = {
    "gmail": {"smtp_host": "smtp.gmail.com", "smtp_port": 587, "smtp_ssl": False},
    "qq":    {"smtp_host": "smtp.qq.com",    "smtp_port": 587, "smtp_ssl": False},
    "163":   {"smtp_host": "smtp.163.com",   "smtp_port": 465, "smtp_ssl": True},
}

TIMEOUT = 30


# ═════════════════════════════════════════════════════════════════════
#  Config
# ═════════════════════════════════════════════════════════════════════

def load_config():
    try:
        if not CONFIG_PATH.exists():
            logger.warning("No email_config.yaml found at %s", CONFIG_PATH)
            return None
        with open(CONFIG_PATH) as f:
            raw = yaml.safe_load(f)
        cfg = raw.get("email", {})
        if not cfg.get("enabled", False):
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


def get_recipients(config):
    return [addr.strip() for addr in config["recipient"].split(",") if addr.strip()]


# ═════════════════════════════════════════════════════════════════════
#  SMTP send
# ═════════════════════════════════════════════════════════════════════

def smtp_send(config, msg, recipients):
    host = config["smtp_host"]
    port = config["smtp_port"]
    sender = config["address"]

    if config.get("smtp_ssl"):
        ctx = ssl.create_default_context()
        with smtplib.SMTP_SSL(host, port, timeout=TIMEOUT, context=ctx) as server:
            server.login(sender, config["password"])
            server.sendmail(sender, recipients, msg.as_string())
    else:
        with smtplib.SMTP(host, port, timeout=TIMEOUT) as server:
            server.ehlo()
            server.starttls(context=ssl.create_default_context())
            server.ehlo()
            server.login(sender, config["password"])
            server.sendmail(sender, recipients, msg.as_string())


def send_plain_email(config, subject, body):
    """Send a plain text email."""
    try:
        msg = MIMEText(body, "plain", "utf-8")
        msg["Message-ID"] = make_msgid(domain=config["address"].split("@")[-1])
        msg["From"] = config["address"]
        msg["To"] = config["address"]
        msg["Subject"] = subject
        msg["Date"] = email.utils.formatdate(localtime=True)

        smtp_send(config, msg, get_recipients(config))
        logger.info("Sent: %s", subject)
        return True
    except Exception as e:
        logger.warning("Failed to send email: %s", e)
        return False


def send_pdf_email(config, subject, body_text, pdf_path):
    """Send email with PDF attachment."""
    try:
        msg = MIMEMultipart()
        msg["Message-ID"] = make_msgid(domain=config["address"].split("@")[-1])
        msg["From"] = config["address"]
        msg["To"] = config["address"]
        msg["Subject"] = subject
        msg["Date"] = email.utils.formatdate(localtime=True)

        msg.attach(MIMEText(body_text, "plain", "utf-8"))

        with open(pdf_path, "rb") as f:
            pdf_part = MIMEBase("application", "pdf")
            pdf_part.set_payload(f.read())
        from email.encoders import encode_base64
        encode_base64(pdf_part)
        pdf_name = pdf_path.name
        pdf_part.add_header("Content-Disposition", "attachment", filename=pdf_name)
        msg.attach(pdf_part)

        smtp_send(config, msg, get_recipients(config))
        logger.info("Sent PDF: %s (%s)", subject, pdf_name)
        return True
    except Exception as e:
        logger.warning("Failed to send PDF email: %s", e)
        return False


# ═════════════════════════════════════════════════════════════════════
#  Mode 1: Per-round plain text progress email
# ═════════════════════════════════════════════════════════════════════

def send_round_email(config, cycle_num, consensus_path=None):
    """Send a quick plain text progress email after each cycle."""
    consensus_text = ""
    if consensus_path and Path(consensus_path).exists():
        consensus_text = Path(consensus_path).read_text(errors="replace")
    elif CONSENSUS_PATH.exists():
        consensus_text = CONSENSUS_PATH.read_text(errors="replace")

    # Try to read cycle log for cost info
    cycle_logs = sorted(glob.glob(str(SCRIPT_DIR / "logs" / f"cycle-{int(cycle_num):04d}-*.log")))
    cost_info = ""
    if cycle_logs:
        try:
            raw = Path(cycle_logs[-1]).read_text(errors="replace")
            data = json.loads(raw)
            cost = data.get("total_cost_usd", "?")
            cost_info = f"API Cost: ${cost}"
        except Exception:
            cost_info = ""

    prefix = config.get("subject_prefix", "[Auto Company]")
    subject = f"{prefix} Cycle #{cycle_num} Complete"

    body = f"""Auto Company — Cycle #{cycle_num} Progress Report
{'=' * 50}
Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
{cost_info}

CURRENT CONSENSUS:
{'-' * 50}
{consensus_text}
{'-' * 50}

This is an automated progress update sent after each cycle.
"""

    return send_plain_email(config, subject, body)


# ═════════════════════════════════════════════════════════════════════
#  Mode 2: Daily PDF report (LaTeX compilation)
# ═════════════════════════════════════════════════════════════════════

def escape_latex(text):
    """Escape special LaTeX characters in plain text."""
    if not text:
        return ""
    # Order matters: & must be first (before we add more &)
    replacements = [
        ("\\", "\\textbackslash{}"),
        ("&", "\\&"),
        ("%", "\\%"),
        ("$", "\\$"),
        ("#", "\\#"),
        ("_", "\\_"),
        ("{", "\\{"),
        ("}", "\\}"),
        ("~", "\\textasciitilde{}"),
        ("^", "\\textasciicircum{}"),
    ]
    for old, new in replacements:
        text = text.replace(old, new)
    return text


def parse_consensus_for_pdf():
    """Extract structured data from consensus.md for LaTeX placeholders."""
    data = {
        "phase": "Day 0",
        "product": "TBD",
        "revenue": "$0",
        "users": "0",
        "what_we_did": "",
        "decisions": "",
        "next_action": "",
        "open_questions": "",
    }

    if not CONSENSUS_PATH.exists():
        return data

    text = CONSENSUS_PATH.read_text(errors="replace")
    sections = re.split(r'^## ', text, flags=re.MULTILINE)

    for section in sections:
        lower = section.lower().strip()
        content = "\n".join(section.split("\n")[1:]).strip()

        if lower.startswith("current phase"):
            data["phase"] = content or "Day 0"
        elif lower.startswith("what we did"):
            data["what_we_did"] = content
        elif lower.startswith("key decision"):
            data["decisions"] = content
        elif lower.startswith("next action"):
            data["next_action"] = content
        elif lower.startswith("company state"):
            for line in content.split("\n"):
                if "product:" in line.lower():
                    data["product"] = line.split(":", 1)[-1].strip()
                elif "revenue:" in line.lower():
                    data["revenue"] = line.split(":", 1)[-1].strip()
                elif "users:" in line.lower():
                    data["users"] = line.split(":", 1)[-1].strip()
        elif lower.startswith("open question"):
            data["open_questions"] = content

    return data


def build_decision_rows(decisions_text, lang="en"):
    """Convert markdown decisions into LaTeX table rows."""
    if not decisions_text:
        if lang == "cn":
            return "暂无 & 第一个周期，尚未做出重大决策 & -- \\\\"
        return "None yet & First cycle, no major decisions made & -- \\\\"

    rows = []
    for line in decisions_text.strip().split("\n"):
        line = line.strip().lstrip("- ")
        if not line:
            continue
        escaped = escape_latex(line)
        # Try to split on common patterns
        parts = escaped.split(" — ", 1) if " — " in escaped else [escaped, ""]
        decision = parts[0][:40]
        reason = parts[1] if len(parts) > 1 else escaped
        rows.append(f"{decision} & {reason} & Agent \\\\\n\\midrule")

    return "\n".join(rows) if rows else ("暂无 & -- & -- \\\\" if lang == "cn" else "None & -- & -- \\\\")


def collect_daily_content(date_str):
    """Collect all daily-*.md content and cycle logs for a given date."""
    daily_file = EDITOR_DIR / f"daily-{date_str}.md"
    if daily_file.exists():
        return daily_file.read_text(errors="replace")

    # Fallback: combine cycle logs from today
    logs = sorted(glob.glob(str(SCRIPT_DIR / "logs" / f"cycle-*-{date_str.replace('-', '')}*.log")))
    parts = []
    for lf in logs[:20]:  # limit
        try:
            raw = Path(lf).read_text(errors="replace")
            data = json.loads(raw)
            result = data.get("result", "")
            if result:
                parts.append(f"### {Path(lf).stem}\n{result[:2000]}")
        except Exception:
            pass
    return "\n\n".join(parts) if parts else "No detailed content available for today."


def compile_daily_pdf(date_str):
    """Compile LaTeX template into PDF with today's data."""
    if not TEMPLATE_PATH.exists():
        logger.error("LaTeX template not found: %s", TEMPLATE_PATH)
        return None

    template = TEMPLATE_PATH.read_text(encoding="utf-8")
    consensus = parse_consensus_for_pdf()
    daily_content = collect_daily_content(date_str)

    # Count cycles today
    today_logs = glob.glob(str(SCRIPT_DIR / "logs" / f"cycle-*-{date_str.replace('-', '')}*.log"))
    cycle_count = len(today_logs)
    cycles_str = f"{cycle_count} cycle(s)" if cycle_count else "N/A"

    # Build cover status
    cover_status = (
        f"Phase: {escape_latex(consensus['phase'])} \\\\[4pt] "
        f"Product: {escape_latex(consensus['product'])} \\\\[4pt] "
        f"Revenue: {escape_latex(consensus['revenue'])}"
    )

    # Metrics block
    metrics_en = (
        f"\\textbf{{Revenue:}} {escape_latex(consensus['revenue'])} \\\\[4pt] "
        f"\\textbf{{Users:}} {escape_latex(consensus['users'])} \\\\[4pt] "
        f"\\textbf{{Cycles Today:}} {cycle_count} \\\\[4pt] "
        f"\\textbf{{Phase:}} {escape_latex(consensus['phase'])}"
    )
    metrics_cn = (
        f"\\textbf{{收入:}} {escape_latex(consensus['revenue'])} \\\\[4pt] "
        f"\\textbf{{用户:}} {escape_latex(consensus['users'])} \\\\[4pt] "
        f"\\textbf{{今日周期:}} {cycle_count} \\\\[4pt] "
        f"\\textbf{{阶段:}} {escape_latex(consensus['phase'])}"
    )

    # Escape content for LaTeX
    what_we_did = escape_latex(consensus["what_we_did"]) or "Cycle in progress."
    next_action = escape_latex(consensus["next_action"]) or "To be determined."
    daily_escaped = escape_latex(daily_content)

    # Do replacements
    replacements = {
        "%%REPORT_DATE%%": date_str,
        "%%CYCLES_COVERED%%": cycles_str,
        "%%COVER_STATUS%%": cover_status,
        "%%CN_EXECUTIVE_SUMMARY%%": what_we_did,
        "%%CN_HIGHLIGHTS%%": what_we_did,
        "%%CN_CYCLE_DETAILS%%": daily_escaped[:3000],
        "%%CN_DECISIONS_ROWS%%": build_decision_rows(consensus["decisions"], "cn"),
        "%%CN_METRICS%%": metrics_cn,
        "%%CN_NEXT_PRIORITIES%%": escape_latex(consensus["next_action"]) or "待定",
        "%%EN_EXECUTIVE_SUMMARY%%": what_we_did,
        "%%EN_HIGHLIGHTS%%": what_we_did,
        "%%EN_CYCLE_DETAILS%%": daily_escaped[:3000],
        "%%EN_DECISIONS_ROWS%%": build_decision_rows(consensus["decisions"], "en"),
        "%%EN_METRICS%%": metrics_en,
        "%%EN_NEXT_PRIORITIES%%": next_action,
    }

    tex_content = template
    for placeholder, value in replacements.items():
        tex_content = tex_content.replace(placeholder, value)

    # Write .tex
    tex_path = LATEX_DIR / "daily_report.tex"
    pdf_path = LATEX_DIR / "daily_report.pdf"
    tex_path.write_text(tex_content, encoding="utf-8")

    # Compile with xelatex (2 passes for TOC)
    xelatex = shutil.which("xelatex")
    if not xelatex:
        logger.error("xelatex not found. Install texlive-xetex.")
        return None

    cmd = [xelatex, "-interaction=nonstopmode", "-output-directory", str(LATEX_DIR), str(tex_path)]

    for pass_num in (1, 2):
        logger.info("xelatex pass %d...", pass_num)
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if result.returncode != 0:
            # xelatex often returns non-zero but still produces PDF
            logger.warning("xelatex pass %d returned %d (may still work)", pass_num, result.returncode)

    if pdf_path.exists() and pdf_path.stat().st_size > 0:
        # Copy to a date-stamped file
        final_pdf = EDITOR_DIR / f"daily-report-{date_str}.pdf"
        shutil.copy2(pdf_path, final_pdf)
        logger.info("PDF compiled: %s (%d bytes)", final_pdf, final_pdf.stat().st_size)
        return final_pdf
    else:
        logger.error("PDF compilation failed — no output file.")
        return None


def send_daily_pdf(config, date_str):
    """Compile PDF and send it as email attachment."""
    pdf_path = compile_daily_pdf(date_str)

    prefix = config.get("subject_prefix", "[Auto Company]")
    subject = f"{prefix} Daily Report — {date_str}"

    if pdf_path:
        body = (
            f"Auto Company Daily Report — {date_str}\n\n"
            f"Please find attached the bilingual (Chinese/English) daily progress report.\n\n"
            f"This PDF was auto-compiled from LaTeX by the Editor Agent.\n"
        )
        return send_pdf_email(config, subject, body, pdf_path)
    else:
        # Fallback: send plain text daily
        logger.warning("PDF compilation failed, sending plain text fallback.")
        content = collect_daily_content(date_str)
        consensus_text = CONSENSUS_PATH.read_text(errors="replace") if CONSENSUS_PATH.exists() else ""
        body = (
            f"Auto Company Daily Report — {date_str}\n"
            f"(PDF compilation failed, plain text fallback)\n\n"
            f"{'=' * 50}\n"
            f"CONSENSUS:\n{consensus_text}\n\n"
            f"{'=' * 50}\n"
            f"DAILY CONTENT:\n{content}\n"
        )
        return send_plain_email(config, subject, body)


def send_daily_plaintext(config, date_str):
    """Send daily report as plain text (skip PDF)."""
    content = collect_daily_content(date_str)
    consensus_text = CONSENSUS_PATH.read_text(errors="replace") if CONSENSUS_PATH.exists() else ""

    prefix = config.get("subject_prefix", "[Auto Company]")
    subject = f"{prefix} Daily Report — {date_str}"
    body = (
        f"Auto Company Daily Report — {date_str}\n\n"
        f"{'=' * 50}\n"
        f"CONSENSUS:\n{consensus_text}\n\n"
        f"{'=' * 50}\n"
        f"DAILY CONTENT:\n{content}\n"
    )
    return send_plain_email(config, subject, body)


# ═════════════════════════════════════════════════════════════════════
#  Main
# ═════════════════════════════════════════════════════════════════════

def main():
    config = load_config()
    if not config:
        logger.error("Email not configured. Create email_config.yaml first.")
        sys.exit(1)

    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    mode = sys.argv[1]

    if mode == "round":
        # Per-round progress email
        cycle_num = sys.argv[2] if len(sys.argv) > 2 else "?"
        consensus_file = sys.argv[3] if len(sys.argv) > 3 else None
        ok = send_round_email(config, cycle_num, consensus_file)
        sys.exit(0 if ok else 1)

    elif mode == "daily":
        # Daily report (PDF or plain text)
        skip_pdf = "--skip-pdf" in sys.argv
        date_str = None
        for arg in sys.argv[2:]:
            if arg != "--skip-pdf" and re.match(r"\d{4}-\d{2}-\d{2}", arg):
                date_str = arg
        if not date_str:
            date_str = datetime.now().strftime("%Y-%m-%d")

        if skip_pdf:
            ok = send_daily_plaintext(config, date_str)
        else:
            ok = send_daily_pdf(config, date_str)
        sys.exit(0 if ok else 1)

    else:
        # Legacy: treat as date string for backward compat
        date_str = mode if re.match(r"\d{4}-\d{2}-\d{2}", mode) else datetime.now().strftime("%Y-%m-%d")
        ok = send_daily_pdf(config, date_str)
        sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
