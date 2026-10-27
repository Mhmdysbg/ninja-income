#!/bin/bash
# Install Ninja Income Bot ke Systemd Timer (Ubuntu 20.04+)
# Script ini akan membuat systemd service dan timer

set -e

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_DIR="$PROJECT_DIR/logs"

# Buat folder logs jika belum ada
mkdir -p "$LOG_DIR"

SERVICE_FILE="/etc/systemd/system/ninja-income-bot.service"
TIMER_FILE="/etc/systemd/system/ninja-income-bot.timer"

echo "🔧 Installing Ninja Income Bot to Systemd..."
echo ""

# Buat service file
cat > "$SERVICE_FILE" << EOF
[Unit]
Description=Ninja Income Bot - Daily Reward Claimer
After=network.target

[Service]
Type=oneshot
WorkingDirectory=$PROJECT_DIR
ExecStart=/usr/bin/python3 bot.py
User=root
Group=root
StandardOutput=append:$LOG_DIR/claim.log
StandardError=append:$LOG_DIR/claim.log

[Install]
WantedBy=multi-user.target
EOF

# Buat timer file
cat > "$TIMER_FILE" << EOF
[Unit]
Description=Daily run of Ninja Income Bot

[Timer]
OnCalendar=*-*-* 09:00:00
Persistent=true
Unit=ninja-income-bot.service

[Install]
WantedBy=timers.target
EOF

# Reload systemd, enable dan start timer
echo "Reloading systemd daemon..."
systemctl daemon-reload

echo "Enabling ninja-income-bot.timer..."
systemctl enable ninja-income-bot.timer

echo "Starting ninja-income-bot.timer..."
systemctl start ninja-income-bot.timer

echo ""
echo "✅ Berhasil install Systemd Timer!"
echo ""
echo "📝 Cek status:"
echo "   systemctl status ninja-income-bot.timer"
echo "   journalctl -u ninja-income-bot.timer -f"
echo ""
echo "🗑️  Untuk remove:"
echo "   systemctl stop ninja-income-bot.timer"
echo "   systemctl disable ninja-income-bot.timer"
echo "   rm $SERVICE_FILE $TIMER_FILE"
echo "   systemctl daemon-reload"
echo ""
echo "📝 Lihat log:"
echo "   tail -f $LOG_DIR/claim.log"
