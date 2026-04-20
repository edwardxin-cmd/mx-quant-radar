@echo off
title MX-Deployer
color 0A
cd /d "F:\mx_radar_web"

echo --- Ready to deploy ---
git add .
git commit -m "Auto Update Dashboard"
git push origin main

echo.
echo --- DONE ---
echo If error says main does not match, change main to master in script.
pause