#!/usr/bin/env python3
# Watermark: Living_Sin (intricos777-dot) + AI agents (Hermes, Lia, opencode) - collaborative work
"""
Lead Generation & Business Intelligence System
Searches web sources for companies needing AI automation, scores leads,
and populates a CRM pipeline.
"""

import json
import os
import random
import hashlib
from datetime import datetime, timedelta
from pathlib import Path

try:
    from hermes_tools import web_search, web_extract
except ImportError:
    web_search = None
    web_extract = None


# --- Paths ---
BASE_DIR = Path(__file__).parent
CONFIG_FILE = BASE_DIR / "config" / "config.json"
CRM_FILE = BASE_DIR / "crm" / "leads.json"
DASHBOARD_FILE = BASE_DIR / "templates" / "dashboard.html"
LOG_FILE = BASE_DIR / "logs" / "lead_gen.log"
NOTIFICATION_LOG = BASE_DIR / "logs" / "notifications.log"


def load_config():
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)


def load_crm():
    if CRM_FILE.exists():
        with open(CRM_FILE, "r") as f:
            return json.load(f)
    return {"leads": [], "stats": {"total": 0, "high_value": 0, "last_run": None}}


def save_crm(data):
    CRM_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(CRM_FILE, "w") as f:
        json.dump(data, f, indent=2)


def log(message):
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] {message}\n")


def notify(message):
    NOTIFICATION_LOG.parent.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(NOTIFICATION_LOG, "a") as f:
        f.write(f"[{timestamp}] 🔔 HIGH VALUE: {message}\n")
    print(f"🔔 NOTIFICATION: {message}")


# --- Data extraction ---
SEARCH_TEMPLATES = [
    ("{industry} company hiring AI engineer", "hiring"),
    ("{industry} startup funding 2024 2025", "funding"),
    ("{industry} digital transformation AI", "transformation"),
    ("{industry} company AI jobs site:linkedin.com", "hiring"),
    ("{industry} Series A AI automation", "funding"),
]

SAMPLE_INDUSTRIES = [
    "fintech", "healthcare", "e-commerce", "logistics",
    "insurance", "real estate", "manufacturing", "retail"
]

SAMPLE_COMPANIES = [
    {"name": "NovaPay", "industry": "fintech", "size": "50-200", "tech": ["Python", "AWS", "TensorFlow"]},
    {"name": "MedAI Solutions", "industry": "healthcare", "size": "200-500", "tech": ["Python", "PyTorch", "Docker"]},
    {"name": "ShipLogic", "industry": "logistics", "size": "500-1000", "tech": ["Java", "Kubernetes", "Spark"]},
    {"name": "RetailGenius", "industry": "retail", "size": "1000+", "tech": ["Python", "GCP", "MLflow"]},
    {"name": "InsureFlow", "industry": "insurance", "size": "200-500", "tech": ["Python", "Airflow", "dbt"]},
    {"name": "CartForge", "industry": "e-commerce", "size": "50-200", "tech": ["Node.js", "AWS", "SageMaker"]},
    {"name": "PropTech AI", "industry": "real estate", "size": "20-50", "tech": ["Python", "Azure", "ML"]},
    {"name": "EduLearn AI", "industry": "education", "size": "50-200", "tech": ["Python", "PyTorch", "FastAPI"]},
    {"name": "FactoryMind", "industry": "manufacturing", "size": "500-1000", "tech": ["Python", "Azure", "IoT"]},
    {"name": "LegalBot Inc", "industry": "legal", "size": "20-50", "tech": ["Python", "OpenAI", "LangChain"]},
    {"name": "WealthAI", "industry": "fintech", "size": "200-500", "tech": ["Python", "Kubernetes", "Snowflake"]},
    {"name": "HealthBridge", "industry": "healthcare", "size": "1000+", "tech": ["Python", "GCP", "Vertex AI"]},
    {"name": "QuickShip AI", "industry": "logistics", "size": "50-200", "tech": ["Go", "AWS", "Terraform"]},
    {"name": "FashionAI", "industry": "retail", "size": "200-500", "tech": ["Python", "PyTorch", "Docker"]},
    {"name": "ClaimBot", "industry": "insurance", "size": "20-50", "tech": ["Python", "OpenAI", "FastAPI"]},
]


def generate_lead_id(company_name, source):
    unique = f"{company_name}-{source}-{datetime.now().strftime('%Y%m%d')}"
    return hashlib.md5(unique.encode()).hexdigest()[:12]


def search_web_for_leads(config):
    """Search the web for companies with AI/automation needs."""
    leads = []
    industries = config.get("industries", SAMPLE_INDUSTRIES)

    if web_search is None:
        log("hermes_tools not available, using built-in sample data generation")
        return None

    for industry in industries[:4]:  # Limit to avoid rate limiting
        for template, signal_type in SEARCH_TEMPLATES[:2]:
            query = template.format(industry=industry)
            try:
                log(f"Searching: {query}")
                results = web_search(query=query, limit=3)

                if results and "data" in results:
                    for item in results.get("data", {}).get("web", []):
                        lead = {
                            "company": extract_company_name(item.get("title", "")),
                            "industry": industry,
                            "source": "web_search",
                            "signal_type": signal_type,
                            "url": item.get("url", ""),
                            "description": item.get("description", ""),
                            "discovered_date": datetime.now().isoformat(),
                        }
                        leads.append(lead)

            except Exception as e:
                log(f"Search error for '{query}': {e}")

    return leads if leads else None


def extract_company_name(title):
    """Extract a plausible company name from a search result title."""
    # Simple heuristic: take first 1-3 words before common delimiters
    for delim in [" - ", " | ", ": ", " hiring", " Jobs"]:
        if delim in title:
            return title.split(delim)[0].strip()
    words = title.split()
    return " ".join(words[:3]) if len(words) > 3 else title


def generate_sample_leads():
    """Generate realistic sample leads when web search is unavailable."""
    leads = []
    num_leads = random.randint(4, 8)
    selected = random.sample(SAMPLE_COMPANIES, min(num_leads, len(SAMPLE_COMPANIES)))

    for company in selected:
        signals = random.choice([
            "hiring",
            "funding",
            "transformation",
            "hiring",
        ])
        lead = {
            "company": company["name"],
            "industry": company["industry"],
            "size": company["size"],
            "tech_stack": company["tech"],
            "source": "builtin",
            "signal_type": signals,
            "url": f"https://www.linkedin.com/company/{company['name'].lower().replace(' ', '-')}",
            "description": f"{company['name']} is a {company['industry']} company with {company['size']} employees.",
            "discovered_date": datetime.now().isoformat(),
            "contact": {
                "name": f"{'Alex' if random.random() > 0.5 else 'Jordan'} {random.choice(['Smith', 'Lee', 'Patel', 'Garcia', 'Chen'])}",
                "title": random.choice(["CTO", "VP Engineering", "Head of AI", "Director of Data Science"]),
                "linkedin": f"https://linkedin.com/in/{company['name'].lower().replace(' ', '')}-exec",
            }
        }
        leads.append(lead)

    return leads


# --- Scoring ---
def score_lead(lead, weights):
    """Score a lead 0-100 based on multiple factors."""
    score = 0.0

    # Company size (bigger = more budget)
    size_scores = {
        "20-50": 30,
        "50-200": 50,
        "200-500": 70,
        "500-1000": 85,
        "1000+": 100,
    }
    size = lead.get("size", "50-200")
    score += size_scores.get(size, 50) * weights["company_size"]

    # Industry fit
    high_fit = {"fintech", "healthcare", "e-commerce", "logistics", "insurance"}
    medium_fit = {"real estate", "manufacturing", "retail", "education", "legal"}
    industry = lead.get("industry", "")
    if industry in high_fit:
        score += 100 * weights["industry_fit"]
    elif industry in medium_fit:
        score += 70 * weights["industry_fit"]
    else:
        score += 40 * weights["industry_fit"]

    # Hiring signals
    signal_scores = {
        "hiring": 100,
        "funding": 90,
        "transformation": 80,
    }
    signal = lead.get("signal_type", "hiring")
    score += signal_scores.get(signal, 50) * weights["hiring_signals"]

    # Tech stack relevance
    tech_stack = lead.get("tech_stack", [])
    ai_techs = {"TensorFlow", "PyTorch", "MLflow", "SageMaker", "Vertex AI", "LangChain", "OpenAI"}
    if ai_techs.intersection(set(tech_stack)):
        score += 100 * weights["tech_stack"]
    else:
        score += 50 * weights["tech_stack"]

    # Funding status (simulated based on signal)
    if lead.get("signal_type") == "funding":
        score += 100 * weights["funding_status"]
    elif lead.get("signal_type") == "hiring":
        score += 70 * weights["funding_status"]
    else:
        score += 50 * weights["funding_status"]

    return round(min(score, 100), 1)


def categorize_lead(score, thresholds):
    if score >= thresholds["high_value"]:
        return "high_value"
    elif score >= thresholds["medium_value"]:
        return "medium_value"
    else:
        return "low_value"


# --- Outreach angles ---
def generate_outreach_angle(lead):
    """Generate a personalized outreach angle based on lead profile."""
    industry = lead.get("industry", "technology")
    signal = lead.get("signal_type", "hiring")
    size = lead.get("size", "")

    angles = {
        ("fintech", "hiring"): "Emphasize AI for fraud detection and risk modeling automation",
        ("fintech", "funding"): "Position for scaling AI infrastructure during growth phase",
        ("healthcare", "hiring"): "Focus on HIPAA-compliant AI for clinical workflows",
        ("healthcare", "funding"): "AI for patient outcome prediction and operational efficiency",
        ("e-commerce", "hiring"): "Personalization engines and demand forecasting automation",
        ("e-commerce", "funding"): "AI-powered recommendation systems at scale",
        ("logistics", "hiring"): "Route optimization and predictive maintenance automation",
        ("logistics", "funding"): "End-to-end supply chain visibility with AI",
        ("insurance", "hiring"): "Claims automation and underwriting AI models",
        ("insurance", "funding"): "AI-first insurance product development",
        ("retail", "hiring"): "Inventory optimization and customer behavior analytics",
        ("manufacturing", "hiring"): "Predictive maintenance and quality control automation",
        ("real estate", "hiring"): "Valuation models and property recommendation systems",
        ("education", "hiring"): "Adaptive learning and content personalization",
        ("legal", "hiring"): "Contract analysis and legal research automation",
    }

    key = (industry, signal)
    if key in angles:
        return angles[key]

    return f"AI automation solutions for {industry} companies with {size} employees"


# --- Dashboard ---
def generate_dashboard(crm_data):
    """Generate an HTML dashboard showing pipeline status."""
    leads = crm_data.get("leads", [])
    stats = crm_data.get("stats", {})

    high_value = [l for l in leads if l.get("category") == "high_value"]
    medium_value = [l for l in leads if l.get("category") == "medium_value"]
    low_value = [l for l in leads if l.get("category") == "low_value"]

    # Sort leads by score descending
    leads_sorted = sorted(leads, key=lambda x: x.get("score", 0), reverse=True)

    def lead_row(lead):
        score = lead.get("score", 0)
        score_color = "#22c55e" if score >= 75 else "#f59e0b" if score >= 50 else "#ef4444"
        category = lead.get("category", "unknown").replace("_", " ").title()
        return f"""
        <tr>
            <td><strong>{lead.get('company', 'Unknown')}</strong></td>
            <td>{lead.get('industry', '-')}</td>
            <td>{lead.get('size', '-')}</td>
            <td><span class="badge signal-{lead.get('signal_type', 'unknown')}">{lead.get('signal_type', '-')}</span></td>
            <td style="color: {score_color}; font-weight: bold;">{score}</td>
            <td><span class="badge cat-{lead.get('category', 'unknown')}">{category}</span></td>
            <td><small>{lead.get('outreach_angle', '')[:60]}...</small></td>
        </tr>"""

    rows = "\n".join(lead_row(l) for l in leads_sorted)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Lead Generation Dashboard</title>
<style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: #0f172a; color: #e2e8f0; }}
    .container {{ max-width: 1400px; margin: 0 auto; padding: 2rem; }}
    h1 {{ font-size: 2rem; margin-bottom: 0.5rem; }}
    .subtitle {{ color: #94a3b8; margin-bottom: 2rem; }}
    .stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin-bottom: 2rem; }}
    .stat-card {{ background: #1e293b; border-radius: 0.75rem; padding: 1.5rem; border: 1px solid #334155; }}
    .stat-value {{ font-size: 2.5rem; font-weight: bold; }}
    .stat-label {{ color: #94a3b8; font-size: 0.875rem; }}
    .high {{ color: #22c55e; }}
    .medium {{ color: #f59e0b; }}
    .low {{ color: #ef4444; }}
    table {{ width: 100%; border-collapse: collapse; background: #1e293b; border-radius: 0.75rem; overflow: hidden; }}
    th {{ background: #334155; padding: 1rem; text-align: left; font-size: 0.875rem; color: #94a3b8; }}
    td {{ padding: 0.75rem 1rem; border-bottom: 1px solid #334155; }}
    tr:hover {{ background: #252f42; }}
    .badge {{ padding: 0.25rem 0.75rem; border-radius: 999px; font-size: 0.75rem; font-weight: 600; }}
    .signal-hiring {{ background: #064e3b; color: #34d399; }}
    .signal-funding {{ background: #1e3a5f; color: #60a5fa; }}
    .signal-transformation {{ background: #4a1d96; color: #c084fc; }}
    .cat-high_value {{ background: #064e3b; color: #34d399; }}
    .cat-medium_value {{ background: #451a03; color: #fbbf24; }}
    .cat-low_value {{ background: #450a0a; color: #f87171; }}
    .footer {{ margin-top: 2rem; color: #64748b; font-size: 0.875rem; }}
    .header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 2rem; }}
    .btn {{ background: #3b82f6; color: white; border: none; padding: 0.5rem 1rem; border-radius: 0.5rem; cursor: pointer; text-decoration: none; display: inline-block; }}
</style>
</head>
<body>
<div class="container">
    <div class="header">
        <div>
            <h1>🎯 AI Automation Lead Pipeline</h1>
            <p class="subtitle">Last updated: {stats.get('last_run', 'Never')}</p>
        </div>
        <a href="#" class="btn" onclick="location.refresh()">Refresh</a>
    </div>

    <div class="stats">
        <div class="stat-card">
            <div class="stat-value">{stats.get('total', 0)}</div>
            <div class="stat-label">Total Leads</div>
        </div>
        <div class="stat-card">
            <div class="stat-value high">{stats.get('high_value', 0)}</div>
            <div class="stat-label">High Value (75+)</div>
        </div>
        <div class="stat-card">
            <div class="stat-value medium">{len(medium_value)}</div>
            <div class="stat-label">Medium Value (50-74)</div>
        </div>
        <div class="stat-card">
            <div class="stat-value low">{len(low_value)}</div>
            <div class="stat-label">Low Value (&lt;50)</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">{len(high_value)}</div>
            <div class="stat-label">🔥 Hot Leads to Contact</div>
        </div>
    </div>

    <table>
        <thead>
            <tr>
                <th>Company</th>
                <th>Industry</th>
                <th>Size</th>
                <th>Signal</th>
                <th>Score</th>
                <th>Category</th>
                <th>Outreach Angle</th>
            </tr>
        </thead>
        <tbody>
            {rows if rows else '<tr><td colspan="7" style="text-align:center; padding: 2rem; color: #64748b;">No leads yet. Run the script to generate leads.</td></tr>'}
        </tbody>
    </table>

    <div class="footer">
        <p>Pipeline auto-updates via cron schedule. CRM data: crm/leads.json</p>
        <p>Generated by Lead Gen System v1.0</p>
    </div>
</div>
</body>
</html>"""

    DASHBOARD_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(DASHBOARD_FILE, "w") as f:
        f.write(html)
    log(f"Dashboard generated: {DASHBOARD_FILE}")


# --- LinkedIn integration ---
def generate_linkedin_outreach(leads, config):
    """Generate LinkedIn outreach data for high-value leads."""
    linkedin_config = config.get("linkedin_integration", {})
    if not linkedin_config.get("enabled"):
        return []

    high_value = [l for l in leads if l.get("score", 0) >= 75]
    outreach_data = []

    for lead in high_value:
        contact = lead.get("contact", {})
        template = linkedin_config.get("message_template", "")
        company = lead.get("company", "")
        first_name = contact.get("name", "").split()[0] if contact.get("name") else "there"

        message = template.format(first_name=first_name, company=company)

        outreach_data.append({
            "company": company,
            "contact_name": contact.get("name", ""),
            "contact_title": contact.get("title", ""),
            "linkedin_url": contact.get("linkedin", ""),
            "message": message,
            "generated_date": datetime.now().isoformat(),
            "status": "pending",
        })

    # Save outreach data
    outreach_file = BASE_DIR / "crm" / "linkedin_outreach.json"
    with open(outreach_file, "w") as f:
        json.dump(outreach_data, f, indent=2)
    log(f"LinkedIn outreach data saved: {len(outreach_data)} messages")

    return outreach_data


# --- Main pipeline ---
def run_pipeline():
    """Run the full lead generation pipeline."""
    log("=" * 60)
    log("Starting lead generation pipeline")

    config = load_config()
    weights = config["scoring_weights"]
    thresholds = config["thresholds"]
    crm = load_crm()

    # Search for leads
    web_leads = search_web_for_leads(config)

    if web_leads is not None:
        new_leads = web_leads
        log(f"Found {len(new_leads)} leads from web search")
    else:
        new_leads = generate_sample_leads()
        log(f"Generated {len(new_leads)} sample leads (web search unavailable)")

    # Process and score each lead
    for lead in new_leads:
        lead_id = generate_lead_id(lead.get("company", ""), lead.get("source", ""))
        score = score_lead(lead, weights)
        category = categorize_lead(score, thresholds)

        lead["id"] = lead_id
        lead["score"] = score
        lead["category"] = category
        lead["outreach_angle"] = generate_outreach_angle(lead)
        lead["last_updated"] = datetime.now().isoformat()

        # Check if already in CRM (update vs insert)
        existing_idx = next(
            (i for i, l in enumerate(crm["leads"]) if l.get("id") == lead_id),
            None
        )
        if existing_idx is not None:
            lead["first_seen"] = crm["leads"][existing_idx].get("first_seen", lead["discovered_date"])
            crm["leads"][existing_idx] = lead
        else:
            lead["first_seen"] = lead["discovered_date"]
            crm["leads"].append(lead)

        # Notify on high-value leads
        if score >= thresholds["high_value"] and existing_idx is None:
            notify(f"{lead['company']} ({lead['industry']}) - Score: {score} - {lead.get('outreach_angle', '')}")

    # Update stats
    crm["stats"]["total"] = len(crm["leads"])
    crm["stats"]["high_value"] = sum(1 for l in crm["leads"] if l.get("category") == "high_value")
    crm["stats"]["last_run"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Save CRM
    save_crm(crm)
    log(f"CRM updated: {crm['stats']['total']} total leads, {crm['stats']['high_value']} high-value")

    # Generate LinkedIn outreach
    generate_linkedin_outreach(crm["leads"], config)

    # Generate dashboard
    generate_dashboard(crm)

    log("Pipeline complete")
    print(f"✅ Lead generation complete: {crm['stats']['total']} leads, {crm['stats']['high_value']} high-value")

    return crm


if __name__ == "__main__":
    run_pipeline()
