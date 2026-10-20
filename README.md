<!-- Watermark: Living_Sin (intricos777-dot) + AI agents (Hermes, Lia, opencode) - collaborative work -->
# AI Lead Generation & Business Intelligence System

Automated lead generation system that researches companies needing AI automation, scores them, and populates a CRM pipeline.

## Features

- **Web Research**: Searches Indeed, LinkedIn, Crunchbase, TechCrunch for AI/automation hiring signals
- **Lead Scoring**: 0-100 score based on company size, industry fit, hiring signals, tech stack, funding status
- **CRM Pipeline**: JSON-based CRM with deduplication and history tracking
- **HTML Dashboard**: Dark-themed real-time pipeline dashboard
- **LinkedIn Integration**: Auto-generates multi-touch outreach sequences
- **Desktop Notifications**: Alerts on high-value leads (score 75+)
- **Cron Scheduling**: Daily automated runs at 8:00 AM

## Quick Start

```bash
cd ~/Projects/other/lead-gen-system

# Run the pipeline
python3 lead_gen.py

# Generate LinkedIn outreach sequences
python3 linkedin_outreach.py

# Send notifications for hot leads
python3 notify.py

# Install cron job (daily at 8 AM)
bash setup_cron.sh
```

## Scoring Algorithm

| Factor | Weight | Description |
|--------|--------|-------------|
| Company Size | 20% | Larger = more budget |
| Industry Fit | 20% | Fintech/healthcare/e-com score highest |
| Hiring Signals | 30% | Active AI hiring = strongest signal |
| Tech Stack | 15% | AI/ML tech (PyTorch, TF, etc.) = fit |
| Funding Status | 15% | Recent funding = budget available |

**Thresholds**: High (75+), Medium (50-74), Low (<50)

## Output Files

```
crm/leads.json              - Main CRM with all scored leads
crm/linkedin_outreach.json  - Multi-touch outreach sequences
crm/linkedin_export.csv     - Ready for browser automation
templates/dashboard.html    - Open in browser for pipeline view
logs/lead_gen.log           - Pipeline execution log
logs/notifications.log      - High-value lead alerts
```

## Dashboard

Open `templates/dashboard.html` in a browser to see:
- Total leads and breakdown by value tier
- Sortable table with scores, industries, outreach angles
- Signal types (hiring/funding/transformation)

## LinkedIn Outreach Sequence

3-step automated sequence per high-value lead:
1. **Connection request** (Day 0) - Personalized intro referencing their AI growth
2. **Follow-up** (Day 3) - Value proposition with specific ROI
3. **Value-add** (Day 7) - Offer free automation audit

## Configuration

Edit `config/config.json` to customize:
- Search queries and industries
- Scoring weights and thresholds
- LinkedIn message templates
- Notification preferences
