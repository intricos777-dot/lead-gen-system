#!/usr/bin/env python3
# Watermark: Living_Sin (intricos777-dot) + AI agents (Hermes, Lia, opencode) - collaborative work
"""
LinkedIn Outreach Integration for Lead Gen System
Reads high-value leads and formats them for LinkedIn outreach.
Can be extended with LinkedIn API or browser automation.
"""

import json
import os
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).parent
CRM_FILE = BASE_DIR / "crm" / "leads.json"
OUTREACH_FILE = BASE_DIR / "crm" / "linkedin_outreach.json"
CONFIG_FILE = BASE_DIR / "config" / "config.json"


def load_json(path):
    if path.exists():
        with open(path, "r") as f:
            return json.load(f)
    return {}


def save_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def generate_outreach_sequence(lead, config):
    """Generate a multi-touch outreach sequence for a lead."""
    linkedin_config = config.get("linkedin_integration", {})
    template = linkedin_config.get("message_template", "")
    company = lead.get("company", "")
    contact = lead.get("contact", {})
    first_name = contact.get("name", "").split()[0] if contact.get("name") else "there"

    connection_msg = template.format(first_name=first_name, company=company)

    follow_up_1 = (
        f"Hi {first_name}, just wanted to follow up on my previous message. "
        f"I've helped similar {lead.get('industry', 'tech')} companies reduce "
        f"operational costs by 30-40% through AI automation. "
        f"Would a 15-minute call be worth your time?"
    )

    follow_up_2 = (
        f"Hi {first_name}, I understand you're busy. I put together a quick "
        f"automation audit for {company} — no strings attached. "
        f"Interested in seeing it?"
    )

    return {
        "company": company,
        "contact": contact,
        "sequence": [
            {
                "step": 1,
                "type": "connection_request",
                "message": connection_msg,
                "delay_days": 0,
                "status": "pending",
            },
            {
                "step": 2,
                "type": "follow_up",
                "message": follow_up_1,
                "delay_days": 3,
                "status": "pending",
            },
            {
                "step": 3,
                "type": "value_add",
                "message": follow_up_2,
                "delay_days": 7,
                "status": "pending",
            },
        ],
        "created_date": datetime.now().isoformat(),
    }


def process_outreach():
    """Process all high-value leads into outreach sequences."""
    config = load_json(CONFIG_FILE)
    crm = load_json(CRM_FILE)

    leads = crm.get("leads", [])
    high_value = [l for l in leads if l.get("score", 0) >= 75]

    if not high_value:
        print("No high-value leads to process for outreach.")
        return []

    sequences = []
    for lead in high_value:
        seq = generate_outreach_sequence(lead, config)
        sequences.append(seq)

    save_json(OUTREACH_FILE, sequences)

    print(f"Generated {len(sequences)} outreach sequences")
    for seq in sequences:
        print(f"  - {seq['company']}: {seq['contact'].get('name', 'N/A')} ({seq['contact'].get('title', 'N/A')})")

    return sequences


def export_for_linkedin_browser(sequences):
    """Export outreach data in a format ready for browser automation."""
    export_file = BASE_DIR / "crm" / "linkedin_export.csv"

    rows = ["company,contact_name,contact_title,linkedin_url,step1_message,step2_message,step3_message"]
    for seq in sequences:
        contact = seq.get("contact", {})
        msgs = {s["step"]: s["message"] for s in seq.get("sequence", [])}
        row = (
            f'"{seq["company"]}",'
            f'"{contact.get("name", "")}",'
            f'"{contact.get("title", "")}",'
            f'"{contact.get("linkedin", "")}",'
            f'"{msgs.get(1, "")}",'
            f'"{msgs.get(2, "")}",'
            f'"{msgs.get(3, "")}"'
        )
        rows.append(row)

    with open(export_file, "w") as f:
        f.write("\n".join(rows))

    print(f"Exported to {export_file}")
    return export_file


if __name__ == "__main__":
    sequences = process_outreach()
    if sequences:
        export_for_linkedin_browser(sequences)
