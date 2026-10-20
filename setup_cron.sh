#!/bin/bash
# Watermark: Living_Sin (intricos777-dot) + AI agents (Hermes, Lia, opencode) - collaborative work
# Lead Generation System - Cronjob Setup
# Sets up a daily cron job to run the lead generation pipeline

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PYTHON_BIN="$(which python3)"
CRON_SCHEDULE="0 8 * * *"  # Daily at 8:00 AM
CRON_COMMENT="# Lead Gen System - Daily pipeline run"

echo "=== Lead Generation System - Cron Setup ==="
echo "Script directory: $SCRIPT_DIR"
echo "Python binary: $PYTHON_BIN"
echo "Schedule: $CRON_SCHEDULE (daily at 8:00 AM)"
echo ""

# Check if cron is available
if ! command -v crontab &> /dev/null; then
    echo "ERROR: crontab not found. Install cronie or vixie-cron first."
    exit 1
fi

# Create the cron command
CRON_CMD="$CRON_SCHEDULE cd $SCRIPT_DIR && $PYTHON_BIN $SCRIPT_DIR/lead_gen.py >> $SCRIPT_DIR/logs/cron.log 2>&1 $CRON_COMMENT"

# Check if already installed
if crontab -l 2>/dev/null | grep -q "lead_gen.py"; then
    echo "Cron job already exists. Updating..."
    crontab -l 2>/dev/null | grep -v "lead_gen.py" | crontab -
fi

# Install new cron job
(crontab -l 2>/dev/null; echo "$CRON_CMD") | crontab -

echo "✅ Cron job installed successfully!"
echo ""
echo "Current crontab:"
crontab -l | grep "lead_gen" || echo "  (not found - check permissions)"
echo ""
echo "To verify the job works, run:"
echo "  cd $SCRIPT_DIR && python3 lead_gen.py"
echo ""
echo "To remove the cron job later, run:"
echo "  crontab -l | grep -v 'lead_gen.py' | crontab -"
