@echo off
title SewLuxe Pattern Intelligence Dashboard
echo Starting SewLuxe Etsy Market Intelligence Dashboard...
cd /d "C:\Users\red1e\.gemini\antigravity\scratch\etsy\01_market_research\dashboard"
python -m uvicorn server:app --host 127.0.0.1 --port 8000 --reload
pause
