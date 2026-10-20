#!/usr/bin/env python3
# Watermark: Living_Sin (intricos777-dot) + AI agents (Hermes, Lia, opencode) - collaborative work
# Copyright (c) 2026 Living Sin (intricos777-dot) + AI agents (Hermes, Lia, opencode) - collaborative work
# Licensed under Living Sin Proprietary License (LSPL-1.0)
# See LICENSE file for details.
"""
Send desktop notifications for high-value leads.
Falls back gracefully if notify-send is not available.
"""

import json
import subprocess
import shutil
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).parent
CRM_FILE = BASE_DIR / "crm" / "leads.json"
NOTIFICATION_LOG = BASE_DIR / "logs" / "notifications.log"


def send_desktop_notification(title, message):
    """Send a desktop notification using notify-send."""
    if shutil.which("notify-send"):
        try:
            subprocess.run(
                ["notify-send", "--urgency=normal", "--app-name=LeadGen", title, message],
                check=False,
                timeout=5,
            )
            return True
        except Exception:
            pass
    return False


def check_and_notify():
    """Check for new high-value leads and send notifications."""
    if not CRM_FILE.exists():
        print("No CRM data found. Run lead_gen.py first.")
        return

    with open(CRM_FILE, "r") as f:
        crm = json.load(f)

    leads = crm.get("leads", [])
    high_value = [l for l in leads if l.get("score", 0) >= 75]

    if not high_value:
        print("No high-value leads to notify about.")
        return

    # Log and notify
    NOTIFICATION_LOG.parent.mkdir(parents=True, exist_ok=True)
    with open(NOTIFICATION_LOG, "a") as f:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for lead in high_value:
            msg = f"[{timestamp}] 🔥 {lead['company']} ({lead['industry']}) - Score: {lead['score']}"
            f.write(msg + "\n")
            print(msg)
            send_desktop_notification(
                f"🔥 Hot Lead: {lead['company']}",
                f"Score: {lead['score']} | {lead.get('outreach_angle', '')[:80]}"
            )

    print(f"\n{len(high_value)} high-value leads notified.")


if __name__ == "__main__":
    check_and_notify()
