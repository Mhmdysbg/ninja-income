#!/bin/bash
# Install Ninja Income Bot ke Crontab
# Script ini akan menambahkan cron job untuk run bot setiap hari jam 9 pagi

set -e

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_DIR="$PROJECT_DIR/logs"

# Buat folder logs jika belum ada
mkdir -p "$LOG_DIR"

# Cron schedule: 0 9 * * * = setiap hari jam 09:00
CRON_SCHEDULE="0 9 * * *"
CRON_CMD="cd $PROJECT_DIR && /usr/bin/python3 bot.py >> $LOG_DIR/claim.log 2>&1"
CRON_LINE="$CRON_SCHEDULE $CRON_CMD"

echo "🔧 Installing Ninja Income Bot to Crontab..."
echo ""
echo "Schedule: $CRON_SCHEDULE (Every day at 09:00)"
echo "Command: $CRON_CMD"
echo ""

# Check if cron job sudah ada
if crontab -l 2>/dev/null | grep -q "ninja-income-bot"; then
    echo "⚠️  Cron job sudah ada. Hapus manual dulu:"
    echo "   crontab -e"
    echo "   (kemudian cari dan hapus baris yang berisi 'ninja-income-bot')"
    exit 1
fi

# Add cron job
(crontab -l 2>/dev/null; echo "$CRON_LINE") | crontab -

echo "✅ Berhasil install cron job!"
echo ""
echo "📝 Lihat log dengan:"
echo "   tail -f $LOG_DIR/claim.log"
echo ""
echo "🗑️  Untuk remove:"
echo "   crontab -e"
echo "   (hapus baris yang berisi 'ninja-income-bot')"
